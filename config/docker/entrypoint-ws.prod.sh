
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

echo "Starting Uvicorn..."
uvicorn peach_market.asgi:application --host 0.0.0.0 --port 8001