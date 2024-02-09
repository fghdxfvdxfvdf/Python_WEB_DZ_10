from django.contrib.auth.views import LoginView
from django.urls import path

from . import views

app_name = "quotes"

urlpatterns = [
    path("", views.main, name="root"),
    path("<int:page>", views.main, name="root_paginate"),
    path("<int:page>/", views.main, name="root_paginate"),
    path("author/<str:id_>/", views.about_author, name="about_author"),
    path("author/<slug:id_>", views.about_author, name="about_author"),
    path("tag/<slug:tag_slug>/", views.quotes_by_tag, name="quotes_by_tag"),
    path("tag/<slug:tag_slug>", views.quotes_by_tag, name="quotes_by_tag"),
    path("post_author/", views.post_author, name="post_author"),
    path("post_author", views.post_author, name="post_author"),
    path("post_quote/", views.post_quote, name="post_quote"),
    path("post_quote", views.post_quote, name="post_quote"),
    path("quote/<int:quote_id>/", views.quote_detail, name="quote_detail"),
    path("author/<int:author_id>/", views.author_detail, name="author_detail"),
    path("detail/<int:note_id>", views.detail, name="detail"),
    path("done/<int:note_id>", views.set_done, name="set_done"),
    path("delete/<int:note_id>", views.delete_note, name="delete"),
]
