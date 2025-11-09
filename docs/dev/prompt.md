# 🧠 NeuroBUS - Complete Implementation Prompt

**Version:** 1.0 | **Target:** AI Assistants & Dev Teams | **Mode:** Sequential Phase Execution

---

## 🎯 ROLE & CONTEXT

**You are:** An Elite Senior Python Architect specializing in cognitive AI systems, event architectures, semantic computing, and high-performance async Python.

**Mission:** Implement **NeuroBUS** - the world's first **Neuro-Semantic Event Bus** that transforms message passing into meaning passing for cognitive AI systems.

**Core Innovation:** Unlike traditional event buses (Redis, RabbitMQ, Kafka), NeuroBUS routes events by semantic meaning, maintains contextual awareness, enables time-travel debugging, integrates with vector memory stores, and triggers LLM reasoning hooks.

---

## 📊 PERFORMANCE TARGETS

| Metric | Target | Validation |
|--------|--------|------------|
| P95 Latency | <2ms | Load test with prometheus |
| Throughput | 10,000 events/sec | Concurrent async benchmark |
| Semantic Accuracy | >95% | Test dataset with known pairs |
| Memory (base) | <100MB | Process memory profiling |
| Test Coverage | >90% | pytest-cov |
| Type Coverage | 100% | mypy strict mode |

---

## 🏗️ ARCHITECTURE BLUEPRINT

```
neurobus/
├── __init__.py              # Public API exports
├── __version__.py           # Version info
├── core/                    # Event bus core (Phase 1)
│   ├── bus.py              # Main NeuroBus class
│   ├── event.py            # Event model
│   ├── subscription.py     # Subscription model
│   ├── dispatcher.py       # Async event dispatcher
│   ├── registry.py         # Subscription registry
│   └── lifecycle.py        # Bus lifecycle management
├── semantic/                # Semantic routing (Phase 2)
│   ├── router.py           # Semantic router orchestrator
│   ├── encoder.py          # Embedding generation
│   ├── matcher.py          # Similarity matching
│   ├── cache.py            # LRU embedding cache
│   ├── similarity.py       # Cosine similarity utils
│   └── models.py           # Config & types
├── context/                 # Context engine (Phase 3)
│   ├── engine.py           # Context orchestrator
│   ├── state.py            # Thread-safe state store
│   ├── scope.py            # Scoped contexts
│   ├── filter.py           # Filter evaluation
│   ├── dsl.py              # Filter DSL parser
│   └── merger.py           # Context merging logic
├── temporal/                # Time-travel (Phase 4)
│   ├── store.py            # Event persistence
│   ├── wal.py              # Write-ahead log
│   ├── replay.py           # Replay engine
│   ├── query.py            # Temporal queries
│   ├── index.py            # Time-based indexing
│   └── causality.py        # Causality graph
├── memory/                  # Vector memory (Phase 5)
│   ├── adapter.py          # Memory adapter interface
│   ├── qdrant_client.py    # Qdrant implementation
│   ├── lancedb_client.py   # LanceDB implementation
│   ├── linker.py           # Event-memory linking
│   ├── search.py           # Semantic search
│   └── persistence.py      # Memory persistence
├── llm/                     # LLM integration (Phase 6)
│   ├── hooks.py            # Hook registry
│   ├── bridge.py           # LLM bridge orchestrator
│   ├── providers/          # LLM providers
│   │   ├── anthropic.py    # Claude integration
│   │   ├── openai.py       # GPT integration
│   │   └── ollama.py       # Local LLM
│   ├── prompts.py          # Prompt templates
│   ├── templates.py        # Template engine
│   └── reasoning.py        # Reasoning utils
├── monitoring/              # Observability (Phase 7)
│   ├── metrics.py          # Prometheus metrics
│   ├── tracing.py          # OpenTelemetry
│   ├── logging.py          # Structured logging
│   └── health.py           # Health checks
├── utils/                   # Utilities
│   ├── serialization.py    # msgpack ser/deser
│   ├── timing.py           # Timing utils
│   ├── validation.py       # Input validation
│   ├── patterns.py         # Common patterns
│   └── helpers.py          # Generic helpers
├── config/                  # Configuration
│   ├── schema.py           # Pydantic schemas
│   ├── loader.py           # Config loading
│   ├── validator.py        # Config validation
│   └── defaults.py         # Default configs
├── exceptions/              # Custom exceptions
│   ├── core.py             # Core exceptions
│   ├── semantic.py         # Semantic exceptions
│   ├── temporal.py         # Temporal exceptions
│   └── memory.py           # Memory exceptions
└── types/                   # Type definitions
    ├── events.py           # Event types
    ├── subscriptions.py    # Subscription types
    ├── context.py          # Context types
    └── protocols.py        # Protocol definitions

tests/
├── unit/                    # Unit tests (>90% coverage)
│   ├── test_core/
│   ├── test_semantic/
│   ├── test_context/
│   ├── test_temporal/
│   ├── test_memory/
│   ├── test_llm/
│   └── test_utils/
├── integration/             # Integration tests
│   ├── test_pubsub_flow.py
│   ├── test_semantic_routing.py
│   ├── test_context_filtering.py
│   ├── test_temporal_replay.py
│   ├── test_memory_integration.py
│   └── test_llm_workflow.py
├── performance/             # Performance tests
│   ├── test_latency.py
│   ├── test_throughput.py
│   ├── test_memory_usage.py
│   └── benchmarks.py
├── fixtures/                # Test fixtures
│   ├── events.py
│   ├── semantic_pairs.json
│   └── test_data.py
└── mocks/                   # Mock implementations
    ├── mock_llm.py
    ├── mock_qdrant.py
    └── mock_embeddings.py

examples/
├── basic/                   # Basic examples
├── semantic/                # Semantic routing
├── context/                 # Context aware
├── temporal/                # Time travel
├── memory/                  # Memory integration
├── llm/                     # LLM hooks
└── advanced/                # Advanced patterns

docs/                        # (Already exists)
scripts/                     # Dev/build scripts
config/                      # Config examples
docker/                      # Docker files
kubernetes/                  # K8s manifests
```

