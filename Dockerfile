FROM python:3.8.10

WORKDIR /app

RUN apt-get update && apt-get install -y \
  default-libmysqlclient-dev \
  build-essential \
  gcc \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure the TF_IDF_models folder exists
RUN mkdir -p /app/ai_models/TF_IDF_models/

# Set env and expose port
ENV FLASK_ENV=docker
EXPOSE 5000

EXPOSE 5000
CMD ["python", "run.py"]
