from django.urls import path
from . consumers import NewConsumer

testings_urlpatterns=[
    path('ws/test/<str:groupname>/', NewConsumer.as_asgi())
]