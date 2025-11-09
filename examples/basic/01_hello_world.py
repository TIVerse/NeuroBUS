"""
Hello World Example for NeuroBUS

Demonstrates basic event publishing and subscription.
"""

import asyncio

from neurobus import Event, NeuroBus


async def main():
    """Run the hello world example."""
    # Create bus instance
    bus = NeuroBus()
    
    # Subscribe to greeting events
    @bus.subscribe("greeting")
    async def handle_greeting(event: Event):
        message = event.data.get("message", "No message")
        print(f"📩 Received greeting: {message}")
    
    # Start bus and publish event
    async with bus:
        print("🚀 NeuroBUS started!")
        
        # Publish a greeting event
        await bus.publish(Event(
            topic="greeting",
            data={"message": "Hello, NeuroBUS!"}
        ))
        
        # Wait a moment for the handler to execute
        await asyncio.sleep(0.1)
        
        print("✅ Done!")


if __name__ == "__main__":
    asyncio.run(main())
