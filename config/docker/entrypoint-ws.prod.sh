
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

echo "Starting uvicorn..."
gunicorn -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8001 peach_market.asgi:application