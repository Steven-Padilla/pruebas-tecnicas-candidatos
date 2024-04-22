from sqlalchemy import CHAR, LargeBinary, TypeDecorator, cast, func, type_coerce


my_key = "B!1w8*NAtS3DUM1T^%kvhUI*S^_"

class CustomBLOB(TypeDecorator):
    impl = LargeBinary
    cache_ok = True

    def bind_expression(self, bindvalue):
        return func.aes_encrypt(
            type_coerce(bindvalue, CHAR()), func.sha2(my_key, 512),
        )

    def column_expression(self, col):
        return cast(
            func.aes_decrypt(col, func.sha2(my_key, 512),),
            CHAR(),
        )