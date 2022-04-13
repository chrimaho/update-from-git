FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY requirements.txt .

RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install --upgrade uvicorn[standard]

WORKDIR /app

CMD [ "uvicorn" \
    , "main:app" \
    , "--app-dir", "./src/api" \
    , "--host", "0.0.0.0" \
    , "--port", "8000" \
    , "--root-path", "." \
    , "--reload" \
    , "--reload-include", "\"*.yaml\"" \
    , "--reload-include", "\"*.joblib\"" \
    , "--reload-include", "\"*.pkl\"" \
    , "--use-colors" \
    , "--log-level", "debug" \
    ]
