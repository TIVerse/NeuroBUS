"""Tests for Subscription model."""

import pytest

from neurobus.core.event import Event
from neurobus.core.subscription import Subscription


class TestSubscription:
    """Test cases for Subscription class."""

    async def test_subscription_creation(self):
        """Test basic subscription creation."""

        async def handler(event: Event):
            pass

        sub = Subscription(pattern="test.event", handler=handler)

        assert sub.pattern == "test.event"
        assert sub.handler == handler
        assert sub.semantic is False
        assert sub.threshold == 0.75
        assert sub.priority == 0

    async def test_subscription_with_priority(self):
        """Test subscription with custom priority."""

        async def handler(event: Event):
            pass

        sub = Subscription(pattern="test", handler=handler, priority=100)

        assert sub.priority == 100

    async def test_subscription_with_filter(self):
        """Test subscription with filter function."""

        async def handler(event: Event):
            pass

        def filter_func(event: Event) -> bool:
            return event.data.get("important") is True

        sub = Subscription(
            pattern="test",
            handler=handler,
            filter_func=filter_func,
        )

        assert sub.filter_func is not None

    async def test_empty_pattern_raises_error(self):
        """Test that empty pattern raises ValueError."""

        async def handler(event: Event):
            pass

        with pytest.raises(ValueError, match="Subscription pattern cannot be empty"):
            Subscription(pattern="", handler=handler)

    async def test_non_callable_handler_raises_error(self):
        """Test that non-callable handler raises TypeError."""
        with pytest.raises(TypeError, match="Subscription handler must be callable"):
            Subscription(pattern="test", handler="not callable")  # type: ignore

    async def test_invalid_threshold_raises_error(self):
        """Test that invalid threshold raises ValueError."""

        async def handler(event: Event):
            pass

        with pytest.raises(ValueError, match="Threshold must be between"):
            Subscription(pattern="test", handler=handler, threshold=1.5)

    async def test_matches_exact(self):
        """Test exact topic matching."""

        async def handler(event: Event):
            pass

        sub = Subscription(pattern="test.event", handler=handler)

        assert sub.matches_exact("test.event") is True
        assert sub.matches_exact("test.other") is False

    async def test_should_handle_without_filter(self):
        """Test should_handle without filter."""

        async def handler(event: Event):
            pass

        sub = Subscription(pattern="test", handler=handler)
        event = Event(topic="test", data={"key": "value"})

        assert sub.should_handle(event) is True

    async def test_should_handle_with_filter_pass(self):
        """Test should_handle with passing filter."""

        async def handler(event: Event):
            pass

        def filter_func(event: Event) -> bool:
            return event.data.get("important") is True

        sub = Subscription(
            pattern="test",
            handler=handler,
            filter_func=filter_func,
        )

        event = Event(topic="test", data={"important": True})
        assert sub.should_handle(event) is True

    async def test_should_handle_with_filter_fail(self):
        """Test should_handle with failing filter."""

        async def handler(event: Event):
            pass

        def filter_func(event: Event) -> bool:
            return event.data.get("important") is True

        sub = Subscription(
            pattern="test",
            handler=handler,
            filter_func=filter_func,
        )

        event = Event(topic="test", data={"important": False})
        assert sub.should_handle(event) is False

    async def test_should_handle_filter_exception(self):
        """Test should_handle when filter raises exception."""

        async def handler(event: Event):
            pass

        def filter_func(event: Event) -> bool:
            raise ValueError("Filter error")

        sub = Subscription(
            pattern="test",
            handler=handler,
            filter_func=filter_func,
        )

        event = Event(topic="test")
        assert sub.should_handle(event) is False

    async def test_handle_event(self):
        """Test handle_event invokes handler."""
        called = []

        async def handler(event: Event):
            called.append(event)

        sub = Subscription(pattern="test", handler=handler)
        event = Event(topic="test")

        await sub.handle_event(event)

        assert len(called) == 1
        assert called[0] == event

    async def test_equality(self):
        """Test subscription equality based on ID."""

        async def handler(event: Event):
            pass

        sub1 = Subscription(pattern="test", handler=handler)
        sub2 = Subscription(pattern="test", handler=handler)

        assert sub1 == sub1
        assert sub1 != sub2  # Different IDs

    async def test_hash(self):
        """Test subscription hashing."""

        async def handler(event: Event):
            pass

        sub = Subscription(pattern="test", handler=handler)

        # Should be hashable
        hash_val = hash(sub)
        assert isinstance(hash_val, int)

    async def test_repr(self):
        """Test string representation."""

        async def handler(event: Event):
            pass

        sub = Subscription(pattern="test.event", handler=handler, priority=10)
        repr_str = repr(sub)

        assert "Subscription" in repr_str
        assert "test.event" in repr_str
        assert "priority=10" in repr_str
