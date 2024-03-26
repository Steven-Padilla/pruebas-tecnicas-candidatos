from typing import Any, Union

from sqlalchemy import or_
from orm_models import Module, ModuleMenu, Permission, Profile
from src.database.db import get_connection_servicecode_orm
from src.utils.errors.CustomException import CustomException
from sqlalchemy.orm import scoped_session, sessionmaker, Session

class ModuleMenuService:
    @classmethod
    def get_module_menus(cls, user_central, service_code):
        try:
            module_menus = ModuleMenu.query.filter_by(admin = 2).all()

            if len(module_menus) == 0:
                return []
            
            if user_central:
                module_menu_list = [mm.to_dict() for mm in module_menus]
                return module_menu_list

            engine = get_connection_servicecode_orm(service_code)
            with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                # Type annotation for db_session
                db_session: Session
                modules = Module.query.filter_by(admin = 2, status=1).all()
                module_ids_list = [m.id for m in modules] #ids de modulos activos
                module_menu_club = db_session.query(ModuleMenuClub).where(ModuleMenuClub.module_id.in_(module_ids_list)).all()
                
                module_menu_list = [cls.update_module_menu_data(mmc.to_dict(), cls.get_model_menu_from_central(mmc.module_id)) for mmc in module_menu_club] #menus de modulos del club que estan activos
                return module_menu_list
        except CustomException as ex:
            raise CustomException(ex)
    @classmethod
    def update_module_menu_data(cls, module_menu_club, module_menu):
        exclusion_list = ["icon", "menu"]
        for key, value in module_menu.items():
            if key not in exclusion_list:
                module_menu_club[key] = value
        return module_menu_club
    
    @classmethod
    def get_model_menu_from_central(cls, module_id):
        module_menu = ModuleMenu.query.filter_by(module_id = module_id, admin = 2).first()
        return module_menu.to_dict()

    @classmethod
    def get_model_menu(cls, id):
        try:
            module_menu = ModuleMenu.query.filter_by(id = id, admin = 2).first()

            if module_menu is None:
                return {}
            
            json_response = module_menu.to_dict()

            return json_response
        except CustomException as ex:
            raise CustomException(ex)

    @classmethod
    def get_menus_by_profile_permissions(cls, profile_id: int, service_code: int, user_system_id: Union[int, None] ) -> list:
        """
            Get a list of menus allowed by profile of the user.

            Args:
                profile_id (int): The ID of the user profile.
                service_code (int): The service code for database connection.
                user_system_id (int or None): The ID of the user system if is None, means that the user is a bdgp user_system.

            Returns:
                list: A list containing menus information.

            Raises:
                CustomException: If an error occurs during the retrieval process.
        """
        try:
            profile: Union[Profile, Any] = cls.get_user_profile(profile_id, service_code, user_system_id)

            if profile is None:
                return []
            
            if user_system_id is not None:
                #permisos de ese perfil
                permissions: list[Permission] = Permission.query.where(
                    Permission.profile_id == profile.id, Permission.admin == 1).filter(
                    or_(
                        Permission.insert == 1,
                        Permission.edit == 1,
                        Permission.delete == 1,
                    )
                ).all() 

                module_menus = [p.module_menu for p in permissions if p.module_menu.module.status == 1 and p.module_menu.module.admin == 2]

                module_menus_list = [mm.to_dict() for mm in module_menus]
            else:
                engine = get_connection_servicecode_orm(service_code)
                with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                        # Type annotation for db_session
                    db_session: Session

                    permissions: list[Permission] = db_session.query(Permission).where(
                        Permission.profile_id == profile.id, Permission.admin == 1).filter(
                        or_(
                            Permission.insert == 1,
                            Permission.edit == 1,
                            Permission.delete == 1,
                        )
                    ).all() 
                    
                    modules = Module.query.filter_by(admin = 2, status=1).all()
                    module_ids_list = [m.id for m in modules] #ids de modulos activos
                    
                    module_menus_club_ids = [p.module_menu_id for p in permissions] #ids de menus permitidos

                    module_menu_club_allowed = db_session.query(ModuleMenu).filter(
                        ModuleMenu.module_id.in_(module_ids_list),
                        ModuleMenu.id.in_(module_menus_club_ids) 
                    ).all()

                    module_menus_list = [cls.update_module_menu_data(mmc.to_dict(), cls.get_model_menu_from_central(mmc.module_id)) for mmc in module_menu_club_allowed]
            return module_menus_list
        except CustomException as ex:
            raise CustomException(ex)

    @classmethod
    def get_user_profile(cls, profile_id, service_code, user_system_id):
        if user_system_id is not None:
            profile: Union[Profile, Any] = Profile.query.filter_by(id = profile_id).first()
        else:
            engine = get_connection_servicecode_orm(service_code)
            with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                    # Type annotation for db_session
                db_session: Session
                profile = db_session.query(Profile).filter_by(id = profile_id).first()
        return profile