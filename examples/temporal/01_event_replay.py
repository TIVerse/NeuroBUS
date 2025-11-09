"""
Event Replay Example

Demonstrates event persistence, querying, and replay capabilities.
"""

import asyncio
from datetime import datetime, timedelta

from neurobus import Event, NeuroBus
from neurobus.config import NeuroBusConfig


async def main():
    """Run the event replay example."""
    # Create bus with temporal persistence enabled
    config = NeuroBusConfig(
        temporal={"enabled": True, "db_path": "example_events.db"}
    )
    bus = NeuroBus(config=config)
    
    print("✅ Temporal engine enabled\n")
    
    # Subscribe to events
    @bus.subscribe("user.*")
    async def handle_user_event(event: Event):
        print(f"📩 Received: {event.topic} at {event.timestamp}")
    
    async with bus:
        print("🚀 Publishing events...\n")
        
        # Publish some events (automatically persisted)
        await bus.publish(Event(topic="user.login", data={"user": "alice"}))
        await asyncio.sleep(0.1)
        
        await bus.publish(Event(topic="user.action", data={"action": "click"}))
        await asyncio.sleep(0.1)
        
        await bus.publish(Event(topic="user.logout", data={"user": "alice"}))
        await asyncio.sleep(0.1)
        
        print("\n📊 Querying stored events...\n")
        
        # Query all user events from the past hour
        past_events = await bus.temporal.query_past(hours=1, topic="user.*")
        print(f"Found {len(past_events)} user events in the past hour:")
        for event in past_events:
            print(f"  - {event.topic} at {event.timestamp}")
        
        print("\n🔁 Replaying events...\n")
        
        # Replay events from 10 seconds ago
        replay_start = datetime.now() - timedelta(seconds=10)
        
        def replay_handler(event: Event):
            print(f"  Replaying: {event.topic}")
        
        replayed = await bus.temporal.replay(
            start_time=replay_start,
            topic="user.*",
            handler=replay_handler
        )
        
        print(f"\nReplayed {len(replayed)} events")
        
        # Show statistics
        stats = bus.get_stats()
        if "temporal" in stats:
            temporal_stats = await stats["temporal"]
            print(f"\n📈 Temporal Stats:")
            print(f"  Total events stored: {temporal_stats['store']['total_events']}")
            print(f"  Events queried: {temporal_stats['store']['events_queried']}")
            print(f"  Events replayed: {temporal_stats['store']['events_replayed']}")
            print(f"  DB size: {temporal_stats['store']['db_size_mb']} MB")
        
        print("\n✅ Done!")


if __name__ == "__main__":
    asyncio.run(main())
