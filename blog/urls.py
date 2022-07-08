from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views 
from blog_app import views as auth_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',auth_view.HomePage.as_view(),name='home'),
    path('blog/',include('blog_app.urls')),
    path('accounts/login/', views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(), name='logout', kwargs={'next_page': '/'}),
]
