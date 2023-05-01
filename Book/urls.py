
from django.urls import path
from .views import (
BookView,
GetBookView,
CreateBookView
)


app_name = "Book"

urlpatterns = [
    path('get/<int:id>/', GetBookView.as_view(), name='book'),
    path('create/', CreateBookView.as_view(), name='book'),
    path('<int:id>/', BookView.as_view(), name='book_detail'),
]