FROM python:3.11

WORKDIR /app

RUN python -m venv /opt/venv

COPY requirements.txt .

RUN . /opt/venv/bin/activate && pip install --no-cache-dir -r requirements.txt

ENV PATH="/opt/venv/bin:$PATH"
ENV DOCKERENV="true"
COPY . .

CMD bash -c "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port $PORT"
