from datetime import datetime
import re
from orm_models import UsersCentral
from src.utils.errors.CustomException import DataTypeException, MissingDataException
from extensions import db

class UserService():
    @classmethod
    def update(cls, user_id, name, lastname, secondsurname, birthday, sex, alias):
        try:
            user = cls.get_user_by_id(user_id)

            if user is None:
                return {'data': [], 'success': True}

            cls.update_user_attributes(user, name, lastname, secondsurname, birthday, sex, alias)

            db.session.commit()
            json_response = {'data': user.to_dict(), 'success': True}

            return json_response
        except Exception as ex:
            print(ex)
            return {'message': f"ERROR: {ex}", 'success': False}
    
    @classmethod
    def get_user_by_id(cls, user_id):
        if not isinstance(user_id, int):
            raise DataTypeException('user_id', int)

        return UsersCentral.query.get(user_id)

    @classmethod
    def update_user_attributes(cls, user, name, lastname, secondsurname, birthday, sex, alias):
        if name and len(name.strip()) != 0:
            user.name = name.strip()
        if lastname and len(lastname.strip()) != 0:
            user.lastname = lastname.strip()
        if secondsurname and len(secondsurname.strip()) != 0:
            user.secondsurname = secondsurname.strip()
        if sex and len(sex.strip()) != 0:
                user.sex = sex.strip()
        if alias and len(alias.strip()) != 0:
            user.alias = alias.strip()

        cls.update_birthday(user, birthday)
    
    @classmethod
    def update_birthday(cls, user, birthday):
        if birthday:
            match = re.match(r'^(\d{4})-(\d{2})-(\d{2})$', birthday)
            if match:
                year, month, day = map(int, match.groups())
                if cls.is_valid_date(year, month, day):
                    user.birthday = '-'.join(match.groups())
                else:
                    raise ValueError('Fecha de nacimiento no válida')
            else:
                raise ValueError('Formato de fecha de nacimiento no válido')

    @classmethod
    def is_valid_date(cls,year, month, day):
        try:
            datetime(year, month, day)
            return True
        except ValueError:
            return False