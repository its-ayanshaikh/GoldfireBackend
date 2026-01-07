from django.urls import path
from employee.consumers import LeaveConsumer

websocket_urlpatterns = [
    path("ws/leave-updates/<int:user_id>/", LeaveConsumer.as_asgi()),
]
