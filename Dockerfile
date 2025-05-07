FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.7.1

# Install system dependencies for Fiona, GDAL, GEOS, PROJ, etc.
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    g++ \
    gcc \
    libgdal-dev \
    gdal-bin \
    libproj-dev \
    libgeos-dev \
    && apt-get clean

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
 && poetry install --no-interaction --no-ansi

COPY . .

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
