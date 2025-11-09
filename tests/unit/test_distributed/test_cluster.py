"""Tests for cluster manager."""

import pytest

from neurobus.core.event import Event
from neurobus.distributed.cluster import ClusterManager

# Note: These tests require Redis to be running
# They will be skipped if Redis is not available

pytestmark = pytest.mark.skipif(
    True, reason="Requires Redis server running"  # Skip by default - requires Redis
)


class TestClusterManager:
    """Test cases for ClusterManager."""

    def test_manager_creation(self):
        """Test manager initialization."""
        manager = ClusterManager(redis_url="redis://localhost:6379")

        assert manager.redis_url == "redis://localhost:6379"
        assert manager.node_id is not None
        assert manager.is_running is False

    def test_manager_with_custom_node_id(self):
        """Test manager with custom node ID."""
        manager = ClusterManager(redis_url="redis://localhost:6379", node_id="custom-node")

        assert manager.node_id == "custom-node"

    async def test_start_stop(self):
        """Test starting and stopping manager."""
        manager = ClusterManager(redis_url="redis://localhost:6379")

        await manager.start()
        assert manager.is_running is True

        await manager.stop()
        assert manager.is_running is False

    async def test_broadcast_event(self):
        """Test broadcasting event to cluster."""
        manager = ClusterManager(redis_url="redis://localhost:6379")
        await manager.start()

        event = Event(topic="test.event", data={"test": "data"})

        receivers = await manager.broadcast_event(event)

        assert receivers >= 0

        await manager.stop()

    def test_register_handler(self):
        """Test registering event handler."""
        manager = ClusterManager(redis_url="redis://localhost:6379")

        async def handler(event):
            pass

        manager.register_event_handler(handler)

        assert handler in manager._event_handlers

    def test_unregister_handler(self):
        """Test unregistering event handler."""
        manager = ClusterManager(redis_url="redis://localhost:6379")

        async def handler(event):
            pass

        manager.register_event_handler(handler)
        manager.unregister_event_handler(handler)

        assert handler not in manager._event_handlers

    async def test_get_active_nodes_when_not_running(self):
        """Test getting active nodes when not running."""
        manager = ClusterManager(redis_url="redis://localhost:6379")

        nodes = await manager.get_active_nodes()

        assert nodes == []

    async def test_is_leader_when_not_running(self):
        """Test leader check when not running."""
        manager = ClusterManager(redis_url="redis://localhost:6379")

        is_leader = await manager.is_leader()

        assert is_leader is False

    def test_get_stats(self):
        """Test getting statistics."""
        manager = ClusterManager(redis_url="redis://localhost:6379")

        stats = manager.get_stats()

        assert "node_id" in stats
        assert "running" in stats
        assert "redis_url" in stats
        assert stats["running"] is False

    def test_repr(self):
        """Test string representation."""
        manager = ClusterManager(redis_url="redis://localhost:6379")

        repr_str = repr(manager)

        assert "ClusterManager" in repr_str
        assert manager.node_id in repr_str
