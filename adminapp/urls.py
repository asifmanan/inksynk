from django.urls import path
from adminapp import views
from classapp.views import CategoryList, CreateCategoryView, EditCategoryView, DeleteCategoryView
app_name = 'adminapp'
urlpatterns=[
  path('post/listpendingpost',views.ListPendingPost.as_view(),name='listpendingpost'),
  path('post/listapprovedpost',views.ListApprovedPost.as_view(),name='listapprovedpost'),
  path('post/listdisapprovedpost',views.ListDisapprovedPost.as_view(),name='listdisapprovedpost'),

  path('comment/list/<str:approval>',views.ListComment.as_view(),name='listcomment'),

  path('post/postapproval/<int:pk>',views.PostApproval.as_view(),name='postapproval'),

  path('categories/all',CategoryList.as_view(),name='categories'),
  path('categories/new',CreateCategoryView.as_view(),name='createcategory'),
  path('categories/edit/<slug:slug>',EditCategoryView.as_view(),name='editcategory'),
  path('categories/<slug:slug>/delete',DeleteCategoryView.as_view(),name='deletecategory'),  
]