# 🎯 NeuroBUS Examples

Comprehensive examples demonstrating all NeuroBUS features.

## 📚 Categories

### 🌟 Basic (`basic/`)
Fundamental concepts and features.

- **01_hello_world.py** - Your first NeuroBUS event
- **02_simple_pubsub.py** - Basic publish/subscribe
- **03_async_handlers.py** - Asynchronous event handling
- **04_wildcard_patterns.py** - Pattern matching with wildcards  
- **05_priorities.py** - Subscription priorities
- **06_filters.py** - Lambda-based event filtering

### 🧠 Semantic (`semantic/`)
Semantic routing with embeddings.

- **01_semantic_matching.py** - Basic semantic routing
- **02_threshold_tuning.py** - Similarity threshold tuning

**Prerequisites**: `pip install neurobus[semantic]`

### 🎯 Context (`context/`)
Hierarchical context management.

- **01_hierarchical_context.py** - Multi-level context
- **02_dsl_filters.py** - DSL filter expressions (NEW!)

### ⏰ Temporal (`temporal/`)
Time-travel and event replay.

- **01_event_replay.py** - Event persistence and replay

### 💾 Memory (`memory/`)
Long-term memory and vector search.

- **01_memory_search.py** - In-memory event storage
- **02_vector_search.py** - Qdrant vector database (NEW!)

**Prerequisites**: `pip install neurobus[memory]`

### 🤖 LLM (`llm/`)
LLM integration and reasoning.

- **01_event_analysis.py** - LLM-powered event analysis
- **02_llm_hooks.py** - Automatic LLM hooks (NEW!)

**Prerequisites**: `pip install neurobus[llm]`

### 🌐 Distributed (`distributed/`)
Multi-node clustering.

- **01_cluster_events.py** - Redis-based clustering

**Prerequisites**: `pip install neurobus[distributed]` + Redis server

### 🚀 Advanced (`advanced/`)
Real-world patterns and use cases.

- **01_microservices.py** - Service-to-service communication (NEW!)
- **02_event_sourcing.py** - Event sourcing pattern (NEW!)

---

## 🏃 Quick Start

### Run a Basic Example
```bash
python examples/basic/01_hello_world.py
```

### With Optional Features
```bash
# Install semantic routing
pip install neurobus[semantic]
python examples/semantic/01_semantic_matching.py

# Install LLM support  
pip install neurobus[llm]
python examples/llm/01_event_analysis.py
```

---

## 📖 Learning Path

### Beginners
1. `basic/01_hello_world.py` - Start here!
2. `basic/02_simple_pubsub.py` - Learn pub/sub basics
3. `basic/04_wildcard_patterns.py` - Pattern matching
4. `context/01_hierarchical_context.py` - Add context

### Intermediate
1. `basic/05_priorities.py` - Handler priorities
2. `basic/06_filters.py` - Event filtering
3. `context/02_dsl_filters.py` - DSL filters
4. `temporal/01_event_replay.py` - Time-travel

### Advanced
1. `semantic/01_semantic_matching.py` - Semantic routing
2. `llm/02_llm_hooks.py` - LLM automation
3. `memory/02_vector_search.py` - Vector search
4. `distributed/01_cluster_events.py` - Clustering
5. `advanced/01_microservices.py` - Real-world patterns

---

## 🔧 Prerequisites by Feature

| Feature | Install Command | Server Required |
|---------|----------------|-----------------|
| **Basic** | `pip install neurobus` | No |
| **Semantic** | `pip install neurobus[semantic]` | No |
| **LLM** | `pip install neurobus[llm]` | No |
| **Memory (Qdrant)** | `pip install neurobus[qdrant]` | Yes (Qdrant) |
| **Distributed** | `pip install neurobus[distributed]` | Yes (Redis) |

### Starting Servers

**Qdrant**:
```bash
docker run -d -p 6333:6333 qdrant/qdrant
```

**Redis**:
```bash
docker run -d -p 6379:6379 redis:latest
```

---

## 📊 Example Matrix

| Example | Events | Features | LOC | Difficulty |
|---------|--------|----------|-----|------------|
| hello_world | 1 | Basic | 20 | ⭐ |
| simple_pubsub | 3 | Pub/Sub | 35 | ⭐ |
| async_handlers | 5 | Async | 45 | ⭐ |
| wildcard_patterns | 4 | Patterns | 50 | ⭐⭐ |
| priorities | 1 | Priority | 55 | ⭐⭐ |
| filters | 5 | Filters | 70 | ⭐⭐ |
| dsl_filters | 5 | DSL | 80 | ⭐⭐⭐ |
| semantic_matching | 3 | Semantic | 60 | ⭐⭐⭐ |
| threshold_tuning | 4 | Semantic | 75 | ⭐⭐⭐ |
| event_replay | 3 | Temporal | 55 | ⭐⭐⭐ |
| memory_search | 5 | Memory | 85 | ⭐⭐⭐ |
| vector_search | 5 | Qdrant | 90 | ⭐⭐⭐⭐ |
| event_analysis | 3 | LLM | 95 | ⭐⭐⭐ |
| llm_hooks | 3 | LLM Hooks | 110 | ⭐⭐⭐⭐ |
| cluster_events | 3 | Distributed | 120 | ⭐⭐⭐⭐ |
| microservices | 4 | Advanced | 150 | ⭐⭐⭐⭐⭐ |
| event_sourcing | 4 | Advanced | 100 | ⭐⭐⭐⭐⭐ |

---

## 💡 Tips

### Running All Examples
```bash
for example in examples/basic/*.py; do
    echo "Running $example"
    python "$example"
done
```

### Testing Examples
```bash
# Dry run to check for syntax errors
python -m py_compile examples/**/*.py
```

### Debugging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 🤝 Contributing Examples

Have a great use case? Contribute an example!

1. Create in appropriate category
2. Follow existing naming convention
3. Include comprehensive docstrings
4. Add to this README
5. Submit PR

---

## 📞 Support

- **Documentation**: https://neurobus.readthedocs.io
- **Issues**: https://github.com/TIVerse/NeuroBUS/issues
- **Discussions**: https://github.com/TIVerse/NeuroBUS/discussions

---

**Happy Coding with NeuroBUS! 🧠✨**
