"""Tests for reasoning engine."""

import json

import pytest

from neurobus.core.event import Event
from neurobus.llm.connector import MockLLMConnector
from neurobus.llm.reasoning import ReasoningEngine


@pytest.fixture
def mock_connector():
    """Create mock LLM connector."""
    responses = [
        json.dumps(
            {
                "classification": "system_error",
                "sentiment": "negative",
                "priority": "high",
                "insights": ["Database connection failed"],
                "recommendations": ["Check database server", "Review connection pool"],
            }
        ),
        json.dumps(
            {
                "patterns": ["Increased error rate"],
                "anomalies": ["Unusual spike in failures"],
                "trends": ["Degrading performance"],
                "summary": "System experiencing issues",
            }
        ),
        json.dumps(
            {
                "chosen_option": "escalate",
                "confidence": 0.9,
                "reasoning": "High severity requires immediate attention",
                "alternatives": ["notify-admin", "auto-fix"],
            }
        ),
    ]
    return MockLLMConnector(responses=responses)


@pytest.fixture
async def reasoning_engine(mock_connector):
    """Create reasoning engine with mock connector."""
    engine = ReasoningEngine(mock_connector)
    await engine.initialize()
    return engine


class TestReasoningEngine:
    """Test cases for ReasoningEngine."""

    def test_engine_creation(self, mock_connector):
        """Test engine initialization."""
        engine = ReasoningEngine(mock_connector)

        assert engine.connector is mock_connector
        assert engine.enable_chain_of_thought is True

    async def test_initialize(self, mock_connector):
        """Test engine initialization."""
        engine = ReasoningEngine(mock_connector)

        await engine.initialize()

        # Should complete without error
        assert engine is not None

    async def test_analyze_event(self, reasoning_engine):
        """Test event analysis."""
        event = Event(topic="system.error", data={"error": "Connection failed"})

        analysis = await reasoning_engine.analyze_event(event)

        assert "classification" in analysis or "raw_analysis" in analysis
        assert "tokens_used" in analysis

    async def test_analyze_event_with_context(self, reasoning_engine):
        """Test event analysis with additional context."""
        event = Event(topic="user.login", data={"user": "alice"})
        context = {"previous_failures": 3}

        analysis = await reasoning_engine.analyze_event(event, context=context)

        assert analysis is not None
        assert "tokens_used" in analysis

    async def test_extract_insights(self, reasoning_engine):
        """Test insight extraction from multiple events."""
        events = [
            Event(topic="error.1", data={"type": "timeout"}),
            Event(topic="error.2", data={"type": "connection"}),
            Event(topic="error.3", data={"type": "timeout"}),
        ]

        insights = await reasoning_engine.extract_insights(events)

        # Check that we got a response (either parsed or raw)
        assert insights is not None
        assert "events_analyzed" in insights
        assert insights["events_analyzed"] == 3
        # Should have some insight data
        assert len(insights) > 2  # At least events_analyzed, tokens_used, and some content

    async def test_extract_insights_with_time_window(self, reasoning_engine):
        """Test insight extraction with time window."""
        events = [Event(topic="test", data={})]

        insights = await reasoning_engine.extract_insights(events, time_window="last hour")

        assert insights is not None
        assert "events_analyzed" in insights

    async def test_make_decision(self, reasoning_engine):
        """Test decision making."""
        event = Event(topic="alert.critical", data={"severity": "high"})
        options = ["escalate", "ignore", "auto-fix"]

        decision = await reasoning_engine.make_decision(event, options)

        # Check that we got a response
        assert decision is not None
        assert "tokens_used" in decision
        # Should have some decision data
        assert len(decision) > 1  # At least tokens_used and some content

    async def test_make_decision_with_criteria(self, reasoning_engine):
        """Test decision making with criteria."""
        event = Event(topic="incident", data={})
        options = ["approve", "reject"]
        criteria = {"urgency": "high", "impact": "critical"}

        decision = await reasoning_engine.make_decision(event, options, criteria=criteria)

        assert decision is not None
        assert "tokens_used" in decision

    async def test_reason_about_events(self, reasoning_engine):
        """Test reasoning about events."""
        events = [
            Event(topic="login", data={"user": "alice"}),
            Event(topic="purchase", data={"amount": 100}),
        ]
        question = "What did the user do?"

        reasoning = await reasoning_engine.reason_about_events(events, question)

        assert reasoning is not None
        assert "tokens_used" in reasoning

    def test_get_stats(self, reasoning_engine):
        """Test statistics retrieval."""
        stats = reasoning_engine.get_stats()

        assert "analyses" in stats
        assert "insights_extracted" in stats
        assert "decisions_made" in stats
        assert "connector_stats" in stats

    async def test_stats_tracking(self, reasoning_engine):
        """Test that statistics are tracked."""
        event = Event(topic="test", data={})

        # Perform operations
        await reasoning_engine.analyze_event(event)
        await reasoning_engine.extract_insights([event])
        await reasoning_engine.make_decision(event, ["opt1", "opt2"])

        stats = reasoning_engine.get_stats()

        assert stats["analyses"] >= 1
        assert stats["insights_extracted"] >= 1
        assert stats["decisions_made"] >= 1

    async def test_close(self, reasoning_engine):
        """Test engine closure."""
        await reasoning_engine.close()

        # Should complete without error
        assert reasoning_engine is not None

    def test_repr(self, reasoning_engine):
        """Test string representation."""
        repr_str = repr(reasoning_engine)

        assert "ReasoningEngine" in repr_str
        assert "MockLLMConnector" in repr_str
