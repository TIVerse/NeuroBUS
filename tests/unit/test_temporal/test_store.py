"""Tests for event store."""

import asyncio
from datetime import datetime, timedelta
from uuid import uuid4

import pytest

from neurobus.core.event import Event
from neurobus.temporal.store import EventStore


@pytest.fixture
async def temp_store(tmp_path):
    """Create a temporary event store."""
    db_path = tmp_path / "test_events.db"
    store = EventStore(db_path=db_path, max_events=1000)
    await store.initialize()
    yield store
    await store.close()
    # Cleanup
    if db_path.exists():
        db_path.unlink()


class TestEventStore:
    """Test cases for EventStore."""

    async def test_store_initialization(self, temp_store):
        """Test store initialization."""
        assert temp_store._initialized is True
        assert temp_store.db_path.exists()

    async def test_store_event(self, temp_store):
        """Test storing an event."""
        event = Event(topic="test.event", data={"key": "value"})

        await temp_store.store_event(event)

        # Verify stored
        retrieved = await temp_store.get_event(event.id)
        assert retrieved is not None
        assert retrieved.id == event.id
        assert retrieved.topic == event.topic
        assert retrieved.data == event.data

    async def test_get_nonexistent_event(self, temp_store):
        """Test getting nonexistent event."""
        event_id = uuid4()

        result = await temp_store.get_event(event_id)

        assert result is None

    async def test_query_by_topic(self, temp_store):
        """Test querying events by topic."""
        # Store multiple events
        await temp_store.store_event(Event(topic="user.login", data={}))
        await temp_store.store_event(Event(topic="user.logout", data={}))
        await temp_store.store_event(Event(topic="system.error", data={}))

        # Query user events
        events = await temp_store.query_by_topic("user%")

        assert len(events) == 2
        assert all("user" in e.topic for e in events)

    async def test_query_time_range(self, temp_store):
        """Test querying events in time range."""
        now = datetime.now()

        # Store events
        event1 = Event(topic="test.1", data={})
        event1.timestamp = now - timedelta(hours=2)
        await temp_store.store_event(event1)

        event2 = Event(topic="test.2", data={})
        event2.timestamp = now - timedelta(hours=1)
        await temp_store.store_event(event2)

        event3 = Event(topic="test.3", data={})
        event3.timestamp = now
        await temp_store.store_event(event3)

        # Query last 90 minutes
        start_time = now - timedelta(minutes=90)
        events = await temp_store.query_time_range(start_time, now)

        assert len(events) == 2  # event2 and event3

    async def test_replay_events(self, temp_store):
        """Test event replay."""
        # Store events
        await temp_store.store_event(Event(topic="event.1", data={}))
        await asyncio.sleep(0.01)
        await temp_store.store_event(Event(topic="event.2", data={}))
        await asyncio.sleep(0.01)
        await temp_store.store_event(Event(topic="event.3", data={}))

        # Replay all events
        events = await temp_store.replay_events()

        assert len(events) == 3
        # Should be in chronological order
        assert events[0].topic == "event.1"
        assert events[1].topic == "event.2"
        assert events[2].topic == "event.3"

    async def test_count_events(self, temp_store):
        """Test counting events."""
        # Store events
        await temp_store.store_event(Event(topic="user.login", data={}))
        await temp_store.store_event(Event(topic="user.logout", data={}))
        await temp_store.store_event(Event(topic="system.error", data={}))

        # Count all events
        total = await temp_store.count_events()
        assert total == 3

        # Count user events
        user_count = await temp_store.count_events("user%")
        assert user_count == 2

    async def test_retention_policy(self, tmp_path):
        """Test retention policy enforcement."""
        db_path = tmp_path / "retention_test.db"
        store = EventStore(db_path=db_path, max_events=5)
        await store.initialize()

        # Store more events than limit
        for i in range(10):
            await store.store_event(Event(topic=f"event.{i}", data={}))

        # Should only have 5 events (oldest removed)
        total = await store.count_events()
        assert total == 5

        await store.close()
        db_path.unlink()

    async def test_get_stats(self, temp_store):
        """Test getting store statistics."""
        await temp_store.store_event(Event(topic="test", data={}))

        stats = await temp_store.get_stats()

        assert "total_events" in stats
        assert "db_size_bytes" in stats
        assert "events_stored" in stats
        assert stats["total_events"] >= 1
        assert stats["events_stored"] >= 1
