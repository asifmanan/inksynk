from django.urls import path
from postapp import views

app_name = 'postapp'
urlpatterns = [
    path('postapproval/<int:pk>', views.PostApproval.as_view(), name='postapproval'),
    path('newpost',views.CreatePostView.as_view(),name='newpost'),
    path('editpost/<int:pk>',views.EditPostView.as_view(),name='editpost'),
    path('drafts',views.ListDraftPosts.as_view(),name='draftposts'),
    
    path('published',views.ListPublishedPosts.as_view(),name='publishedposts'),
    path('published/<int:pk>',views.PublishedPostView.as_view(),name='publishedpost'),
    
    path('approved',views.ListApprovedPosts.as_view(),name='approvedposts'),
    path('listpostapproval',views.ListPostApproval.as_view(),name='listpostapproval'),
    path('publishpost/<int:post_pk>',views.PublishPostView.as_view(),name='publishpost'),
    path('deletepost/delete/<int:pk>',views.DiscardDraft.as_view(),name='deletepost'),
    path('unpublishpost/unpublish/<int:pk>',views.UnpublishPost.as_view(),name='unpublishpost'),

    path('image/new/<int:post_pk>',views.CreatePostImage.as_view(),name='addpostimage'),

]
