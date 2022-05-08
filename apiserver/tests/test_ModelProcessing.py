import os
import pytest
from contextlib import nullcontext as does_not_raise


from app.modules import ModelProcessing


MLFLOW_S3_ENDPOINT_URL = os.getenv(key='MLFLOW_S3_ENDPOINT_URL', default='')
AWS_ACCESS_KEY_ID = os.getenv(key='AWS_ACCESS_KEY_ID', default='')
AWS_SECRET_ACCESS_KEY = os.getenv(key='AWS_SECRET_ACCESS_KEY', default='')
BUCKET = os.getenv(key='BUCKET', default='')
ARTIFACT_STORE = os.getenv(key='ARTIFACT_STORE', default='')
MLFLOW_URI = 'http://127.0.0.1:5000'
MODEL_NAME = os.getenv(key='MODEL_NAME', default='')


class TestModelProcessing:

    @pytest.mark.parametrize(
        argnames='mlflow_uri_error',
        argvalues=[None, False, '', 123, 12.3, ['text'], {'text': 'text1'}, ], )
    def test_init_mlflow_uri_error(self, mlflow_uri_error):
        with pytest.raises(TypeError) as e_info:
            init = ModelProcessing(
                mlflow_uri=mlflow_uri_error,
                model_name=MODEL_NAME, )

    @pytest.mark.parametrize(
        argnames='mlflow_uri_success',
        argvalues=['123', 'text', 'Text123', 'text!@#$/', ], )
    def test_init_mlflow_uri_success(self, mlflow_uri_success):
        with does_not_raise() as e_info:
            init = ModelProcessing(
                mlflow_uri=mlflow_uri_success,
                model_name=MODEL_NAME, )
            assert init.mlflow_uri is not None

    @pytest.mark.parametrize(
        argnames='model_name_error',
        argvalues=[None, False, '', 123, 12.3, ['text'], {'text': 'text1'}, ], )
    def test_init_model_name_error(self, model_name_error):
        with pytest.raises(TypeError) as e_info:
            init = ModelProcessing(
                mlflow_uri=MLFLOW_URI,
                model_name=model_name_error, )

    @pytest.mark.parametrize(
        argnames='model_name_success',
        argvalues=['123', 'text', 'Text123', 'text!@#$/', ], )
    def test_init_model_name_success(self, model_name_success):
        with does_not_raise() as e_info:
            init = ModelProcessing(
                mlflow_uri=MLFLOW_URI,
                model_name=model_name_success, )
            assert init.model_name is not None

    @pytest.mark.parametrize(
        argnames='mlflow_uri_error',
        argvalues=['http://incorrect_mlflow_uri', 'incorrect_mlflow_uri'], )
    def test_set_connect_error(self, mlflow_uri_error):
        with pytest.raises(ConnectionError) as e_info:
            init = ModelProcessing(
                mlflow_uri=mlflow_uri_error,
                model_name=MODEL_NAME, )
            init.load()

    def test_set_connect_success(self):
        with does_not_raise() as e_info:
            init = ModelProcessing(
                mlflow_uri=MLFLOW_URI,
                model_name=MODEL_NAME, )
            init.load()
            assert init._connection == 'success'

    def test_load_error_mlflow_uri(self):
        with pytest.raises(ValueError) as e_info:
            init = ModelProcessing(
                mlflow_uri=MLFLOW_URI,
                model_name='incorrect_model_name', )
            init.load()


if __name__ == 'main':
    pytest.main()
