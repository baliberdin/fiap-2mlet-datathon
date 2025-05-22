import pandas as pd
from data_transform_utilities import flatten
from io import StringIO

def test_should_flatten_nested_dict_in_dataframe():
    # Test with a dataframe containing a nested dictionary
    data = pd.DataFrame([{'a': 1, 'b': {'c': 2, 'd': 3}}])
    expected = pd.DataFrame([{'a': 1, 'b_c': 2, 'b_d': 3}])
    
    # When
    result = flatten(data)
    
    # Then
    pd.testing.assert_frame_equal(result, expected, check_like=True)
    
    
def test_should_do_nothing_with_simple_dataframe():
    # Test with a simple dataframe without nested dictionaries
    data = pd.DataFrame([{'a': 1, 'b': 2}])
    expected = pd.DataFrame([{'a': 1, 'b': 2}])
    
    # When
    result = flatten(data)
    
    # Then
    pd.testing.assert_frame_equal(result, expected, check_like=True)
    