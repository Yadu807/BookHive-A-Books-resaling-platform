from django.urls import path
from My_app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),  # Add name='login' here
    path('forgotpassword', views.forgotpassword, name='forgotpassword'),
    path('forgot_password_post', views.forgot_password_post, name='forgot_password_post'),  # For form submission
    path('checkemail', views.checkemail, name='checkemail'),  # For form submission
    path('checkuname', views.checkuname, name='checkuname'),  # For form submission

    path('adminhome', views.adminhome),
    path('logincode', views.logincode),
    path('registration/', views.registration, name='registration'),
    path('reg_code_user/', views.reg_code_user, name='reg_code_user'),
    path('userhome', views.userhome),
    path('sellerhome', views.sellerhome),
    path('addbook', views.addbook),
    path('add_book', views.add_book),
    path('DeleteBook/<id>', views.DeleteBook),
    path('UpdateBook/<id>', views.UpdateBook),
    path('update_book_post', views.update_book_post),
    path('book_detail/<int:book_id>/', views.book_detail, name='book_detail'),
    path('book_detail2/<int:book_id>/', views.book_detail2, name='book_detail2'),
    path('sellerSearch/', views.sellerSearch, name='sellerSearch'),
    path('book_detail1', views.book_detail1, name='book_detail1'),
    path('book_detail3', views.book_detail3, name='book_detail3'),
    path('sellerSearch', views.sellerSearch, name='sellerSearch'),
    path('userhomesearch', views.userhomesearch, name='userhomesearch'),
    path('terms', views.terms, name='terms'),
    path('addfav', views.addfav, name='addfav'),
    path('owner_chat_to_user/<id>', views.owner_chat_to_user, name='owner_chat_to_user'),
    path('coun_msg/<id>', views.coun_msg, name='coun_msg'),
    path('chat_view', views.chat_view, name='chat_view'),
    path('chat_send/<msg>', views.chat_send, name='chat_send'),
    # path('chat_send/<msg>', views.chat_send, name='chat_send'),
    path('upload_image', views.upload_image, name='upload_image'),
    path('home_chat', views.home_chat, name='home_chat'),
    path('chatview', views.chatview, name='chatview'),

    path('favorites', views.favorites_view, name='favorites'),  # Favorites view
    path('fav_view', views.fav_view, name='fav_view'),  # Favorites view
]