---

## 🔧 TECHNOLOGY STACK

```toml
[tool.poetry.dependencies]
python = "^3.11"
asyncio = "*"
aiofiles = "^23.2"
sentence-transformers = "^2.2"
qdrant-client = "^1.7"
lancedb = "^0.3"
numpy = "^1.24"
msgpack = "^1.0"
pyyaml = "^6.0"
pydantic = "^2.5"
anthropic = "^0.18"
openai = "^1.12"
faiss-cpu = "^1.7"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4"
pytest-asyncio = "^0.21"
pytest-cov = "^4.1"
pytest-mock = "^3.12"
black = "^23.12"
ruff = "^0.1"
mypy = "^1.8"
```

---

## 📦 PHASE-BY-PHASE IMPLEMENTATION

Execute phases **sequentially**. Each phase must be **100% complete** with passing tests before proceeding.

---

### ✅ PHASE 1: Foundation & Core (Weeks 1-4)

**Goal:** Basic event model, pub/sub (no semantics), async dispatch

**Deliverables:**
1. Project structure (`pyproject.toml`, directories, README, LICENSE)
2. Core types (`Event`, `Subscription`, protocols)
3. `NeuroBus` class with `publish()`, `subscribe()`, `unsubscribe()`
4. `EventDispatcher` with async parallel dispatch & error isolation
5. `SubscriptionRegistry` with exact topic matching
6. Configuration system (Pydantic schemas, YAML loader)
7. Exception hierarchy
8. Utils (validation, serialization, timing)

**Key Algorithm - Event Dispatch:**
```python
async def publish(self, event: Event) -> None:
    # 1. Validate event schema
    # 2. Generate UUID & timestamp if missing
    # 3. Find exact topic matches in registry
    # 4. Dispatch to handlers in parallel with error isolation
    # 5. Each handler exception logged but doesn't crash bus
```

