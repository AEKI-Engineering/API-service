import pytest

@pytest.fixture
def numbers():
    a = 2
    b = 2
    return [a,b]

class TestApp:
    def test_addition(self, numbers):
        res = numbers[0] + numbers[1]
        assert res == 4