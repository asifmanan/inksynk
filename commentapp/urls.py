from django.urls import path
from commentapp import views

app_name = 'commentapp'
urlpatterns = [
    path('list/<str:approval>', views.UserCommentList.as_view(), name='usercommentlist'),
]