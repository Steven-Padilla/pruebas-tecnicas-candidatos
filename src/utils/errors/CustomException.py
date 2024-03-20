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
    def __init__(self, tablename, id_value, db_name):
        self.message = f"El registro con id = {id_value} no existe en la tabla '{tablename}' de {db_name}"
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