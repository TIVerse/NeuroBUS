"""Tests for semantic encoder."""

import pytest

pytest.importorskip("sentence_transformers")

import numpy as np

from neurobus.semantic.encoder import SemanticEncoder


class TestSemanticEncoder:
    """Test cases for SemanticEncoder."""

    def test_encoder_creation(self):
        """Test encoder initialization."""
        encoder = SemanticEncoder(
            model_name="all-MiniLM-L6-v2",
            cache_size=100,
            cache_ttl=60.0,
        )

        assert encoder.model_name == "all-MiniLM-L6-v2"
        assert not encoder._model_loaded

    def test_encode_single_text(self):
        """Test encoding single text."""
        encoder = SemanticEncoder(model_name="all-MiniLM-L6-v2")

        embedding = encoder.encode("hello world")

        assert isinstance(embedding, np.ndarray)
        assert embedding.shape[0] == encoder.embedding_dim
        # Should be normalized
        assert np.isclose(np.linalg.norm(embedding), 1.0)

    def test_encode_uses_cache(self):
        """Test that encoding uses cache."""
        encoder = SemanticEncoder(model_name="all-MiniLM-L6-v2")

        # First encoding
        embedding1 = encoder.encode("test text")

        # Second encoding (should hit cache)
        embedding2 = encoder.encode("test text")

        assert np.array_equal(embedding1, embedding2)

        stats = encoder.cache.get_stats()
        assert stats["hits"] > 0

    def test_encode_batch(self):
        """Test batch encoding."""
        encoder = SemanticEncoder(model_name="all-MiniLM-L6-v2")

        texts = ["hello", "world", "test"]
        embeddings = encoder.encode_batch(texts)

        assert len(embeddings) == 3
        for emb in embeddings:
            assert isinstance(emb, np.ndarray)
            assert np.isclose(np.linalg.norm(emb), 1.0)

    def test_similarity(self):
        """Test similarity computation."""
        encoder = SemanticEncoder(model_name="all-MiniLM-L6-v2")

        emb1 = encoder.encode("hello world")
        emb2 = encoder.encode("hello world")
        emb3 = encoder.encode("goodbye universe")

        # Same text should be very similar
        sim1 = encoder.similarity(emb1, emb2)
        assert sim1 > 0.99

        # Different text should be less similar
        sim2 = encoder.similarity(emb1, emb3)
        assert sim2 < 0.99

    def test_similarity_batch(self):
        """Test batch similarity computation."""
        encoder = SemanticEncoder(model_name="all-MiniLM-L6-v2")

        query = encoder.encode("user login")
        candidates = [
            encoder.encode("user authentication"),
            encoder.encode("system error"),
            encoder.encode("user signin"),
        ]

        similarities = encoder.similarity_batch(query, candidates)

        assert len(similarities) == 3
        assert all(0 <= sim <= 1 for sim in similarities)

        # "user authentication" and "user signin" should be more similar to "user login"
        # than "system error"
        assert similarities[0] > similarities[1]
        assert similarities[2] > similarities[1]

    def test_get_stats(self):
        """Test getting encoder statistics."""
        encoder = SemanticEncoder(model_name="all-MiniLM-L6-v2")

        encoder.encode("test")

        stats = encoder.get_stats()

        assert stats["model_name"] == "all-MiniLM-L6-v2"
        assert stats["model_loaded"] is True
        assert stats["embedding_dim"] is not None
        assert "cache" in stats

    def test_repr(self):
        """Test string representation."""
        encoder = SemanticEncoder(model_name="all-MiniLM-L6-v2")

        repr_str = repr(encoder)

        assert "SemanticEncoder" in repr_str
        assert "all-MiniLM-L6-v2" in repr_str
