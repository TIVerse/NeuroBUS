"""
Semantic Threshold Tuning Example

Demonstrates how to tune similarity thresholds for semantic matching.
"""

import asyncio

from neurobus import Event, NeuroBus
from neurobus.config import NeuroBusConfig


async def main():
    """Demonstrate semantic threshold tuning."""
    # Enable semantic routing
    config = NeuroBusConfig(semantic={"enabled": True})
    bus = NeuroBus(config=config)

    print("🎯 Semantic Threshold Tuning Example\n")
    print("Different thresholds affect which events match semantically\n")

    # Strict matching (threshold=0.9) - only very similar events
    @bus.subscribe("user_authentication", semantic=True, threshold=0.9)
    async def strict_auth_handler(event: Event):
        print(f"🔒 STRICT (0.9): {event.topic}")

    # Moderate matching (threshold=0.7) - reasonably similar events
    @bus.subscribe("user_authentication", semantic=True, threshold=0.7)
    async def moderate_auth_handler(event: Event):
        print(f"🟡 MODERATE (0.7): {event.topic}")

    # Loose matching (threshold=0.5) - broadly similar events
    @bus.subscribe("user_authentication", semantic=True, threshold=0.5)
    async def loose_auth_handler(event: Event):
        print(f"🟢 LOOSE (0.5): {event.topic}\n")

    async with bus:
        await bus.start()

        print("Publishing events with varying similarity...\n")

        # Very similar
        print("Event 1: user_login (very similar)")
        await bus.publish(Event(topic="user_login", data={}))
        await asyncio.sleep(0.2)

        # Moderately similar
        print("Event 2: authentication_success (moderately similar)")
        await bus.publish(Event(topic="authentication_success", data={}))
        await asyncio.sleep(0.2)

        # Somewhat similar
        print("Event 3: signin_complete (somewhat similar)")
        await bus.publish(Event(topic="signin_complete", data={}))
        await asyncio.sleep(0.2)

        # Less similar
        print("Event 4: password_reset (less similar)")
        await bus.publish(Event(topic="password_reset", data={}))
        await asyncio.sleep(0.2)

        print("\n💡 Tips for threshold tuning:")
        print("   0.9-1.0:  Very strict, only near-exact semantic matches")
        print("   0.7-0.9:  Moderate, good for related concepts")
        print("   0.5-0.7:  Loose, broader semantic matching")
        print("   <0.5:     Very loose, may match unrelated topics")


if __name__ == "__main__":
    asyncio.run(main())
