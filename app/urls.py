from django.urls import path
from .views import *

from django.contrib.auth.views import (
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    path('',index,name="index"),

    path('contact/',contact,name="contact"),
    path('login/',login_view,name="login"),
    path('register/',register_view,name="register"),
    path('logout/',logout_view,name="logout"),
    path('contact/',contact,name="contact"),
    path('code_page/',code_page,name="code_page"),

    path('blog_detail/',blogs,name="blogs"),
    path('blog_detail/<int:blog_id>/',singleBlog,name='singleBlog'),
    path('comment/<int:blog_id>/',comment,name='comment'),
    path('tutorials/',tutorials,name="tutorials"),
    path('tutorials/<int:tut_id>/',tutorialView,name="tutorialView"),
    path('tutorials/post/<int:post_id>/',tutorialPost,name="tutorialPost"),
    path('meme/',meme,name="meme"),
    path('code/',code,name="code"),
    path('code_page/<int:lan_id>/',code_pages,name="code_page"),

    path('upload_meme/',upload_meme,name="upload_meme"),
    path('upload_blog/',post_blog,name="add_blog"),

    path('password-reset/', PasswordResetView.as_view(template_name='password/password_reset.html'),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='password/reset_password_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'),name='password_reset_complete'),
    
]
