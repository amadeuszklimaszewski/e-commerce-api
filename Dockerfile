# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10.4-bullseye

ARG ENV

ENV ENV="$ENV" \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=1 

WORKDIR /app

RUN apt-get update -q && apt-get install -yq netcat

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

EXPOSE 8000

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
