"""Tests for context DSL parser."""

from neurobus.context.dsl import FilterDSL, parse_filter


class TestFilterDSL:
    """Test cases for FilterDSL."""

    def test_dsl_creation(self):
        """Test DSL parser creation."""
        dsl = FilterDSL()
        assert dsl is not None

    def test_simple_equality(self):
        """Test simple equality filter."""
        dsl = FilterDSL()
        filter_func = dsl.parse("user.mood == 'happy'")

        assert filter_func({"user": {"mood": "happy"}}) is True
        assert filter_func({"user": {"mood": "sad"}}) is False

    def test_numeric_comparison(self):
        """Test numeric comparison filters."""
        dsl = FilterDSL()

        filter_func = dsl.parse("user.age >= 18")
        assert filter_func({"user": {"age": 25}}) is True
        assert filter_func({"user": {"age": 15}}) is False

        filter_func = dsl.parse("priority > 5")
        assert filter_func({"priority": 10}) is True
        assert filter_func({"priority": 3}) is False

    def test_and_operator(self):
        """Test AND logical operator."""
        dsl = FilterDSL()
        filter_func = dsl.parse("user.age >= 18 AND user.verified == true")

        assert filter_func({"user": {"age": 25, "verified": True}}) is True
        assert filter_func({"user": {"age": 25, "verified": False}}) is False
        assert filter_func({"user": {"age": 15, "verified": True}}) is False

    def test_or_operator(self):
        """Test OR logical operator."""
        dsl = FilterDSL()
        filter_func = dsl.parse("priority >= 5 OR location.city == 'NYC'")

        assert filter_func({"priority": 10, "location": {"city": "LA"}}) is True
        assert filter_func({"priority": 3, "location": {"city": "NYC"}}) is True
        assert filter_func({"priority": 3, "location": {"city": "LA"}}) is False

    def test_not_operator(self):
        """Test NOT logical operator."""
        dsl = FilterDSL()
        filter_func = dsl.parse("NOT user.banned == true")

        assert filter_func({"user": {"banned": False}}) is True
        assert filter_func({"user": {"banned": True}}) is False

    def test_complex_expression(self):
        """Test complex nested expression."""
        dsl = FilterDSL()
        filter_func = dsl.parse(
            "(user.age >= 18 AND user.verified == true) OR user.role == 'admin'"
        )

        assert filter_func({"user": {"age": 25, "verified": True, "role": "user"}}) is True
        assert filter_func({"user": {"age": 15, "verified": False, "role": "admin"}}) is True
        assert filter_func({"user": {"age": 15, "verified": False, "role": "user"}}) is False

    def test_empty_expression(self):
        """Test empty expression returns True."""
        dsl = FilterDSL()
        filter_func = dsl.parse("")

        assert filter_func({}) is True
        assert filter_func({"any": "context"}) is True

    def test_missing_path_returns_false(self):
        """Test that missing context path returns False."""
        dsl = FilterDSL()
        filter_func = dsl.parse("user.missing.path == 'value'")

        assert filter_func({"user": {}}) is False
        assert filter_func({}) is False

    def test_parse_filter_convenience(self):
        """Test parse_filter convenience function."""
        filter_func = parse_filter("priority >= 5")

        assert filter_func({"priority": 10}) is True
        assert filter_func({"priority": 3}) is False

    def test_boolean_literals(self):
        """Test boolean literal handling."""
        dsl = FilterDSL()

        filter_func = dsl.parse("enabled == true")
        assert filter_func({"enabled": True}) is True
        assert filter_func({"enabled": False}) is False

        filter_func = dsl.parse("disabled == false")
        assert filter_func({"disabled": False}) is True
        assert filter_func({"disabled": True}) is False

    def test_string_with_spaces(self):
        """Test string values with spaces."""
        dsl = FilterDSL()
        filter_func = dsl.parse("message == 'hello world'")

        assert filter_func({"message": "hello world"}) is True
        assert filter_func({"message": "goodbye"}) is False

    def test_inequality(self):
        """Test inequality operator."""
        dsl = FilterDSL()
        filter_func = dsl.parse("status != 'inactive'")

        assert filter_func({"status": "active"}) is True
        assert filter_func({"status": "inactive"}) is False

    def test_float_comparison(self):
        """Test float value comparison."""
        dsl = FilterDSL()
        filter_func = dsl.parse("temperature > 98.6")

        assert filter_func({"temperature": 99.5}) is True
        assert filter_func({"temperature": 98.0}) is False
