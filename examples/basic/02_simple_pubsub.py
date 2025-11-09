"""
Simple Pub/Sub Example

Demonstrates multiple subscribers and event types.
"""

import asyncio

from neurobus import Event, NeuroBus


async def main():
    """Run the pub/sub example."""
    bus = NeuroBus()
    
    # Subscribe to user events
    @bus.subscribe("user.login")
    async def handle_login(event: Event):
        username = event.data["username"]
        print(f"👤 User logged in: {username}")
    
    @bus.subscribe("user.logout")
    async def handle_logout(event: Event):
        username = event.data["username"]
        print(f"👋 User logged out: {username}")
    
    # Subscribe to all user events with wildcard
    @bus.subscribe("user.*")
    async def log_user_activity(event: Event):
        print(f"📝 Logging user event: {event.topic}")
    
    # Start bus
    async with bus:
        print("🚀 Publishing events...\n")
        
        # Publish login event
        await bus.publish(Event(
            topic="user.login",
            data={"username": "alice", "timestamp": "2024-01-01T10:00:00"}
        ))
        
        await asyncio.sleep(0.05)
        print()
        
        # Publish logout event
        await bus.publish(Event(
            topic="user.logout",
            data={"username": "alice", "timestamp": "2024-01-01T11:00:00"}
        ))
        
        await asyncio.sleep(0.05)
        print("\n✅ Done!")


if __name__ == "__main__":
    asyncio.run(main())
