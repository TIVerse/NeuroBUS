"""Tests for embedding cache."""

import time

import numpy as np

from neurobus.semantic.cache import EmbeddingCache


class TestEmbeddingCache:
    """Test cases for EmbeddingCache."""

    def test_cache_creation(self):
        """Test cache initialization."""
        cache = EmbeddingCache(max_size=100, ttl=60.0)

        assert cache.max_size == 100
        assert cache.ttl == 60.0
        assert cache.size() == 0

    def test_set_and_get(self):
        """Test setting and getting embeddings."""
        cache = EmbeddingCache()
        embedding = np.array([0.1, 0.2, 0.3])

        cache.set("test", embedding)

        retrieved = cache.get("test")
        assert retrieved is not None
        assert np.array_equal(retrieved, embedding)

    def test_cache_miss(self):
        """Test cache miss."""
        cache = EmbeddingCache()

        result = cache.get("nonexistent")

        assert result is None

    def test_ttl_expiration(self):
        """Test TTL-based expiration."""
        cache = EmbeddingCache(max_size=100, ttl=0.1)  # 100ms TTL
        embedding = np.array([0.1, 0.2, 0.3])

        cache.set("test", embedding)
        assert cache.get("test") is not None

        # Wait for expiration
        time.sleep(0.15)

        assert cache.get("test") is None

    def test_no_ttl(self):
        """Test cache without TTL."""
        cache = EmbeddingCache(max_size=100, ttl=0)  # No expiration
        embedding = np.array([0.1, 0.2, 0.3])

        cache.set("test", embedding)
        time.sleep(0.1)

        # Should still be there
        assert cache.get("test") is not None

    def test_lru_eviction(self):
        """Test LRU eviction policy."""
        cache = EmbeddingCache(max_size=2, ttl=0)
        emb1 = np.array([0.1, 0.2, 0.3])
        emb2 = np.array([0.4, 0.5, 0.6])
        emb3 = np.array([0.7, 0.8, 0.9])

        cache.set("key1", emb1)
        cache.set("key2", emb2)
        cache.set("key3", emb3)  # Should evict key1

        assert cache.get("key1") is None  # Evicted
        assert cache.get("key2") is not None
        assert cache.get("key3") is not None

    def test_lru_update(self):
        """Test LRU update on access."""
        cache = EmbeddingCache(max_size=2, ttl=0)
        emb1 = np.array([0.1, 0.2, 0.3])
        emb2 = np.array([0.4, 0.5, 0.6])
        emb3 = np.array([0.7, 0.8, 0.9])

        cache.set("key1", emb1)
        cache.set("key2", emb2)

        # Access key1 to make it most recent
        cache.get("key1")

        # Add key3, should evict key2 (least recent)
        cache.set("key3", emb3)

        assert cache.get("key1") is not None  # Still there
        assert cache.get("key2") is None  # Evicted
        assert cache.get("key3") is not None

    def test_clear(self):
        """Test clearing cache."""
        cache = EmbeddingCache()
        cache.set("key1", np.array([0.1, 0.2, 0.3]))
        cache.set("key2", np.array([0.4, 0.5, 0.6]))

        cache.clear()

        assert cache.size() == 0
        assert cache.get("key1") is None
        assert cache.get("key2") is None

    def test_statistics(self):
        """Test cache statistics."""
        cache = EmbeddingCache(max_size=100, ttl=60)
        emb = np.array([0.1, 0.2, 0.3])

        cache.set("key1", emb)

        # Hit
        cache.get("key1")

        # Miss
        cache.get("nonexistent")

        stats = cache.get_stats()

        assert stats["size"] == 1
        assert stats["max_size"] == 100
        assert stats["hits"] == 1
        assert stats["misses"] == 1
        assert stats["hit_rate"] == 0.5
        assert stats["total_requests"] == 2

    def test_reset_stats(self):
        """Test resetting statistics."""
        cache = EmbeddingCache()

        cache.set("key1", np.array([0.1, 0.2, 0.3]))
        cache.get("key1")
        cache.get("nonexistent")

        cache.reset_stats()

        stats = cache.get_stats()
        assert stats["hits"] == 0
        assert stats["misses"] == 0

    def test_len(self):
        """Test __len__ method."""
        cache = EmbeddingCache()

        assert len(cache) == 0

        cache.set("key1", np.array([0.1, 0.2, 0.3]))
        assert len(cache) == 1

        cache.set("key2", np.array([0.4, 0.5, 0.6]))
        assert len(cache) == 2

    def test_repr(self):
        """Test string representation."""
        cache = EmbeddingCache(max_size=100)
        cache.set("key1", np.array([0.1, 0.2, 0.3]))
        cache.get("key1")

        repr_str = repr(cache)

        assert "EmbeddingCache" in repr_str
        assert "1/100" in repr_str
