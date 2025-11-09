"""Tests for semantic router."""

import pytest

pytest.importorskip("sentence_transformers")

from neurobus.core.event import Event
from neurobus.core.subscription import Subscription
from neurobus.semantic.router import SemanticRouter


class TestSemanticRouter:
    """Test cases for SemanticRouter."""

    def test_router_creation(self):
        """Test router initialization."""
        router = SemanticRouter(
            model_name="all-MiniLM-L6-v2",
            default_threshold=0.75,
        )

        assert router.default_threshold == 0.75
        assert router.encoder.model_name == "all-MiniLM-L6-v2"

    async def test_find_semantic_matches(self):
        """Test finding semantic matches."""
        router = SemanticRouter(model_name="all-MiniLM-L6-v2")

        # Create semantic subscriptions
        async def handler(event: Event):
            pass

        sub1 = Subscription(
            pattern="user authentication",
            handler=handler,
            semantic=True,
            threshold=0.7,
        )

        sub2 = Subscription(
            pattern="system errors",
            handler=handler,
            semantic=True,
            threshold=0.7,
        )

        # Event about user login (should match sub1)
        event = Event(topic="user.login", data={})

        matches = router.find_semantic_matches(
            event,
            [sub1, sub2],
            threshold=0.7,
        )

        # Should find matches
        assert len(matches) > 0

        # First match should be sub1 (more similar to "user login")
        assert matches[0][0] == sub1
        assert matches[0][1] > 0.7  # Similarity score

    async def test_respects_threshold(self):
        """Test that threshold is respected."""
        router = SemanticRouter(model_name="all-MiniLM-L6-v2")

        async def handler(event: Event):
            pass

        sub = Subscription(
            pattern="completely unrelated topic",
            handler=handler,
            semantic=True,
            threshold=0.95,  # Very high threshold
        )

        event = Event(topic="user.login", data={})

        matches = router.find_semantic_matches(
            event,
            [sub],
            threshold=0.95,
        )

        # Should not match due to high threshold
        assert len(matches) == 0

    async def test_filters_non_semantic_subscriptions(self):
        """Test that non-semantic subscriptions are filtered."""
        router = SemanticRouter(model_name="all-MiniLM-L6-v2")

        async def handler(event: Event):
            pass

        semantic_sub = Subscription(
            pattern="user login",
            handler=handler,
            semantic=True,
        )

        pattern_sub = Subscription(
            pattern="user.*",
            handler=handler,
            semantic=False,
        )

        event = Event(topic="user.login", data={})

        matches = router.find_semantic_matches(
            event,
            [semantic_sub, pattern_sub],
        )

        # Should only return semantic subscription
        assert len(matches) == 1
        assert matches[0][0] == semantic_sub

    def test_compute_similarity(self):
        """Test direct similarity computation."""
        router = SemanticRouter(model_name="all-MiniLM-L6-v2")

        sim = router.compute_similarity("hello world", "hello world")

        assert sim > 0.99
        assert 0 <= sim <= 1

    def test_get_embedding(self):
        """Test getting embeddings."""
        router = SemanticRouter(model_name="all-MiniLM-L6-v2")

        embedding = router.get_embedding("test text")

        assert embedding is not None
        assert len(embedding.shape) == 1

    def test_get_stats(self):
        """Test getting router statistics."""
        router = SemanticRouter(model_name="all-MiniLM-L6-v2")

        router.get_embedding("test")

        stats = router.get_stats()

        assert "total_queries" in stats
        assert "total_matches" in stats
        assert "default_threshold" in stats
        assert "encoder" in stats

    def test_reset_stats(self):
        """Test resetting statistics."""
        router = SemanticRouter(model_name="all-MiniLM-L6-v2")

        router.get_embedding("test")

        router.reset_stats()

        stats = router.get_stats()
        assert stats["total_queries"] == 0
        assert stats["total_matches"] == 0

    def test_repr(self):
        """Test string representation."""
        router = SemanticRouter(model_name="all-MiniLM-L6-v2")

        repr_str = repr(router)

        assert "SemanticRouter" in repr_str
        assert "all-MiniLM-L6-v2" in repr_str
