import pytest
import sys

from rpn.calculator import calculate, RPNError, eval_rpn, to_rpn


@pytest.mark.parametrize("expr", ["0", "42", "3.1415", "1000000"])
def test_single_number(expr):
    assert calculate(expr) == pytest.approx(float(expr))


@pytest.mark.parametrize(
    "expr, expected",
    [
        ("2 + 2", 4),
        ("5 - 4", 1),
        ("10 - 17", -7),
        ("6 * 7", 42),
        ("256 / 16", 16),
    ],
)
def test_valid_expressions(expr, expected):
    result = calculate(expr)
    assert result == pytest.approx(expected)


@pytest.mark.parametrize(
    "expr, expected",
    [
        ("2.5 + 3.2", 5.7),
        ("5 / 2", 2.5),
        ("3.3 - 4", -0.7),
        ("2.2 * 8", 17.6),
    ],
)
def test_float_value(expr, expected):
    result = calculate(expr)
    assert result == pytest.approx(expected)


@pytest.mark.parametrize(
    "expr",
    [
        "a + 2",
        "3 + #",
        "5 +",
        "+ 4",
        "3 * (2 + )",
        "3 + 4 5",
        "()",
        "(2 + 3",
        "2 + 3)",
    ],
)
def test_invalid_syntax(expr):
    with pytest.raises(RPNError):
        calculate(expr)


@pytest.mark.parametrize(
    "expr, expected",
    [
        ("2 + 3 - 1", 4),
        ("2 + 3 * 4", 14),
        ("2 + 8 / 4", 4),
        ("10 - 2 * 3", 4),
        ("18 - 12 / 3", 14),
        ("6 * 3 / 2", 9),
    ],
)
def test_mixed_two_operations(expr, expected):
    result = calculate(expr)
    assert result == pytest.approx(expected)


@pytest.mark.parametrize(
    "expr, expected",
    [
        ("(2 + 3) * 4", 20),
        ("(10 - 2) * (5 + 1)", 48),
        ("((2 + 3) * (4 + 1)) / 5", 5),
        ("5 + (6 - 2) * 3", 17),
        ("10 + 2 * 3 - 1", 15),
        ("(8 / (4 - 2)) + (6 * (2 + 1))", 22),
    ],
)
def test_complex_expressions(expr, expected):
    result = calculate(expr)
    assert result == pytest.approx(expected)


@pytest.mark.parametrize(
    "expr, expected_rpn",
    [
        ("2 + 3", ["2", "3", "+"]),
        ("2 + 3 * 4", ["2", "3", "4", "*", "+"]),
        ("(2 + 3) * 4", ["2", "3", "+", "4", "*"]),
        ("(10 - 2) * (5 + 1)", ["10", "2", "-", "5", "1", "+", "*"]),
        ("((2 + 3) * (4 + 1)) / 5", ["2", "3", "+", "4", "1", "+", "*", "5", "/"]),
        ("5 + (6 - 2) * 3", ["5", "6", "2", "-", "3", "*", "+"]),
        ("10 + 2 * 3 - 1", ["10", "2", "3", "*", "+", "1", "-"]),
    ],
)
def test_to_rpn_output(expr, expected_rpn):
    assert to_rpn(expr) == expected_rpn


def test_unknown_operator_in_eval_rpn():
    rpn_tokens = ["3", "1", "@"]
    with pytest.raises(RPNError, match="Unknown operator: '@'"):
        eval_rpn(rpn_tokens)


def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        calculate("10 / 0")


def test_empty_expression():
    with pytest.raises(RPNError):
        calculate("")


def test_whitespace_expression():
    with pytest.raises(RPNError):
        calculate("   ")


if __name__ == "__main__":
    sys.exit(pytest.main())
