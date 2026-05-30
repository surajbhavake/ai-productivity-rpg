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



    class Meta : 
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        
    def __str__(self):
        return f"{self.username}(Level {self.level})"
    

    #--------PROPERTIES(COMPUTABLE FIELDS)---------

    @property  #using function as a variable
    def xp_to_next_level(self):
        return self.level * 100
    
    @property
    def xp_progress_percentage(self):
        if self.xp_to_next_level == 0:
            return 100
        return int((self.xp/self.xp_to_next_level)*100)
    @property
    def rank_title(self):
        ranks = {
            range(1,5):"Apprentice",
            range(5,10):"Journeyman",
            range(10,20):"Expert",
            range(20,30):"Master",
            range(30,50):"Grandmaster",
            range(50,101):"Legend",
        
        }
        for  level_range,title in ranks.items():
            if self.level in level_range:
                return title
            
        return "Transendent"
    
    #------METHODS(BUSINESS LOGIC)-------(adding ,removing or updating dataing the database)

    def add_xp(self,amount,source="task"):
        self.xp += amount
        self.total_xp_earned += amount

        leveled_up = False
        new_level = self.level

        while self.xp >= self.xp_to_next_level:
            self.xp -= self.xp_to_next_level
            self.level += 1
            leveled_up = True
            new_level = self.level

        self.save()

        return{
            'leveled_up':leveled_up,
            'new_level':new_level,
            'current_xp':self.xp,
            'xp_added':amount
        }
    
    def update_streak(self):

        today = timezone.now().date()

        if self.last_activity_date is None:
            self.current_streak = 1

        elif self.last_activity_date == today :
            pass

        elif (today - self.last_activity_date).days == 1:
            self.current_streak +=1
        else :
            self.current_streak = 1

        #longest streak

        if self.current_streak > self.longest_streak:
            self.longest_streak = self.current_streak

        self.last_activity_date = today
        self.save()

    






