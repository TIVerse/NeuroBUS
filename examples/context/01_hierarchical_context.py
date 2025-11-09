"""
Hierarchical Context Example

Demonstrates hierarchical context management with automatic inheritance.
"""

import asyncio

from neurobus import Event, NeuroBus
from neurobus.config.schema import NeuroBusConfig


async def main():
    """Run the hierarchical context example."""
    # Create bus with context enabled
    config = NeuroBusConfig(
        context={"enabled": True}
    )
    bus = NeuroBus(config=config)
    
    # Set global context (available everywhere)
    bus.context.set_global("app_name", "MyApp")
    bus.context.set_global("app_version", "1.0.0")
    bus.context.set_global("environment", "production")
    
    # Set session context (expires after 1 hour by default)
    bus.context.set_session("session_123", "user_id", "alice")
    bus.context.set_session("session_123", "login_time", "2024-01-01T10:00:00")
    bus.context.set_session("session_123", "ip_address", "192.168.1.1")
    
    # Set user context (expires after 2 hours by default)
    bus.context.set_user("alice", "email", "alice@example.com")
    bus.context.set_user("alice", "role", "admin")
    bus.context.set_user("alice", "preferences", {"theme": "dark", "lang": "en"})
    
    print("✅ Context set up\n")
    
    # Subscribe to events and show enriched context
    @bus.subscribe("user.*")
    async def handle_user_event(event: Event):
        print(f"📩 Event: {event.topic}")
        print(f"   Context keys: {list(event.context.keys())}")
        print(f"   - app_name: {event.context.get('app_name')}")
        print(f"   - app_version: {event.context.get('app_version')}")
        print(f"   - user_id: {event.context.get('user_id')}")
        print(f"   - email: {event.context.get('email')}")
        print(f"   - role: {event.context.get('role')}")
        print()
    
    async with bus:
        print("🚀 Publishing events...\n")
        
        # Publish event with minimal context
        # Context engine will automatically enrich it with:
        # - Global context (app_name, app_version, environment)
        # - Session context (user_id, login_time, ip_address)
        # - User context (email, role, preferences)
        await bus.publish(Event(
            topic="user.action",
            data={"action": "clicked_button"},
            context={"session_id": "session_123", "user_id": "alice"}
        ))
        
        await asyncio.sleep(0.1)
        
        # Manually get merged context
        print("🔍 Manually querying merged context:")
        merged = bus.context.get_merged_context(
            session_id="session_123",
            user_id="alice"
        )
        print(f"   Merged context has {len(merged)} keys:")
        for key, value in merged.items():
            print(f"   - {key}: {value}")
        print()
        
        # Show statistics
        stats = bus.get_stats()
        if "context" in stats:
            print("📊 Context Stats:")
            store_stats = stats["context"]["store"]
            print(f"   Total entries: {store_stats['total_entries']}")
            print(f"   Hit rate: {store_stats['hit_rate']:.1%}")
            print(f"   Scopes:")
            for scope, count in store_stats['scopes'].items():
                print(f"     - {scope}: {count} identifiers")
        
        print("\n✅ Done!")


if __name__ == "__main__":
    asyncio.run(main())
