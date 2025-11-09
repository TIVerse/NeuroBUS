"""Pytest configuration and shared fixtures."""

import asyncio
from datetime import datetime
from uuid import uuid4

import pytest

from neurobus import Event, NeuroBus, Subscription
from neurobus.config.schema import NeuroBusConfig


@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def sample_event() -> Event:
    """Create a sample event for testing."""
    return Event(
        id=uuid4(),
        topic="test.event",
        data={"message": "test message", "value": 42},
        timestamp=datetime.now(),
        context={"user_id": "test_user", "session_id": "test_session"},
        metadata={"priority": 1, "tags": ["test"]},
    )


@pytest.fixture
def user_login_event() -> Event:
    """Create a user login event."""
    return Event(
        topic="user.login",
        data={"username": "alice", "success": True},
        context={"ip": "127.0.0.1"},
    )


@pytest.fixture
def error_event() -> Event:
    """Create an error event."""
    return Event(
        topic="system.error",
        data={"error": "Something went wrong", "code": 500},
        context={"component": "api"},
    )


@pytest.fixture
async def handler_called():
    """Track if a handler was called."""
    called = {"count": 0, "events": []}

    async def handler(event: Event):
        called["count"] += 1
        called["events"].append(event)

    handler.called = called  # type: ignore
    return handler


@pytest.fixture
def test_config() -> NeuroBusConfig:
    """Create a test configuration."""
    return NeuroBusConfig(
        environment="testing",
        debug=False,
        core={
            "max_subscriptions": 100,
            "dispatch_timeout": 5.0,
            "handler_timeout": 2.0,
            "enable_error_isolation": True,
            "enable_parallel_dispatch": True,
            "max_concurrent_handlers": 10,
        },
        monitoring={"enabled": False, "logging_level": "WARNING"},
    )


@pytest.fixture
async def bus(test_config) -> NeuroBus:
    """Create a NeuroBUS instance."""
    bus_instance = NeuroBus(config=test_config)
    await bus_instance.start()
    yield bus_instance
    await bus_instance.stop()


@pytest.fixture
async def simple_subscription() -> Subscription:
    """Create a simple subscription."""

    async def handler(event: Event):
        pass

    return Subscription(
        pattern="test.event",
        handler=handler,
        priority=0,
    )
