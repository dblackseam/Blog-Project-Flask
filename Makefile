run:
	docker build . -t python-flask
	docker run -d -p 80:5000 -e SECRET_KEY --name flask-container --rm python-flask
run-dev:
	docker build . -t flask-project:V1
	docker run -d -p 80:5000 --env-file ./.env --mount type=volume,destination=/app/db --name flask-container --rm flask-project:V1
stop:
	docker stop flask-container
