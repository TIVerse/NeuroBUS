"""Tests for Event model."""

from datetime import datetime
from uuid import UUID, uuid4

import pytest

from neurobus.core.event import Event


class TestEvent:
    """Test cases for Event class."""

    def test_event_creation(self):
        """Test basic event creation."""
        event = Event(topic="test.event", data={"key": "value"})

        assert event.topic == "test.event"
        assert event.data == {"key": "value"}
        assert isinstance(event.id, UUID)
        assert isinstance(event.timestamp, datetime)
        assert event.context == {}
        assert event.metadata == {}
        assert event.parent_id is None

    def test_event_with_id(self):
        """Test event creation with explicit ID."""
        event_id = uuid4()
        event = Event(topic="test", id=event_id)

        assert event.id == event_id

    def test_event_with_context(self):
        """Test event with context."""
        event = Event(
            topic="test",
            context={"user_id": "123", "session": "abc"},
        )

        assert event.context["user_id"] == "123"
        assert event.context["session"] == "abc"

    def test_event_with_metadata(self):
        """Test event with metadata."""
        event = Event(
            topic="test",
            metadata={"priority": 1, "tags": ["important"]},
        )

        assert event.metadata["priority"] == 1
        assert event.metadata["tags"] == ["important"]

    def test_event_with_parent(self):
        """Test event with parent ID."""
        parent_id = uuid4()
        event = Event(topic="test", parent_id=parent_id)

        assert event.parent_id == parent_id

    def test_empty_topic_raises_error(self):
        """Test that empty topic raises ValueError."""
        with pytest.raises(ValueError, match="Event topic cannot be empty"):
            Event(topic="")

    def test_invalid_topic_type_raises_error(self):
        """Test that non-string topic raises TypeError."""
        with pytest.raises(TypeError, match="Event topic must be str"):
            Event(topic=123)  # type: ignore

    def test_with_context(self):
        """Test with_context method."""
        event = Event(topic="test", context={"a": 1})
        new_event = event.with_context(b=2, c=3)

        assert event.context == {"a": 1}  # Original unchanged
        assert new_event.context == {"a": 1, "b": 2, "c": 3}
        assert new_event.id == event.id  # Same ID
        assert new_event.topic == event.topic

    def test_child_event(self):
        """Test child_event method."""
        parent = Event(
            topic="parent",
            data={"parent_data": True},
            context={"user": "alice"},
        )

        child = parent.child_event("child", data={"child_data": True})

        assert child.parent_id == parent.id
        assert child.topic == "child"
        assert child.data == {"child_data": True}
        assert child.context == {"user": "alice"}

    def test_to_dict(self):
        """Test to_dict serialization."""
        event = Event(
            topic="test",
            data={"key": "value"},
            context={"user": "bob"},
        )

        event_dict = event.to_dict()

        assert event_dict["topic"] == "test"
        assert event_dict["data"] == {"key": "value"}
        assert event_dict["context"] == {"user": "bob"}
        assert "id" in event_dict
        assert "timestamp" in event_dict

    def test_from_dict(self):
        """Test from_dict deserialization."""
        data = {
            "id": str(uuid4()),
            "topic": "test",
            "data": {"key": "value"},
            "timestamp": datetime.now().isoformat(),
            "context": {"user": "charlie"},
            "metadata": {"priority": 1},
        }

        event = Event.from_dict(data)

        assert event.topic == "test"
        assert event.data == {"key": "value"}
        assert event.context == {"user": "charlie"}
        assert event.metadata == {"priority": 1}

    def test_from_dict_minimal(self):
        """Test from_dict with minimal data."""
        data = {"topic": "test"}
        event = Event.from_dict(data)

        assert event.topic == "test"
        assert event.data == {}
        assert event.context == {}
        assert isinstance(event.id, UUID)

    def test_repr(self):
        """Test string representation."""
        event = Event(topic="test.event")
        repr_str = repr(event)

        assert "Event" in repr_str
        assert "test.event" in repr_str
        assert str(event.id)[:8] in repr_str
