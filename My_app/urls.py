from django.urls import path
from My_app import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),  # Add name='login' here
    path('logout', views.logout_view, name='logout'),

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

    path('profile/', views.profile_view, name='profile'),
    path('update_profile/', views.update_profile_view, name='update_profile'),
    path('get-previous-keywords/', views.get_previous_keywords, name='get_previous_keywords'),
    path('buynow/', views.buynow, name='buynow'),
    path('Request/', views.request_view, name='request_view'),
    path('on_payment_success', views.on_payment_success, name='on_payment_success'),
    path('user_pay_proceed/<int:id>/<int:amt>', views.user_pay_proceed, name='user_pay_proceed'),

    path('seller_request_view', views.seller_request_view, name='seller_request_view'),
    path('accept_request/<int:id>', views.accept_request, name='accept_request'),
    path('reject_request/<int:id>', views.reject_request, name='reject_request'),
    path('shipped_request/<int:id>', views.shipped_request, name='shipped_request'),

    path('request_view_cancel/<int:id>', views.request_view_cancel, name='request_view_cancel'),
    path('request_view_remove/<int:id>', views.request_view_remove, name='request_view_remove'),
    path('request_view_recieved/<int:id>', views.request_view_recieved, name='request_view_recieved'),

    path('provide_feedback/<int:id>', views.provide_feedback, name='provide_feedback'),
    path('sendfeedbackpost/', views.sendfeedbackpost, name='sendfeedbackpost'),


    path('profile/<int:user_id>/', views.view_profile, name='view_profile'),

    path('manage-users/', views.manage_users, name='manage-users'),  # Ensure name is 'manage-users
    path('book-management/', views.admin_book_management, name='admin_book_management'),
    path('delete-book/<int:book_id>/', views.delete_book, name='delete_book'),
    path('manage-categories/', views.manage_categories, name='manage_categories'),

    path('report_book/<int:book_id>/', views.report_book, name='report_book'),
    path('sales_statistics', views.sales_statistics, name='sales_statistics'),
    path('reports/', views.admin_view_reports, name='admin_view_reports'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),

    path('order-history/', views.order_history, name='order_history'),

]
