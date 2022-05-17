FROM gcr.io/deeplearning-platform-release/base-cpu
WORKDIR /app

COPY bitcoin_predictor.py .
COPY requirements.txt .

## install requirements
RUN pip install --no-cache-dir -r ./requirements.txt

ENTRYPOINT ["python", "bitcoin_predictor.py"]
