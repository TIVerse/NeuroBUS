"""
Async Handlers Example

Demonstrates parallel async handler execution.
"""

import asyncio
import time

from neurobus import Event, NeuroBus


async def main():
    """Run the async handlers example."""
    bus = NeuroBus()
    
    # Handler with delay
    @bus.subscribe("task")
    async def slow_handler_1(event: Event):
        print(f"🔄 Handler 1 started at {time.time():.2f}")
        await asyncio.sleep(0.2)  # Simulate slow operation
        print(f"✅ Handler 1 completed at {time.time():.2f}")
    
    # Another handler with delay
    @bus.subscribe("task")
    async def slow_handler_2(event: Event):
        print(f"🔄 Handler 2 started at {time.time():.2f}")
        await asyncio.sleep(0.2)  # Simulate slow operation
        print(f"✅ Handler 2 completed at {time.time():.2f}")
    
    # Fast handler
    @bus.subscribe("task")
    async def fast_handler(event: Event):
        print(f"⚡ Fast handler executed at {time.time():.2f}")
    
    async with bus:
        print("🚀 Publishing event with parallel handlers...\n")
        start = time.time()
        
        await bus.publish(Event(topic="task", data={"job": "process_data"}))
        
        # Wait for all handlers to complete
        await asyncio.sleep(0.3)
        
        elapsed = time.time() - start
        print(f"\n⏱️  Total time: {elapsed:.2f}s")
        print("📊 Handlers ran in parallel!")


if __name__ == "__main__":
    asyncio.run(main())
