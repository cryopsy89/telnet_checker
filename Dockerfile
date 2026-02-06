FROM python:3.9-alpine

WORKDIR /app

COPY telnet_checker.py .

RUN apk add --no-cache \
    && python -m pip install --no-cache-dir --upgrade pip \
    && adduser -D -u 1000 checkeruser

USER checkeruser
EXPOSE 8080

# Запускаем сервер
CMD ["python", "telnet_checker.py", "8080"]