# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Load Django settings
export DJANGO_SETTINGS_MODULE=peach_market.settings

echo "Starting uvicorn..."
uvicorn peach_market.asgi:application --host 0.0.0.0 --port 8001