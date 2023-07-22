from django.urls import path
from .views import ArtListView, ArtCreateView, AllArticlesView, CategoryCreateView, ArtDetailView, ArtUpdateView, ArtDeleteView

app_name="articulos"

urlpatterns = [
    path('', ArtListView.as_view(), name="home"),
    path('create/', ArtCreateView.as_view(), name="create"),
    path('all-articles/', AllArticlesView.as_view(), name="all_articles"),
    path('create-category/', CategoryCreateView.as_view(), name="create_category"),
    path('Article/<int:post_id>/', ArtDetailView.as_view(), name="detail"),
    path('<int:pk>/update/', ArtUpdateView.as_view(), name="update"),
    path('<int:pk>/delete/', ArtDeleteView.as_view(), name="delete")
]