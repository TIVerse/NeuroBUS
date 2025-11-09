"""
LLM Event Analysis Example

Demonstrates using LLM reasoning engine to analyze events intelligently.
"""

import asyncio

from neurobus import Event, NeuroBus
from neurobus.config.schema import NeuroBusConfig


async def main():
    """Run the LLM event analysis example."""
    # Create bus with LLM reasoning enabled (using mock for demo)
    config = NeuroBusConfig(
        llm={
            "enabled": True,
            "provider": "mock",  # Use mock for demo (no API key needed)
            "enable_chain_of_thought": True,
        }
    )
    bus = NeuroBus(config=config)
    
    print("✅ Reasoning engine enabled with mock LLM\n")
    
    async with bus:
        print("🚀 Publishing events for analysis...\n")
        
        # Create some events
        event1 = Event(
            topic="user.login",
            data={"user": "alice", "ip": "192.168.1.100", "success": True}
        )
        
        event2 = Event(
            topic="system.error",
            data={"error": "Database connection failed", "severity": "high"}
        )
        
        event3 = Event(
            topic="user.purchase",
            data={"user": "bob", "item": "laptop", "amount": 1299.99}
        )
        
        await bus.publish(event1)
        await bus.publish(event2)
        await bus.publish(event3)
        
        await asyncio.sleep(0.1)
        
        print("\n🔍 Analyzing individual event...\n")
        
        # Analyze a single event
        analysis = await bus.reasoning.analyze_event(event2)
        
        if "error" not in analysis:
            print(f"Classification: {analysis.get('classification', 'N/A')}")
            print(f"Sentiment: {analysis.get('sentiment', 'N/A')}")
            print(f"Priority: {analysis.get('priority', 'N/A')}")
            print(f"Insights: {analysis.get('insights', [])}")
            print(f"Tokens used: {analysis.get('tokens_used', 0)}")
        else:
            print(f"Raw analysis: {analysis.get('raw_analysis', 'N/A')}")
        
        print("\n📊 Extracting insights from multiple events...\n")
        
        # Extract insights from multiple events
        insights = await bus.reasoning.extract_insights(
            [event1, event2, event3],
            time_window="last 5 minutes"
        )
        
        if "error" not in insights:
            print(f"Patterns detected: {insights.get('patterns', [])}")
            print(f"Anomalies: {insights.get('anomalies', [])}")
            print(f"Trends: {insights.get('trends', [])}")
            print(f"Summary: {insights.get('summary', 'N/A')}")
            print(f"Events analyzed: {insights.get('events_analyzed', 0)}")
        else:
            print(f"Raw insights: {insights.get('raw_response', 'N/A')}")
        
        print("\n🎯 Making decision...\n")
        
        # Make a decision about an event
        decision = await bus.reasoning.make_decision(
            event2,
            options=["escalate", "auto-fix", "ignore", "notify-admin"],
            criteria={"severity": "high", "impact": "database"}
        )
        
        if "error" not in decision:
            print(f"Chosen option: {decision.get('chosen_option', 'N/A')}")
            print(f"Confidence: {decision.get('confidence', 0)}")
            print(f"Reasoning: {decision.get('reasoning', 'N/A')}")
            print(f"Alternatives: {decision.get('alternatives', [])}")
        else:
            print(f"Raw decision: {decision.get('raw_response', 'N/A')}")
        
        print("\n🧠 Reasoning about events...\n")
        
        # Reason about events
        reasoning = await bus.reasoning.reason_about_events(
            [event1, event2, event3],
            question="What is the most critical issue that needs attention?"
        )
        
        if "error" not in reasoning:
            print(f"Answer: {reasoning.get('answer', 'N/A')}")
            if "reasoning_steps" in reasoning:
                print(f"Reasoning steps: {reasoning['reasoning_steps']}")
            print(f"Confidence: {reasoning.get('confidence', 'N/A')}")
        else:
            print(f"Raw reasoning: {reasoning.get('reasoning', 'N/A')}")
        
        # Show statistics
        stats = bus.get_stats()
        if "reasoning" in stats:
            reasoning_stats = stats["reasoning"]
            print(f"\n📈 Reasoning Stats:")
            print(f"  Analyses performed: {reasoning_stats['analyses']}")
            print(f"  Insights extracted: {reasoning_stats['insights_extracted']}")
            print(f"  Decisions made: {reasoning_stats['decisions_made']}")
            
            connector_stats = reasoning_stats.get('connector_stats', {})
            print(f"  LLM requests: {connector_stats.get('requests', 0)}")
            print(f"  Tokens used: {connector_stats.get('tokens_used', 0)}")
        
        print("\n✅ Done!")
        print("\n💡 Note: This example uses a mock LLM. For real analysis:")
        print("   - Set provider to 'openai' or 'anthropic'")
        print("   - Provide API key in config")
        print("   - Install: pip install openai  # or pip install anthropic")


if __name__ == "__main__":
    asyncio.run(main())
