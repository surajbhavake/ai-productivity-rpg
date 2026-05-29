from django.db import models
from django.conf import settings
from django.utils import timezone


#We use models.Model to create table in User didn't use it because of AbstractUser
class Category(models.Model):
    name = models.CharField(max_length=100)

    color = models.CharField(
        max_length=7,
        default='#6366f1'
    )

    icon =models.CharField(
        max_length=50,
        default='📋'
    )
    #here user(it can be anything)(Django automaticaly created user_id in column) the column for category table to link with User table
    #models.ForeignKey make the link 
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, #its the target model for the foreign key relationship, it points to the user model 
        on_delete = models.CASCADE, #it deletes all the categories of a user when the user is deleted
        related_name='categories' #Forward Lookup: Looking at a dog and asking, "Who is the owner?" (The dog has a collar with a name).
                                  #Reverse Lookup: Looking at the owner and asking, "What dogs do you have? 
    )

    created_at = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        db_table = 'categories'
        verbose_name_plural ='categories'
        unique_together = ['name', 'user'] # This makes Unique category names per user

    def __str__(self):
        return f"{self.icon} {self.name}"
    

#------TASK MODEL--------


class Task(models.Model):

    #------PRIORITY CHOICES------

    #modesl.Model created Tables and modesl.TextChoices created DropDown for table
    #like inside a table column we can use this dropdown
    class Priority(models.TextChoices):
        LOW = 'low','Low'
        MEDIUM = 'medium','Medium'
        HIGH = 'high','High'
        URGENT = 'urgent','Urgent'

    
    class Status(models.TextChoices):
        TODO = 'todo','To Do'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        ARCHIVED = 'archived', 'Archived'

     

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,#here if we delete the user the task also gets deleted
        related_name='tasks',
        db_index=True
    )

    category = models.ForeignKey(
        Category,#here we our linked target was Category 
        on_delete=models.SET_NULL,#here if we delete the category it doesn't delete the task
        null=True,#mean we can allow the database to store task without category
        blank=True,# mean we can allow the form to save the task without category
        related_name='tasks'

    )
# Create your models here.
