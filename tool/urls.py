from django.urls import path
from .views import *

urlpatterns = [
    path('', ToolListCreateView.as_view(), name='ListCreateView'),
    path('<int:id>/', ToolRetrieveUpdateDestroyView.as_view(), name="RetrieveUpdateDestroyView"),
]
