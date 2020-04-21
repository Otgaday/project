
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include
from resource_accounting.views import *

app_name = 'resource_accounting'
urlpatterns = [
    path('', Create_resource.as_view()),
    path('<int:pk>/', Update_delete_resources.as_view()),
    path('total_cost/', Total_cost.as_view()),

]
urlpatterns = format_suffix_patterns(urlpatterns)