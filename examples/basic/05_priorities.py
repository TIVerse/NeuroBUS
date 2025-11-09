"""
Subscription Priority Example

Demonstrates how subscription priorities affect handler execution order.
"""

import asyncio

from neurobus import Event, NeuroBus


async def main():
    """Demonstrate subscription priorities."""
    bus = NeuroBus()

    print("🎯 Subscription Priority Example\n")
    print("Handlers execute in priority order (high to low)\n")

    # High priority handler (executes first)
    @bus.subscribe("task", priority=10)
    async def high_priority(event: Event):
        print("🔴 HIGH PRIORITY (10): Processing critical task")
        await asyncio.sleep(0.1)

    # Medium priority handler
    @bus.subscribe("task", priority=5)
    async def medium_priority(event: Event):
        print("🟡 MEDIUM PRIORITY (5): Processing normal task")
        await asyncio.sleep(0.1)

    # Low priority handler (executes last)
    @bus.subscribe("task", priority=1)
    async def low_priority(event: Event):
        print("🟢 LOW PRIORITY (1): Processing background task")
        await asyncio.sleep(0.1)

    # Default priority (0)
    @bus.subscribe("task")
    async def default_priority(event: Event):
        print("⚪ DEFAULT PRIORITY (0): Processing with default priority")
        await asyncio.sleep(0.1)

    async with bus:
        print("Publishing event...\n")

        await bus.publish(Event(topic="task", data={"task_id": "123"}))

        # Wait for handlers to complete
        await asyncio.sleep(1)

        print("\n✅ Notice how handlers executed in priority order!")
        print("   Priority: 10 → 5 → 1 → 0")


if __name__ == "__main__":
    asyncio.run(main())
