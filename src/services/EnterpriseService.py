from typing import Any, Union

from flask import jsonify
from src.models import Enterprise
from src.database.db import get_connection_servicecode_orm
from src.utils.Text import get_db_name_app
from src.utils.errors.CustomException import CustomException, MissingDataException
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from extensions import db

class EnterpriseService:

    @classmethod
    def get_enterprise_data(cls, service_code:int) -> list:
        """
            Get a list of court information from 'zonas' table.

            Args:
                service_code (int): The service code for database connection.

            Returns:
                list: A list containing the courts information.

            Raises:
                CustomException: If an error occurs during the retrieval process or if the court is not found.
        """
        try:
            response = {}
            engine = get_connection_servicecode_orm(service_code)
            with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                # Type annotation for db_session

                db_session: Session
            
                enterprise_data = db_session.query(Enterprise).filter(Enterprise.service_code == service_code).filter(Enterprise.status == 1).first()

                response = enterprise_data.to_dict()

                return response
            
        except CustomException as ex:
            raise CustomException(ex)
        

    @classmethod
    def save_enterprise(cls, service_code: int ) -> dict:
        """
            Save a new  into 'tablename' table.

            Args:
                service_code (int): The service code for database connection.


            Returns:
                dict: A dictionary containing the newly created  data.

            Raises:
                CustomException: If an error occurs during the saving process.
        """
        try:
            engine = get_connection_servicecode_orm(service_code)
            with scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))() as db_session:
                db_session: Session
                #TODO: añadir los atributos correspondientes
                new_ = ()

                db_session.add(new_)
                db_session.commit()

                return new_.to_dict()
        except CustomException as e:
            raise CustomException(str(e))
    pass