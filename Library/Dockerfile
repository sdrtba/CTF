FROM python:3.11-slim
COPY server.py /app/server.py
WORKDIR /app
USER nobody
EXPOSE 31337
CMD ["python3", "server.py"]
