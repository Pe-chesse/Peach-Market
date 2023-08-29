
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

echo "Starting Uvicorn..."
gunicorn peach_market.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8001