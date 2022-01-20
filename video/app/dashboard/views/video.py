# coding:utf-8

from django.shortcuts import redirect, reverse
from django.views.generic import View

from app.model.video import Video, VideoSub as video_sub, VideoStar as video_star
from app.utils.permission import dashboard_auth
from libs.base_render import render_to_response
from app.utils.video_enum import VideoType, FromType, NationalityType, IdentityType
from app.utils.common import check_and_get_video_type


class ExternalVideo(View):
    TEMPLATE = 'dashboard/video/externalvideo.html'

    @dashboard_auth
    def get(self, request):
        error = request.GET.get("error")
        data = {"error": error}

        videos = Video.objects.exclude(video_source=FromType.custom.value)
        for video in videos:
            video.created_time = video.created_time.strftime('%Y-%m-%d %H:%M:%S')
            video.updated_time = video.updated_time.strftime('%Y-%m-%d %H:%M:%S')
        data["videos"] = videos
        return render_to_response(request, self.TEMPLATE, data=data)

    def post(self, request):
        name = request.POST.get("video_name")
        image = request.POST.get("video_image")
        video_type = request.POST.get("video_type")
        video_source = request.POST.get("video_source")
        country = request.POST.get("country")
        info = request.POST.get("video_info")
        if not all([name, image, video_type, video_source, country, info]):
            return redirect('{}?error={}'.format(reverse('external_video'), '缺少必要字段'))
        result = check_and_get_video_type(VideoType, video_type, '不支持该类型视频')
        if result.get("code") != 0:
            return redirect('{}?error={}'.format(reverse('external_video'), result["msg"]))
        result = check_and_get_video_type(FromType, video_source, '不支持该视频来源')
        if result.get("code") != 0:
            return redirect('{}?error={}'.format(reverse('external_video'), result["msg"]))
        result = check_and_get_video_type(NationalityType, country, '没有该国家的视频')
        if result.get("code") != 0:
            return redirect('{}?error={}'.format(reverse('external_video'), result["msg"]))
        try:
            Video.objects.create(video_name=name, image=image,
                                 video_type=video_type, video_source=video_source,
                                 country=country, info=info)
        except:
            return redirect(reverse('{}?error={}'.format(reverse('external_video'), '创建失败')))
        return redirect(reverse('external_video'))


class VideoSub(View):
    TEMPLATE = 'dashboard/video/videosub.html'

    @dashboard_auth
    def get(self, request, video_id):
        data = {}
        video = Video.objects.get(pk=video_id)
        error = request.GET.get("error", "")
        data["video"] = video
        data["error"] = error
        return render_to_response(request, self.TEMPLATE, data=data)

    def post(self, request, video_id):
        url = request.POST.get("url")
        video = Video.objects.get(pk=video_id)
        length = video.video_sub.count()
        number = length + 1
        path_format = "{}".format(reverse('video_sub', kwargs={'video_id': video_id}))
        try:
            video_sub.objects.create(video=video, url=url, number=number)
        except:
            return redirect(reverse('{}?error={}'.format(path_format, "创建失败")))
        return redirect(reverse('video_sub', kwargs={'video_id': video_id}))


class VideoStar(View):

    def post(self, request):
        name = request.POST.get("name")
        identity = request.POST.get("identity")
        video_id = request.POST.get("video_id")
        path_format = "{}".format(reverse('video_sub', kwargs={'video_id': video_id}))
        if not all([name, identity, video_id]):
            return redirect(reverse('{}?error={}'.format(path_format, "缺少必要字段")))
        result = check_and_get_video_type(IdentityType, identity, '非法身份')
        if result.get("code") != 0:
            return redirect(reverse('{}?error={}'.format(path_format, result["msg"])))
        video = Video.objects.get(pk=video_id)
        try:
            video_star.objects.create(video=video, name=name, identity=identity)
        except:
            return redirect(reverse('{}?error={}'.format(path_format, "创建失败")))
        return redirect(reverse('video_sub', kwargs={'video_id': video_id}))


class StarDelete(View):

    def get(self, request, star_id, video_id):
        path_format = "{}".format(reverse('video_sub', kwargs={'video_id': video_id}))
        try:
            video_star.objects.filter(id=star_id).delete()
        except:
            return redirect(reverse('{}?error={}'.format(path_format, "删除失败")))
        return redirect(reverse('video_sub', kwargs={'video_id': video_id}))


class VideoUrlDelete(View):

    def get(self, request, video_sub_id, video_id):
        path_format = "{}".format(reverse('video_sub', kwargs={'video_id': video_id}))
        try:
            video_sub.objects.filter(pk=video_sub_id).delete()
        except:
            return redirect(reverse('{}?error={}'.format(path_format, "删除失败")))
        return redirect(reverse('video_sub', kwargs={'video_id': video_id}))
