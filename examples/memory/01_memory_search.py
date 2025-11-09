"""
Memory Search Example

Demonstrates long-term memory storage and semantic search capabilities.
"""

import asyncio

from neurobus import Event, NeuroBus
from neurobus.config.schema import NeuroBusConfig


async def main():
    """Run the memory search example."""
    # Create bus with memory enabled
    config = NeuroBusConfig(
        memory={
            "enabled": True,
            "enable_semantic": True,
            "max_memories": 1000,
        }
    )
    bus = NeuroBus(config=config)
    
    print("✅ Memory engine enabled with semantic search\n")
    
    async with bus:
        print("🚀 Publishing events (automatically stored as memories)...\n")
        
        # Publish events that will be remembered
        await bus.publish(Event(
            topic="user.login",
            data={"user": "alice", "action": "authenticated"}
        ))
        
        await bus.publish(Event(
            topic="user.action",
            data={"user": "alice", "action": "viewed dashboard"}
        ))
        
        await bus.publish(Event(
            topic="system.error",
            data={"error": "database connection failed"}
        ))
        
        await bus.publish(Event(
            topic="user.logout",
            data={"user": "alice", "action": "signed out"}
        ))
        
        await asyncio.sleep(0.2)  # Allow time for processing
        
        print("\n🔍 Searching memories...\n")
        
        # Semantic search for user-related memories
        user_memories = await bus.memory.search(
            "user authentication and actions",
            limit=5
        )
        
        print(f"Found {len(user_memories)} memories related to 'user authentication':")
        for memory in user_memories:
            print(f"  - {memory.topic} (importance: {memory.importance:.2f})")
            print(f"    Content: {memory.content[:80]}...")
            print()
        
        # Get recent memories
        print("📅 Recent memories:")
        recent = bus.memory.get_recent(limit=3)
        for memory in recent:
            print(f"  - {memory.topic} at {memory.timestamp}")
        
        # Get most important memories
        print("\n⭐ Most important memories:")
        important = bus.memory.get_important(limit=3)
        for memory in important:
            print(f"  - {memory.topic} (importance: {memory.importance:.2f})")
        
        # Topic-based search
        print("\n🏷️  User-related memories (topic search):")
        user_topic_memories = bus.memory.search_by_topic("user.*", limit=5)
        for memory in user_topic_memories:
            print(f"  - {memory.topic}")
        
        # Show statistics
        stats = bus.get_stats()
        if "memory" in stats:
            memory_stats = stats["memory"]["store"]
            print(f"\n📊 Memory Stats:")
            print(f"  Total memories: {memory_stats['total_memories']}")
            print(f"  Memories added: {memory_stats['memories_added']}")
            print(f"  Memories accessed: {memory_stats['memories_accessed']}")
            print(f"  Searches performed: {memory_stats['searches']}")
        
        print("\n✅ Done!")


if __name__ == "__main__":
    asyncio.run(main())
