"""
Event Filtering Example

Demonstrates using lambda filters to selectively handle events.
"""

import asyncio

from neurobus import Event, NeuroBus


async def main():
    """Demonstrate event filtering."""
    bus = NeuroBus()

    print("🎯 Event Filtering Example\n")

    # Filter by data content
    @bus.subscribe("order", filter=lambda e: e.data.get("amount", 0) > 100)
    async def handle_large_orders(event: Event):
        print(f"💰 Large order: ${event.data['amount']}")
        print(f"   Customer: {event.data['customer']}\n")

    # Filter by metadata
    @bus.subscribe("log", filter=lambda e: e.metadata.get("level") == "ERROR")
    async def handle_errors(event: Event):
        print(f"❌ Error log: {event.data['message']}")
        print(f"   Source: {event.metadata.get('source', 'unknown')}\n")

    # Complex filter
    @bus.subscribe(
        "user.*",
        filter=lambda e: e.context.get("premium", False)
        and e.data.get("action") == "purchase",
    )
    async def handle_premium_purchases(event: Event):
        print(f"⭐ Premium user purchase!")
        print(f"   User: {e.context.get('user_id')}")
        print(f"   Item: {event.data.get('item')}\n")

    async with bus:
        print("Publishing events (some will be filtered out)...\n")

        # This will match (amount > 100)
        await bus.publish(
            Event(
                topic="order",
                data={"amount": 250, "customer": "Alice", "item": "Laptop"},
            )
        )

        # This will NOT match (amount <= 100)
        await bus.publish(
            Event(
                topic="order",
                data={"amount": 50, "customer": "Bob", "item": "Mouse"},
            )
        )

        # This will match (ERROR level)
        await bus.publish(
            Event(
                topic="log",
                data={"message": "Database connection failed"},
                metadata={"level": "ERROR", "source": "db_module"},
            )
        )

        # This will NOT match (INFO level)
        await bus.publish(
            Event(
                topic="log",
                data={"message": "Server started"},
                metadata={"level": "INFO", "source": "server"},
            )
        )

        # This will match (premium + purchase)
        await bus.publish(
            Event(
                topic="user.action",
                data={"action": "purchase", "item": "Premium Feature"},
                context={"premium": True, "user_id": "alice123"},
            )
        )

        # Wait for processing
        await asyncio.sleep(0.5)

        print("\n✅ Only filtered events were handled!")


if __name__ == "__main__":
    asyncio.run(main())
