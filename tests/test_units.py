import pytest

from units import deg_to_rad, kph_to_mps


def test_deg_to_rad():
    # Arrange
    degrees = 10

    # Act
    radians = deg_to_rad(degrees)

    # Assert
    assert radians == pytest.approx(0.1745329251994)


def test_kph_to_mps():
    # Arrange
    velocity_kph = 100  # kph

    # Act
    velocity_mps = kph_to_mps(velocity_kph)

    # Assert
    assert velocity_mps == pytest.approx(27.777777777)
