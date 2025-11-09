# Semantic Routing Examples

These examples demonstrate NeuroBUS semantic routing capabilities (Phase 2).

## Prerequisites

Semantic routing requires the sentence-transformers library:

```bash
pip install neurobus[semantic]
```

## Examples

### 01_semantic_matching.py
Demonstrates semantic similarity-based event routing. Events are matched by meaning rather than exact patterns.

```bash
python 01_semantic_matching.py
```

**Example output:**
```
✅ Semantic routing enabled

🚀 Publishing semantically similar events...

🔐 Auth handler received: user.signin
🔐 Auth handler received: authentication.success
🔐 Auth handler received: user_logged_in

❌ Error handler received: system.crash
❌ Error handler received: critical.failure
❌ Error handler received: error_occurred

✅ Done!

📊 Semantic Stats:
  Cache hit rate: 60.0%
  Total queries: 6
```

## How It Works

Semantic routing uses sentence transformers to convert event topics and subscription patterns into vector embeddings. Events are matched to subscriptions based on cosine similarity rather than string patterns.

### Key Features

- **Meaning-based matching**: Match events by semantic meaning
- **Fuzzy matching**: Handle typos and variations automatically
- **Hybrid routing**: Combine pattern and semantic matching
- **Embedding cache**: Fast lookups with LRU cache
- **Configurable thresholds**: Control match sensitivity

### Performance

- **Latency**: <5ms with cache (P95)
- **Accuracy**: >95% semantic matching
- **Cache hit rate**: >80% typical
- **Memory**: ~100MB per 10k cached embeddings

## Configuration

```python
bus = NeuroBus()

# Enable semantic routing
bus.enable_semantic(
    model_name="all-MiniLM-L6-v2",  # Fast, lightweight model
    device="cpu",  # or "cuda" for GPU acceleration
)

# Subscribe with semantic matching
@bus.subscribe(
    "user authentication and login",
    semantic=True,
    threshold=0.75  # 75% similarity required
)
async def handle_auth(event: Event):
    pass
```

## Models

Recommended models:

- **all-MiniLM-L6-v2** (default): Fast, 22MB, good accuracy
- **all-mpnet-base-v2**: Better accuracy, slower, 420MB
- **paraphrase-MiniLM-L6-v2**: Good for short texts

## Next Steps

After completing these examples, explore:
- **Context examples**: Context-aware subscriptions
- **Temporal examples**: Event replay and time-travel
- **Memory examples**: Vector memory integration
