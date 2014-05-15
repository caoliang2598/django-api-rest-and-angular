from rest_framework import generics, permissions, mixins, request


from .serializers import UserSerializer, PostSerializer, PhotoSerializer, PlanSerializer, ActivitySerializer
from .models import User, Post, Photo, Plan, Activity
from .permissions import IsOwnerOrReadOnly,PostAuthorCanEditPermission, IsUerOrReadOnly
from .form import LoginForm
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, login, logout, authenticate
)

class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = '#/buddies'
    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(username=username,
                            password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def form_invalid(self):
        return HttpResponseRedirect(reverse('/'))

    def get_success_url(self):
        return self.success_url

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid()


class UserList(generics.ListAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]


class UserDetail(generics.RetrieveUpdateAPIView):
    model = User
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsUerOrReadOnly
    ]




class PlanList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    model = Plan
    serializer_class = PlanSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]


    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


    def pre_save(self,obj):
        obj.author=self.request.user
        return super(PlanList, self).pre_save(obj)


class UserPlanList(PlanList):

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

    def get_queryset(self):
        queryset = super(UserPlanList, self).get_queryset()
        return queryset.filter(usr__username=self.kwargs.get('username'))

class PlanDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    model = Plan
    serializer_class = PlanSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]


    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class PlanActivityList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    model = Activity
    serializer_class = ActivitySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def pre_save(self,obj):
        obj.plan=self.request.plan
        return super(PlanActivityList, self).pre_save(obj)

    def get_queryset(self):
        queryset = super(PlanActivityList, self).get_queryset()
        return queryset.filter(plan__pk=self.kwargs.get('pk'))


class PlanActivityDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    model = Activity
    serializer_class = ActivitySerializer
    permission_class = (permissions.IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class PostMixin(object):
    model = Post
    serializer_class = PostSerializer
    permission_classes = [
        PostAuthorCanEditPermission
    ]
    
    def pre_save(self, obj):
        """Force author to the current user on save"""
        obj.author = self.request.user
        return super(PostMixin, self).pre_save(obj)


class PostList(PostMixin, generics.ListCreateAPIView):
    pass


class PostDetail(PostMixin, generics.RetrieveUpdateDestroyAPIView):
    pass


class UserPostList(generics.ListAPIView):
    model = Post
    serializer_class = PostSerializer
    
    def get_queryset(self):
        queryset = super(UserPostList, self).get_queryset()
        return queryset.filter(author__username=self.kwargs.get('username'))


class PhotoList(generics.ListCreateAPIView):
    model = Photo
    serializer_class = PhotoSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]


class PhotoDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Photo
    serializer_class = PhotoSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]


class PostPhotoList(generics.ListAPIView):
    model = Photo
    serializer_class = PhotoSerializer
    
    def get_queryset(self):
        queryset = super(PostPhotoList, self).get_queryset()
        return queryset.filter(post__pk=self.kwargs.get('pk'))
