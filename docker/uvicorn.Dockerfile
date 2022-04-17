# Base image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

# Load requirements
COPY requirements.txt .

# Install dependencies
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install --upgrade uvicorn[standard]

# Copy static files
COPY templates templates
COPY src src

# Change working directory
WORKDIR /app

# Set command line
CMD [ "uvicorn" \
    , "main:app" \
    , "--app-dir", "src/api" \
    , "--host", "0.0.0.0" \
    , "--port", "8880" \
    , "--root-path", "." \
    , "--use-colors" \
    ]
