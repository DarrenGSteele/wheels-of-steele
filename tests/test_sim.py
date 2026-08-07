def test_aero_drag_force():
    # Arrange
    v = 100 * 1000 / 3600 # m/s
    rho = 1.225 # kg.m^3
    cd = 0.3 # coefficient
    area = 2.02 #m^2

    # Act
    current_drag = aero_drag(v, rho, cd, area) # N

    # Assert
    #assert(current_drag == 286.4)
    assert(current_drag == pytest.approx(286.4))
           