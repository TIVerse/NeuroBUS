"""Tests for context store."""

import time

from neurobus.context.store import ContextEntry, ContextStore
from neurobus.types.context import ContextScope


class TestContextEntry:
    """Test cases for ContextEntry."""

    def test_entry_creation(self):
        """Test entry initialization."""
        entry = ContextEntry("key1", "value1", ContextScope.GLOBAL, ttl=60.0)

        assert entry.key == "key1"
        assert entry.value == "value1"
        assert entry.scope == ContextScope.GLOBAL
        assert entry.created_at > 0
        assert entry.expires_at > entry.created_at

    def test_entry_no_ttl(self):
        """Test entry without TTL."""
        entry = ContextEntry("key1", "value1", ContextScope.GLOBAL, ttl=0.0)

        assert entry.expires_at == 0.0

    def test_is_expired(self):
        """Test expiration check."""
        entry = ContextEntry("key1", "value1", ContextScope.GLOBAL, ttl=0.1)

        assert not entry.is_expired()

        time.sleep(0.15)

        assert entry.is_expired()

    def test_is_expired_no_ttl(self):
        """Test that entries without TTL never expire."""
        entry = ContextEntry("key1", "value1", ContextScope.GLOBAL, ttl=0.0)

        time.sleep(0.01)

        assert not entry.is_expired()


