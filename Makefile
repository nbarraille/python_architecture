start_api:
	FLASK_APP=grocery/presentation/api/__init__.py \
		FLASK_ENV=development \
		poetry run flask run