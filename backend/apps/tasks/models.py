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


    #--------CORE FIELDS----------

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True,default='')

    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TODO
    )


    #-----SCHEDULING-------

    due_date = models.DateTimeField(null=True,blank=True)

    #both below are used for AI so it can learn 
    estimated_minutes = models.PositiveIntegerField(null=True,blank=True)
    actual_minutes = models.PositiveIntegerField(null=True,blank=True)



    #-----GAMIFICATION----------

    xp_reward = models.PositiveIntegerField(default=10)#by default we will give 10xp
    bonus_xp = models.PositiveIntegerField(default=0)


    #------COMPLETION---------

    completed_at = models.DateTimeField(null=True,blank=True)


    #-----RECURRENCE----------- basically here we are make a column to check if the
                                #    task are recurring and if yes then which
            
    is_recurring = models.BooleanField(default=False)#its check if the tasks are recurring or not 

    recurring_pattern = models.JSONField( #it stores recurring rules or specific details 
        #and we use JSON cause we are not showing any relationship here and  
        null=True,
        blank=True
    )

        # ── METADATA ─────────────────────────────────────
    tags = models.JSONField(default=list)
    # Store tags as JSON array: ["work", "urgent", "meeting"]
    # WHY JSON not separate Tag model?
    # Simple tags don't need full relational model
    # If tags need more features later → migrate to model

    notes = models.TextField(blank=True,default='')

    #--------TIMESTAMPS---------

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = 'tasks'

        ordering = ['-created_at']#by doing this we automatically told that whenever you retrive them
                                  #give the newest first
        
        #it creates database indexes on common query combination this make the searching much faster
        indexes = [
            models.Index(fields=['user','status']),
            # "Get all IN_PROGRESS tasks for user 5"

            models.Index(fields=['user','due_date']),
            # "Get all tasks due today for user 5"

            models.Index(fields=['user','priority']),
            # "Get all URGENT tasks for user 5"
        ]


    def __str__(self):
        return f"{self.title} ({self.status})"
    

    def save(self,*args,**kwargs):
         # Calculate XP based on priority
        xp_map = {
            self.Priority.LOW :5,
            self.Priority.MEDIUM :10,
            self.Priority.HIGH : 25,
            self.Priority.URGENT : 35,

        }

        self.xp_reward = xp_map.get(self.priority,10)#It means if priority exist the use that else use 10
        #get give use a callback 

        if self.status == self.Status.COMPLETED and not self.completed_at:
            #it means if tasks is completed and completion time doesn't exists then use current time
            self.completed_at = timezone.now() 

        super().save(*args,**kwargs)#super is used to access the parent class
        # and here we used *args, **kwargs cause we need to accept 
        # tupes and dictionary instruction i don't know more about it 

    
    @property
    def is_overdue(self):
      #"""Check if task is past due date."""
        if self.due_date and self.status != self.Status.COMPLETED:
            return timezone.now()>self.due_date
        return False
    
    @property
    def total_xp(self):
        #"""Total XP this task gives."""
        return self.xp_reward +self.bonus_xp



# Create your models here.

