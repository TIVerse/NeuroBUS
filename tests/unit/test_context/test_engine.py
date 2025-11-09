"""Tests for context engine."""

from neurobus.context.engine import ContextEngine
from neurobus.core.event import Event
from neurobus.types.context import ContextScope


class TestContextEngine:
    """Test cases for ContextEngine."""

    def test_engine_creation(self):
        """Test engine initialization."""
        engine = ContextEngine()

        assert engine is not None
        assert engine.store is not None

    def test_set_and_get_global(self):
        """Test global context operations."""
        engine = ContextEngine()

        engine.set_global("app_name", "MyApp")
        value = engine.get_global("app_name")

        assert value == "MyApp"

    def test_set_and_get_session(self):
        """Test session context operations."""
        engine = ContextEngine()

        engine.set_session("session_123", "user_id", "alice")
        value = engine.get_session("session_123", "user_id")

        assert value == "alice"

    def test_set_and_get_user(self):
        """Test user context operations."""
        engine = ContextEngine()

        engine.set_user("alice", "email", "alice@example.com")
        value = engine.get_user("alice", "email")

        assert value == "alice@example.com"

    def test_set_and_get_event(self):
        """Test event context operations."""
        engine = ContextEngine()

        engine.set_event("event_123", "processed", True)
        value = engine.get_event("event_123", "processed")

        assert value is True

    def test_get_all_global(self):
        """Test getting all global context."""
        engine = ContextEngine()

        engine.set_global("key1", "value1")
        engine.set_global("key2", "value2")

        all_global = engine.get_all_global()

        assert len(all_global) == 2
        assert all_global["key1"] == "value1"
        assert all_global["key2"] == "value2"

    def test_get_all_session(self):
        """Test getting all session context."""
        engine = ContextEngine()

        engine.set_session("session_123", "key1", "value1")
        engine.set_session("session_123", "key2", "value2")

        all_session = engine.get_all_session("session_123")

        assert len(all_session) == 2
        assert all_session["key1"] == "value1"

    def test_clear_session(self):
        """Test clearing session context."""
        engine = ContextEngine()

        engine.set_session("session_123", "key1", "value1")
        engine.set_session("session_123", "key2", "value2")

        count = engine.clear_session("session_123")

        assert count == 2
        assert engine.get_session("session_123", "key1") is None

    def test_clear_user(self):
        """Test clearing user context."""
        engine = ContextEngine()

        engine.set_user("alice", "key1", "value1")

        count = engine.clear_user("alice")

        assert count == 1
        assert engine.get_user("alice", "key1") is None

    def test_clear_event(self):
        """Test clearing event context."""
        engine = ContextEngine()

        engine.set_event("event_123", "key1", "value1")

        count = engine.clear_event("event_123")

        assert count == 1
        assert engine.get_event("event_123", "key1") is None

    def test_get_merged_context(self):
        """Test getting merged context from all scopes."""
        engine = ContextEngine()

        # Set at different scopes
        engine.set_global("app_name", "MyApp")
        engine.set_global("env", "prod")

        engine.set_session("session_123", "session_key", "session_value")
        engine.set_session("session_123", "env", "session_override")  # Override

        engine.set_user("alice", "email", "alice@example.com")

        engine.set_event("event_123", "event_key", "event_value")

        # Get merged context
        merged = engine.get_merged_context(
            session_id="session_123", user_id="alice", event_id="event_123"
        )

        # Should have values from all scopes
        assert merged["app_name"] == "MyApp"
        assert merged["env"] == "session_override"  # Session overrides global
        assert merged["session_key"] == "session_value"
        assert merged["email"] == "alice@example.com"
        assert merged["event_key"] == "event_value"

    def test_enrich_event(self):
        """Test enriching event with hierarchical context."""
        engine = ContextEngine()

        # Set up context
        engine.set_global("app_version", "1.0.0")
        engine.set_session("session_123", "user_id", "alice")
        engine.set_user("alice", "role", "admin")

        # Create event with minimal context
        event = Event(
            topic="user.action",
            data={"action": "click"},
            context={"session_id": "session_123", "user_id": "alice"},
        )

        # Enrich event
        enriched = engine.enrich_event(event)

        # Should have merged context
        assert enriched.context["app_version"] == "1.0.0"
        assert enriched.context["user_id"] == "alice"  # From event, not session
        assert enriched.context["role"] == "admin"
        assert enriched.context["session_id"] == "session_123"

    def test_query_context(self):
        """Test querying context with filter."""
        engine = ContextEngine()

        engine.set_global("key1", "value1")
        engine.set_global("key2", "value2")
        engine.set_global("secret", "hidden")

        # Query with filter
        filtered = engine.query_context(
            ContextScope.GLOBAL, filter_func=lambda k, v: not k.startswith("secret")
        )

        assert len(filtered) == 2
        assert "key1" in filtered
        assert "key2" in filtered
        assert "secret" not in filtered

    def test_query_context_no_filter(self):
        """Test querying context without filter."""
        engine = ContextEngine()

        engine.set_global("key1", "value1")
        engine.set_global("key2", "value2")

        all_context = engine.query_context(ContextScope.GLOBAL)

        assert len(all_context) == 2

    def test_cleanup_expired(self):
        """Test cleaning up expired entries."""
        engine = ContextEngine()

        import time

        engine.set_global("key1", "value1", ttl=0.1)
        engine.set_global("key2", "value2", ttl=10.0)

        time.sleep(0.15)

        count = engine.cleanup_expired()

        assert count == 1
        assert engine.get_global("key1") is None
        assert engine.get_global("key2") == "value2"

    def test_get_stats(self):
        """Test getting engine statistics."""
        engine = ContextEngine()

        engine.set_global("key1", "value1")
        engine.get_global("key1")

        stats = engine.get_stats()

        assert "store" in stats
        assert "default_ttl" in stats
        assert stats["store"]["sets"] >= 1

    def test_repr(self):
        """Test string representation."""
        engine = ContextEngine()

        engine.set_global("key1", "value1")
        engine.get_global("key1")

        repr_str = repr(engine)

        assert "ContextEngine" in repr_str
        assert "entries=" in repr_str
