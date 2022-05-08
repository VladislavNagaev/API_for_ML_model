import os
import pytest
from contextlib import nullcontext as does_not_raise

from app.modules import TokenVerification


POSTGRES_USER = os.getenv(key='POSTGRES_USER', default='')
POSTGRES_PASSWORD = os.getenv(key='POSTGRES_PASSWORD', default='')
POSTGRES_HOST = '127.0.0.1'
POSTGRES_PORT = os.getenv(key='POSTGRES_PORT', default='')
POSTGRES_DB = os.getenv(key='POSTGRES_DB', default='')
TOKEN = os.getenv(key='TOKEN', default='')


class TestTokenVerification:

    @pytest.mark.parametrize(
        argnames='postgres_user_error',
        argvalues=[None, False, '', 123, 12.3, ['user'], {'user': 'user1'}, ], )
    def test_init_postgres_user_error(self, postgres_user_error):
        with pytest.raises(TypeError) as e_info:
            init = TokenVerification(
                postgres_user=postgres_user_error,
                postgres_password=POSTGRES_PASSWORD,
                postgres_host=POSTGRES_HOST,
                postgres_port=POSTGRES_PORT,
                postgres_db=POSTGRES_DB, )

    @pytest.mark.parametrize(
        argnames='postgres_user_success',
        argvalues=['123', 'user', 'User123', 'user!@#$/', ], )
    def test_init_postgres_user_success(self, postgres_user_success):
        with does_not_raise() as e_info:
            init = TokenVerification(
                postgres_user=postgres_user_success,
                postgres_password=POSTGRES_PASSWORD,
                postgres_host=POSTGRES_HOST,
                postgres_port=POSTGRES_PORT,
                postgres_db=POSTGRES_DB, )
            assert init.postgres_user is not None

    @pytest.mark.parametrize(
        argnames='postgres_password_error',
        argvalues=[
            None, False, '', 123, 12.3, ['password'], {'password': 'password1'}, 
        ], )
    def test_init_postgres_password_error(self, postgres_password_error):
        with pytest.raises(TypeError) as e_info:
            init = TokenVerification(
                postgres_user=POSTGRES_USER,
                postgres_password=postgres_password_error,
                postgres_host=POSTGRES_HOST,
                postgres_port=POSTGRES_PORT,
                postgres_db=POSTGRES_DB, )

    @pytest.mark.parametrize(
        argnames='postgres_password_success',
        argvalues=['123', 'password', 'Password123', 'password!@#$/', ], )
    def test_init_postgres_password_success(self, postgres_password_success):
        with does_not_raise() as e_info:
            init = TokenVerification(
                postgres_user=POSTGRES_USER,
                postgres_password=postgres_password_success,
                postgres_host=POSTGRES_HOST,
                postgres_port=POSTGRES_PORT,
                postgres_db=POSTGRES_DB, )
            assert init.postgres_password is not None

    @pytest.mark.parametrize(
        argnames='postgres_host_error',
        argvalues=[None, False, '', 123, 12.3, ['host'], {'host': 'host1'}, ], )
    def test_init_postgres_host_error(self, postgres_host_error):
        with pytest.raises(TypeError) as e_info:
            init = TokenVerification(
                postgres_user=POSTGRES_USER,
                postgres_password=POSTGRES_PASSWORD,
                postgres_host=postgres_host_error,
                postgres_port=POSTGRES_PORT,
                postgres_db=POSTGRES_DB, )

    @pytest.mark.parametrize(
        argnames='postgres_host_success',
        argvalues=[
            '123', 'host', 'Host123', 'host!@#$/', 
            'https://www.google.com/', '127.0.0.1', 
        ], )
    def test_init_postgres_host_success(self, postgres_host_success):
        with does_not_raise() as e_info:
            init = TokenVerification(
                postgres_user=POSTGRES_USER,
                postgres_password=POSTGRES_PASSWORD,
                postgres_host=postgres_host_success,
                postgres_port=POSTGRES_PORT,
                postgres_db=POSTGRES_DB, )
            assert init.postgres_host is not None

    @pytest.mark.parametrize(
        argnames='postgres_port_error',
        argvalues=[
            None, False, '', 123, 12.3, 'port', 'Port123', ['port'], 
            {'port': 'port1'}, 'port!@#$/', 
        ], )
    def test_init_postgres_port_error(self, postgres_port_error):
        with pytest.raises(TypeError) as e_info:
            init = TokenVerification(
                postgres_user=POSTGRES_USER,
                postgres_password=POSTGRES_PASSWORD,
                postgres_host=POSTGRES_HOST,
                postgres_port=postgres_port_error,
                postgres_db=POSTGRES_DB, )

    @pytest.mark.parametrize(
        argnames='postgres_port_success',
        argvalues=['123', ], )
    def test_init_postgres_port_success(self, postgres_port_success):
        with does_not_raise() as e_info:
            init = TokenVerification(
                postgres_user=POSTGRES_USER,
                postgres_password=POSTGRES_PASSWORD,
                postgres_host=POSTGRES_HOST,
                postgres_port=postgres_port_success,
                postgres_db=POSTGRES_DB, )
            assert init.postgres_port is not None

    @pytest.mark.parametrize(
        argnames='postgres_db_error',
        argvalues=[None, False, '', 123, 12.3, ['db'], {'db': 'db1'}, ], )
    def test_init_postgres_db_error(self, postgres_db_error):
        with pytest.raises(TypeError) as e_info:
            init = TokenVerification(
                postgres_user=POSTGRES_USER,
                postgres_password=POSTGRES_PASSWORD,
                postgres_host=POSTGRES_HOST,
                postgres_port=POSTGRES_PORT,
                postgres_db=postgres_db_error, )

    @pytest.mark.parametrize(
        argnames='postgres_db_success',
        argvalues=['123', 'db', 'Db123', 'db!@#$/', ], )
    def test_init_postgres_db_success(self, postgres_db_success):
        with does_not_raise() as e_info:
            init = TokenVerification(
                postgres_user=POSTGRES_USER,
                postgres_password=POSTGRES_PASSWORD,
                postgres_host=POSTGRES_HOST,
                postgres_port=POSTGRES_PORT,
                postgres_db=postgres_db_success, )
            assert init.postgres_db is not None

    @pytest.mark.parametrize(
        argnames='params',
        argvalues=[
            dict(
                postgres_password=POSTGRES_PASSWORD,
                postgres_host=POSTGRES_HOST,
                postgres_port=POSTGRES_PORT,
                postgres_db=POSTGRES_DB, ),
            dict(
                postgres_user=POSTGRES_USER,
                postgres_host=POSTGRES_HOST,
                postgres_port=POSTGRES_PORT,
                postgres_db=POSTGRES_DB, ),
            dict(
                postgres_user=POSTGRES_USER,
                postgres_password=POSTGRES_PASSWORD,
                postgres_port=POSTGRES_PORT,
                postgres_db=POSTGRES_DB, ),
            dict(
                postgres_user=POSTGRES_USER,
                postgres_password=POSTGRES_PASSWORD,
                postgres_host=POSTGRES_HOST,
                postgres_db=POSTGRES_DB, ),
            dict(
                postgres_user=POSTGRES_USER,
                postgres_password=POSTGRES_PASSWORD,
                postgres_host=POSTGRES_HOST,
                postgres_port=POSTGRES_PORT, ), ], )
    def test_init_no_params(seld, params):
        with pytest.raises(TypeError) as e_info:
            init = TokenVerification(**params)

    def test_set_connect_error(self):
        with pytest.raises(ConnectionError) as e_info: 
            init = TokenVerification(
                postgres_user=POSTGRES_USER,
                postgres_password=POSTGRES_PASSWORD,
                postgres_host='incorrect_host',
                postgres_port=POSTGRES_PORT,
                postgres_db=POSTGRES_DB, )
            valid = init.verify_token(token=TOKEN)
    
    def test_set_connect_success(self):
        with does_not_raise() as e_info: 
            init = TokenVerification(
                postgres_user=POSTGRES_USER,
                postgres_password=POSTGRES_PASSWORD,
                postgres_host=POSTGRES_HOST,
                postgres_port=POSTGRES_PORT,
                postgres_db=POSTGRES_DB, )
            valid = init.verify_token(token=TOKEN)
            assert init._connection == 'seccess'

    @pytest.mark.parametrize(
        argnames='token',
        argvalues=[
            None, False, '', 123, 12.3, ['token'], {'token': 'token1'}, 
        ], )
    def test_verify_token_error(self, token):
        with pytest.raises(TypeError) as e_info:
            init = TokenVerification(
                postgres_user=POSTGRES_USER,
                postgres_password=POSTGRES_PASSWORD,
                postgres_host=POSTGRES_HOST,
                postgres_port=POSTGRES_PORT,
                postgres_db=POSTGRES_DB, )
            valid = init.verify_token(token=token)
    
    def test_verify_token_denied(self):
        with does_not_raise() as e_info: 
            init = TokenVerification(
                postgres_user=POSTGRES_USER,
                postgres_password=POSTGRES_PASSWORD,
                postgres_host=POSTGRES_HOST,
                postgres_port=POSTGRES_PORT,
                postgres_db=POSTGRES_DB, )
            valid = init.verify_token(token='incorrect_token')
            assert valid == False

    def test_verify_token_allowed(self):
        with does_not_raise() as e_info: 
            init = TokenVerification(
                postgres_user=POSTGRES_USER,
                postgres_password=POSTGRES_PASSWORD,
                postgres_host=POSTGRES_HOST,
                postgres_port=POSTGRES_PORT,
                postgres_db=POSTGRES_DB, )
            valid = init.verify_token(token=TOKEN)
            assert valid == True

    def test_verify_token_no_params(seld, ):
        with pytest.raises(TypeError) as e_info:
            init = TokenVerification(
                postgres_user=POSTGRES_USER,
                postgres_password=POSTGRES_PASSWORD,
                postgres_host=POSTGRES_HOST,
                postgres_port=POSTGRES_PORT,
                postgres_db=POSTGRES_DB, )
            valid = init.verify_token()


if __name__ == 'main':
    pytest.main()
