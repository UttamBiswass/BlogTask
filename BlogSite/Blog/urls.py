
from django.urls import path
from . import views
from rest_framework import routers
from .views import UserBlogs

router=routers.DefaultRouter()


router.register('alluser',views.AllUsers,basename='alluser')
router.register('all-blogs',views.UserBlog,basename='blogs') 
router.register('comments',views.UserComments,basename='comments') 
router.register('user-likes',views.UserLikes,basename='user-likes')
router.register('tags',views.BlogTags,basename='tags') 



urlpatterns = [
    path('', views.Index, name='index'),
    path('login/', views.LoginApi.as_view(), name='LoginApi'), 
    path('user-blog/', UserBlogs, name='user-blogs'),
    path('blogs/<int:id>/', views.blog_detail, name='blog_detail'),
    path('register/',views.RegisterUserAPIView.as_view()), 
    
]

urlpatterns += router.urls