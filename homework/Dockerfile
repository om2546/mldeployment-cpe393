FROM python:3.8-slim
WORKDIR /app

COPY app/ /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 9000

CMD ["python", "homework.py"]
