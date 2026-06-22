"""计算器模块的单元测试"""
import pytest
from calculator import add, subtract, multiply, divide


class TestCalculator:
    """计算器测试类"""

    def test_add(self):
        """测试加法"""
        assert add(1, 2) == 3
        assert add(-1, 1) == 0
        assert add(0, 0) == 0

    def test_subtract(self):
        """测试减法"""
        assert subtract(5, 3) == 2
        assert subtract(10, 5) == 5
        assert subtract(0, 0) == 0

    def test_multiply(self):
        """测试乘法"""
        assert multiply(3, 4) == 12
        assert multiply(0, 5) == 0
        assert multiply(-2, 3) == -6

    def test_divide(self):
        """测试除法"""
        assert divide(10, 2) == 5
        assert divide(9, 3) == 3

    def test_divide_by_zero(self):
        """测试除数为零的情况"""
        with pytest.raises(ValueError):
            divide(10, 0)