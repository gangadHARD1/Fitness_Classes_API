from django.urls import path
from .import views

#to map the endpoints to the appropriate views in the fitness_studio_app
urlpatterns = [
    path("classes",views.classes, name="classes"),
    path("book",views.book_class,name="book_class"),
    path("bookings",views.bookings,name="bookings")
    ]

