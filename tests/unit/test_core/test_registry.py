"""Tests for SubscriptionRegistry."""

import pytest

from neurobus.core.event import Event
from neurobus.core.registry import SubscriptionRegistry
from neurobus.core.subscription import Subscription
from neurobus.exceptions.core import (
    DuplicateSubscriptionError,
    RegistryFullError,
    SubscriptionNotFoundError,
)


class TestSubscriptionRegistry:
    """Test cases for SubscriptionRegistry."""

    def test_registry_creation(self):
        """Test registry initialization."""
        registry = SubscriptionRegistry(max_size=100)

        assert registry.max_size == 100
        assert registry.count() == 0

    async def test_add_subscription(self):
        """Test adding a subscription."""
        registry = SubscriptionRegistry()

        async def handler(event: Event):
            pass

        sub = Subscription(pattern="test", handler=handler)
        registry.add(sub)

        assert registry.count() == 1
        assert sub.id in registry

    async def test_add_duplicate_raises_error(self):
        """Test adding duplicate subscription raises error."""
        registry = SubscriptionRegistry()

        async def handler(event: Event):
            pass

        sub = Subscription(pattern="test", handler=handler)
        registry.add(sub)

        with pytest.raises(DuplicateSubscriptionError):
            registry.add(sub)

    async def test_add_exceeds_max_size(self):
        """Test adding beyond max size raises error."""
        registry = SubscriptionRegistry(max_size=2)

        async def handler(event: Event):
            pass

        sub1 = Subscription(pattern="test1", handler=handler)
        sub2 = Subscription(pattern="test2", handler=handler)
        sub3 = Subscription(pattern="test3", handler=handler)

        registry.add(sub1)
        registry.add(sub2)

        with pytest.raises(RegistryFullError):
            registry.add(sub3)

    async def test_remove_subscription(self):
        """Test removing a subscription."""
        registry = SubscriptionRegistry()

        async def handler(event: Event):
            pass

        sub = Subscription(pattern="test", handler=handler)
        registry.add(sub)

        removed = registry.remove(sub.id)

        assert removed is True
        assert registry.count() == 0
        assert sub.id not in registry

    async def test_remove_nonexistent(self):
        """Test removing nonexistent subscription returns False."""
        registry = SubscriptionRegistry()

        from uuid import uuid4

        removed = registry.remove(uuid4())

        assert removed is False

    async def test_get_subscription(self):
        """Test getting a subscription by ID."""
        registry = SubscriptionRegistry()

        async def handler(event: Event):
            pass

        sub = Subscription(pattern="test", handler=handler)
        registry.add(sub)

        retrieved = registry.get(sub.id)

        assert retrieved == sub

    async def test_get_nonexistent_raises_error(self):
        """Test getting nonexistent subscription raises error."""
        registry = SubscriptionRegistry()

        from uuid import uuid4

        with pytest.raises(SubscriptionNotFoundError):
            registry.get(uuid4())

    async def test_find_exact_matches(self):
        """Test finding exact topic matches."""
        registry = SubscriptionRegistry()

        async def handler(event: Event):
            pass

        sub = Subscription(pattern="user.login", handler=handler)
        registry.add(sub)

        event = Event(topic="user.login")
        matches = registry.find_matches(event)

        assert len(matches) == 1
        assert matches[0] == sub

    async def test_find_no_matches(self):
        """Test finding no matches."""
        registry = SubscriptionRegistry()

        async def handler(event: Event):
            pass

        sub = Subscription(pattern="user.login", handler=handler)
        registry.add(sub)

        event = Event(topic="user.logout")
        matches = registry.find_matches(event)

        assert len(matches) == 0

    async def test_find_wildcard_matches(self):
        """Test finding wildcard pattern matches."""
        registry = SubscriptionRegistry()

        async def handler(event: Event):
            pass

        sub = Subscription(pattern="user.*", handler=handler)
        registry.add(sub)

        event1 = Event(topic="user.login")
        event2 = Event(topic="user.logout")
        event3 = Event(topic="system.error")

        assert len(registry.find_matches(event1)) == 1
        assert len(registry.find_matches(event2)) == 1
        assert len(registry.find_matches(event3)) == 0

    async def test_find_matches_sorted_by_priority(self):
        """Test matches are sorted by priority."""
        registry = SubscriptionRegistry()

        async def handler(event: Event):
            pass

        sub_low = Subscription(pattern="test", handler=handler, priority=1)
        sub_high = Subscription(pattern="test", handler=handler, priority=100)
        sub_mid = Subscription(pattern="test", handler=handler, priority=50)

        registry.add(sub_low)
        registry.add(sub_high)
        registry.add(sub_mid)

        event = Event(topic="test")
        matches = registry.find_matches(event)

        assert len(matches) == 3
        assert matches[0] == sub_high
        assert matches[1] == sub_mid
        assert matches[2] == sub_low

    async def test_find_by_pattern(self):
        """Test finding subscriptions by pattern."""
        registry = SubscriptionRegistry()

        async def handler(event: Event):
            pass

        sub1 = Subscription(pattern="test", handler=handler)
        sub2 = Subscription(pattern="test", handler=handler)
        sub3 = Subscription(pattern="other", handler=handler)

        registry.add(sub1)
        registry.add(sub2)
        registry.add(sub3)

        test_subs = registry.find_by_pattern("test")

        assert len(test_subs) == 2
        assert sub1 in test_subs
        assert sub2 in test_subs

    async def test_get_all(self):
        """Test getting all subscriptions."""
        registry = SubscriptionRegistry()

        async def handler(event: Event):
            pass

        sub1 = Subscription(pattern="test1", handler=handler)
        sub2 = Subscription(pattern="test2", handler=handler)

        registry.add(sub1)
        registry.add(sub2)

        all_subs = registry.get_all()

        assert len(all_subs) == 2
        assert sub1 in all_subs
        assert sub2 in all_subs

    async def test_clear(self):
        """Test clearing all subscriptions."""
        registry = SubscriptionRegistry()

        async def handler(event: Event):
            pass

        sub = Subscription(pattern="test", handler=handler)
        registry.add(sub)

        registry.clear()

        assert registry.count() == 0

    async def test_get_stats(self):
        """Test getting registry statistics."""
        registry = SubscriptionRegistry(max_size=100)

        async def handler(event: Event):
            pass

        sub1 = Subscription(pattern="exact", handler=handler)
        sub2 = Subscription(pattern="wild.*", handler=handler)

        registry.add(sub1)
        registry.add(sub2)

        stats = registry.get_stats()

        assert stats["total_subscriptions"] == 2
        assert stats["exact_patterns"] == 1
        assert stats["wildcard_patterns"] == 1
        assert stats["capacity"] == 100
