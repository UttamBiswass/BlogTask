from django.shortcuts import render,redirect
from django.http import HttpResponse
import re
from django.shortcuts import render, get_object_or_404
from .models import *
from .serializers import *
from rest_framework import viewsets, status, generics, filters, views,mixins
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from .paginations import *
from django_filters.rest_framework import DjangoFilterBackend
from django.conf import settings
from django.core.mail import send_mail



def Index(request):

    return render (request,'loginUsers.html')



class LoginApi(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        email = data['email']
        password = data['password']

        try:
            user = User.objects.get(email = email)
            validate = check_password(password, user.password)
            
            if validate:
                token = str(RefreshToken.for_user(user))
                access = str(RefreshToken.for_user(user).access_token)
                return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "access": access,
                "refresh": token,
                "is_staff": user.is_staff,  
                "is_superuser": user.is_superuser  
            

                })
            else:
                content = {"detail": "Password Do not Match"}
                return Response(content, status=status.HTTP_404_NOT_FOUND)
        except:
            content = {"detail": "No active account found with the given credentials"}
            return Response(content, status=status.HTTP_404_NOT_FOUND)



class RegisterUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super(RegisterUserAPIView, self).create(request, *args, **kwargs)
        if response.status_code == 201:
            user = User.objects.get(pk = response.data['id'])

            token = str(RefreshToken.for_user(user))
            access = str(RefreshToken.for_user(user).access_token)
        
            return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "access": access,
            "refresh": token,
            }, 
            status = status.HTTP_201_CREATED)
        return response
    


# ###-------All Users
class AllUsers(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=AllUserSerializer



class UserBlog(viewsets.ModelViewSet):
    queryset=Blog.objects.all()
    serializer_class=BlogSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    pagination_class = CustomPagination



def UserBlogs(request):

    return render(request,'blog_list.html')

def blog_detail(request, id):
    blog = get_object_or_404(Blog, id=id)

    if request.method == "POST":
        if 'comment' in request.POST:
            content = request.POST.get("content")
            if content:
                Comment.objects.create(blog=blog, content=content)
                return redirect('blog_detail', id=id)

        if 'like' in request.POST:
            try:
                like = Like.objects.get(blog=blog, user=request.user)
                like.delete()  # Unlike
            except Like.DoesNotExist:
                Like.objects.create(blog=blog, user=request.user)  # Like
            return redirect('blog_detail', id=id)

        if 'email' in request.POST:
            recipient_email = request.POST.get('recipient_email')
            print(recipient_email, '-----------recipient_email--')
            if recipient_email:
                subject = f"Check out this blog post: {blog.title}"
                message = f"""
                Hello,
                Dear User,

                Title: {blog.title}
                Description: {blog.description}
                Posted at: {blog.post_at}



                Best regards,
                Uttam Biswas
                """
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient_email])
                return redirect('blog_detail', id=id) 


    comments = blog.comments.all().order_by('-created_at')
    likes_count = blog.likes.count()
    user_has_liked = blog.likes.filter(user=request.user).exists()

    return render(request, 'blog_detail.html', {
        'blog': blog,
        'comments': comments,
        'likes_count': likes_count,
        'user_has_liked': user_has_liked,
    })



class UserComments(viewsets.ModelViewSet):
    queryset=Comment.objects.all()
    serializer_class=CommentSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    pagination_class = CustomPagination


class UserLikes(viewsets.ModelViewSet):
    queryset=Like.objects.all()
    serializer_class=LikeSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    pagination_class = CustomPagination



class BlogTags(viewsets.ModelViewSet):
    queryset=Tag.objects.all()
    serializer_class=TagsSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    pagination_class = CustomPagination



    