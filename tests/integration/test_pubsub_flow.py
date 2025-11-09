"""Integration tests for pub/sub flow."""

import asyncio

import pytest

from neurobus import Event, NeuroBus


@pytest.mark.integration
class TestPubSubFlow:
    """Integration tests for event publishing and subscription."""

    async def test_simple_pubsub(self):
        """Test basic publish-subscribe flow."""
        bus = NeuroBus()
        received_events = []

        @bus.subscribe("greeting")
        async def handler(event: Event):
            received_events.append(event)

        async with bus:
            await bus.publish(Event(topic="greeting", data={"message": "Hello, World!"}))
            await asyncio.sleep(0.01)

        assert len(received_events) == 1
        assert received_events[0].topic == "greeting"
        assert received_events[0].data["message"] == "Hello, World!"

    async def test_multiple_events(self):
        """Test publishing multiple events."""
        bus = NeuroBus()
        counter = {"count": 0}

        @bus.subscribe("test")
        async def handler(event: Event):
            counter["count"] += 1

        async with bus:
            for i in range(10):
                await bus.publish(Event(topic="test", data={"index": i}))

            await asyncio.sleep(0.05)

        assert counter["count"] == 10

    async def test_wildcard_patterns(self):
        """Test wildcard pattern matching."""
        bus = NeuroBus()
        events = []

        @bus.subscribe("user.*")
        async def user_handler(event: Event):
            events.append(("user_handler", event.topic))

        @bus.subscribe("*.error")
        async def error_handler(event: Event):
            events.append(("error_handler", event.topic))

        async with bus:
            await bus.publish(Event(topic="user.login"))
            await bus.publish(Event(topic="user.logout"))
            await bus.publish(Event(topic="system.error"))
            await bus.publish(Event(topic="network.error"))

            await asyncio.sleep(0.05)

        assert len(events) == 4
        assert ("user_handler", "user.login") in events
        assert ("user_handler", "user.logout") in events
        assert ("error_handler", "system.error") in events
        assert ("error_handler", "network.error") in events

    async def test_priority_ordering(self):
        """Test handler execution priority."""
        bus = NeuroBus()
        execution_order = []

        @bus.subscribe("test", priority=1)
        async def low(event: Event):
            execution_order.append("low")

        @bus.subscribe("test", priority=50)
        async def medium(event: Event):
            execution_order.append("medium")

        @bus.subscribe("test", priority=100)
        async def high(event: Event):
            execution_order.append("high")

        async with bus:
            await bus.publish(Event(topic="test"))
            await asyncio.sleep(0.01)

        assert execution_order == ["high", "medium", "low"]

    async def test_context_filtering(self):
        """Test event filtering by context."""
        bus = NeuroBus()
        received = []

        @bus.subscribe("message", filter=lambda e: e.data.get("urgent") is True)
        async def urgent_handler(event: Event):
            received.append("urgent")

        @bus.subscribe("message")
        async def all_handler(event: Event):
            received.append("all")

        async with bus:
            # Should trigger both handlers
            await bus.publish(Event(topic="message", data={"urgent": True, "text": "Help!"}))
            await asyncio.sleep(0.01)

            assert "urgent" in received
            assert "all" in received

            received.clear()

            # Should only trigger all_handler
            await bus.publish(Event(topic="message", data={"urgent": False, "text": "Info"}))
            await asyncio.sleep(0.01)

            assert "urgent" not in received
            assert "all" in received

    async def test_parallel_dispatch(self):
        """Test parallel handler execution."""
        bus = NeuroBus()
        start_times = []

        @bus.subscribe("test")
        async def slow_handler1(event: Event):
            start_times.append(asyncio.get_event_loop().time())
            await asyncio.sleep(0.01)

        @bus.subscribe("test")
        async def slow_handler2(event: Event):
            start_times.append(asyncio.get_event_loop().time())
            await asyncio.sleep(0.01)

        async with bus:
            await bus.publish(Event(topic="test"))
            await asyncio.sleep(0.05)

        # Both should start at approximately the same time
        assert len(start_times) == 2
        time_diff = abs(start_times[0] - start_times[1])
        assert time_diff < 0.01  # Started within 10ms of each other

    async def test_error_isolation(self):
        """Test that one handler's error doesn't affect others."""
        bus = NeuroBus()
        success_count = {"count": 0}

        @bus.subscribe("test")
        async def failing_handler(event: Event):
            raise RuntimeError("Intentional error")

        @bus.subscribe("test")
        async def working_handler1(event: Event):
            success_count["count"] += 1

        @bus.subscribe("test")
        async def working_handler2(event: Event):
            success_count["count"] += 1

        async with bus:
            await bus.publish(Event(topic="test"))
            await asyncio.sleep(0.01)

        # Both working handlers should execute despite the error
        assert success_count["count"] == 2

    async def test_dynamic_subscription(self):
        """Test adding subscriptions dynamically."""
        bus = NeuroBus()
        events = []

        async def handler(event: Event):
            events.append(event.topic)

        async with bus:
            # Publish before subscription
            await bus.publish(Event(topic="test"))
            await asyncio.sleep(0.01)

            assert len(events) == 0

            # Subscribe dynamically
            bus.subscribe("test", handler=handler)

            # Publish after subscription
            await bus.publish(Event(topic="test"))
            await asyncio.sleep(0.01)

            assert len(events) == 1

    async def test_unsubscribe_during_operation(self):
        """Test unsubscribing while bus is running."""
        bus = NeuroBus()
        counter = {"count": 0}

        async def handler(event: Event):
            counter["count"] += 1

        subscription = bus.subscribe("test", handler=handler)

        async with bus:
            await bus.publish(Event(topic="test"))
            await asyncio.sleep(0.01)

            assert counter["count"] == 1

            # Unsubscribe
            bus.unsubscribe(subscription)

            # Should not receive events after unsubscribe
            await bus.publish(Event(topic="test"))
            await asyncio.sleep(0.01)

            assert counter["count"] == 1  # Still 1
