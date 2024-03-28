python manage.py import_uszips cargo/data/uszips.csv
python manage.py add_vehicles

GET /api/cargo/?weight_min=200
GET /api/cargo/?weight_min=200&weight_max=500

 celery -A drf_project beat -l INFO
 celery -A drf_project worker -l INFO