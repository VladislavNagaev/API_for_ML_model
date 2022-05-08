# Образ на основе которого будет создан контейнер
FROM python:3.8

# Изменение рабочего пользователя
USER root
# Выбор рабочей директории
WORKDIR /


# Задание переменных пользователя
ARG \
    user=appuser \
    uid=1001 \
    gid=appgroup \
    # 
    POSTGRES_USER \
    POSTGRES_PASSWORD \
    POSTGRES_HOST \
    POSTGRES_PORT \
    POSTGRES_DB \
    # 
    MLFLOW_S3_ENDPOINT_URL \
    AWS_ACCESS_KEY_ID \
    AWS_SECRET_ACCESS_KEY \
    BUCKET \
    ARTIFACT_STORE \
    MLFLOW_URI \
    MODEL_NAME 

# 
ENV \
    # Задание директории домашнего каталога
    HOME=/home/$user \
    # 
    POSTGRES_USER=$POSTGRES_USER \
    POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
    POSTGRES_HOST=$POSTGRES_HOST \
    POSTGRES_PORT=$POSTGRES_PORT \
    POSTGRES_DB=$POSTGRES_DB \
    # 
    MLFLOW_S3_ENDPOINT_URL=$MLFLOW_S3_ENDPOINT_URL \
    AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
    AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
    BUCKET=$BUCKET \
    ARTIFACT_STORE=$ARTIFACT_STORE \
    MLFLOW_URI=$MLFLOW_URI \
    MODEL_NAME=$MODEL_NAME \
    # 
    APP_HOME=/opt/ml-model-api \
    PATH_TO_SOURCE=app \
    SERVER_HOST=0.0.0.0 \
    SERVER_PORT=8000 \
    # Переменные окружения для Python (не создавать файлы кэша .pyc, не помещать в буфер потоки stdout и stderr)
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN \
    # Создание домашней директории
    mkdir -p $HOME && \
    # Создание группы и отдельного пользователя в ней
    groupadd $gid && \
    useradd --system --create-home --home-dir $HOME --shell /bin/bash --gid $gid --groups sudo --uid $uid $user && \
    # Создание каталогов для приложения
    mkdir -p $APP_HOME && \
    # Изменение прав пользователя
    chown -R $user:$gid $APP_HOME && \
    chmod -R 777 $APP_HOME

# Копирование файла зависимостей
COPY ./requirements.txt /requirements.txt
# Копирование shell-скрипта entrypoint.sh
COPY ./entrypoint.sh /entrypoint.sh

# Установка пакетов python
RUN /usr/local/bin/python -m pip install --upgrade pip && \
    pip install --no-cache-dir --requirement /requirements.txt

# Выбор рабочей директории
WORKDIR $APP_HOME
# Копирование исходного кода
COPY ./app $PATH_TO_SOURCE

# Открытие порта наружу
EXPOSE $SERVER_PORT

# Изменение рабочего пользователя
USER $user

# Точка входа
ENTRYPOINT /entrypoint.sh