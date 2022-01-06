from django.contrib import admin
from flip.models import *
from django.contrib.auth.admin import UserAdmin


class UserAccountsAdmin(UserAdmin):
    list_display = ['id','username','first_name','email','phone','image','date_joined','last_login','is_staff','is_admin']
    search_fields = ['id','username','first_name','email','phone','image']
    readonly_fields = ['date_joined','last_login','is_active','is_staff','is_admin']

    filter_horizontal = []
    list_filter = []
    fieldsets = []
admin.site.register(UserAccounts, UserAccountsAdmin)


class PostUploadAdmin(admin.ModelAdmin):
    list_display = ['id','user','post','caption','post_type','date_post']
admin.site.register(PostUploadModel, PostUploadAdmin)


class LikeAdmin(admin.ModelAdmin):
    list_display = ['id','user','post','value']
admin.site.register(LikeModel, LikeAdmin)


class CommentsAdmin(admin.ModelAdmin):
    list_display = ['id','user','post','body']
admin.site.register(CommentsModels, CommentsAdmin)


class BasicInfoAdmin(admin.ModelAdmin):
    list_display = ['id','user','web_link','bio']
admin.site.register(BasicInfoModel, BasicInfoAdmin)


class FollowerAdmin(admin.ModelAdmin):
    list_display = ['id','follower','following']
admin.site.register(FollowsModel, FollowerAdmin)


class StreamAdmin(admin.ModelAdmin):
    list_display = ['id','following','user']
admin.site.register(StreamModel, StreamAdmin)