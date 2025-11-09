"""
Distributed Cluster Example

Demonstrates distributed event bus with multiple nodes communicating via Redis.
"""

import asyncio

from neurobus import Event, NeuroBus
from neurobus.config.schema import NeuroBusConfig


async def node_worker(node_id: str, port: int = 6379):
    """Run a cluster node."""
    config = NeuroBusConfig(
        distributed={
            "enabled": True,
            "redis_url": f"redis://localhost:{port}",
            "node_id": node_id,
        }
    )
    
    bus = NeuroBus(config=config)
    
    print(f"🔷 Node {node_id} starting...")
    
    # Subscribe to events
    @bus.subscribe("user.*")
    async def handle_user_event(event: Event):
        print(f"[{node_id}] 📩 Received: {event.topic} - {event.data}")
    
    @bus.subscribe("system.*")
    async def handle_system_event(event: Event):
        print(f"[{node_id}] 🔧 System event: {event.topic}")
    
    async with bus:
        print(f"✅ Node {node_id} connected to cluster\n")
        
        # Check if leader
        is_leader = await bus.cluster.is_leader()
        if is_leader:
            print(f"👑 Node {node_id} is the cluster LEADER!\n")
        
        # Get active nodes
        nodes = await bus.cluster.get_active_nodes()
        print(f"📊 Active nodes in cluster: {len(nodes)}")
        for node in nodes:
            print(f"  - {node['node_id']}")
        print()
        
        # Publish some events
        if node_id == "node-1":
            await asyncio.sleep(1)
            print(f"[{node_id}] 📤 Publishing user.login event")
            await bus.publish(Event(
                topic="user.login",
                data={"user": "alice", "node": node_id}
            ))
            
            await asyncio.sleep(0.5)
            print(f"[{node_id}] 📤 Publishing system.health event")
            await bus.publish(Event(
                topic="system.health",
                data={"status": "ok", "node": node_id}
            ))
        
        elif node_id == "node-2":
            await asyncio.sleep(2)
            print(f"[{node_id}] 📤 Publishing user.logout event")
            await bus.publish(Event(
                topic="user.logout",
                data={"user": "bob", "node": node_id}
            ))
        
        # Wait for events to propagate
        await asyncio.sleep(3)
        
        # Show statistics
        stats = bus.get_stats()
        if "cluster" in stats:
            cluster_stats = stats["cluster"]
            print(f"\n📈 Node {node_id} Stats:")
            print(f"  Events published: {cluster_stats['backend']['events_published']}")
            print(f"  Events received: {cluster_stats['backend']['events_received']}")
            print(f"  Nodes discovered: {cluster_stats['backend']['nodes_discovered']}")
        
        await asyncio.sleep(1)
    
    print(f"🔷 Node {node_id} stopped\n")


async def main():
    """Run the distributed cluster example."""
    print("🚀 Starting Distributed NeuroBUS Cluster Example\n")
    print("=" * 60)
    print("This example demonstrates:")
    print("  - Multiple nodes in a cluster")
    print("  - Event broadcasting across nodes")
    print("  - Leader election")
    print("  - Distributed subscriptions")
    print("=" * 60)
    print()
    
    print("⚠️  Prerequisites:")
    print("  - Redis server running on localhost:6379")
    print("  - Install: pip install redis")
    print()
    
    try:
        # Run multiple nodes concurrently
        await asyncio.gather(
            node_worker("node-1"),
            node_worker("node-2"),
            node_worker("node-3"),
        )
        
        print("\n✅ Cluster example completed!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Make sure Redis is running:")
        print("   docker run -d -p 6379:6379 redis:latest")
        print("   # or")
        print("   redis-server")


if __name__ == "__main__":
    asyncio.run(main())
