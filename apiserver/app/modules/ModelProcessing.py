import numpy as np
import pandas as pd
import sklearn
import sklearn.preprocessing
import mlflow
import _pickle as cPickle
import requests
import json
from typing import Dict, Union, List, Tuple
from app.forms import PredictionData, AnswerData


class ModelProcessing:

    def __init__(self, mlflow_uri: str, model_name: str) -> None:

        if (
            (not isinstance(mlflow_uri, str)) or
            (mlflow_uri.isspace()) or
            (mlflow_uri == '')
        ):
            raise TypeError(
                '<mlflow_uri> should be a non-empty '
                'string variable without spaces!'
            )

        if (
            (not isinstance(model_name, str)) or
            (model_name.isspace()) or
            (model_name == '')
        ):
            raise TypeError(
                '<model_name> should be a non-empty '
                'string variable without spaces!'
            )

        self.mlflow_uri = mlflow_uri
        self.model_name = model_name
        self.threshold = 0.5
        self._connection = 'failure'

    def load(self) -> None:

        mlflow_uri = self.mlflow_uri
        model_name = self.model_name

        client = self.__set_connect(mlflow_uri=mlflow_uri)
        self._connection = 'success'

        model_uri, run_id = self.__get_model_params(
            client=client,
            model_name=model_name
        )

        model = self.__load_model(model_uri=model_uri)

        dictionary = self.__load_dictionary(client=client, run_id=run_id)

        encoder_features = dictionary.get('encoder_features')
        scaler_features = dictionary.get('scaler_features')
        target_column = dictionary.get('target_column')

        label_encoders = self.__load_label_encoders(
            encoder_features=encoder_features,
            client=client,
            run_id=run_id,
        )

        feature_scalers = self.__load_feature_scalers(
            scaler_features=scaler_features,
            client=client,
            run_id=run_id,
        )

        target_encoder = self.__load_target_encoder(
            target_column=target_column,
            client=client,
            run_id=run_id,
        )

        self.model = model
        self.label_encoders = label_encoders
        self.feature_scalers = feature_scalers
        self.target_encoder = target_encoder

    def __set_connect(self, mlflow_uri: str) -> mlflow.tracking.MlflowClient:

        mlflow_uri_health = mlflow_uri + '/health'

        try:
            response = requests.get(url=mlflow_uri_health)
        except requests.exceptions.ConnectionError:
            raise ConnectionError('Connection to {mlflow_uri_health} refused!')
        except requests.exceptions.MissingSchema:
            raise ConnectionError(
                'Incorrect URL: {mlflow_uri_health}. '
                'URL must start with "http://"'
            )

        if response.status_code != 200:
            raise ConnectionError('Server {mlflow_uri} is not health!')

        client = mlflow.tracking.MlflowClient(tracking_uri=mlflow_uri)

        return client


    def __get_model_params(
        self,
        client: mlflow.tracking.MlflowClient,
        model_name: str
    ) -> Tuple[str, str]:

        try:
            model_info = client.get_latest_versions(
                name=model_name,
                stages=['Production']
            )
        except mlflow.exceptions.RestException:
            raise ValueError(f'Model named "{model_name}" does not exist!')

        model_uri = model_info[0].source
        run_id = model_info[0].run_id

        return model_uri, run_id

    def __load_dictionary(
        self,
        client: mlflow.tracking.MlflowClient,
        run_id: str
    ) -> Dict[str, Union[str, List[str]]]:

        dictionary_path = 'dictionary.json'

        try:
            dictionary_artifact = client.download_artifacts(
                run_id=run_id,
                path=dictionary_path
            )
        except Exception:
            raise FileNotFoundError(f'File "{dictionary_path}" not found!')

        with open(dictionary_artifact, 'rb') as fid:
            dictionary = json.load(fid)

        return dictionary

    def __load_model(self, model_uri: str) -> mlflow.pyfunc.PyFuncModel:

        model = mlflow.pyfunc.load_model(
            model_uri=model_uri,
            suppress_warnings=True
        )
        return model

    def __load_label_encoders(
        self,
        encoder_features: List[str],
        client: mlflow.tracking.MlflowClient,
        run_id: str,
    ) -> Dict[str, sklearn.preprocessing._label.LabelEncoder]:

        label_encoders = {}

        for feature in encoder_features:
            label_encoder_name = f'label_encoder_{feature}'
            label_encoder_path = label_encoder_name + '.pkl'
            label_encoder_artifact = client.download_artifacts(
                run_id=run_id,
                path=label_encoder_path
            )
            with open(label_encoder_artifact, 'rb') as fid:
                label_encoder = cPickle.load(fid)

            label_encoders[feature] = label_encoder

        return label_encoders

    def __load_feature_scalers(
        self,
        scaler_features: List[str],
        client: mlflow.tracking.MlflowClient,
        run_id: str,
    ) -> Dict[str, sklearn.preprocessing._data.StandardScaler]:

        feature_scalers = {}

        for feature in scaler_features:
            feature_scaler_name = f'feature_scaler_{feature}'
            feature_scaler_path = feature_scaler_name + '.pkl'
            feature_scaler_artifact = client.download_artifacts(
                run_id=run_id,
                path=feature_scaler_path
            )
            with open(feature_scaler_artifact, 'rb') as fid:
                feature_scaler = cPickle.load(fid)

            feature_scalers[feature] = feature_scaler

        return feature_scalers

    def __load_target_encoder(
        self,
        target_column: str,
        client: mlflow.tracking.MlflowClient,
        run_id: str,
    ) -> Dict[str, sklearn.preprocessing._label.LabelEncoder]:

        feature = target_column
        label_encoder_name = f'label_encoder_{feature}'
        label_encoder_path = label_encoder_name + '.pkl'
        label_encoder_artifact = client.download_artifacts(
            run_id=run_id,
            path=label_encoder_path
        )
        with open(label_encoder_artifact, 'rb') as fid:
            label_encoder = cPickle.load(fid)

        return label_encoder

    def predict(
        self,
        data: dict,
        inverse_target: bool = True
    ) -> AnswerData:

        model = self.model
        label_encoders = self.label_encoders
        feature_scalers = self.feature_scalers
        target_encoder = self.target_encoder

        if (not isinstance(data, dict)) or (not bool(data)):
            raise TypeError('<data> should be a non-empty dict')

        if not self._connection == 'success':
            raise ImportError(
                'Establish a connection by calling the <load> function '
                'before calling this function!'
            )

        if (
            (not model) or
            (not label_encoders) or
            (not feature_scalers) or
            (not target_encoder)
        ):
            raise ImportError('Model data or artifacts are not loaded.')

        frame_data = self.__prepare_data(
            dict_data=data,
            label_encoders=label_encoders,
            feature_scalers=feature_scalers,
        )

        prediction = self.__model_predict(
            model=model,
            data=frame_data.values
        )[0]

        class_predicted = (prediction >= self.threshold).astype(np.int32)

        if inverse_target:

            class_predicted = self.__target_inverse_transform(
                predicted=class_predicted,
                target_encoder=target_encoder,
            )

        answer_dict = AnswerData.parse_obj({
            'Churn': class_predicted[0],
            'Probability': prediction[0]
        }).dict(by_alias=True)

        return answer_dict

    def __prepare_data(
        self,
        dict_data: PredictionData,
        label_encoders: Dict[str, sklearn.preprocessing._label.LabelEncoder],
        feature_scalers: Dict[str, sklearn.preprocessing._data.StandardScaler],
    ) -> pd.DataFrame:

        features = PredictionData.schema().get('required')

        frame_data = self.__get_data_frame(
            dict_data=dict_data,
            features=features
        )

        frame_data = self.__encoder_labels(
            frame_data=frame_data,
            label_encoders=label_encoders,
        )

        frame_data = self.__scale_features(
            frame_data=frame_data,
            feature_scalers=feature_scalers,
        )

        return frame_data

    def __get_data_frame(
        self,
        dict_data: dict,
        features: list = None
    ) -> pd.DataFrame:

        frame_data = pd.DataFrame(data=dict_data, index=[0])

        if features:
            frame_data = frame_data.loc[:, features]

        return frame_data

    def __encoder_labels(
        self,
        frame_data: pd.DataFrame,
        label_encoders: Dict[str, sklearn.preprocessing._label.LabelEncoder],
    ) -> pd.DataFrame:

        frame_data_corr = frame_data.copy()

        for feature, label_encoder in label_encoders.items():
            frame_data_corr.loc[:, feature] = label_encoder.transform(
                frame_data_corr.loc[:, feature]
            )

        return frame_data_corr

    def __scale_features(
        self,
        frame_data: pd.DataFrame,
        feature_scalers: Dict[str, sklearn.preprocessing._data.StandardScaler],
    ) -> pd.DataFrame:

        frame_data_corr = frame_data.copy()

        for feature, feature_scaler in feature_scalers.items():
            frame_data_corr.loc[:, feature] = feature_scaler.transform(
                frame_data_corr.loc[:, feature].values.reshape(-1, 1)
            )

        return frame_data_corr

    def __model_predict(
        self,
        model: mlflow.pyfunc.PyFuncModel,
        data: np.ndarray
    ) -> float:

        prediction = model.predict(data)

        return prediction

    def __target_inverse_transform(
        self,
        predicted: np.ndarray,
        target_encoder: Dict[str, sklearn.preprocessing._label.LabelEncoder],
    ) -> np.ndarray:

        inverse_predicted = target_encoder.inverse_transform(predicted)

        return inverse_predicted