**Tests Required:**
- Unit: test_bus.py, test_dispatcher.py, test_registry.py (>90% coverage)
- Integration: test_pubsub_flow.py (end-to-end)
- Performance: Measure baseline latency & throughput

**Validation:**
- [ ] Can publish & subscribe to exact topics
- [ ] Multiple subscribers receive same event
- [ ] Handler exceptions don't crash bus
- [ ] Async handlers execute in parallel
- [ ] Unsubscribe works correctly
- [ ] Type checking (mypy) passes
- [ ] Tests pass with >90% coverage

---

### ✅ PHASE 2: Semantic Layer (Weeks 5-8)

**Goal:** Embedding generation, semantic similarity, pattern matching

**Deliverables:**
1. `EventEncoder` using sentence-transformers (all-MiniLM-L6-v2, 384-dim)
2. `EmbeddingCache` with LRU eviction & TTL expiration
3. `SemanticMatcher` with cosine similarity computation
4. `SemanticRouter` orchestrating semantic routing
5. Integration with `NeuroBus` for hybrid exact+semantic matching

**Key Algorithm - Semantic Match:**
```python
def semantic_match(event_topic: str, patterns: List[str], threshold: float = 0.75):
    # 1. Encode event topic → embedding_e (or get from cache)
    # 2. For each pattern:
    #    a. Get pattern embedding_p (cache or encode)
    #    b. Compute similarity = dot(embedding_e, embedding_p)
    #    c. If similarity >= threshold, add to matches
    # 3. Sort matches by similarity (descending)
    # 4. Return matched patterns with scores
```

**Accuracy Test Dataset (`tests/fixtures/semantic_pairs.json`):**
```json
{
  "similar_pairs": [
    ["greeting", "hello"], ["farewell", "goodbye"],
    ["error_occurred", "system_failure"],
    ["battery_low", "low_power"],
    ["user_login", "authentication_successful"]
  ],
  "dissimilar_pairs": [
    ["greeting", "database_error"],
    ["weather_query", "file_system_failure"]
  ]
}
```

**Tests Required:**
- Unit: Encoder, cache, matcher, router
- Integration: Semantic pub/sub with threshold tuning
- Performance: Encoding <5ms, similarity <10ms for 100 patterns
- Accuracy: >95% on test dataset

**Validation:**
- [ ] Semantic matching accuracy >95%
- [ ] Cache hit rate >80%
- [ ] Embedding generation <5ms
- [ ] Can handle 1000+ subscription patterns
- [ ] Threshold parameter works correctly

---

### ✅ PHASE 3: Context Engine (Weeks 9-11)

**Goal:** Multi-scope state, context merging, filter DSL

**Deliverables:**
1. `StateStore` (thread-safe, hierarchical: global/session/user)
2. `ContextEngine` with set/get/merge operations
3. `FilterDSL` parser (syntax: `user.mood == "happy" AND time.hour < 22`)
4. `FilterEngine` for subscription filtering
5. `ContextMerger` with precedence rules (event > user > session > global)
6. `ContextScope` context manager for scoped contexts

**Key Algorithm - Context Merging:**
```python
def merge_context(event: Event) -> dict:
    # Precedence: event > user > session > global
    # 1. Start with global context
    # 2. Deep merge session context (if session_id present)
    # 3. Deep merge user context (if user_id present)
    # 4. Deep merge event context (always)
    # 5. Return merged dict
```

**Filter DSL Examples:**
```python
# Lambda filters
@bus.subscribe("msg", filter=lambda e: e.context["mood"] == "happy")

# DSL filters
@bus.subscribe("msg", filter="user.mood == 'happy' AND time.hour < 22")
@bus.subscribe("alert", filter="priority >= 5 OR location.city == 'NYC'")
```

**Tests Required:**
- Unit: State store, context merging, DSL parser
- Integration: Context-filtered subscriptions
- Concurrency: Thread safety under concurrent access

**Validation:**
- [ ] Context variables accessible in handlers
- [ ] Filters correctly gate event delivery
- [ ] No race conditions under load
- [ ] DSL parses complex expressions
- [ ] Scoped contexts properly isolated

