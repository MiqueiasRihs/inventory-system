FROM python:3.9

WORKDIR /home/dev/inventory-system/app

COPY . .

RUN apt-get update && \
    apt-get install postgresql-client -y && \
    pip install --no-cache-dir -r requirements.txt && \
    chmod +x ./setup_env.sh

COPY app .

CMD ["../setup_env.sh"]