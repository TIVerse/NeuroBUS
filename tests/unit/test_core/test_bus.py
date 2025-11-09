"""Tests for NeuroBUS main class."""

import asyncio

import pytest

from neurobus import Event, NeuroBus
from neurobus.config.schema import NeuroBusConfig
from neurobus.exceptions.core import BusNotStartedError


class TestNeuroBus:
    """Test cases for NeuroBus class."""

    def test_bus_creation(self):
        """Test bus initialization."""
        bus = NeuroBus()

        assert bus is not None
        assert bus.is_running is False
        assert bus.state == "created"

    def test_bus_with_config(self):
        """Test bus with custom config."""
        config = NeuroBusConfig(
            core={"max_subscriptions": 50},
        )
        bus = NeuroBus(config=config)

        assert bus.config.core.max_subscriptions == 50

    async def test_bus_start_stop(self):
        """Test bus lifecycle."""
        bus = NeuroBus()

        await bus.start()
        assert bus.is_running is True

        await bus.stop()
        assert bus.is_running is False

    async def test_bus_context_manager(self):
        """Test bus as async context manager."""
        bus = NeuroBus()

        async with bus:
            assert bus.is_running is True

        assert bus.is_running is False

    async def test_publish_before_start_raises_error(self):
        """Test publishing before start raises error."""
        bus = NeuroBus()
        event = Event(topic="test")

        with pytest.raises(BusNotStartedError):
            await bus.publish(event)

    async def test_subscribe_decorator(self):
        """Test subscribe as decorator."""
        bus = NeuroBus()
        called = []

        @bus.subscribe("test.event")
        async def handler(event: Event):
            called.append(event)

        await bus.start()
        event = Event(topic="test.event", data={"value": 42})
        await bus.publish(event)
        await asyncio.sleep(0.01)  # Allow dispatch to complete
        await bus.stop()

        assert len(called) == 1
        assert called[0].topic == "test.event"

    async def test_subscribe_direct_call(self):
        """Test subscribe as direct function call."""
        bus = NeuroBus()
        called = []

        async def handler(event: Event):
            called.append(event)

        subscription = bus.subscribe("test", handler=handler)

        assert subscription is not None
        assert subscription.pattern == "test"

        await bus.start()
        await bus.publish(Event(topic="test"))
        await asyncio.sleep(0.01)
        await bus.stop()

        assert len(called) == 1

    async def test_subscribe_with_priority(self):
        """Test subscription with priority."""
        bus = NeuroBus()
        order = []

        @bus.subscribe("test", priority=1)
        async def low_priority(event: Event):
            order.append("low")

        @bus.subscribe("test", priority=100)
        async def high_priority(event: Event):
            order.append("high")

        await bus.start()
        await bus.publish(Event(topic="test"))
        await asyncio.sleep(0.01)
        await bus.stop()

        # High priority should execute first
        assert order == ["high", "low"]

    async def test_subscribe_with_filter(self):
        """Test subscription with filter."""
        bus = NeuroBus()
        called = []

        @bus.subscribe("test", filter=lambda e: e.data.get("important"))
        async def handler(event: Event):
            called.append(event)

        await bus.start()

        # Should not be handled
        await bus.publish(Event(topic="test", data={"important": False}))
        await asyncio.sleep(0.01)
        assert len(called) == 0

        # Should be handled
        await bus.publish(Event(topic="test", data={"important": True}))
        await asyncio.sleep(0.01)
        assert len(called) == 1

        await bus.stop()

    async def test_wildcard_subscription(self):
        """Test wildcard pattern matching."""
        bus = NeuroBus()
        called = []

        @bus.subscribe("user.*")
        async def handler(event: Event):
            called.append(event.topic)

        await bus.start()

        await bus.publish(Event(topic="user.login"))
        await bus.publish(Event(topic="user.logout"))
        await bus.publish(Event(topic="system.error"))

        await asyncio.sleep(0.01)
        await bus.stop()

        assert len(called) == 2
        assert "user.login" in called
        assert "user.logout" in called

    async def test_unsubscribe(self):
        """Test unsubscribing a handler."""
        bus = NeuroBus()
        called = []

        async def handler(event: Event):
            called.append(event)

        subscription = bus.subscribe("test", handler=handler)

        await bus.start()
        await bus.publish(Event(topic="test"))
        await asyncio.sleep(0.01)

        assert len(called) == 1

        # Unsubscribe
        removed = bus.unsubscribe(subscription)
        assert removed is True

        # Should not receive events after unsubscribe
        await bus.publish(Event(topic="test"))
        await asyncio.sleep(0.01)

        assert len(called) == 1  # Still 1, not 2

        await bus.stop()

    async def test_get_subscriptions(self):
        """Test getting all subscriptions."""
        bus = NeuroBus()

        @bus.subscribe("test1")
        async def handler1(event: Event):
            pass

        @bus.subscribe("test2")
        async def handler2(event: Event):
            pass

        subs = bus.get_subscriptions()
        assert len(subs) == 2

    async def test_clear_subscriptions(self):
        """Test clearing all subscriptions."""
        bus = NeuroBus()

        @bus.subscribe("test")
        async def handler(event: Event):
            pass

        bus.clear_subscriptions()

        subs = bus.get_subscriptions()
        assert len(subs) == 0

    async def test_get_stats(self):
        """Test getting bus statistics."""
        bus = NeuroBus()

        @bus.subscribe("test")
        async def handler(event: Event):
            pass

        stats = bus.get_stats()

        assert "state" in stats
        assert "registry" in stats
        assert "dispatcher" in stats
        assert stats["registry"]["total_subscriptions"] == 1

    async def test_multiple_handlers_same_topic(self):
        """Test multiple handlers for same topic."""
        bus = NeuroBus()
        called = []

        @bus.subscribe("test")
        async def handler1(event: Event):
            called.append("handler1")

        @bus.subscribe("test")
        async def handler2(event: Event):
            called.append("handler2")

        await bus.start()
        await bus.publish(Event(topic="test"))
        await asyncio.sleep(0.01)
        await bus.stop()

        assert len(called) == 2
        assert "handler1" in called
        assert "handler2" in called

    async def test_handler_error_isolation(self):
        """Test that handler errors don't crash bus."""
        bus = NeuroBus()
        called = []

        @bus.subscribe("test")
        async def failing_handler(event: Event):
            raise ValueError("Handler error")

        @bus.subscribe("test")
        async def working_handler(event: Event):
            called.append("success")

        await bus.start()
        await bus.publish(Event(topic="test"))
        await asyncio.sleep(0.01)
        await bus.stop()

        # Working handler should still execute
        assert len(called) == 1
        assert called[0] == "success"
