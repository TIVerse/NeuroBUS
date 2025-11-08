# neurobus — Complete Project Architecture
## File and Folder Structure

**Version:** 1.0  
**Date:** November 2025  
**Project:** neurobus — Universal Neuro-Semantic Event Bus  
**Organization:** TIVerse Labs

---

## Directory Tree Overview

```
neurobus/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml
│   │   ├── release.yml
│   │   ├── docs.yml
│   │   └── security.yml
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   └── question.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── CODEOWNERS
│   └── dependabot.yml
│
├── neurobus/
│   ├── __init__.py
│   ├── __version__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── bus.py
│   │   ├── event.py
│   │   ├── subscription.py
│   │   ├── dispatcher.py
│   │   ├── registry.py
│   │   └── lifecycle.py
│   ├── semantic/
│   │   ├── __init__.py
│   │   ├── router.py
│   │   ├── encoder.py
│   │   ├── matcher.py
│   │   ├── cache.py
│   │   ├── similarity.py
│   │   └── models.py
│   ├── context/
│   │   ├── __init__.py
│   │   ├── engine.py
│   │   ├── state.py
│   │   ├── scope.py
│   │   ├── filter.py
│   │   ├── dsl.py
│   │   └── merger.py
│   ├── temporal/
│   │   ├── __init__.py
│   │   ├── store.py
│   │   ├── wal.py
│   │   ├── replay.py
│   │   ├── query.py
│   │   ├── index.py
│   │   └── causality.py
│   ├── memory/
│   │   ├── __init__.py
│   │   ├── adapter.py
│   │   ├── qdrant_client.py
│   │   ├── lancedb_client.py
│   │   ├── linker.py
│   │   ├── search.py
│   │   └── persistence.py
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── hooks.py
│   │   ├── bridge.py
│   │   ├── providers/
│   │   │   ├── __init__.py
│   │   │   ├── anthropic.py
│   │   │   ├── openai.py
│   │   │   └── ollama.py
│   │   ├── prompts.py
│   │   ├── templates.py
│   │   └── reasoning.py
│   ├── monitoring/
│   │   ├── __init__.py
│   │   ├── metrics.py
│   │   ├── tracing.py
│   │   ├── logging.py
│   │   └── health.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── serialization.py
│   │   ├── timing.py
│   │   ├── validation.py
│   │   ├── patterns.py
│   │   └── helpers.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── schema.py
│   │   ├── loader.py
│   │   ├── validator.py
│   │   └── defaults.py
│   ├── exceptions/
│   │   ├── __init__.py
│   │   ├── core.py
│   │   ├── semantic.py
│   │   ├── temporal.py
│   │   └── memory.py
│   └── types/
│       ├── __init__.py
│       ├── events.py
│       ├── subscriptions.py
│       ├── context.py
│       └── protocols.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_core/
│   │   │   ├── __init__.py
│   │   │   ├── test_bus.py
│   │   │   ├── test_event.py
│   │   │   ├── test_subscription.py
│   │   │   ├── test_dispatcher.py
│   │   │   └── test_lifecycle.py
│   │   ├── test_semantic/
│   │   │   ├── __init__.py
│   │   │   ├── test_router.py
│   │   │   ├── test_encoder.py
│   │   │   ├── test_matcher.py
│   │   │   ├── test_cache.py
│   │   │   └── test_similarity.py
│   │   ├── test_context/
│   │   │   ├── __init__.py
│   │   │   ├── test_engine.py
│   │   │   ├── test_state.py
│   │   │   ├── test_filter.py
│   │   │   └── test_dsl.py
│   │   ├── test_temporal/
│   │   │   ├── __init__.py
│   │   │   ├── test_store.py
│   │   │   ├── test_wal.py
│   │   │   ├── test_replay.py
│   │   │   └── test_query.py
│   │   ├── test_memory/
│   │   │   ├── __init__.py
│   │   │   ├── test_adapter.py
│   │   │   ├── test_linker.py
│   │   │   └── test_search.py
│   │   ├── test_llm/
│   │   │   ├── __init__.py
│   │   │   ├── test_hooks.py
│   │   │   ├── test_bridge.py
│   │   │   └── test_providers.py
│   │   └── test_utils/
│   │       ├── __init__.py
│   │       ├── test_serialization.py
│   │       └── test_validation.py
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_pubsub_flow.py
│   │   ├── test_semantic_routing.py
│   │   ├── test_context_filtering.py
│   │   ├── test_temporal_replay.py
│   │   ├── test_memory_integration.py
│   │   ├── test_llm_workflow.py
│   │   └── test_end_to_end.py
│   ├── performance/
│   │   ├── __init__.py
│   │   ├── test_latency.py
│   │   ├── test_throughput.py
│   │   ├── test_memory_usage.py
│   │   ├── test_concurrent_load.py
│   │   └── benchmarks.py
│   ├── fixtures/
│   │   ├── __init__.py
│   │   ├── events.py
│   │   ├── subscriptions.py
│   │   ├── contexts.py
│   │   └── test_data.py
│   └── mocks/
│       ├── __init__.py
│       ├── mock_llm.py
│       ├── mock_qdrant.py
│       └── mock_embeddings.py
│
├── examples/
│   ├── __init__.py
│   ├── basic/
│   │   ├── 01_hello_world.py
│   │   ├── 02_simple_pubsub.py
│   │   ├── 03_async_handlers.py
│   │   └── README.md
│   ├── semantic/
│   │   ├── 01_semantic_subscription.py
│   │   ├── 02_multi_pattern.py
│   │   ├── 03_similarity_tuning.py
│   │   └── README.md
│   ├── context/
│   │   ├── 01_context_aware.py
│   │   ├── 02_filtered_subscription.py
│   │   ├── 03_scoped_contexts.py
│   │   ├── 04_dsl_filters.py
│   │   └── README.md
│   ├── temporal/
│   │   ├── 01_event_logging.py
│   │   ├── 02_time_travel_debug.py
│   │   ├── 03_replay_workflow.py
│   │   ├── 04_causality_analysis.py
│   │   └── README.md
│   ├── memory/
│   │   ├── 01_memory_linking.py
│   │   ├── 02_semantic_search.py
│   │   ├── 03_episodic_recall.py
│   │   └── README.md
│   ├── llm/
│   │   ├── 01_llm_hooks.py
│   │   ├── 02_reasoning_callback.py
│   │   ├── 03_error_analysis.py
│   │   ├── 04_multi_provider.py
│   │   └── README.md
│   ├── advanced/
│   │   ├── 01_luna_integration.py
│   │   ├── 02_robot_sensor_fusion.py
│   │   ├── 03_multi_agent_system.py
│   │   ├── 04_iot_hub.py
│   │   └── README.md
│   └── tutorials/
│       ├── tutorial_01_getting_started.py
│       ├── tutorial_02_semantic_power.py
│       ├── tutorial_03_context_magic.py
│       ├── tutorial_04_time_travel.py
│       └── tutorial_05_full_stack.py
│
├── docs/
│   ├── source/
│   │   ├── conf.py
│   │   ├── index.rst
│   │   ├── getting_started/
│   │   │   ├── index.rst
│   │   │   ├── installation.rst
│   │   │   ├── quickstart.rst
│   │   │   ├── configuration.rst
│   │   │   └── first_app.rst
│   │   ├── user_guide/
│   │   │   ├── index.rst
│   │   │   ├── core_concepts.rst
│   │   │   ├── semantic_routing.rst
│   │   │   ├── context_engine.rst
│   │   │   ├── temporal_store.rst
│   │   │   ├── memory_integration.rst
│   │   │   ├── llm_hooks.rst
│   │   │   └── best_practices.rst
│   │   ├── api_reference/
│   │   │   ├── index.rst
│   │   │   ├── core.rst
│   │   │   ├── semantic.rst
│   │   │   ├── context.rst
│   │   │   ├── temporal.rst
│   │   │   ├── memory.rst
│   │   │   ├── llm.rst
│   │   │   └── utils.rst
│   │   ├── architecture/
│   │   │   ├── index.rst
│   │   │   ├── overview.rst
│   │   │   ├── components.rst
│   │   │   ├── data_flow.rst
│   │   │   ├── performance.rst
│   │   │   └── security.rst
│   │   ├── tutorials/
│   │   │   ├── index.rst
│   │   │   ├── beginner.rst
│   │   │   ├── intermediate.rst
│   │   │   └── advanced.rst
│   │   ├── deployment/
│   │   │   ├── index.rst
│   │   │   ├── standalone.rst
│   │   │   ├── docker.rst
│   │   │   ├── kubernetes.rst
│   │   │   └── monitoring.rst
│   │   ├── research/
│   │   │   ├── index.rst
│   │   │   ├── whitepaper.rst
│   │   │   ├── benchmarks.rst
│   │   │   ├── case_studies.rst
│   │   │   └── citations.rst
│   │   └── community/
│   │       ├── index.rst
│   │       ├── contributing.rst
│   │       ├── code_of_conduct.rst
│   │       ├── roadmap.rst
│   │       └── changelog.rst
│   ├── build/
│   ├── diagrams/
│   │   ├── architecture.svg
│   │   ├── event_flow.svg
│   │   ├── semantic_routing.svg
│   │   └── component_interaction.svg
│   └── static/
│       ├── logo.svg
│       ├── favicon.ico
│       └── custom.css
│
├── scripts/
│   ├── dev/
│   │   ├── setup_dev_env.sh
│   │   ├── run_tests.sh
│   │   ├── format_code.sh
│   │   ├── type_check.sh
│   │   └── generate_docs.sh
│   ├── build/
│   │   ├── build_package.sh
│   │   ├── build_docs.sh
│   │   └── build_docker.sh
│   ├── deploy/
│   │   ├── deploy_pypi.sh
│   │   ├── deploy_docs.sh
│   │   └── tag_release.sh
│   ├── benchmark/
│   │   ├── run_benchmarks.py
│   │   ├── plot_results.py
│   │   └── compare_versions.py
│   └── utils/
│       ├── generate_fixtures.py
│       ├── validate_config.py
│       └── migrate_db.py
│
├── benchmarks/
│   ├── __init__.py
│   ├── latency_bench.py
│   ├── throughput_bench.py
│   ├── memory_bench.py
│   ├── semantic_bench.py
│   ├── datasets/
│   │   ├── topics_1k.json
│   │   ├── topics_10k.json
│   │   └── realistic_workload.json
│   └── results/
│       ├── .gitkeep
│       └── README.md
│
├── config/
│   ├── neurobus.default.yaml
│   ├── neurobus.development.yaml
│   ├── neurobus.production.yaml
│   ├── neurobus.testing.yaml
│   └── schemas/
│       └── config_schema.json
│
├── docker/
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   ├── docker-compose.yml
│   ├── docker-compose.dev.yml
│   └── entrypoint.sh
│
├── kubernetes/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   └── monitoring/
│       ├── prometheus-config.yaml
│       └── grafana-dashboard.json
│
├── .vscode/
│   ├── settings.json
│   ├── launch.json
│   ├── tasks.json
│   └── extensions.json
│
├── .idea/
│   └── (PyCharm configuration files)
│
├── assets/
│   ├── logo/
│   │   ├── neurobus_logo.svg
│   │   ├── neurobus_logo.png
│   │   └── neurobus_icon.svg
│   ├── diagrams/
│   │   └── source/
│   │       ├── architecture.drawio
│   │       └── event_flow.drawio
│   └── presentations/
│       ├── intro_slides.pdf
│       └── demo_video.mp4
│
├── .gitignore
├── .gitattributes
├── .editorconfig
├── .pre-commit-config.yaml
├── pyproject.toml
├── poetry.lock
├── setup.py
├── setup.cfg
├── MANIFEST.in
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── LICENSE
├── SECURITY.md
├── CITATION.cff
└── VERSION
```
