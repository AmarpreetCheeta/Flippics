from django.urls import path
from flip import views
from django.contrib.auth import views as as_views
from . forms import ForgetPasswordForm, PasswordResetSetForm

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('explore/', views.Explore.as_view(), name='explore'),
    path('post_view/<int:pk>/', views.ExplorePostView.as_view(), name='explore_post_view'),

    path('Upload/', views.Upload.as_view(), name='Upload'),
    path('notifications/', views.Like.as_view(), name='Like'),
    
    path('acc/<int:pk>/', views.AccountsCLass.as_view(), name='accounts'),
    path('acc/<int:pk>/videos/', views.Videos.as_view(), name='videos'),

    path('accounts_user_post/<int:pk>/', views.AccountUserPost.as_view(), name='accounts_user_post'),
    path('user_post_editing/<int:pk>/', views.UserPostEditing.as_view(), name='user_post_editing'),
    path('user_post_delete/<int:pk>/', views.DeleteUserPOST, name='user_post_delete'),

    path('search_for_users/', views.SearchForUserCLass, name='searchforusers'),

    path('<int:pk>/', views.UsersAccountsCLass.as_view(), name='usersaccounts'),
    path('<int:pk>/acc_vid/', views.UserAccountsVideos.as_view(), name='usersaccvid'),
    path('<int:pk>/users_post_view/', views.UsersAccountsPostView.as_view(), name='userspostview'),

    path('like_post/', views.Post_Liked, name='liked_Post'),
    path('user_like_post/', views.User_Post_Liked, name='user_liked_Post'),
    path('user_explore_like_post/', views.User_Explore_Post_Liked, name='user_explore_liked_Post'),
    path('user_stream_home_like_post/<int:pk>/', views.User_Stream_home_Post_Liked, name='user_stream_home_liked_Post'),

    path('users/edits/', views.UsersEdits.as_view(), name='users_edits'),

    path('change_password/', views.ChangePasswordClass.as_view(success_url='/change_password_done/'),name='change_password'),
    path('change_password_done/', views.ChangePasswordDoneClass.as_view(),name='change_password_done'),

    path('basic_info/', views.BasicInfoClass.as_view(),name='basic_info'),
    path('basic_info_up/<int:pk>/', views.BasicInfoUpdateClass.as_view(),name='basic_info_up'),
    path('basic_info_del/<int:pk>/', views.Basic_InfoDelete,name='basic_info_del'),

    path('<int:pk>/following/', views.followView, name='following'),
    path('<int:pk>/following_video/', views.followVideoView, name='following_video'),

    path('password_reset/',as_views.PasswordResetView.as_view(template_name='password_reset/password_reset.html',form_class=ForgetPasswordForm,success_url='/password_reset_done/'), name='password_reset'),
    path('password_reset_done/',as_views.PasswordResetDoneView.as_view(template_name='password_reset/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',as_views.PasswordResetConfirmView.as_view(template_name='password_reset/password_reset_confirm.html',form_class=PasswordResetSetForm,success_url='/password_reset_complete/'), name='password_reset_confirm'),
    path('password_reset_complete/',as_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'), name='password_reset_complete'),

    path('delete_account/', views.DeleteAccountClass.as_view(), name='delete_account'),
    path('delete_account_func/<int:pk>/', views.DeleteAccount_Func, name='delete_account_func'),

    path('acc/logout/', views.LogOutClass.as_view(), name='logout'),
]