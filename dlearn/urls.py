from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('course/', include('course.urls')),
    path('course/', include('task.urls')),
    path('course/', include('quiz.urls')),
    path('', include('homepage.urls')),
    # path('__debug__/', include('debug_toolbar.urls'))
]

api_urlpatterns = [
    path('auth/', include('authentication.api.urls')),
    path('course/', include('course.api.urls')),
    path('task/', include('task.api.urls')),
    path('quiz/', include('quiz.api.urls')),
]

urlpatterns += [
    path('api/1.0/', include(api_urlpatterns)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
