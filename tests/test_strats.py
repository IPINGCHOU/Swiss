from app.strats.moving_window import back_testing

def test_back_testing():
    # Create sample data    
    data = [100.0, 120.0, 110.0, 85.0, 80.0, 90.0, 100.0, 40.0, 50.0, 60.0, 70.0, 20.0] 
    drop = 0.15
    
    # Run back testing
    result = back_testing(data, drop)
    
    # Expected result
    expected = [
        (1, 3, 120.0, 85.0),
        (6, 7, 100.0, 40.0),
        (10, 11, 70.0, 20.0)
    ]
    
    assert result == expected