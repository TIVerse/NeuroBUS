# Basic Examples

This directory contains basic examples to get started with NeuroBUS.

## Examples

### 01_hello_world.py
The simplest possible example - publish and subscribe to a single event.

```bash
python 01_hello_world.py
```

### 02_simple_pubsub.py
Demonstrates multiple subscribers and wildcard patterns.

```bash
python 02_simple_pubsub.py
```

### 03_async_handlers.py
Shows parallel async handler execution and timing.

```bash
python 03_async_handlers.py
```

## Running Examples

All examples can be run directly with Python:

```bash
cd examples/basic
python 01_hello_world.py
```

Or with Poetry:

```bash
poetry run python examples/basic/01_hello_world.py
```

## Next Steps

After completing these examples, check out:
- **Semantic examples** - Semantic routing and similarity matching
- **Context examples** - Context-aware subscriptions and filtering
- **Advanced examples** - Complex patterns and integrations
