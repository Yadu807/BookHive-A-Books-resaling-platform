from django.urls import path
from My_app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),  # Add name='login' here
    path('forgotpassword', views.forgotpassword, name='forgotpassword'),
    path('forgot_password_post', views.forgot_password_post, name='forgot_password_post'),  # For form submission
    path('adminhome', views.adminhome),
    path('logincode', views.logincode),
    path('registration', views.registration, name='register'),
    path('reg_code_user', views.reg_code_user),
    path('userhome', views.userhome),
    path('sellerhome', views.sellerhome),
    path('addbook', views.addbook),
    path('add_book', views.add_book),
    path('UpdateBook/<id>', views.UpdateBook),
    path('update_book_post', views.update_book_post),

]
