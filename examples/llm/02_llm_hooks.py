"""
LLM Hooks Example

Demonstrates automatic LLM reasoning triggered by event patterns.
"""

import asyncio

from neurobus import Event, NeuroBus
from neurobus.llm import LLMBridge


async def main():
    """Demonstrate LLM hooks."""
    bus = NeuroBus()

    print("🎯 LLM Hooks Example\n")
    print("Automatically triggers LLM reasoning when events match patterns\n")

    # Create LLM bridge with mock provider (no API key needed)
    llm = LLMBridge(provider="mock")
    await llm.initialize()

    # Register hook for error events
    @llm.hook(
        "error.*",
        prompt_template="""Analyze this error:
Topic: {topic}
Error: {data[error]}
Timestamp: {timestamp}

Provide:
1. Root cause
2. Impact assessment
3. Recommended action
""",
    )
    async def analyze_error(event, reasoning):
        print(f"🤖 LLM Error Analysis:")
        print(f"   Event: {event.topic}")
        print(f"   Analysis: {reasoning[:200]}...\n")

    # Register hook for user feedback
    @llm.hook(
        "user.feedback",
        prompt_template="""Analyze user feedback:
User: {data[user]}
Rating: {data[rating]}/5
Comment: {data[comment]}

Categorize sentiment and extract key points.
""",
    )
    async def analyze_feedback(event, reasoning):
        print(f"💬 LLM Feedback Analysis:")
        print(f"   User: {event.data['user']}")
        print(f"   Insights: {reasoning[:200]}...\n")

    # Register hook for performance metrics
    @llm.hook(
        "performance.*",
        prompt_template="""Analyze performance metrics:
Metric: {topic}
Value: {data[value]}
Threshold: {data[threshold]}

Should we be concerned? Recommend actions.
""",
    )
    async def analyze_performance(event, reasoning):
        print(f"📊 LLM Performance Analysis:")
        print(f"   Metric: {event.topic}")
        print(f"   Recommendation: {reasoning[:200]}...\n")

    async with bus:
        print("Publishing events (LLM hooks will trigger automatically)...\n")

        # Error event - triggers error analysis hook
        await bus.publish(
            Event(
                topic="error.database",
                data={
                    "error": "Connection timeout after 30s",
                    "database": "users_db",
                    "retries": 3,
                },
            )
        )

        # Process hook
        await llm.process_event(
            Event(
                topic="error.database",
                data={
                    "error": "Connection timeout after 30s",
                    "database": "users_db",
                    "retries": 3,
                },
            )
        )
        await asyncio.sleep(0.5)

        # Feedback event - triggers feedback analysis hook
        feedback_event = Event(
            topic="user.feedback",
            data={
                "user": "alice123",
                "rating": 4,
                "comment": "Great product but could use better documentation",
            },
        )
        await bus.publish(feedback_event)
        await llm.process_event(feedback_event)
        await asyncio.sleep(0.5)

        # Performance event - triggers performance analysis hook
        perf_event = Event(
            topic="performance.cpu_usage",
            data={"value": 92, "threshold": 80, "duration": "5min"},
        )
        await bus.publish(perf_event)
        await llm.process_event(perf_event)
        await asyncio.sleep(0.5)

        print("\n✅ LLM hooks provide automatic intelligent analysis!")
        print("   No manual LLM integration needed")
        print("   Pattern-based triggering")
        print("   Async execution doesn't block event processing")


if __name__ == "__main__":
    asyncio.run(main())
