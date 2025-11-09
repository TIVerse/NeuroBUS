"""Tests for memory store."""

import time
from datetime import datetime, timedelta
from uuid import uuid4

from neurobus.memory.store import MemoryEntry, MemoryStore


class TestMemoryEntry:
    """Test cases for MemoryEntry."""

    def test_entry_creation(self):
        """Test memory entry initialization."""
        event_id = uuid4()
        entry = MemoryEntry(
            event_id=event_id,
            topic="test.event",
            content="Test memory content",
            importance=0.8,
        )

        assert entry.event_id == event_id
        assert entry.topic == "test.event"
        assert entry.content == "Test memory content"
        assert entry.importance == 0.8
        assert entry.access_count == 0

    def test_entry_access(self):
        """Test recording memory access."""
        entry = MemoryEntry(uuid4(), "test", "content")

        initial_count = entry.access_count
        entry.access()

        assert entry.access_count == initial_count + 1
        assert entry.last_access > 0

    def test_importance_decay(self):
        """Test importance decay."""
        entry = MemoryEntry(uuid4(), "test", "content", importance=0.5)

        entry.decay_importance(0.1)

        assert entry.importance == 0.4

        # Should not go below 0
        entry.decay_importance(1.0)
        assert entry.importance == 0.0

    def test_importance_boost(self):
        """Test importance boost."""
        entry = MemoryEntry(uuid4(), "test", "content", importance=0.5)

        entry.boost_importance(0.2)

        assert entry.importance == 0.7

        # Should not exceed 1
        entry.boost_importance(1.0)
        assert entry.importance == 1.0

    def test_to_dict(self):
        """Test converting to dictionary."""
        entry = MemoryEntry(uuid4(), "test.topic", "content", metadata={"key": "value"})

        data = entry.to_dict()

        assert "id" in data
        assert "event_id" in data
        assert data["topic"] == "test.topic"
        assert data["content"] == "content"
        assert data["metadata"] == {"key": "value"}


class TestMemoryStore:
    """Test cases for MemoryStore."""

    def test_store_creation(self):
        """Test store initialization."""
        store = MemoryStore(max_memories=100)

        assert store.max_memories == 100
        assert store.count() == 0

    def test_add_memory(self):
        """Test adding a memory."""
        store = MemoryStore()
        entry = MemoryEntry(uuid4(), "test.event", "content")

        store.add(entry)

        assert store.count() == 1

        # Should be retrievable
        retrieved = store.get(entry.id)
        assert retrieved is not None
        assert retrieved.id == entry.id

    def test_get_nonexistent(self):
        """Test getting nonexistent memory."""
        store = MemoryStore()

        result = store.get(uuid4())

        assert result is None

    def test_search_by_topic(self):
        """Test searching by topic pattern."""
        store = MemoryStore()

        store.add(MemoryEntry(uuid4(), "user.login", "content1"))
        store.add(MemoryEntry(uuid4(), "user.logout", "content2"))
        store.add(MemoryEntry(uuid4(), "system.error", "content3"))

        # Search for user events
        results = store.search_by_topic("user.*")

        assert len(results) == 2
        assert all("user" in r.topic for r in results)

    def test_search_by_time(self):
        """Test searching by time range."""
        store = MemoryStore()

        now = datetime.now()

        # Create entries with different timestamps
        entry1 = MemoryEntry(uuid4(), "test.1", "content1")
        entry1.timestamp = now - timedelta(hours=2)
        store.add(entry1)

        entry2 = MemoryEntry(uuid4(), "test.2", "content2")
        entry2.timestamp = now - timedelta(hours=1)
        store.add(entry2)

        entry3 = MemoryEntry(uuid4(), "test.3", "content3")
        entry3.timestamp = now
        store.add(entry3)

        # Search last 90 minutes
        start_time = now - timedelta(minutes=90)
        results = store.search_by_time(start_time=start_time)

        assert len(results) == 2  # entry2 and entry3

    def test_get_recent(self):
        """Test getting recent memories."""
        store = MemoryStore()

        # Add memories with delays to ensure ordering
        for i in range(5):
            store.add(MemoryEntry(uuid4(), f"test.{i}", f"content{i}"))
            time.sleep(0.01)

        recent = store.get_recent(limit=3)

        assert len(recent) == 3
        # Should be in reverse chronological order
        assert recent[0].topic == "test.4"

    def test_get_most_important(self):
        """Test getting most important memories."""
        store = MemoryStore()

        store.add(MemoryEntry(uuid4(), "low", "content", importance=0.2))
        store.add(MemoryEntry(uuid4(), "high", "content", importance=0.9))
        store.add(MemoryEntry(uuid4(), "medium", "content", importance=0.5))

        important = store.get_most_important(limit=2)

        assert len(important) == 2
        assert important[0].topic == "high"
        assert important[1].topic == "medium"

    def test_capacity_pruning(self):
        """Test automatic pruning when capacity reached."""
        store = MemoryStore(max_memories=3)

        # Add more than capacity
        for i in range(5):
            entry = MemoryEntry(uuid4(), f"test.{i}", "content")
            entry.importance = 0.1 * i  # Increasing importance
            store.add(entry)

        # Should only have max_memories
        assert store.count() == 3

    def test_decay_all(self):
        """Test applying decay to all memories."""
        store = MemoryStore(decay_enabled=True, decay_rate=0.1)

        entry = MemoryEntry(uuid4(), "test", "content", importance=0.5)
        store.add(entry)

        store.decay_all()

        # Should be decayed
        retrieved = store.get(entry.id)
        assert retrieved.importance == 0.4

    def test_consolidate(self):
        """Test memory consolidation."""
        store = MemoryStore(decay_enabled=True, decay_rate=0.5)

        # Add memories with low importance
        entry1 = MemoryEntry(uuid4(), "test.1", "content", importance=0.2)
        entry2 = MemoryEntry(uuid4(), "test.2", "content", importance=0.05)
        store.add(entry1)
        store.add(entry2)

        initial_count = store.count()

        # Consolidate
        store.consolidate()

        # Should prune very low importance memories
        assert store.count() < initial_count

    def test_clear(self):
        """Test clearing all memories."""
        store = MemoryStore()

        store.add(MemoryEntry(uuid4(), "test.1", "content"))
        store.add(MemoryEntry(uuid4(), "test.2", "content"))

        store.clear()

        assert store.count() == 0

    def test_get_stats(self):
        """Test getting store statistics."""
        store = MemoryStore()

        store.add(MemoryEntry(uuid4(), "test", "content"))
        store.search_by_topic("test.*")

        stats = store.get_stats()

        assert stats["total_memories"] == 1
        assert stats["memories_added"] == 1
        assert stats["searches"] == 1
        assert stats["decay_enabled"] is True
