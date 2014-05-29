from django.conf.urls import patterns, url, include
from django.http import HttpRequest
from .api import UserList, UserDetail
from .api import PostList, PostDetail, UserPostList, UserPlanList
from .api import PhotoList, PhotoDetail, PostPhotoList, PlanDetail
from .api import PlanList, PlanDetail
from .api import PlanActivityList, PlanActivityDetail
from .api import LoginView, logout_view

user_urls = patterns('',
                     url(r'^/(?P<username>[0-9a-zA-Z_-]+)/plans$', UserPlanList.as_view(), name='userplan-list'),
                     url(r'^/(?P<username>[0-9a-zA-Z_-]+)$', UserDetail.as_view(), name='user-detail'),
                     url(r'^$', UserList.as_view(), name='user-list')
)

activity_urls = patterns(
    '',
    url(r'^$', PlanActivityList.as_view(), name='planactivity-list'),
    url(r'^/(?P<pk>\d+)$', PlanActivityDetail.as_view(), name='planactivity-detail')
)

plan_urls = patterns(
    '',
    url(r'^$', PlanList.as_view(), name='plan-list'),
    url(r'/(?P<pk>\d+)$', PlanDetail.as_view(), name='plan-detail'),
    url(r'^/(?P<pk>\d+)/activities$', include(activity_urls), name=''),
)
post_urls = patterns('',
                     url(r'^/(?P<pk>\d+)/photos$', PostPhotoList.as_view(), name='postphoto-list'),
                     url(r'^/(?P<pk>\d+)$', PostDetail.as_view(), name='post-detail'),
                     url(r'^$', PostList.as_view(), name='post-list')
)

photo_urls = patterns('',
                      url(r'^/(?P<pk>\d+)$', PhotoDetail.as_view(), name='photo-detail'),
                      url(r'^$', PhotoList.as_view(), name='photo-list')
)

urlpatterns = patterns('',
                       url(r'^users', include(user_urls)),
                       url(r'^posts', include(post_urls)),
                       url(r'^photos', include(photo_urls)),
                       url(r'^plans', include(plan_urls)),
                       url(r'^login/', LoginView.as_view(),name='login'),
                       url(r'^logout/', 'example.api.api.logout_view')
)

urlpatterns += patterns('',
                        url(r'^api-auth/', include('rest_framework.urls',
                                                   namespace='rest_framework')),
)

urlpatterns += patterns('',

)