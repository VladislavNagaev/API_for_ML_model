# Образ на основе которого будет создан контейнер
FROM ubuntu:20.04

# Изменение рабочего пользователя
USER root
# Выбор рабочей директории
WORKDIR /


ARG \
    # Задание переменных пользователя
    user=mlflow \
    uid=1001 \
    gid=mlflow-group \
    # Задание переменных для entrypoint
    POSTGRES_USER \
    POSTGRES_PASSWORD \
    POSTGRES_HOST \
    POSTGRES_PORT \
    POSTGRES_DB

ENV \
    # Задание директории домашнего каталога
    HOME=/home/$user \
    # Переменные окружения для entrypoint
    POSTGRES_USER=$POSTGRES_USER \
    POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
    POSTGRES_HOST=$POSTGRES_HOST \
    POSTGRES_PORT=$POSTGRES_PORT \
    POSTGRES_DB=$POSTGRES_DB \
    MLFLOW_HOME=/opt/mlflow \
    ARTIFACT_STORE=$MLFLOW_HOME/mlruns \
    SERVER_HOST=0.0.0.0 \
    SERVER_PORT=5000 \
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
    mkdir -p $MLFLOW_HOME && \
    mkdir -p $ARTIFACT_STORE && \
    # Изменение прав пользователя
    chown -R $user:$gid $MLFLOW_HOME && \
    chmod -R 777 $MLFLOW_HOME && \
    # Установка пакетов
    apt -y update && \
    # echo Y | apt upgrade && \
    echo Y | apt install wget && \
    # Установка C compiler (GCC)
    echo Y | apt install build-essential && \
    apt install manpages-dev && \
    # Уствнока Python
    echo Y | apt install python3.8 && \
    # Установка pip
    apt install -y python3-pip && \
    # Установка дополнительных инструментов
    echo Y | apt install libpq-dev build-essential libssl-dev libffi-dev python3-dev && \
    # Обновление путей
    apt -y update

# Копирование файла зависимостей
COPY ./requirements.txt ./
# Копирование shell-скрипта entrypoint.sh
COPY ./entrypoint.sh ./

# Установка пакетов python
RUN pip install --no-cache-dir --requirement ./requirements.txt

# Открытие порта наружу
EXPOSE $SERVER_PORT/tcp

# Монтирование внешнего тома
VOLUME ["${MLFLOW_HOME}", "${ARTIFACT_STORE}"]

# Изменение рабочего пользователя
USER $user
# Выбор рабочей директории
WORKDIR $MLFLOW_HOME

# Точка входа
ENTRYPOINT /entrypoint.sh