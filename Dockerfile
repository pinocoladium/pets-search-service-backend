FROM python:3.14-slim
ENV PYTHONUNBUFFERED 1
ENV LANG ru_RU.UTF-8

RUN apt-get update &&  \
    apt-get install --no-install-recommends -y \
    git \
    curl \
    gettext \
    binutils \
    libproj-dev \
    libpq-dev `# build psycopg2` \
    gcc `# install psycopg2 & pre-commit` \
    gdal-bin && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Установка зависимостей
COPY ./requirements.txt .
RUN pip install uv && uv pip install --system -r requirements.txt && pip cache purge && uv cache clean

WORKDIR /code
COPY . /code


CMD [ "gunicorn", "-c", "gunicorn.conf.py", "dutssd_tyumen.wsgi:application" ]
EXPOSE 8000
