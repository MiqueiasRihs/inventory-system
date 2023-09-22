FROM python:3.9

WORKDIR /home/dev/inventory-system/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt && \
    chmod +x ./wait-for-it.sh

COPY app .

CMD ["../wait-for-it.sh", "db:5432", "--timeout=5", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]