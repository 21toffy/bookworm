# bookworm


Requirements
Docker
Docker Compose


Setup
Clone the repository: git@github.com:21toffy/bookworm.git


create a .env file in the home directory mocking the .env.example




Build the Docker images Start the services: docker-compose up --build

Start the services in detached mode: docker-compose up --d

Your application should now be running on http://localhost:8007

Usage
To stop the services: 
docker-compose down


To run management commands: docker-compose run workdistro_be python manage.py [command]

To enter the bash of workdistro_be container: docker-compose run workdistro_be bash

Development 

Entering shell
docker-compose exec -it bookworm_api /bin/sh

Debugging
To check logs: docker-compose logs


The bookworm_api app is a simple Django app that provides a CRUD API for managing books. It uses Django REST Framework (DRF) to build the API views and serializers, and RabbitMQ as a message broker for publishing and consuming messages.

The app consists of the following components:

models.py: defines the data model for the Book object. The Book object has the following fields: title, author, description, published_date, and created_date.

serializers.py: defines the serializer classes for the Book object. The serializer classes are used to serialize and deserialize the Book object to and from JSON.

views.py: defines the CRUD API views for the Book object. The views are implemented as classes that inherit from APIView. The views handle HTTP requests and return HTTP responses.

urls.py: defines the URLs for the API views. The URLs map the HTTP requests to the appropriate views.

settings.py: contains the Django settings for the app. It includes the DRF and RabbitMQ settings.

tasks.py: defines the tasks for consuming messages from RabbitMQ. The tasks use the process_message() function in the BookView class to process the messages.

The API views include the following methods:

GET: retrieves a single book by ID or a list of all books.

POST: creates a new book.

DELETE: deletes a book by ID.

PATCH: partially updates a book by ID.

The API views also publish messages to RabbitMQ when a book is created or deleted. The messages are consumed by a Celery worker that processes the messages and performs the appropriate action.

The API views are also documented using DRF's swagger_auto_schema decorator, which generates documentation for the API endpoints. The documentation includes information on the parameters, request and response data types, and examples.

Overall, the bookworm_api app provides a simple and scalable solution for managing books through a RESTful API.

