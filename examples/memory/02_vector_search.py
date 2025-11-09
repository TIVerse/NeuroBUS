"""
Vector Database Search Example

Demonstrates using Qdrant for semantic event search.
Note: Requires Qdrant server running and sentence-transformers installed.
"""

import asyncio

from neurobus import Event, NeuroBus
from neurobus.memory import QdrantAdapter
from neurobus.semantic import EventEncoder


async def main():
    """Demonstrate vector database search."""
    print("🎯 Vector Database Search Example\n")
    print("⚠️  Prerequisites:")
    print("   - Qdrant running: docker run -p 6333:6333 qdrant/qdrant")
    print("   - pip install qdrant-client sentence-transformers\n")

    try:
        # Create encoder and adapter
        encoder = EventEncoder(model_name="all-MiniLM-L6-v2")
        adapter = QdrantAdapter(url="http://localhost:6333", collection_name="neurobus_demo")

        await adapter.initialize()
        print("✅ Connected to Qdrant\n")

        # Store some events with embeddings
        print("Storing events...\n")

        events = [
            Event(topic="user_login", data={"user": "alice", "method": "oauth"}),
            Event(topic="authentication_success", data={"user": "bob", "method": "password"}),
            Event(topic="password_reset", data={"user": "charlie", "reason": "forgotten"}),
            Event(topic="user_logout", data={"user": "alice", "duration": "2h"}),
            Event(topic="session_expired", data={"user": "bob", "timeout": "30m"}),
        ]

        for event in events:
            # Generate embedding
            embedding = encoder.encode(event.topic)
            # Store in Qdrant
            await adapter.store_event(event, embedding)
            print(f"   Stored: {event.topic}")

        print("\n🔍 Searching for similar events...\n")

        # Search for authentication-related events
        query = "user authentication"
        query_embedding = encoder.encode(query)

        results = await adapter.search_similar(query_embedding, k=3)

        print(f"Query: '{query}'")
        print(f"Top {len(results)} results:\n")

        for i, result in enumerate(results, 1):
            print(f"{i}. {result.payload['topic']}")
            print(f"   Similarity: {result.score:.3f}")
            print(f"   User: {result.payload['data'].get('user', 'N/A')}\n")

        # Get statistics
        stats = adapter.get_stats()
        print(f"📊 Statistics:")
        print(f"   Events stored: {stats['events_stored']}")
        print(f"   Searches performed: {stats['searches_performed']}")

        # Cleanup
        await adapter.close()

    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("\nInstall with:")
        print("   pip install qdrant-client sentence-transformers")

    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nMake sure Qdrant is running:")
        print("   docker run -d -p 6333:6333 qdrant/qdrant")


if __name__ == "__main__":
    asyncio.run(main())
