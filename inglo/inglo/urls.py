from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include('accounts.urls')),
    path('api/v1/issues/', include('issues.urls')),
    path('api/v1/posts/', include('posts.urls')),
    path('api/v1/sketches/', include('sketches.urls')),
]
