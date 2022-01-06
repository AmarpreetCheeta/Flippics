from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from flip.models import *
from flip.forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.views import *
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def Registration(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                messages.success(request, 'Your Flippics account has been created.')
                form.save()
                return redirect('registration')
        else:
            form = RegistrationForm()
        return render(request, 'signup.html',{'form':form})
    else:
        return redirect('home')


def Authentications(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationUserForm(request=request, data=request.POST)
            if form.is_valid():
                usr = form.cleaned_data['username']
                pas = form.cleaned_data['password']
                log = authenticate(username=usr,password=pas)
                if log is not None:
                    login(request, log)
                    return redirect('home')
        else:
            form = AuthenticationUserForm()
        return render(request, 'login.html',{'form':form})
    else:
        return redirect('home')



class Home(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            user = UserAccounts.objects.filter()
            users_explore_post = PostUploadModel.objects.filter()
            users_explore_post_ph = PostUploadModel.objects.filter(post_type='Photos')
            users_explore_post_vd = PostUploadModel.objects.filter(post_type='Videos')
            context = {'users':user,'users_explore_post_ph':users_explore_post_ph,
            'users_explore_post_vd':users_explore_post_vd,'users_explore_post':users_explore_post}
            return render(request, 'flip/home.html', context)
        else:
            return redirect('authentications')


class Explore(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            user = UserAccounts.objects.filter()
            user_info = BasicInfoModel.objects.filter()
            context = {'users':user,'user_info':user_info}
            return render(request, 'flip/explore.html', context)
        else:
            return redirect('authentications')


class ExplorePostView(TemplateView):
    def get(self, request, pk):
        if request.user.is_authenticated:
            post_data1 = PostUploadModel.objects.filter(pk=pk)
            post_for_comment = PostUploadModel.objects.get(pk=pk)
            current_user = request.user
            comment_form = CommentsForm()
            comment_data = CommentsModels.objects.filter(post=post_for_comment)
            comment_data1 = CommentsModels.objects.filter(user=request.user)
            com_counts = comment_data.count() 
            upload_data_ph = PostUploadModel.objects.filter(pk=pk, post_type='Photos')
            upload_data_vd = PostUploadModel.objects.filter(pk=pk, post_type='Videos')  
            context = {'post_data1':post_data1,'upload_data_ph':upload_data_ph,'comment_data':comment_data,
            'upload_data_vd':upload_data_vd,'current_user':current_user,'comment_form':comment_form,
            'com_counts':com_counts,'comment_data1':comment_data1}
            return render(request, 'flip/explore_post_view.html', context)
        else:
            return redirect('authentications')

    def post(self, request, pk):
        post_for_comment = PostUploadModel.objects.get(pk=pk)
        comment_form = CommentsForm(request.POST)
        if comment_form.is_valid():
            user = request.user
            post = post_for_comment
            bdy = comment_form.cleaned_data['body']
            reg = CommentsModels(user=user, post=post, body=bdy)
            reg.save()
            return redirect('explore_post_view', post_for_comment.id)


class Upload(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            user = UserAccounts.objects.filter()
            upload_form = PostUploadForm(data=request.POST, files=request.FILES)
            context = { 'upload_form':upload_form,'user':user}
            return render(request, 'flip/upload.html', context)
        else:
            return redirect('authentications')

    def post(self, request):
        upload_form = PostUploadForm(data=request.POST, files=request.FILES)
        if upload_form.is_valid():
            usr = request.user
            cap = upload_form.cleaned_data['caption']
            pos = upload_form.cleaned_data['post']
            pty = upload_form.cleaned_data['post_type']
            upload = PostUploadModel(user=usr,caption=cap,post=pos,post_type=pty)
            messages.success(request, 'Your post has uploaded successfully.')
            upload.save()
            return redirect('Upload')



class Like(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            user = UserAccounts.objects.filter()
            follow_data_notify = StreamModel.objects.filter(following=request.user)
            context = {'user':user,'follow_data_notify':follow_data_notify}
            return render(request, 'flip/like.html', context)
        else:
            return redirect('authentications')


class AccountsCLass(TemplateView):
    def get(self, request, pk):
        if request.user.is_authenticated:
            counts_posts_ph = 0
            counts_posts_vd = 0
            counts_posts_sv = 0
            users = UserAccounts.objects.get(pk=pk)
            user = UserAccounts.objects.filter(pk=pk)
            upload_data_ph = PostUploadModel.objects.filter(user=request.user, post_type='Photos')
            upload_data_vd = PostUploadModel.objects.filter(user=request.user, post_type='Videos')
            counts_posts_ph = upload_data_ph.count() 
            counts_posts_vd = upload_data_vd.count()
            bio_data = BasicInfoModel.objects.filter(user=request.user)
            follow_status2 = FollowsModel.objects.filter(following=users).count()
            follow_status3 = FollowsModel.objects.filter(follower=users).count()
            context = {'upload_data_ph':upload_data_ph,'user':user,'bio_data':bio_data,
            'counts_posts_sv':counts_posts_sv,'counts_posts_ph':counts_posts_ph,'counts_posts_vd':counts_posts_vd,
            'follow_status2':follow_status2,'follow_status3':follow_status3}
            return render(request, 'flip/account.html', context)
        else:
            return redirect('authentications')


class AccountUserPost(TemplateView):
    def get(self, request, pk):
        if request.user.is_authenticated:
            user = UserAccounts.objects.filter()
            post_for_comments = PostUploadModel.objects.get(pk=pk)
            current_user = request.user
            comment_form = CommentsForm()
            comment_data = CommentsModels.objects.filter(post=post_for_comments)
            com_counts = comment_data.count() 
            post_data1 = PostUploadModel.objects.filter(pk=pk)
            upload_data_ph = PostUploadModel.objects.filter(pk=pk, post_type='Photos')
            upload_data_vd = PostUploadModel.objects.filter(pk=pk, post_type='Videos')
            context = {'user':user,'upload_data_ph':upload_data_ph,'current_user':current_user,'comment_form':comment_form,
            'upload_data_vd':upload_data_vd,'post_data1':post_data1,'comment_data':comment_data,
            'com_counts':com_counts}
            return render(request, 'flip/account_user_post.html',context)
        else:
            return redirect('authentications')

    def post(self, request, pk):
        post_for_comments = PostUploadModel.objects.get(pk=pk)
        comment_form = CommentsForm(request.POST)
        if comment_form.is_valid():
            user = request.user
            post = post_for_comments
            bdy = comment_form.cleaned_data['body']
            reg = CommentsModels(user=user, post=post, body=bdy)
            reg.save()
            return redirect('accounts_user_post', post_for_comments.id)


class UserPostEditing(TemplateView):
    def get(self, request, pk):
        if request.user.is_authenticated:
            upload_data_ph = PostUploadModel.objects.filter(pk=pk, post_type='Photos')
            upload_data_vd = PostUploadModel.objects.filter(pk=pk, post_type='Videos')
            post_data = PostUploadModel.objects.get(pk=pk)
            post_form = PostUploadForm(instance=post_data)
            context = {'upload_form':post_form,'upload_data_ph':upload_data_ph,'upload_data_vd':upload_data_vd}
            return render(request, 'flip/user_post_edit.html', context)
        else:
            return redirect('authentications')

    def post(self, request, pk):
        post_data = PostUploadModel.objects.get(pk=pk)
        post_form = PostUploadForm(data=request.POST,files=request.FILES,instance=post_data)
        if post_form.is_valid():
            post_form.save()
            messages.success(request, 'Your post is edited successfully.')
            return redirect('user_post_editing', post_data.pk)


def DeleteUserPOST(request, pk):
    if request.method == 'POST':
        post_data = PostUploadModel.objects.get(pk=pk)
        post_data.delete()
        return redirect('accounts',request.user.id)


# Users Accounts :

class UsersAccountsCLass(TemplateView):
    def get(self, request, pk):
        if request.user.is_authenticated:
            count_post_ph = 0
            count_post_vd = 0
            us_req = request.user
            user = UserAccounts.objects.filter(pk=pk)
            users = UserAccounts.objects.get(pk=pk)
            upload_data = PostUploadModel.objects.filter(pk=pk)
            bio_users_data = BasicInfoModel.objects.filter(user=pk)
            current_user = BasicInfoModel.objects.filter(user=request.user)
            upload_data_ph = PostUploadModel.objects.filter(user=pk, post_type='Photos')
            upload_data_vd = PostUploadModel.objects.filter(user=pk, post_type='Videos')
            count_post_ph = upload_data_ph.count() 
            count_post_vd = upload_data_vd.count()
            follow_status1 = FollowsModel.objects.filter(follower=us_req,following=users)
            follow_status2 = FollowsModel.objects.filter(following=users).count()
            follow_status3 = FollowsModel.objects.filter(follower=users).count()
            context = {'user':user,'upload_data':upload_data,'upload_data_ph':upload_data_ph,
            'count_post_ph':count_post_ph,'count_post_vd':count_post_vd,'bio_users_data':bio_users_data,
            'current_user':current_user,'follow_status1':follow_status1,'follow_status2':follow_status2,
            'follow_status3':follow_status3}
            return render(request, 'flip/users_accounts.html', context)
        else:
            return redirect('authentications')



class UserAccountsVideos(TemplateView):
    def get(self, request, pk):
        if request.user.is_authenticated:
            count_post_ph = 0
            count_post_vd = 0
            us_req = request.user
            user = UserAccounts.objects.filter(pk=pk)
            users = UserAccounts.objects.get(pk=pk)
            upload_data = PostUploadModel.objects.filter(pk=pk)
            bio_users_data = BasicInfoModel.objects.filter(user=pk)
            upload_data_ph = PostUploadModel.objects.filter(user=pk, post_type='Photos')
            upload_data_vd = PostUploadModel.objects.filter(user=pk, post_type='Videos')
            count_post_ph = upload_data_ph.count() 
            count_post_vd = upload_data_vd.count()
            follow_status1 = FollowsModel.objects.filter(follower=us_req,following=users)
            follow_status2 = FollowsModel.objects.filter(following=users).count()
            follow_status3 = FollowsModel.objects.filter(follower=users).count()
            context = {'user':user,'upload_data':upload_data,'upload_data_vd':upload_data_vd,
            'count_post_ph':count_post_ph,'count_post_vd':count_post_vd,'bio_users_data':bio_users_data,
            'follow_status1':follow_status1,'follow_status2':follow_status2,'follow_status3':follow_status3}
            return render(request, 'flip/users_accounts_video.html', context)
        else:
            return redirect('authentications')


class UsersAccountsPostView(TemplateView):
    def get(self, request, pk):
        if request.user.is_authenticated:
            user = UserAccounts.objects.filter(pk=pk)
            post_comment_id = PostUploadModel.objects.get(pk=pk)
            comment_form = CommentsForm()
            comment_data = CommentsModels.objects.filter(post=post_comment_id)
            current_user = request.user
            com_counts = comment_data.count() 
            post_data1 = PostUploadModel.objects.filter(pk=pk)
            upload_data_ph = PostUploadModel.objects.filter(pk=pk, post_type='Photos')
            upload_data_vd = PostUploadModel.objects.filter(pk=pk, post_type='Videos')
            context = {'users':user,'upload_data_ph':upload_data_ph,'upload_data_vd':upload_data_vd,'post_data1':post_data1,
            'current_user':current_user,'comment_form':comment_form, 'comment_data':comment_data,'com_counts':com_counts}
            return render(request, 'flip/users_accounts_post_view.html', context)
        else:
            return redirect('authentications')

    def post(self, request, pk):
        post_comment_id = PostUploadModel.objects.get(pk=pk)
        comment_form = CommentsForm(request.POST)
        if comment_form.is_valid():
            user = request.user
            post = post_comment_id
            bdy = comment_form.cleaned_data['body']
            reg = CommentsModels(user=user,post=post,body=bdy)
            reg.save()
            return redirect('userspostview', post_comment_id.id)

# End Users Accounts 

def SearchForUserCLass(request):
    if request.method == 'POST':
        search_name = request.POST.get('search_users')
        search_data = UserAccounts.objects.filter(username__icontains=search_name)
        context = {'search_data':search_data}
    return render(request, 'flip/search_for_users.html', context)   
            

class Videos(TemplateView):
    def get(self, request, pk):
        if request.user.is_authenticated:
            user = UserAccounts.objects.filter(pk=pk)
            users = UserAccounts.objects.get(pk=pk)
            upload_data_ph = PostUploadModel.objects.filter(user=request.user, post_type='Photos')
            upload_data_vd = PostUploadModel.objects.filter(user=request.user, post_type='Videos')
            counts_posts = upload_data_ph.count() + upload_data_vd.count()
            bio_data = BasicInfoModel.objects.filter(user=request.user)
            counts_posts_ph = upload_data_ph.count() 
            counts_posts_vd = upload_data_vd.count()
            follow_status2 = FollowsModel.objects.filter(following=users).count()
            follow_status3 = FollowsModel.objects.filter(follower=users).count()
            context = {'upload_data_vd':upload_data_vd,'user':user,'counts_posts':counts_posts,
            'bio_data':bio_data,'counts_posts_ph':counts_posts_ph,
            'counts_posts_vd':counts_posts_vd,'follow_status2':follow_status2,'follow_status3':follow_status3}
            return render(request, 'flip/videos.html', context)
        else:
            return redirect('authentications')


class UsersEdits(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            bio_data = BasicInfoModel.objects.filter(user=request.user)
            form = UsersEditsForm(instance=request.user)
            context = {'forms':form,'bio_data':bio_data}
            return render(request, 'flip/user_edits.html', context)
        else:
            return redirect('authentications')

    def post(self, request):
        form = UsersEditsForm(data=request.POST,files=request.FILES,instance=request.user)
        if form.is_valid():
            messages.success(request, 'Your data has been changed successfully.')
            form.save()
            return redirect('users_edits')



class BasicInfoClass(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            form = BasicInfoForm()
            context = {'form':form}
            return render(request, 'flip/basic_info.html', context)
        else:
            return redirect('authentications')

    def post(self,request):
        form = BasicInfoForm(request.POST)
        if form.is_valid():
            usr = request.user
            web = form.cleaned_data['web_link']
            wbio = form.cleaned_data['bio']
            reg = BasicInfoModel(user=usr, web_link=web, bio=wbio)
            reg.save()
            return redirect('basic_info_up', reg.pk)

class BasicInfoUpdateClass(TemplateView):
    def get(self, request,pk):
        if request.user.is_authenticated:
            bio_data12 = BasicInfoModel.objects.filter(user=request.user)
            bio_data = BasicInfoModel.objects.get(pk=pk)
            form = BasicInfoForm(instance=bio_data)
            context = {'form':form,'bio_data12':bio_data12}
            return render(request, 'flip/basic_info.html', context)
        else:
            return redirect('authentications')

    def post(self,request,pk):
        bio_data = BasicInfoModel.objects.get(pk=pk)
        form = BasicInfoForm(request.POST, instance=bio_data)
        if form.is_valid():
            form.save()
            return redirect('basic_info_up', bio_data.id)

def Basic_InfoDelete(request, pk):
    if request.method == 'POST':
        bio_data = BasicInfoModel.objects.get(pk=pk)
        bio_data.delete()
        return redirect('basic_info')


class DeleteAccountClass(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'flip/delete_account.html')
        else:
            return redirect('authentications')

        
def DeleteAccount_Func(request, pk):
    if request.method == 'POST':
        user_data = UserAccounts.objects.filter(pk=pk)
        user_data.delete()
        return redirect('authentications')


# Like Buttons:

def Post_Liked(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = PostUploadModel.objects.get(id=post_id)

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)

        like, created = LikeModel.objects.get_or_create(user=user, post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'

    return redirect('accounts_user_post', post_obj.id)


def User_Post_Liked(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = PostUploadModel.objects.get(id=post_id)

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)

        like, created = LikeModel.objects.get_or_create(user=user, post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        
        like.save()
    return redirect('userspostview', post_obj.id)


def User_Explore_Post_Liked(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = PostUploadModel.objects.get(id=post_id)

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)

        like, created = LikeModel.objects.get_or_create(user=user, post_id=post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        
        like.save()
    return redirect('explore_post_view', post_obj.id)

def User_Stream_home_Post_Liked(request, pk):
    user = request.user
    if request.method == 'POST':
        post_obj = PostUploadModel.objects.get(id=pk)

        if user in post_obj.liked.all():
            post_obj.liked.remove(user)
        else:
            post_obj.liked.add(user)

        like, created = LikeModel.objects.get_or_create(user=user, post_id=pk)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        
        like.save()
    return redirect('home')

# End Like Buttons

# Follow Button :

def followView(request, pk):
    if request.method == 'POST':
        user = request.user
        following = UserAccounts.objects.get(pk=pk)

        fol, created = FollowsModel.objects.get_or_create(follower=user, following=following)
                
        if created:
            stream = StreamModel(following=following,user=user).save()
        else:
            fol.delete() 
            StreamModel.objects.get(following=following,user=user).delete()

    return redirect('usersaccounts', following.id)


def followVideoView(request, pk):
    if request.method == 'POST':
        user = request.user
        following = UserAccounts.objects.get(pk=pk)

        fol, created = FollowsModel.objects.get_or_create(follower=user, following=following)
                
        if created:
            stream = StreamModel(following=following,user=user).save()
        else:
            fol.delete() 
            StreamModel.objects.get(following=following,user=user).delete()
        
    return redirect('usersaccvid', following.id)
    
# Follow Button End

class ChangePasswordClass(PasswordChangeView):
    def get(self, request):
        if request.user.is_authenticated:
            bio_data = BasicInfoModel.objects.filter(user=request.user)
            form = ChangePasswordCLassForm(request.POST)
            context = {'form':form,'bio_data':bio_data}
            return render(request, 'flip/change_password.html', context)
        else:
            return redirect('authentications')
            
class ChangePasswordDoneClass(PasswordChangeDoneView):
    def get(self, request):
        if request.user.is_authenticated:     
            return render(request, 'flip/change_password_done.html')
        else:
            return redirect('authentications')


@method_decorator(login_required, name='dispatch')
class LogOutClass(LogoutView):
    next_page = '/accounts/authentication/'
