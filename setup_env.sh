#!/bin/bash

attempts=0
max_attempts=10

while [ $attempts -lt $max_attempts ]; do
    if pg_isready -h postgres_inventory -p 5432 -U postgres -d solfacil; then
        echo "Banco de dados PostgreSQL está pronto!"
        python -m pytest
        uvicorn main:app --host 0.0.0.0 --port 8000 --reload
        break
    else
        echo "Tentativa $attempts: Banco de dados não está pronto. Aguardando..."
        attempts=$((attempts+1))
        sleep 5
    fi
done

if [ $attempts -eq $max_attempts ]; then
    echo "O banco de dados não subiu após $max_attempts tentativas."
fi
