
echo "Collecting static files..."
python manage.py collectstatic --clear

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Start Gunicorn processes
echo "Starting Gunicorn..."
gunicorn peach_market.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 