
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

echo "Starting daphne..."
daphne -b 0.0.0.0 -p 8001 peach_market.asgi:application