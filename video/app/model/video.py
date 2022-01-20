# coding:utf-8


from django.db import models

from app.utils.video_enum import VideoType, FromType, NationalityType


class Video(models.Model):
    video_name = models.CharField(max_length=100, null=True)
    image = models.CharField(max_length=500, default='')
    video_type = models.CharField(max_length=50, default=VideoType.other.value)
    video_source = models.CharField(max_length=20, null=True, default=FromType.custom.value)
    country = models.CharField(max_length=20, default=NationalityType.other.value)
    info = models.TextField()
    status = models.BooleanField(default=True, db_index=True)
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("video_name", "video_type", "video_source", "country")

    def __str__(self):
        return self.video_name


class VideoStar(models.Model):
    video = models.ForeignKey(Video, related_name='video_star', on_delete=models.SET_NULL,
                              blank=True, null=True)
    name = models.CharField(max_length=100, null=False)
    identity = models.CharField(max_length=50, default='')

    class Meta:
        unique_together = ("video", "name", "identity")

    def __str__(self):
        return self.name


class VideoSub(models.Model):
    video = models.ForeignKey(Video, related_name='video_sub', on_delete=models.SET_NULL,
                              blank=True, null=True)
    url = models.CharField(max_length=200, null=False)
    number = models.IntegerField(default=1)

    class Meta:
        unique_together = ("video", "number")

    def __str__(self):
        return "video:{} - number:{}".format(self.video.name, self.number)
