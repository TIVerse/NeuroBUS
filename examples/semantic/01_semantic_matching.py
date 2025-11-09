"""
Semantic Matching Example

Demonstrates semantic similarity-based event routing.
Events are matched by meaning rather than exact topic patterns.
"""

import asyncio

from neurobus import Event, NeuroBus


async def main():
    """Run the semantic matching example."""
    # Create bus and enable semantic routing
    bus = NeuroBus()
    
    # Enable semantic routing (requires sentence-transformers)
    try:
        bus.enable_semantic()
        print("✅ Semantic routing enabled\n")
    except ImportError:
        print("❌ Semantic routing requires: pip install neurobus[semantic]")
        return
    
    # Subscribe with semantic matching
    @bus.subscribe(
        "user authentication and login",
        semantic=True,
        threshold=0.75
    )
    async def handle_auth_events(event: Event):
        print(f"🔐 Auth handler received: {event.topic}")
    
    @bus.subscribe(
        "system errors and failures",
        semantic=True,
        threshold=0.7
    )
    async def handle_error_events(event: Event):
        print(f"❌ Error handler received: {event.topic}")
    
    # Start bus
    async with bus:
        print("🚀 Publishing semantically similar events...\n")
        
        # These should match "user authentication and login"
        await bus.publish(Event(topic="user.signin", data={}))
        await asyncio.sleep(0.1)
        
        await bus.publish(Event(topic="authentication.success", data={}))
        await asyncio.sleep(0.1)
        
        await bus.publish(Event(topic="user_logged_in", data={}))
        await asyncio.sleep(0.1)
        
        print()
        
        # These should match "system errors and failures"
        await bus.publish(Event(topic="system.crash", data={}))
        await asyncio.sleep(0.1)
        
        await bus.publish(Event(topic="critical.failure", data={}))
        await asyncio.sleep(0.1)
        
        await bus.publish(Event(topic="error_occurred", data={}))
        await asyncio.sleep(0.1)
        
        print("\n✅ Done!")
        
        # Show statistics
        stats = bus.get_stats()
        if "semantic" in stats:
            print(f"\n📊 Semantic Stats:")
            print(f"  Cache hit rate: {stats['semantic']['encoder']['cache']['hit_rate']:.1%}")
            print(f"  Total queries: {stats['semantic']['total_queries']}")


if __name__ == "__main__":
    asyncio.run(main())
