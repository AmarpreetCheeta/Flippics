from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserBaseManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must there username.')
        if not username:
            raise ValueError('Users must there email.')
        
        user = self.model(
            email = self.normalize_email(email),
            username = username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserAccounts(AbstractBaseUser):
    username = models.CharField(verbose_name='Username',max_length=200,unique=True)
    first_name = models.CharField(verbose_name='Full Name',max_length=300)
    email = models.EmailField(verbose_name='Email Address',unique=True)
    phone = models.CharField(verbose_name='Phone',max_length=13)
    image = models.ImageField(verbose_name='Profile Image',upload_to='profile/%y')
    date_joined = models.DateTimeField(verbose_name='Date Joined',auto_now=True)
    last_login = models.DateTimeField(verbose_name='Last Login',auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserBaseManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return self.username

    def has_perm(self, perms, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True



# class ProfileImageModel(models.Model):
#     user = models.ForeignKey(UserAccounts, on_delete=models.CASCADE)
#     image = models.ImageField(verbose_name='Profile Image',upload_to='profile/%y')
#     date_upload = models.DateTimeField(verbose_name='Upload Date',auto_now_add=True)



POST_TYPES = (
    ('Photos','Photos'),
    ('Videos','Videos'),
)

class PostUploadModel(models.Model):
    user = models.ForeignKey(UserAccounts, on_delete=models.CASCADE)
    caption = models.TextField(verbose_name='Caption', max_length=100)
    post = models.FileField(verbose_name='Post', upload_to='upload_post/%y')
    post_type = models.CharField(verbose_name='Post Type',choices=POST_TYPES, max_length=20)
    liked = models.ManyToManyField(UserAccounts, default=None, blank=True, related_name='liked')
    saved = models.ManyToManyField(UserAccounts, default=None, blank=True, related_name='saved')
    date_post = models.DateTimeField(verbose_name='Date Post',auto_now_add=True)

    def __str__(self):
        return str(self.post)

    @property
    def num_like(self):
        return self.liked.all().count()


LIKED_POST = (
    ('Like','Like'),
    ('Unlike','Unlike'),
)

class LikeModel(models.Model):
    user = models.ForeignKey(UserAccounts, on_delete=models.CASCADE)
    post = models.ForeignKey(PostUploadModel, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKED_POST, max_length=20, default='Like')


class CommentsModels(models.Model):
    user = models.ForeignKey(UserAccounts, on_delete=models.CASCADE)
    post = models.ForeignKey(PostUploadModel, on_delete=models.CASCADE)
    body = models.TextField()


class BasicInfoModel(models.Model):
    user = models.ForeignKey(UserAccounts, on_delete=models.CASCADE)
    web_link = models.CharField(max_length=2000)
    bio = models.TextField()


class FollowsModel(models.Model):
    follower = models.ForeignKey(UserAccounts, on_delete=models.CASCADE, null=True,related_name='follower')
    following = models.ForeignKey(UserAccounts, on_delete=models.CASCADE, null=True,related_name='following')    


class StreamModel(models.Model):
    following = models.ForeignKey(UserAccounts, on_delete=models.CASCADE,related_name='stream_following')
    user = models.ForeignKey(UserAccounts, on_delete=models.CASCADE)