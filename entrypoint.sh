#!/bin/bash
set -e

# Start SQL Server in the background
/opt/mssql/bin/sqlservr &
MSSQL_PID=$!

echo "Waiting for SQL Server to be ready..."
for i in $(seq 1 30); do
    /opt/mssql-tools18/bin/sqlcmd \
        -S localhost -U sa -P "$MSSQL_SA_PASSWORD" \
        -C -Q "SELECT 1" \
        > /dev/null 2>&1 && break
    echo "  attempt $i/30 — not ready yet, retrying in 2s..."
    sleep 2
done

echo "Running init.sql..."
/opt/mssql-tools18/bin/sqlcmd \
    -S localhost -U sa -P "$MSSQL_SA_PASSWORD" \
    -C -i /init.sql

echo "Database initialization complete."

# Hand off to SQL Server foreground process
wait $MSSQL_PID
