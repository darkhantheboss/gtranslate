FROM python:3.10

WORKDIR /src/gtranslate/
ENV PYTHONPATH="${PYTHONPATH}:/src/gtranslate"

RUN apt update \
        && apt -y install libssl-dev swig python3-dev gcc \
        && apt clean

COPY . /src/gtranslate/

RUN pip install pipenv setuptools && PIPENV_VENV_IN_PROJECT=1 pipenv install --system --deploy

EXPOSE 8000

CMD alembic upgrade head & gunicorn -k uvicorn.workers.UvicornWorker --access-logformat '%(h)s %(l)s %(h)s %(l)s %(t)s "%(r)s" %(s)s %(T)s' --workers=1 -b 0.0.0.0:8000 app:app
