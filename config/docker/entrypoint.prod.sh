
# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Start Gunicorn processes
echo "Starting Gunicorn..."
exec gunicorn your_project_name.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 # 워커 수 조정 가능