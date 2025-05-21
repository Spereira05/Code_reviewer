FROM python:3.13-slim

WORKDIR /app 

COPY pyproject.toml ./ 
RUN pip install --no-cache-dir uv 

COPY . .

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0"]

