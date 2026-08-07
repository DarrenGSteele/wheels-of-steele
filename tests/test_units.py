import pytest

from units import deg_to_rad


def test_deg_to_rad():
    # Arrange
    degrees = 10

    # Act
    radians = deg_to_rad(degrees)

    # Assert
    assert radians == pytest.approx(0.1745329251994)
