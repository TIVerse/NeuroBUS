"""
Wildcard Pattern Matching Example

Demonstrates using wildcard patterns to subscribe to multiple related topics.
"""

import asyncio

from neurobus import Event, NeuroBus


async def main():
    """Demonstrate wildcard pattern matching."""
    bus = NeuroBus()

    print("🎯 Wildcard Pattern Matching Example\n")

    # Subscribe to all user events
    @bus.subscribe("user.*")
    async def handle_user_events(event: Event):
        print(f"📝 User event: {event.topic}")
        print(f"   Data: {event.data}\n")

    # Subscribe to all system events
    @bus.subscribe("system.*")
    async def handle_system_events(event: Event):
        print(f"🔧 System event: {event.topic}")
        print(f"   Data: {event.data}\n")

    # Subscribe to specific nested pattern
    @bus.subscribe("user.profile.*")
    async def handle_profile_events(event: Event):
        print(f"👤 Profile event: {event.topic}")
        print(f"   Data: {event.data}\n")

    async with bus:
        # Publish various events
        print("Publishing events...\n")

        await bus.publish(
            Event(topic="user.login", data={"username": "alice", "timestamp": "2025-01-10"})
        )

        await bus.publish(
            Event(topic="user.profile.update", data={"field": "email", "value": "new@example.com"})
        )

        await bus.publish(Event(topic="system.startup", data={"version": "1.0.0"}))

        await bus.publish(
            Event(topic="user.logout", data={"username": "alice", "duration": "45min"})
        )

        # Wait for all events to be processed
        await asyncio.sleep(0.5)

        # Show statistics
        stats = bus.get_stats()
        print(f"\n📊 Statistics:")
        print(f"   Total subscriptions: {stats['registry']['total_subscriptions']}")


if __name__ == "__main__":
    asyncio.run(main())