class TestContextStore:
    """Test cases for ContextStore."""

    def test_store_creation(self):
        """Test store initialization."""
        store = ContextStore()

        assert store is not None
        assert store.enable_auto_cleanup is True

    def test_set_and_get_global(self):
        """Test setting and getting global context."""
        store = ContextStore()

        store.set("key1", "value1", ContextScope.GLOBAL)
        value = store.get("key1", ContextScope.GLOBAL)

        assert value == "value1"

    def test_set_and_get_session(self):
        """Test setting and getting session context."""
        store = ContextStore()

        store.set("user_id", "alice", ContextScope.SESSION, "session_123")
        value = store.get("user_id", ContextScope.SESSION, "session_123")

        assert value == "alice"

    def test_set_and_get_user(self):
        """Test setting and getting user context."""
        store = ContextStore()

        store.set("email", "alice@example.com", ContextScope.USER, "alice")
        value = store.get("email", ContextScope.USER, "alice")

        assert value == "alice@example.com"

    def test_set_and_get_event(self):
        """Test setting and getting event context."""
        store = ContextStore()

        store.set("processed", True, ContextScope.EVENT, "event_456")
        value = store.get("processed", ContextScope.EVENT, "event_456")

        assert value is True

    def test_get_nonexistent(self):
        """Test getting nonexistent key."""
        store = ContextStore()

        value = store.get("nonexistent", ContextScope.GLOBAL, default="default")

        assert value == "default"

    def test_ttl_expiration(self):
        """Test TTL-based expiration."""
        store = ContextStore()

        store.set("key1", "value1", ContextScope.GLOBAL, ttl=0.1)

        # Should exist initially
        assert store.get("key1", ContextScope.GLOBAL) == "value1"

        # Wait for expiration
        time.sleep(0.15)

        # Should be expired
        assert store.get("key1", ContextScope.GLOBAL) is None

    def test_hierarchical_fallback(self):
        """Test hierarchical context lookup."""
        store = ContextStore()

        # Set at different scopes
        store.set("key1", "global", ContextScope.GLOBAL)
        store.set("key1", "session", ContextScope.SESSION, "session_123")
        store.set("key1", "user", ContextScope.USER, "alice")

        # Event scope should find user value
        value = store.get_hierarchical(
            "key1", ContextScope.EVENT, "event_123", session_id="session_123", user_id="alice"
        )
        assert value == "user"

        # Session scope should find its own value
        value = store.get_hierarchical("key1", ContextScope.SESSION, "session_123", user_id="alice")
        assert value == "session"

        # Global scope should find global value
        value = store.get_hierarchical("key1", ContextScope.GLOBAL)
        assert value == "global"

    def test_delete(self):
        """Test deleting context."""
        store = ContextStore()

        store.set("key1", "value1", ContextScope.GLOBAL)
        assert store.get("key1", ContextScope.GLOBAL) is not None

        deleted = store.delete("key1", ContextScope.GLOBAL)
        assert deleted is True

        assert store.get("key1", ContextScope.GLOBAL) is None

        # Delete nonexistent
        deleted = store.delete("nonexistent", ContextScope.GLOBAL)
        assert deleted is False

    def test_clear_scope(self):
        """Test clearing entire scope."""
        store = ContextStore()

        store.set("key1", "value1", ContextScope.SESSION, "session_123")
        store.set("key2", "value2", ContextScope.SESSION, "session_123")
        store.set("key3", "value3", ContextScope.SESSION, "session_123")

        count = store.clear_scope(ContextScope.SESSION, "session_123")

        assert count == 3
        assert store.get("key1", ContextScope.SESSION, "session_123") is None

    def test_cleanup_expired(self):
        """Test cleaning up expired entries."""
        store = ContextStore()

        # Set some entries with short TTL
        store.set("key1", "value1", ContextScope.GLOBAL, ttl=0.1)
        store.set("key2", "value2", ContextScope.GLOBAL, ttl=0.1)
        store.set("key3", "value3", ContextScope.GLOBAL, ttl=10.0)  # Long TTL

        # Wait for expiration
        time.sleep(0.15)

        # Cleanup
        count = store.cleanup_expired()

        assert count == 2  # Two expired
        assert store.get("key1", ContextScope.GLOBAL) is None
        assert store.get("key2", ContextScope.GLOBAL) is None
        assert store.get("key3", ContextScope.GLOBAL) == "value3"  # Still there

    def test_get_all(self):
        """Test getting all context in scope."""
        store = ContextStore()

        store.set("key1", "value1", ContextScope.GLOBAL)
        store.set("key2", "value2", ContextScope.GLOBAL)
        store.set("key3", "value3", ContextScope.GLOBAL)

        all_context = store.get_all(ContextScope.GLOBAL)

        assert len(all_context) == 3
        assert all_context["key1"] == "value1"
        assert all_context["key2"] == "value2"
        assert all_context["key3"] == "value3"

    def test_get_all_filters_expired(self):
        """Test that get_all filters expired entries."""
        store = ContextStore()

        store.set("key1", "value1", ContextScope.GLOBAL, ttl=0.1)
        store.set("key2", "value2", ContextScope.GLOBAL, ttl=10.0)

        time.sleep(0.15)

        all_context = store.get_all(ContextScope.GLOBAL)

        assert len(all_context) == 1
        assert "key2" in all_context
        assert "key1" not in all_context

    def test_statistics(self):
        """Test store statistics."""
        store = ContextStore()

        store.set("key1", "value1", ContextScope.GLOBAL)
        store.get("key1", ContextScope.GLOBAL)  # Hit
        store.get("nonexistent", ContextScope.GLOBAL)  # Miss

        stats = store.get_stats()

        assert stats["total_entries"] >= 1
        assert stats["sets"] == 1
        assert stats["gets"] == 2
        assert stats["hits"] == 1
        assert stats["misses"] == 1
        assert stats["hit_rate"] == 0.5

    def test_reset_stats(self):
        """Test resetting statistics."""
        store = ContextStore()

        store.set("key1", "value1", ContextScope.GLOBAL)
        store.get("key1", ContextScope.GLOBAL)

        store.reset_stats()

        stats = store.get_stats()
        assert stats["sets"] == 0
        assert stats["gets"] == 0
        assert stats["hits"] == 0
        assert stats["misses"] == 0

    def test_repr(self):
        """Test string representation."""
        store = ContextStore()

        store.set("key1", "value1", ContextScope.GLOBAL)
        store.get("key1", ContextScope.GLOBAL)

        repr_str = repr(store)

        assert "ContextStore" in repr_str
        assert "entries=" in repr_str