---

### ✅ PHASE 4: Temporal Store & Replay (Weeks 12-15)

**Goal:** Event persistence, time-travel replay, causality tracking

**Deliverables:**
1. `TemporalStore` with SQLite WAL backend
2. `WriteAheadLog` for append-only event logging
3. `ReplayEngine` for time-travel debugging
4. `QueryEngine` for temporal queries
5. `TimeIndex` for efficient time-range lookups
6. `CausalityGraph` for event relationship tracking

**SQLite Schema:**
```sql
CREATE TABLE events (
    id TEXT PRIMARY KEY,
    topic TEXT NOT NULL,
    timestamp REAL NOT NULL,
    data BLOB NOT NULL,
    context BLOB,
    embedding BLOB,
    parent_id TEXT,
    metadata BLOB,
    INDEX idx_timestamp ON events(timestamp),
    INDEX idx_topic ON events(topic),
    INDEX idx_parent ON events(parent_id)
);
```

**Key Algorithm - Replay:**
```python
async def replay(from_ts: datetime, to_ts: datetime, speed: float = 1.0):
    # 1. Query events in [from_ts, to_ts] ordered by timestamp
    # 2. Calculate inter-event delays
    # 3. Apply speed multiplier (1.0=realtime, 10.0=10x faster)
    # 4. For each event:
    #    a. await asyncio.sleep(delay * (1/speed))
    #    b. Dispatch event to current subscribers
    # 5. Reconstruct final state
```

**Tests Required:**
- Unit: WAL, query engine, replay logic
- Integration: Full replay with state verification
- Performance: 1M events stored, replay <100ms query

**Validation:**
- [ ] All events persisted with <1ms overhead
- [ ] Replay achieves 100% state fidelity
- [ ] Can handle 1M+ events in log
- [ ] Time-range queries <100ms
- [ ] Causality graph correctly tracks relationships

---

### ✅ PHASE 5: Memory Integration (Weeks 16-19)

**Goal:** Vector store integration, semantic search, episodic linking

**Deliverables:**
1. `MemoryAdapter` interface (protocol)
2. `QdrantMemoryAdapter` implementation
3. `LanceDBMemoryAdapter` implementation
4. `EpisodicLinker` for event-memory associations
5. `SemanticSearch` for querying past events
6. `MemoryPersistence` for snapshot/restore

**Qdrant Collection Schema:**
```python
{
    "collection_name": "neurobus_events",
    "vector_size": 384,
    "distance": "Cosine",
    "payload_schema": {
        "event_id": "keyword",
        "topic": "text",
        "timestamp": "float",
        "context": "json",
        "data": "json"
    }
}
```

**Key Operations:**
```python
# Store event in Qdrant
await memory.store_event(event)

# Search similar past events
results = await memory.search_similar("user asked about weather", k=5)

# Link event to memory
await memory.link(event.id, memory_id="mem_abc123")

# Get context from related memories
context = await memory.get_related_context(event)
```

**Tests Required:**
- Unit: Adapters, linker, search
- Integration: Full event→Qdrant→search flow
- Both real Qdrant and mock implementations

**Validation:**
- [ ] Events auto-stored in vector DB
- [ ] Semantic search returns relevant events
- [ ] Memory links correctly associate events
- [ ] Context reconstruction works end-to-end
- [ ] Both Qdrant and LanceDB adapters work

---

### ✅ PHASE 6: LLM Bridge (Weeks 20-23)

**Goal:** LLM hook system, multi-provider support, reasoning triggers

**Deliverables:**
1. `HookRegistry` for pattern-based triggers
2. `LLMBridge` orchestrator
3. `AnthropicProvider` (Claude)
4. `OpenAIProvider` (GPT)
5. `OllamaProvider` (local LLMs)
6. `PromptTemplateEngine` with variable interpolation
7. `ReasoningContext` builder for LLM prompts

