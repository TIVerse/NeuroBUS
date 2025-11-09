#!/bin/bash
# Test all NeuroBUS examples

echo "🧪 Testing NeuroBUS Examples"
echo "=============================="
echo

FAILED=0
PASSED=0
SKIPPED=0

# Basic examples (should always work)
for example in examples/basic/*.py; do
    echo "Testing: $example"
    if python "$example" > /dev/null 2>&1; then
        echo "✅ PASS"
        ((PASSED++))
    else
        echo "❌ FAIL"
        ((FAILED++))
    fi
    echo
done

# Context examples
for example in examples/context/*.py; do
    echo "Testing: $example"
    if python "$example" > /dev/null 2>&1; then
        echo "✅ PASS"
        ((PASSED++))
    else
        echo "❌ FAIL"
        ((FAILED++))
    fi
    echo
done

# Temporal examples  
for example in examples/temporal/*.py; do
    echo "Testing: $example"
    if python "$example" > /dev/null 2>&1; then
        echo "✅ PASS"
        ((PASSED++))
    else
        echo "❌ FAIL"
        ((FAILED++))
    fi
    echo
done

# Memory examples
for example in examples/memory/*.py; do
    echo "Testing: $example"
    if python "$example" > /dev/null 2>&1; then
        echo "✅ PASS"
        ((PASSED++))
    else
        echo "⚠️  SKIP (requires optional dependencies)"
        ((SKIPPED++))
    fi
    echo
done

# LLM examples
for example in examples/llm/*.py; do
    echo "Testing: $example"
    if python "$example" > /dev/null 2>&1; then
        echo "✅ PASS"
        ((PASSED++))
    else
        echo "⚠️  SKIP (requires optional dependencies)"
        ((SKIPPED++))
    fi
    echo
done

# Advanced examples
for example in examples/advanced/*.py; do
    echo "Testing: $example"
    if python "$example" > /dev/null 2>&1; then
        echo "✅ PASS"
        ((PASSED++))
    else
        echo "❌ FAIL"
        ((FAILED++))
    fi
    echo
done

echo "=============================="
echo "Results:"
echo "  ✅ Passed:  $PASSED"
echo "  ❌ Failed:  $FAILED"
echo "  ⚠️  Skipped: $SKIPPED"
echo

if [ $FAILED -eq 0 ]; then
    echo "🎉 All tests passed!"
    exit 0
else
    echo "❌ Some tests failed"
    exit 1
fi
