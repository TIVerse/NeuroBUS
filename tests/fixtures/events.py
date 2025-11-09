"""Event fixtures for testing."""

from datetime import datetime
from uuid import uuid4

from neurobus import Event


def create_event(
    topic: str = "test.topic",
    data: dict | None = None,
    context: dict | None = None,
) -> Event:
    """
    Create a test event.

    Args:
        topic: Event topic
        data: Event data
        context: Event context

    Returns:
        Event instance
    """
    return Event(
        id=uuid4(),
        topic=topic,
        data=data or {},
        timestamp=datetime.now(),
        context=context or {},
    )


def create_batch_events(count: int, topic_prefix: str = "test") -> list[Event]:
    """
    Create a batch of test events.

    Args:
        count: Number of events to create
        topic_prefix: Prefix for event topics

    Returns:
        List of events
    """
    return [
        create_event(
            topic=f"{topic_prefix}.event_{i}",
            data={"index": i, "batch": True},
        )
        for i in range(count)
    ]
