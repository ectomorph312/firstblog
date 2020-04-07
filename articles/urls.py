from django.urls import path
from django.conf.urls import url

from .views import *

urlpatterns = [
    path('<int:pk>/edit/',
         ArticleUpdateView.as_view(), name='article_edit'),
    path('<int:pk>/',
         ArticleDetailView.as_view(), name='article_detail'),
    path('<int:pk>/delete/',
         ArticleDeleteView.as_view(), name='article_delete'),
    path('new/', ArticleCreateView.as_view(), name='article_new'),
    path('', ArticleListView.as_view(), name='article_list'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('<int:pk>/addlike/', add_like, name='add_like'),
    path('<int:pk>/adddislike/', add_dislike,name='add_dislike'),
#     path('<int:pk>/comment/', 
#           CommentView.as_view(), name='add_comment'),
]