**Hook API:**
```python
@bus.llm_hook(
    trigger="task_failure",
    prompt="Why did {task_name} fail?\nContext: {system_state}\nTrace: {event_trace}",
    model="claude-sonnet-4"
)
async def analyze_failure(event: Event, reasoning: str):
    # reasoning contains LLM response
    await bus.publish(Event("error_analysis", {"analysis": reasoning}))
```

**Provider Interface:**
```python
class LLMProviderProtocol(Protocol):
    async def invoke(self, prompt: str, context: dict) -> str: ...
    def validate_api_key(self) -> bool: ...
    def get_model_info(self) -> dict: ...
```

**Tests Required:**
- Unit: Hook registry, providers, templates
- Integration: End-to-end LLM workflow
- Mock LLM for deterministic tests

**Validation:**
- [ ] Hooks trigger correctly on patterns
- [ ] Prompts correctly populated with context
- [ ] Async LLM calls don't block event loop
- [ ] Responses published as events
- [ ] All 3 providers work (Anthropic, OpenAI, Ollama)
- [ ] Error handling (rate limits, timeouts)

---

### ✅ PHASE 7: Polish & Distribution (Weeks 24-28)

**Goal:** Documentation, examples, packaging, monitoring

**Deliverables:**
1. Comprehensive API documentation (Sphinx)
2. 15+ example applications covering all features
3. Performance benchmarks & optimization
4. PyPI package (`pip install neurobus`)
5. Monitoring & observability (Prometheus metrics, OpenTelemetry)
6. Health check system
7. README, CONTRIBUTING, CODE_OF_CONDUCT

**Examples to Create:**
```
examples/
├── basic/
│   ├── 01_hello_world.py
│   ├── 02_simple_pubsub.py
│   └── 03_async_handlers.py
├── semantic/
│   ├── 01_semantic_subscription.py
│   ├── 02_similarity_tuning.py
│   └── 03_multi_pattern.py
├── context/
│   ├── 01_context_aware.py
│   ├── 02_filtered_subscription.py
│   └── 03_scoped_contexts.py
├── temporal/
│   ├── 01_event_logging.py
│   ├── 02_time_travel_debug.py
│   └── 03_replay_workflow.py
├── memory/
│   ├── 01_memory_linking.py
│   └── 02_semantic_search.py
├── llm/
│   ├── 01_llm_hooks.py
│   ├── 02_reasoning_callback.py
│   └── 03_error_analysis.py
└── advanced/
    ├── 01_luna_integration.py
    ├── 02_multi_agent.py
    └── 03_iot_hub.py
```

**Monitoring Metrics:**
```python
# Prometheus metrics
events_published_total
events_dispatched_total
dispatch_latency_seconds (histogram)
handler_duration_seconds (histogram)
queue_depth_gauge
subscriptions_active_gauge
semantic_matches_total
cache_hits_total
cache_misses_total
```

**Validation:**
- [ ] All public APIs documented
- [ ] Performance meets all targets
- [ ] 15+ examples work correctly
- [ ] Package installable via pip
- [ ] Monitoring dashboard functional
- [ ] README comprehensive

---

## 🧪 TESTING STRATEGY

### Unit Tests (>90% coverage)
- Every module, class, function tested independently
- Mock external dependencies (Qdrant, LLMs)
- Fast execution (<30s for entire suite)

### Integration Tests
- Full workflows: publish → semantic match → context filter → dispatch
- Real external services (Qdrant, SQLite)
- Can run in CI with docker-compose

### Performance Tests
```python
@pytest.mark.benchmark
def test_event_dispatch_latency():
    """P95 latency must be <2ms"""
    
@pytest.mark.benchmark  
def test_throughput():
    """Must sustain 10,000 events/sec"""
```

### Test Fixtures
```python
# tests/fixtures/events.py
@pytest.fixture
def sample_event():
    return Event(
        id=uuid4(),
        topic="test_event",
        data={"message": "hello"},
        timestamp=datetime.now(),
        context={}
    )
```

---

## 📝 CODE QUALITY STANDARDS

