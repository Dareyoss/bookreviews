from django.urls import path
from . import views

urlpatterns = [
    path('<int:book_id>', views.detail, name='detail'),
    path('<int:book_id>/create', views.createreview,
         name='createreview'),
    path('review/<int:review_id>', views.updatereview,
         name='updatereview'),
    path('review/<int:review_id>/delete', views.deletereview,
         name='deletereview'),
]