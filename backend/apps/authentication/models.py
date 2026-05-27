from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.


class User(AbstractUser):
    """
    Custom User model extending Django's built-in User.
    
    WHY AbstractUser instead of AbstractBaseUser?
    AbstractUser: Keeps username, email, password, is_staff
                  We just ADD our custom fields
                  Easier and faster
                  
    AbstractBaseUser: Build from scratch
                      More control
                      More complex
                      Use for: Very custom auth systems
    """
       
    #------PROFILE FIELDS------

    avatar = models.ImageField(
        upload_to='avatars/',
        null= True,
        black=True
    )

    bio = models.TextField(
        max_length=500,
        blank=True,
        default=''

    )

    #------ GAMIFICATION FIELDS--------

    xp = models.PositiveIntegerField(
        default=0
    )

    level = models.PositiveIntegerField(default=1)
    
    total_xp_earned = models.PositiveIntegerField(default=0)


    #-------- STREAK FIELDS----------

    current_streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    last_activity_date =models.DateField(null=True,blank = True)

    #--------SETTING FIELDS ----------

    timezone = models.CharField(
        max_length=50,
        default="UTC"
    )

    notification_enabled = models.BooleanField(default=True)

    updated_at =  models.DateTimeField(auto_now=True)