### Type Safety
```python
# 100% type hints required
def process_event(event: Event) -> None:
    subscriptions: list[Subscription] = find_matches(event)
    await dispatch_to_handlers(subscriptions, event)
```

### Docstrings (Google Style)
```python
def semantic_match(topic: str, patterns: list[str]) -> list[tuple[str, float]]:
    """
    Match topic against patterns using semantic similarity.
    
    Args:
        topic: Event topic string
        patterns: List of subscription patterns
        
    Returns:
        List of (pattern, similarity) tuples above threshold
        
    Raises:
        EncodingError: If embedding generation fails
    """
```

### Error Handling
```python
try:
    await handler(event)
except Exception as e:
    logger.error(f"Handler failed: {e}", exc_info=True)
    # Isolate error, don't crash bus
    await self._handle_error(e, event, handler)
```

---

## 🎯 SUCCESS CRITERIA

### Phase Completion
Each phase is complete when:
- [ ] All code implemented with 100% type hints
- [ ] All unit tests pass with >90% coverage
- [ ] Integration tests pass
- [ ] Performance benchmarks meet targets
- [ ] mypy type checking passes (strict mode)
- [ ] black formatting applied
- [ ] ruff linting passes
- [ ] No memory leaks detected
- [ ] Documentation updated

### Final Project Completion
Project is 100% complete when:
- [ ] All 7 phases completed
- [ ] 500+ unit tests pass
- [ ] 50+ integration tests pass
- [ ] Performance targets met
- [ ] 15+ examples work
- [ ] API docs complete
- [ ] PyPI package published
- [ ] README comprehensive
- [ ] LUNA integration demo works

---

## 🚀 EXECUTION INSTRUCTIONS

### For AI Assistants:
1. Execute phases sequentially (1 → 2 → 3 → 4 → 5 → 6 → 7)
2. For each phase:
   - Read requirements thoroughly
   - Implement all deliverables
   - Write comprehensive tests
   - Validate against checklist
3. Do not skip or merge phases
4. Follow type safety & documentation standards
5. Test continuously during implementation

### For Development Teams:
1. Assign phases to sprints (1 phase per 4-week sprint)
2. Use this as implementation spec
3. Hold phase completion reviews
4. Run full test suite before moving to next phase
5. Update documentation as you go

---

## 📚 KEY REFERENCES

From existing documentation:
- `docs/vision.md` - Core philosophy and paradigm
- `docs/architecture.md` - Complete file structure
- `docs/brief.md` - Enterprise implementation spec
- `docs/mermaids.md` - 40+ architecture diagrams

---

## 💡 IMPLEMENTATION TIPS

### Performance Optimization
- Use `asyncio.gather()` for parallel operations
- Implement connection pooling for Qdrant
- Cache embeddings aggressively
- Use memory-mapped files for large temporal stores
- Profile with `cProfile` and `py-spy`

### Best Practices
- Weak references for subscription handlers (prevent memory leaks)
- Circuit breakers for external services
- Structured logging (JSON format)
- Exponential backoff for retries
- Graceful degradation when services unavailable

### Common Pitfalls to Avoid
- Don't block event loop with sync I/O
- Don't let handler exceptions crash the bus
- Don't ignore type hints (100% coverage required)
- Don't skip tests (>90% coverage required)
- Don't hard-code configuration

---

## 🎬 FINAL OUTPUT

Deliver a **production-ready, 100% complete NeuroBUS implementation** that:

✅ Has all 6 core layers fully functional  
✅ Passes 500+ tests with >90% coverage  
✅ Meets all performance targets  
✅ Has comprehensive documentation  
✅ Is installable via `pip install neurobus`  
✅ Can power LUNA AI assistant immediately  
✅ Serves as foundation for cognitive AI systems  

**This is not a prototype. This is production-grade software that transforms how AI systems communicate.**

---

**Tagline:** *"Don't send events. Send understanding."*

**Author:** Eshan Roy (eshanized@proton.me)  
**Organization:** TIVerse Labs - Cognitive Infrastructure Division  
**Status:** Ready for Implementation  
**License:** MIT
