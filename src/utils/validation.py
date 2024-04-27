from src.utils.errors.CustomException import DataTypeException, MissingKeyException
from typing import Any, Union

def validate_data(data: dict[str, Any], types: dict[str, dict[str, Union[type, bool]]]) -> None:
    """
    Validate data based on the provided types dictionary.

    Args:
        data (dict): The data to be validated.
        types (dict): A dictionary specifying the expected types for each key.
            Each key in the dictionary represents a data key, and the corresponding value is a dictionary with the following keys:
            - 'type': The expected data type.
            - 'required' (bool): Indicates whether the key is required or optional.

    Raises:
        MissingKeyException: If a required key is missing in the data.
        DataTypeException: If the data type of a key does not match the expected type.

    Example:
        # Define the types dictionary
        types = {
            'name': {'type': str, 'required': True},
            'price': {'type': float, 'required': True},
            'optional_value': {'type': int, 'required': False},
        }

        # Data to be validated
        data = {
            'name': 'Padel racket',
            'price': 100.00,
            'optional_value': 'not_an_int'  # This key is optional
        }

        # Validate data
        validate_data(data, types)
    """
    # Crear listas de claves requeridas y opcionales
    required_keys = [key for key, info in types.items() if info['required']]
    optional_keys = [key for key, info in types.items() if not info['required']]
    
    # Validar datos requeridos
    for key in required_keys:
        if key not in data:
            raise MissingKeyException(missing_key=key)
        
        if not isinstance(data[key], types[key]['type']):
            raise DataTypeException(key, types[key]['type'])
    
    # Validar datos opcionales
    for key in optional_keys:
        if key in data and not isinstance(data[key], types[key]['type']):
            raise DataTypeException(key, types[key]['type'])