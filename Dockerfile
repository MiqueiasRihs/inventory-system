FROM python:3.9

WORKDIR /home/dev/inventory-system

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
