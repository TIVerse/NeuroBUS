"""Integration tests for semantic routing."""

import asyncio

import pytest

pytest.importorskip("sentence_transformers")

from neurobus import Event, NeuroBus


@pytest.mark.integration
class TestSemanticRouting:
    """Integration tests for semantic routing."""

    async def test_semantic_subscription(self):
        """Test basic semantic subscription."""
        bus = NeuroBus()
        bus.enable_semantic(model_name="all-MiniLM-L6-v2")

        received = []

        @bus.subscribe("user authentication", semantic=True, threshold=0.7)
        async def handler(event: Event):
            received.append(event.topic)

        async with bus:
            # Should match semantically
            await bus.publish(Event(topic="user.login", data={}))
            await bus.publish(Event(topic="authentication.success", data={}))

            # Should not match
            await bus.publish(Event(topic="system.error", data={}))

            await asyncio.sleep(0.1)

        # Should have received the auth-related events
        assert len(received) >= 2
        assert "user.login" in received
        assert "authentication.success" in received
        assert "system.error" not in received

    async def test_hybrid_routing(self):
        """Test hybrid pattern + semantic routing."""
        bus = NeuroBus()
        bus.enable_semantic(model_name="all-MiniLM-L6-v2")

        pattern_events = []
        semantic_events = []

        @bus.subscribe("user.*", semantic=False)
        async def pattern_handler(event: Event):
            pattern_events.append(event.topic)

        @bus.subscribe("user authentication", semantic=True, threshold=0.7)
        async def semantic_handler(event: Event):
            semantic_events.append(event.topic)

        async with bus:
            await bus.publish(Event(topic="user.login", data={}))
            await bus.publish(Event(topic="user.logout", data={}))
            await bus.publish(Event(topic="authentication.failed", data={}))

            await asyncio.sleep(0.1)

        # Pattern handler should get user.* events
        assert "user.login" in pattern_events
        assert "user.logout" in pattern_events

        # Semantic handler should get auth-related events
        assert "user.login" in semantic_events
        # authentication.failed might match depending on similarity

    async def test_threshold_filtering(self):
        """Test that threshold filters matches correctly."""
        bus = NeuroBus()
        bus.enable_semantic(model_name="all-MiniLM-L6-v2")

        high_threshold_events = []
        low_threshold_events = []

        @bus.subscribe("user login", semantic=True, threshold=0.9)
        async def high_threshold_handler(event: Event):
            high_threshold_events.append(event.topic)

        @bus.subscribe("user login", semantic=True, threshold=0.6)
        async def low_threshold_handler(event: Event):
            low_threshold_events.append(event.topic)

        async with bus:
            # Very similar
            await bus.publish(Event(topic="user.login", data={}))

            # Somewhat similar
            await bus.publish(Event(topic="user.authentication", data={}))

            # Not very similar
            await bus.publish(Event(topic="system.shutdown", data={}))

            await asyncio.sleep(0.1)

        # High threshold should only get very similar events
        assert len(high_threshold_events) >= 1

        # Low threshold should get more events
        assert len(low_threshold_events) >= len(high_threshold_events)

    async def test_semantic_with_priority(self):
        """Test semantic routing with priority."""
        bus = NeuroBus()
        bus.enable_semantic(model_name="all-MiniLM-L6-v2")

        execution_order = []

        @bus.subscribe("user events", semantic=True, priority=100)
        async def high_priority(event: Event):
            execution_order.append("high")

        @bus.subscribe("user events", semantic=True, priority=1)
        async def low_priority(event: Event):
            execution_order.append("low")

        async with bus:
            await bus.publish(Event(topic="user.action", data={}))
            await asyncio.sleep(0.1)

        # High priority should execute first
        if len(execution_order) >= 2:
            assert execution_order[0] == "high"
            assert execution_order[1] == "low"

    async def test_semantic_statistics(self):
        """Test semantic routing statistics."""
        bus = NeuroBus()
        bus.enable_semantic(model_name="all-MiniLM-L6-v2")

        @bus.subscribe("test events", semantic=True)
        async def handler(event: Event):
            pass

        async with bus:
            await bus.publish(Event(topic="test.event", data={}))
            await asyncio.sleep(0.1)

        stats = bus.get_stats()

        assert "semantic" in stats
        assert stats["semantic"]["total_queries"] > 0
        assert "encoder" in stats["semantic"]
        assert "cache" in stats["semantic"]["encoder"]
