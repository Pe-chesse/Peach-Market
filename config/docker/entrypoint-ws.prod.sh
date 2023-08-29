
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

echo "Starting daphne..."
export DJANGO_SETTINGS_MODULE=peach_market.settings
daphne -b 0.0.0.0 -p 8001 peach_market.asgi:application