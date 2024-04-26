from typing import Optional, Union
from orm_models import Profile
from src.database.db import get_connection_servicecode_orm
from src.services.ProfilePermissionsService import ProfilePermissionsService
from src.utils.Text import get_db_name_app
from src.utils.errors.CustomException import CustomException, MissingDataException
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from extensions import db
class ProfileService:
    @classmethod
    def get_profiles(cls, service_code: int, user_system_central:bool) -> list:
        """
        Get a list of profile information from 'perfiles' table.

        Args:
            service_code (int): The service code for database connection.
            user_system_central (bool): Indicates if the user making the request is from bdcentralgp.

        Returns:
            list: A list containing the profile information.

        Raises:
            CustomException: If an error occurs during the retrieval process.
        """
        try:
            if user_system_central:
                profiles = Profile.query.filter(Profile.status != 2).all()
            else:
                engine = get_connection_servicecode_orm(service_code)
                with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                    # Type annotation for db_session
                    db_session: Session

                    profiles = db_session.query(Profile).filter(Profile.status != 2).all()

            items = [profile.to_dict() for profile in profiles]

            return items
        except CustomException as ex:
            raise CustomException(ex)

    @classmethod
    def get_profile_by_id(cls, profile_id: int, service_code: int, user_system_central: bool) -> dict:
        """
        Get profile information from 'perfiles' table based on ID.

        Args:
            profile_id (int): The ID of the profile.
            service_code (int): The service code for database connection.
            user_system_central (bool): Indicates if the user making the request is from bdcentralgp.

        Returns:
            dict: A dictionary containing the profile information.

        Raises:
            CustomException: If an error occurs during the retrieval process.
        """
        try:
            if user_system_central:
                profile = Profile.query.filter_by(id = profile_id).first()
            else:
                engine = get_connection_servicecode_orm(service_code)
                with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                    # Type annotation for db_session
                    db_session: Session

                    profile = db_session.query(Profile).filter_by(id = profile_id).first()

            if profile is None:
                return {}
            
            profile_dict = profile.to_dict()
            permissions_list = ProfilePermissionsService.get_permissions(profile_id, service_code, user_system_central)
            profile_dict.update({"permissions": permissions_list})

            return profile_dict
        except CustomException as ex:
            raise CustomException(ex)
        
    @classmethod
    def save_new_profile(cls, service_code: int, name: str, status: int, permissions:list, user_system_central: bool) -> dict:
        """
        Save a new profile into 'perfiles' table.

        Args:
            service_code (int): The service code for database connection.
            name (str): The name of the profile.
            status (int): The status value of the profile.
            permissions (list): A list of permissions of the profile.
            user_system_central (bool): Indicates if the user making the request is from bdcentralgp.

        Returns:
            dict: A dictionary containing the newly created profile data.

        Raises:
            CustomException: If an error occurs during the saving process.
        """
        try:
            new_profile: Profile = Profile(
                name = name, 
                status = status
            )

            if user_system_central:    
                db.session.add(new_profile)
                db.session.commit()
                new_profile_dict = new_profile.to_dict()

                permissions_list = ProfilePermissionsService.update_profile_permissions(permissions, new_profile.id, db.session)
                new_profile_dict.update({"permissions": permissions_list})
            else:
                engine = get_connection_servicecode_orm(service_code)
                with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                    # Type annotation for db_session
                    db_session: Session

                    db_session.add(new_profile)
                    db_session.commit()
                    new_profile_dict = new_profile.to_dict()

                    permissions_list = ProfilePermissionsService.update_profile_permissions(permissions, new_profile.id, db_session)
                    new_profile_dict.update({"permissions": permissions_list})

            return new_profile_dict
        except CustomException as ex:
            raise CustomException(ex)
        
    @classmethod
    def update_profile(cls, profile_id: int, service_code: int, user_system_central: bool, name: Optional[str] = None, status: Optional[int] = None, permissions: list = []) -> dict:
        """
        Update a profile from 'perfiles' table based on ID.

        Args:
            profile_id (int):  The ID of the profile.
            service_code (int): The service code for database connection.
            user_system_central (bool): Indicates if the user making the request is from bdcentralgp.
            name (Optional[str]): The name of the profile (optional).
            status (Optional[int]): The status value of the profile (optional).
            permissions (list): A list of permissions of the profile.

        Returns:
            dict: A dictionary containing the result of the operation.

        Raises:
            CustomException: If an error occurs during the updating process.
        """
        try:
            if user_system_central:
                profile = Profile.query.filter_by(id = profile_id).first()
                if profile is None:
                    raise MissingDataException(tablename=Profile.__tablename__, db_name=get_db_name_app(), id_value=profile_id)

                cls.update_profile_attributes(name, status, profile)
                
                db.session.commit()

                updated_profile = profile.to_dict()

                permission_list = ProfilePermissionsService.update_profile_permissions(permissions, profile_id, db.session)
                updated_profile.update({'permissions': permission_list})
            else:
                engine = get_connection_servicecode_orm(service_code)
                with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                    # Type annotation for db_session
                    db_session: Session

                    profile = db_session.query(Profile).filter_by(id = profile_id).first()
                    if profile is None:
                        raise MissingDataException(tablename=Profile.__tablename__, db_name=engine.url.database, id_value=profile_id)                

                    cls.update_profile_attributes(name, status, profile)

                    db_session.commit()

                    updated_profile = profile.to_dict()
                
                    permission_list = ProfilePermissionsService.update_profile_permissions(permissions, profile_id, db_session)
                    updated_profile.update({'permissions': permission_list})

            return updated_profile
        except CustomException as ex:
            raise CustomException(ex)

    @classmethod
    def update_profile_attributes(cls, name: Union[None, str], status: Union[None, int], profile: Profile):    
        if name is not None and name.strip():
            profile.name = name.strip()
        if status is not None:
            profile.status = status
    
    @classmethod
    def delete_profile(cls, profile_id: int, service_code:int, user_system_central: bool) -> dict:
        """
        Delete profile from 'permisos' table based on ID.
        
        Args:
            profile_id (int): The ID of the profile to delete.
            service_code (int): The service code for database connection.
            user_system_central (bool): Indicates if the user making the request is from bdcentralgp.

        Returns:
            dict: A dictionary containing the result of the operation.

        Raises:
            CustomException: If an error occurs during the deletion process.
        """
        try:
            if user_system_central:
                profile = Profile.query.filter_by(id = profile_id).first()
                if profile is None:
                    return {'message': 'El perfil no existe', 'success': True}
                
                profile.status = 2
                db.session.commit()
            else:
                engine = get_connection_servicecode_orm(service_code)
                with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                    # Type annotation for db_session
                    db_session: Session

                    profile = db_session.query(Profile).filter_by(id = profile_id).first()
                    if profile is None:
                        return {'message': 'El perfil no existe', 'success': True}
                    
                    profile.status = 2
                    db_session.commit()

            return {'message': 'Perfil eliminado exitosamente', 'success': True}
        except Exception as e:
            print(f'Error: {str(e)}')
            return {'message': f'ERROR: {e}', 'success': False}