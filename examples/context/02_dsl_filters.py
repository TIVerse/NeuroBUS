"""
DSL Filter Example

Demonstrates using DSL (Domain Specific Language) filters for complex event filtering.
"""

import asyncio

from neurobus import Event, NeuroBus
from neurobus.config import NeuroBusConfig


async def main():
    """Demonstrate DSL filters."""
    config = NeuroBusConfig()
    bus = NeuroBus(config=config)

    print("🎯 Advanced Filter Example\n")
    print("Lambda filters allow complex conditional logic\n")

    # Simple comparison using lambda filter
    @bus.subscribe("alert", filter=lambda e: e.context.get('priority', 0) >= 5)
    async def handle_high_priority(event: Event):
        print(f"🔴 High priority alert!")
        print(f"   Priority: {event.context['priority']}")
        print(f"   Message: {event.data['message']}\n")

    # Complex AND condition using lambda
    @bus.subscribe("user.action", filter=lambda e: e.context.get('user', {}).get('age', 0) >= 18 and e.context.get('user', {}).get('verified', False))
    async def handle_verified_adults(event: Event):
        print(f"✅ Verified adult user action")
        print(f"   User: {event.context['user']}")
        print(f"   Action: {event.data['action']}\n")

    # OR condition using lambda
    @bus.subscribe("notification", filter=lambda e: e.context.get('priority', 0) > 8 or e.context.get('user', {}).get('role') == 'admin')
    async def handle_important(event: Event):
        print(f"📢 Important notification")
        print(f"   Priority: {event.context.get('priority', 'N/A')}")
        print(f"   Role: {event.context.get('user', {}).get('role', 'user')}\n")

    async with bus:
        print("Publishing events with context...\n")

        # High priority alert (matches)
        await bus.publish(
            Event(
                topic="alert",
                data={"message": "Server CPU at 95%"},
                context={"priority": 8},
            )
        )

        # Low priority alert (doesn't match)
        await bus.publish(
            Event(
                topic="alert",
                data={"message": "Cache cleared"},
                context={"priority": 2},
            )
        )

        # Verified adult user (matches)
        await bus.publish(
            Event(
                topic="user.action",
                data={"action": "purchase"},
                context={"user": {"age": 25, "verified": True, "name": "Alice"}},
            )
        )

        # Unverified user (doesn't match)
        await bus.publish(
            Event(
                topic="user.action",
                data={"action": "browse"},
                context={"user": {"age": 20, "verified": False, "name": "Bob"}},
            )
        )

        # Admin notification (matches via OR)
        await bus.publish(
            Event(
                topic="notification",
                data={"message": "System update available"},
                context={"priority": 5, "user": {"role": "admin"}},
            )
        )

        await asyncio.sleep(0.5)

        print("\n✅ Lambda filters provide powerful conditional filtering!")
        print("   Supports: AND, OR, comparisons, nested data access")


if __name__ == "__main__":
    asyncio.run(main())
