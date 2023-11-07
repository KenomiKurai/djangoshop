from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("blog/", views.index, name="main"),
    path("blog/post-<str:title>/", views.post, name="post"),
    path("about", views.about, name="about"),
    path("contacts", views.contacts, name="contacts"),
    path("services", views.services, name="services"),
    path('blog/category/<str:name>', views.category, name='category'),
    path("blog/search/", views.search, name='search'),
    path("blog/create/", views.create, name="create"),
path('create_category/', views.create_category, name='create_category'),
    path("blog/login", LoginView.as_view(), name="blog_login"),
    path("blog/logout/", LogoutView.as_view(), name="blog_logout"),
    path("blog/registration/", views.registration_user, name="registration"),
    path("blog/profile/", views.profile, name="profile"),
    path("edit_profile/", views.edit_profile, name="editProfile"),
    path('edit_avatar/', views.edit_avatar, name='edit_avatar'),
    # path("<dynamic_url>", views.pro_url, name="test"),
]
