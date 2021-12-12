from django.contrib import admin
from django.urls import path
from django.urls.conf import include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('course/', include('course.urls')),
    path('course/', include('task.urls')),
    path('', include('homepage.urls')),
]
