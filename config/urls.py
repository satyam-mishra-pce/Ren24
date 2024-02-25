"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views
from config import settings
from django.conf.urls.static import static
from account.forms import LoginForm

admin.site.site_header = "Renaissance Admin Panel"
admin.site.site_title = "Renaissance Admin Panel"
admin.site.index_title = "Welcome to Renaissance 2024 Admin Panel"

urlpatterns = [
    path('',include('ticket.urls')),
    path('',include('main.urls')),
    path('u/',include('account.urls')),
    path('cart/',include('cart.urls')),
    # path(
    #     'admin/login/',
    #     views.LoginView.as_view(
    #         # template_name="login.html",
    #         authentication_form=LoginForm
    #         ),
    #     name='login'
    # ),
    path('admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
