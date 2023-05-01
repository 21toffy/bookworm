import pika
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated


class GetBookView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        # Get a book by ID
        book_id = str(id) #request.GET.get('id')
        try:
            book = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(book)
        return Response(serializer.data)
    
class CreateBookView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # Create a new book
        serializer = BookSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            book = serializer.save()
            message = f"New book created: {book.title} by {book.author}"
            publish_message(message)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, id):
        # Delete a book by ID
        book_id = str(id)
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        book.delete()
        message = f"Book deleted: {book.title} by {book.author}"
        publish_message(message)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request, id):
        # Update a book by ID partially
        book_id = str(id)
        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            book = serializer.save()
            message = f"Book updated: {book.title} by {book.author}"
            publish_message(message)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
def publish_message(message):
    # Publish a message to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=settings.BOOK_RABBITMQ_QUEUE)
    channel.basic_publish(exchange='', routing_key=settings.BOOK_RABBITMQ_QUEUE, body=message)
    connection.close()
    
def consume_messages():
    # Consume messages from RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=settings.BOOK_RABBITMQ_QUEUE)
    channel.basic_consume(queue=settings.BOOK_RABBITMQ_QUEUE, on_message_callback=self.process_message, auto_ack=True)
    channel.start_consuming()
    
def process_message(ch, method, properties, body):
    # Process a message received from RabbitMQ
    print(body.decode('utf-8'))

