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

def validate_data_with_nested_types(data: dict, types: dict) -> None:
    """
    Validate data based on the provided types dictionary.

    Args:
        data (dict): The data to be validated.
        types (dict): A dictionary specifying the expected types for each key.
            Each key in the dictionary represents a data key, and the corresponding value is a dictionary with the following keys:
            - 'type': The expected data type.
            - 'required' (bool): Indicates whether the key is required or optional.
            - 'nested_types' (dict): A dictionary specifying the expected types for nested keys (used when the type is 'dict').

    Raises:
        MissingKeyException: If a required key is missing in the data.
        DataTypeException: If the data type of a key does not match the expected type.

    Example:
        # Define the types dictionary
        types = {
            'title': {'type': str, 'required': True},
            'details': {
                'type': dict,
                'required': True,
                'nested_types': {
                    'description': {'type': str, 'required': True},
                    'price': {'type': float, 'required': True},
                }
            }
        }

        # Data to be validated
        data = {
            'title': 'Product Title',
            'details': {
                'description': 'Product Description',
                'price': 100.00,
            }
        }

        # Validate data
        validate_data(data, types)
    """
    for key, info in types.items():
        # Validate if the key is required and present
        if info['required'] and key not in data:
            raise MissingKeyException(missing_key=key)
        
        # Validate data type if key is present
        if key in data:
            if isinstance(info['type'], type):
                if not isinstance(data[key], info['type']):
                    raise DataTypeException(key, info['type'])
            elif isinstance(info['type'], tuple):
                if not any(isinstance(data[key], t) for t in info['type']):
                    raise DataTypeException(key, info['type'])
            elif isinstance(info['type'], dict):
                try:
                    validate_data(data[key], info['nested_types'])
                except MissingKeyException as e:
                    raise MissingKeyException(f"{key}.{e.missing_key}")
                except DataTypeException as e:
                    raise DataTypeException(f"{key}.{e.key}", e.expected_type)