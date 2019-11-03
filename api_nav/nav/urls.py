from django.urls import path
from .views import NestedCategoryView

app_name = 'nested_category'

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path("categories/", NestedCategoryView.as_view()),
]
