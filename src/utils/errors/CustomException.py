class CustomException(Exception):
    pass
    # status_code = 400

    # def __init__(self, message=None,status_code=None, payload=None):
    #     super().__init__()
    #     if message is not None:
    #         self.message = message
    #     else:
    #         self.message = "An error occurred"
    #     if status_code is not None:
    #         self.status_code = status_code
    #     self.payload = payload
    
    # def to_dict(self):
    #     rv = dict(self.payload or ())
    #     rv["message"] = self.message
    #     rv["success"] = False
    #     return rv

class MissingKeyException(Exception):
    def __init__(self, missing_key):
        self.message = f'La clave {missing_key} es requerida.'
        super().__init__(self.message)

class MissingDataException(Exception):
    def __init__(self, tablename, db_name, id_value = None,):
        if id_value is not None:
            self.message = f"El registro con id = {id_value} no existe en la tabla '{tablename}' de {db_name}"
        else:
            self.message = f"El registro buscado no existe en la tabla '{tablename}' de {db_name}"
        super().__init__(self.message)

class DataTypeException(Exception):
    def __init__(self, variable, expected_type):
        self.message = f"'{variable}' debe ser de tipo {expected_type.__name__}."
        super().__init__(self.message)

class WhatsAppException(Exception):
    def __init__(self, message, error_type=None, error_code=None, details=None, fbtrace_id=None):
        self.message = message
        self.error_type = error_type
        self.error_code = error_code
        self.details = details
        self.fbtrace_id = fbtrace_id
        super().__init__(message)
        
class OverlappedReservationException(Exception):
     pass
 
        
class ReservationPriceException(Exception):
     pass
 

class FrontendApiException(Exception):
    def __init__(self, message="", status_code=200, error_code=""):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code

    def to_dict(self):
        return {
            'message': self.message,
            'error_code': self.error_code,  # Include the custom error code
            'success': False
        }