# coding:utf-8

from django.urls import path

from .views.auth import Login, AdminManager, Logout, UpdateAdminStatus
from .views.index import Index
from .views.video import ExternalVideo, VideoSub, VideoStar, StarDelete, VideoUrlDelete

urlpatterns = [
    path('', Index.as_view(), name='dashboard_index'),
    path('login', Login.as_view(), name='dashboard_login'),
    path('admin', AdminManager.as_view(), name='dashboard_admin'),
    path('logout', Logout.as_view(), name='dashboard_logout'),
    path('admin/update/status', UpdateAdminStatus.as_view(), name='admin_update_status'),
    path('video/externalvideo', ExternalVideo.as_view(), name='external_video'),
    path('video/videosub/<int:video_id>', VideoSub.as_view(), name='video_sub'),
    path('video/star/', VideoStar.as_view(), name='video_star'),
    path('video/star/delete/<int:star_id>/<int:video_id>', StarDelete.as_view(), name='star_delete'),
    path('video/sub/delete/<int:video_sub_id>/<int:video_id>', VideoUrlDelete.as_view(), name='video_sub_delete')
]
