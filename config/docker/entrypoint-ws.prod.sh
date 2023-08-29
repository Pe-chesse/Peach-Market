echo "Starting Gunicorn..."
gunicorn peach_market.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8001

echo "Starting Uvicorn..."
uvicorn --reload peach_market.asgi:application --host 0.0.0.0 --port 8001