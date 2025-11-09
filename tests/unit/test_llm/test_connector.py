"""Tests for LLM connectors."""

import pytest

from neurobus.llm.connector import (
    LLMMessage,
    LLMProvider,
    LLMResponse,
    MockLLMConnector,
    create_connector,
)


class TestLLMMessage:
    """Test cases for LLMMessage."""

    def test_message_creation(self):
        """Test message initialization."""
        msg = LLMMessage(role="user", content="Hello")

        assert msg.role == "user"
        assert msg.content == "Hello"


class TestLLMResponse:
    """Test cases for LLMResponse."""

    def test_response_creation(self):
        """Test response initialization."""
        response = LLMResponse(
            content="Hi there!",
            provider="mock",
            model="mock-model",
            tokens_used=10,
        )

        assert response.content == "Hi there!"
        assert response.provider == "mock"
        assert response.model == "mock-model"
        assert response.tokens_used == 10


class TestMockLLMConnector:
    """Test cases for MockLLMConnector."""

    def test_connector_creation(self):
        """Test connector initialization."""
        connector = MockLLMConnector()

        assert connector.model == "mock-model"
        assert len(connector.responses) > 0

    async def test_generate(self):
        """Test text generation."""
        connector = MockLLMConnector(responses=["Test response"])

        response = await connector.generate("Hello")

        assert isinstance(response, LLMResponse)
        assert response.content == "Test response"
        assert response.provider == "mock"
        assert response.tokens_used > 0

    async def test_generate_cycles_responses(self):
        """Test that generate cycles through responses."""
        connector = MockLLMConnector(responses=["First", "Second"])

        response1 = await connector.generate("Test 1")
        response2 = await connector.generate("Test 2")
        response3 = await connector.generate("Test 3")

        assert response1.content == "First"
        assert response2.content == "Second"
        assert response3.content == "First"  # Cycles back

    async def test_chat(self):
        """Test chat completion."""
        connector = MockLLMConnector(responses=["Chat response"])

        messages = [
            LLMMessage(role="user", content="Hello"),
            LLMMessage(role="assistant", content="Hi"),
            LLMMessage(role="user", content="How are you?"),
        ]

        response = await connector.chat(messages)

        assert isinstance(response, LLMResponse)
        assert response.content == "Chat response"

    def test_get_stats(self):
        """Test statistics tracking."""
        connector = MockLLMConnector()

        stats = connector.get_stats()

        assert "provider" in stats
        assert "requests" in stats
        assert "tokens_used" in stats
        assert stats["requests"] == 0

    async def test_stats_tracking(self):
        """Test that stats are tracked correctly."""
        connector = MockLLMConnector()

        await connector.generate("Test 1")
        await connector.generate("Test 2")

        stats = connector.get_stats()

        assert stats["requests"] == 2
        assert stats["tokens_used"] > 0

    def test_reset_stats(self):
        """Test stats reset."""
        connector = MockLLMConnector()
        connector._stats["requests"] = 5
        connector._stats["tokens_used"] = 100

        connector.reset_stats()

        stats = connector.get_stats()
        assert stats["requests"] == 0
        assert stats["tokens_used"] == 0


class TestCreateConnector:
    """Test cases for create_connector factory."""

    def test_create_mock_connector(self):
        """Test creating mock connector."""
        connector = create_connector("mock")

        assert isinstance(connector, MockLLMConnector)

    def test_create_with_provider_enum(self):
        """Test creating with provider enum."""
        connector = create_connector(LLMProvider.MOCK)

        assert isinstance(connector, MockLLMConnector)

    def test_create_with_model(self):
        """Test creating with custom model."""
        connector = create_connector("mock", model="custom-model")

        assert connector.model == "custom-model"

    def test_create_with_temperature(self):
        """Test creating with custom temperature."""
        connector = create_connector("mock", temperature=0.5)

        assert connector.temperature == 0.5

    def test_create_unknown_provider(self):
        """Test that unknown provider raises error."""
        with pytest.raises(ValueError, match="Unknown provider"):
            create_connector("unknown-provider")
