from typing import Any, Optional, Union

from sqlalchemy import or_
from orm_models import Module, ModuleMenu, Permission, Profile
from src.database.db import get_connection_servicecode_orm
from src.services.ProfilePermissionsService import ProfilePermissionsService
from src.utils.Text import get_db_name_app
from src.utils.errors.CustomException import CustomException, MissingDataException
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from extensions import db
class ModuleMenuService:
    @classmethod
    def get_module_menus(cls, user_system_central, service_code):
        try:
            if user_system_central:
                module_menus: list[ModuleMenu] = ModuleMenu.query.filter(ModuleMenu.admin == 2, ModuleMenu.status != 2).all()

                if not module_menus:
                    return []
                
                module_menu_list = [mm.to_dict() for mm in module_menus]
            else:
                engine = get_connection_servicecode_orm(service_code)
                with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                    # Type annotation for db_session
                    db_session: Session
                    
                    module_menu_club = db_session.query(ModuleMenu).filter(ModuleMenu.admin == 2, ModuleMenu.status != 2).all()
                    
                    module_menu_list = [mmc.to_dict() for mmc in module_menu_club]
            return module_menu_list
        except CustomException as ex:
            raise CustomException(ex)
    
    @classmethod
    def get_menus_by_profile_permissions(cls, profile_id: int, service_code: int, user_system_central: bool ) -> list:
        """
            Get a list of menus allowed by profile of the user.

            Args:
                profile_id (int): The ID of the user profile.
                service_code (int): The service code for database connection.
                user_system_central (bool): Indicates if the user making the request is from bdcentralgp.

            Returns:
                list: A list containing menus information.

            Raises:
                CustomException: If an error occurs during the retrieval process.
        """
        try:
            if user_system_central:
                if profile_id is None:
                    return []
                #permisos de ese perfil
                permissions: list[Permission] = Permission.query.where(
                    Permission.profile_id == profile_id, Permission.admin == 1).filter(
                    or_(
                        Permission.insert == 1,
                        Permission.edit == 1,
                        Permission.delete == 1,
                    )
                ).all() 

                module_menu_ids = [p.module_menu_id for p in permissions]

                module_menus: list[ModuleMenu] = ModuleMenu.query.where(
                        ModuleMenu.id.in_(module_menu_ids), ModuleMenu.status == 1
                    ).all()
                
                module_menus_list = [mm.to_dict() for mm in module_menus]
            else:
                engine = get_connection_servicecode_orm(service_code)
                with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                        # Type annotation for db_session
                    db_session: Session

                    permissions: list[Permission] = db_session.query(Permission).where(
                        Permission.profile_id == profile_id, Permission.admin == 1).filter(
                        or_(
                            Permission.insert == 1,
                            Permission.edit == 1,
                            Permission.delete == 1,
                        )
                    ).all() 

                    module_menu_ids = [p.module_menu_id for p in permissions]
                    
                    module_menus: list[ModuleMenu] = db_session.query(ModuleMenu).where(
                        ModuleMenu.id.in_(module_menu_ids), ModuleMenu.status == 1
                    ).all()

                    module_menus_list = [mmc.to_dict() for mmc in module_menus]

            return module_menus_list
        except CustomException as ex:
            raise CustomException(ex)

    @classmethod
    def get_module_menu(cls, id: int, service_code: int, user_system_central: bool) -> dict:
        try:
            if user_system_central:
                module_menu: Union[ModuleMenu, Any] = ModuleMenu.query.filter_by(id = id, admin = 2).first()

                if module_menu is None:
                    return {}
                
                json_response = module_menu.to_dict()
            else:
                engine = get_connection_servicecode_orm(service_code)
                with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                    # Type annotation for db_session
                    db_session: Session

                    module_menu_club: Union[ModuleMenu, Any] = db_session.query(ModuleMenu).filter_by(id = id, admin = 2).first()

                    if module_menu_club is None:
                        return {}
                    
                    json_response = module_menu_club.to_dict()
            return json_response
        except CustomException as ex:
            raise CustomException(ex)
    
    @classmethod
    def save_new_module_menu(cls, service_code: int, module_id: int, name: str, status: int, level: int, path: str, user_system_central: bool, profile_id: int) -> dict:
        """
        Save a new module_menu into 'modulos_menu' table.

        Args:
            service_code (int): The service code for database connection.
            module_id (int): The ID of the module parent.
            name (str): The name of the menu.
            status (int): The status value of the menu.
            level (int): The level value of the menu.
            path (str): The route of the menu.
            user_system_central (bool): Indicates if the user making the request is from bdcentralgp.
            profile_id (int): The ID of the profile to create a new permission into "perfiles_permisos"

        Returns:
            dict: A dictionary containing the newly created module_menu data.

        Raises:
            CustomException: If an error occurs during the saving process.
        """
        try:
            if user_system_central:
                new_module_menu: ModuleMenu = ModuleMenu(
                    module_id = module_id,
                    menu = name,
                    file = path,
                    file_path = '',
                    level = level,
                    status = status,
                    icon = '',
                    admin = 2,
                )
                
                db.session.add(new_module_menu)
                db.session.commit()

                #Create the permission with insert = 0, delete = 0, update = 0
                permissions = ProfilePermissionsService.update_profile_permissions([{'module_menu_id': new_module_menu.id, "insert": 1}], profile_id, db.session)
                
                json_response = new_module_menu.to_dict()
            else:
                engine = get_connection_servicecode_orm(service_code)
                with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                    # Type annotation for db_session
                    db_session: Session

                    module_menu_club: ModuleMenu = ModuleMenu(
                        module_id = module_id,
                        menu = name,
                        file = path,
                        file_path = '',
                        level = level,
                        status = status,
                        icon = '',
                        admin = 2,
                    )

                    db_session.add(module_menu_club)
                    db_session.commit()

                    permissions = ProfilePermissionsService.update_profile_permissions([{'module_menu_id': module_menu_club.id, "insert": 1}], profile_id, db_session)
                    
                    json_response = module_menu_club.to_dict()
            return json_response
        except CustomException as ex:
            raise CustomException(ex)
    
    @classmethod
    def update_module_menu(cls, module_menu_id: int, service_code: int, user_system_central: bool,
    module_id: Optional[int] = None, name: Optional[str] = None, status: Optional[int] = None, level: Optional[int] = None, path: Optional[str] = None):
        """
        Update a module_menu from 'modulos_menu' table based on ID.

        Args:
            module_id (int):  The ID of the module.
            service_code (int): The service code for database connection.
            user_system_central (bool): Indicates if the user making the request is from bdcentralgp.
            module_id (Optional[int]): The ID of the module parent (optional).
            name (Optional[str]): The name of the menu (optional).
            status (Optional[int]): The status value of the menu (optional).
            level (Optional[int]): The level value of the menu (optional).
            path (Optional[str]): The route of the menu (optional).
            
        Returns:
            dict: A dictionary containing the result of the operation.

        Raises:
            CustomException: If an error occurs during the updating process.
        """
        try:
            if user_system_central:
                module_menu: Union[ModuleMenu, Any] = ModuleMenu.query.filter_by(id = module_menu_id).first()
                if module_menu is None:
                    raise MissingDataException(tablename=ModuleMenu.__tablename__, db_name=get_db_name_app(), id_value=module_menu_id)
                
                cls.update_module_menu_attributes(name, status, level, module_id, path, module_menu)

                db.session.commit()

                module_menu_dict = module_menu.to_dict()
            else:
                engine = get_connection_servicecode_orm(service_code)
                with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                    # Type annotation for db_session
                    db_session: Session

                    module_menu: Union[ModuleMenu, Any] = db_session.query(ModuleMenu).filter_by(id = module_menu_id).first()
                    if module_menu is None:
                        raise MissingDataException(tablename=ModuleMenu.__tablename__, db_name=engine.url.database, id_value=module_menu_id)
                    
                    cls.update_module_menu_attributes(name, status, level, module_id, path, module_menu)

                    db_session.commit()

                    module_menu_dict = module_menu.to_dict()
            return module_menu_dict
        except CustomException as ex:
            raise CustomException(ex)

    @classmethod
    def update_module_menu_attributes(cls, name, status, level, module_id, path, module_menu):
        if name is not None and name.strip():
            module_menu.name = name.strip()
        if status is not None:
            module_menu.status = status
        if level is not None:
            module_menu.level = level
        if module_id is not None:
            module_menu.module_id = module_id
        if path is not None and path.strip():
            module_menu.file = path
    
    @classmethod
    def delete_module_menu(cls, module_menu_id: int, service_code:int, user_system_central: bool) -> dict:
        """
        Delete module_menu from 'modulos_menu' table based on ID.
        
        Args:
            module_menu_id (int): The ID of the menu to delete.
            service_code (int): The service code for database connection.
            user_system_central (bool): Indicates if the user making the request is from bdcentralgp.

        Returns:
            dict: A dictionary containing the result of the operation.

        Raises:
            CustomException: If an error occurs during the deletion process.
        """
        try:
            if user_system_central:
                module_menu: Union[ModuleMenu, Any] = ModuleMenu.query.filter_by(id = module_menu_id).first()
                if module_menu is None:
                    return {'message': 'El menú no existe', 'success': True}
                
                module_menu.status = 2
                module_menu.file += str(module_menu_id)

                db.session.commit()
            else:
                engine = get_connection_servicecode_orm(service_code)
                with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                    # Type annotation for db_session
                    db_session: Session

                    module_menu: Union[ModuleMenu, Any] = db_session.query(ModuleMenu).filter_by(id = module_menu_id).first()
                    if module_menu is None:
                        return {'message': 'El menú no existe', 'success': True}
                    
                    module_menu.status = 2
                    module_menu.file += str(module_menu_id)

                    db_session.commit()
            return {'message': 'Menú eliminado exitosamente', 'success': True}
        except Exception as e:
            print(f'Error: {str(e)}')
            return {'message': f'ERROR: {e}', 'success': False}

    @classmethod
    def validate_route_name(cls, route: str, service_code: int, user_system_central: bool) -> dict:
        try:
            module_menu = None
            json_response = {}
            if user_system_central:
                module_menu: Union[ModuleMenu, Any] = ModuleMenu.query.filter(ModuleMenu.file == route).first()
            else:
                engine = get_connection_servicecode_orm(service_code)
                with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                    # Type annotation for db_session
                    db_session: Session

                    module_menu: Union[ModuleMenu, Any] = db_session.query(ModuleMenu).filter(ModuleMenu.file == route).first()
            if module_menu:
                json_response = {"message": f"La ruta {route} ya pertenece a otro menú", "validate": False}
            else:
                json_response = {"message": f"{route} esta disponible", "validate": True}

            return json_response
        except CustomException as ex:
            raise CustomException(ex)
