from typing import Any, Union
from orm_models import Permission
from src.database.db import get_connection_servicecode_orm
from src.utils.errors.CustomException import CustomException
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from extensions import db
class ProfilePermissionsService:
    @classmethod
    def get_permissions(cls, profile_id, service_code, user_system_central):
        """
        Get a list of permissions from the 'perfiles_permisos' table based on the profile ID.

        Args:
            profile_id (int): The profile ID of the permissions
            service_code (int): The service code for database connection.
            user_system_central (bool): Indicates if the user making the request is from bdcentralgp.

        Returns:
            list: A list containing the permissions information of the profile ID.

        Raises:
            CustomException: If an error occurs during the retrieval process.
        """
        try:
            if user_system_central:
                permissions: list[Permission] = Permission.query.filter(
                    Permission.admin == 1, 
                    Permission.profile_id == profile_id
                ).all()

                items = [p.to_dict() for p in permissions]
            else:
                engine = get_connection_servicecode_orm(service_code)
                with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                    # Type annotation for db_session
                    db_session: Session

                    permissions: list[Permission] = db_session.query(Permission).filter(
                        Permission.admin == 1, 
                        Permission.profile_id == profile_id
                    ).all()

                    items = [p.to_dict() for p in permissions]
            return items
        except CustomException as ex:
            raise CustomException(ex)
        
    @classmethod
    def get_permission_module_by_profile_id(cls, submodule_id: int, profile_id: int, service_code: int, user_system_central: bool) -> dict:
        """
        Get the permissions information from the 'perfiles_permisos' table based on the submodule ID and the profile ID.

        Args:
            submodule_id (int): The submodule ID of the permission.
            profile_id (int): The profile ID of the permissions
            service_code (int): The service code for database connection.
            user_system_central (bool): Indicates if the user making the request is from bdcentralgp.

        Returns:
            dict: A dictionary containing the permission information.

        Raises:
            CustomException: If an error occurs during the retrieval process.
        """
        try:
            if user_system_central:
                permission: Union[Permission, Any] = Permission.query.filter(
                    Permission.module_menu_id == submodule_id,
                    Permission.profile_id == profile_id, 
                    Permission.admin == 1
                ).first()
            else:
                engine = get_connection_servicecode_orm(service_code)
                with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                    # Type annotation for db_session
                    db_session: Session
                    
                    permission: Union[Permission, Any] = db_session.query(Permission).filter(
                        Permission.module_menu_id == submodule_id,
                        Permission.profile_id == profile_id, 
                        Permission.admin == 1
                    ).first()

            if permission is None:
                return  {
                    "admin": 1,
                    "delete": 0,
                    "edit": 0,
                    "insert": 0,
                    "id": -1,
                    "module_menu_id": submodule_id,
                    "profile_id": profile_id
                }

            return permission.to_dict(rules=("-module_menu","-profile"))
        except CustomException as ex:
            raise CustomException(ex)
        
    @classmethod
    def update_profile_permissions(cls, permissions: list[dict], profile_id: int, session: Session) -> list:
        """
        Update the permissions information from the 'perfiles_permisos' table based on the permissions list and the profile ID.

        Args:
            permissions (list): A list containing the permissions information of the profile.
            profile_id (int): The profile ID of the permissions
            session (Session): The session for database connection.

        Raises:
            CustomException: If an error occurs during the retrieval process.
        """
        try:
            if not permissions:
                return []

            cls.process_permissions(permissions, profile_id, session)

            updated_permissions: list[Permission] = session.query(Permission).filter(
                Permission.admin == 1, 
                Permission.profile_id == profile_id
            ).all()

            items = [p.to_dict() for p in updated_permissions]

            return items
        except CustomException as ex:
            raise CustomException(ex)
        
    @classmethod
    def process_permissions(cls, permissions: list[dict[str, Any]], profile_id:int, session: Session):
        for permission_dict in permissions:
            delete = permission_dict.get('delete', 0)
            edit = permission_dict.get('edit', 0)
            insert = permission_dict.get('insert', 0)
            module_menu_id = permission_dict.get('module_menu_id')

            if module_menu_id is None:
                continue  # Salta a la siguiente posición en la lista

            permission: Union[Permission, Any] = session.query(Permission).filter(
                Permission.profile_id == profile_id,
                Permission.module_menu_id == module_menu_id
            ).first()

            if permission is None:
                # Crea el permiso para el submódulo especificado
                permission = Permission(
                    profile_id=profile_id,
                    module_menu_id=module_menu_id,
                    delete=delete,
                    edit=edit,
                    insert=insert,
                    admin=1
                )
                session.add(permission)
                session.commit()
            else:
                # Edita el permiso para el submódulo especificado
                permission.delete = delete
                permission.edit = edit
                permission.insert = insert
                session.commit()