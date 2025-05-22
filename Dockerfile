FROM python:3.11-slim

WORKDIR /app 

# Install uv package manager first
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir uv

# Install dependencies using uv with --system flag
RUN uv pip install --system --no-cache-dir fastapi uvicorn sqlalchemy passlib[bcrypt] \
    python-jose[cryptography] python-multipart email-validator \
    psycopg2-binary pydantic crewai requests langchain langchain-openai

COPY . .

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0"]

