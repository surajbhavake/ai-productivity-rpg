from rest_framework import serializers
from .models import Task,Category

#Seralizer is a translator which convert django/Python object into JSON
#(class CategorySerializer)here we are creating JSON translator
#ModelSerializer Automatically converts our model fields into seralizer fields
class CategorySerializer(serializers.ModelSerializer):
    #    """
    # Converts Category model ↔ JSON
    
    # ModelSerializer automatically:
    # ├─ Creates fields from model
    # ├─ Handles validation
    # ├─ Handles create/update
    # └─ Saves you 90% of boilerplate code
    # """
    #meta means extra information
    class Meta:
        model = Category#here we are telling use Category model
        #When converting to the JSON it include the below fields
        #why not convert all the fields ,because if we have some secret field
        #we don't we frontend to see it 
        fields=[
            'id',
            'name',
            'color',
            'icon',
            'created_at',

        ]

        #here read_only_fields  user can only see it  he cannot change or send it
        read_only_fields = [
            'id',
            'created_at'
        ]

class TaskSerializer(serializers.ModelSerializer):

    #Used for reading it show full category details like name, color,icon along side
    #task details and we can only read that we cannot change the category fields through task api
    category = CategorySerializer(read_only=True)

    #we used category_id here because in task model we created a link field for them 
    #that was named category_id 
    #it creates link between category and task in database we can write it but it is not required
    category_id = serializers.IntegerField(
        write_only = True,
        required =False,
        allow_null = True,
    )
     # Computed properties from model
     #as in model we calculated it but in here we are showing 
     #it in api section when user access api/task those two will show with task fields
    is_overdue = serializers.BooleanField(read_only=True)
    total_xp = serializers.IntegerField(read_only=True)
    #ModelSerializer only looks for dababase coloum it ignores python method and property
    #so that's why we need to specifiy them

    class Meta:
        model = Task
        fields=[
            'id',
            'title',
            'description',
            'priority',
            'status',
            'category',
            'category_id',
            'due_date',
            'estimated_minutes',
            'actual_minutes',
            'xp_reward',
            'bonus_reward',
            'total_reward',
            'is_overdue',
            'tags',
            'notes',
            'is_recurring',
            'recurrence_pattern',
            'competed_at',
            'created_at',
            'updated_at',
        ]

        read_only_fields=[
            'id',
            'created_at',
            'completed_at',
            'xp_reward',
            'updated_at',
        ]



        #value.strip() removes the empty spaces from start to end
        #

    def validate_title(self,value):
        
        #here we check if the text is empty after removing the spaces
        
        if not value.strip():
            #if user type nothing('') or just typed space(" ")
            #so the condition will become true
            raise serializers.ValidationError(
                "Title cannot be empty or be whitespaces"
            )
        return value.strip()#if text is valid it will return the cleaner version for database
    
    def validate_due_date(self,value):
        
        from django.utils import timezone
        #it check if the user is not typing the old date for due_date
        if value < timezone.now():
            raise serializers.ValidationError(
                "Due date must be in future"
            )
        return value
    

    #it is a cross-field validate mean it can inspect everything and its a multiple field validation
    #attrs means entire set of data 
    def validate(self,attrs):
        #check if user said "yes this task should repeat"
        #and then check if the user failed to provid the pattern e.g.daily, weekly then
        #it will raise the alert
        if attrs.get('is_recurring') and not attrs.get('recurrence_pattern'):
            raise serializers.ValidationError({
                'recurrence_pattern':'Recurring task must have a recurrence pattern'
            })
        return attrs
    

    #after all the procecure what we have mention in serializers the the model will made 
    #e.g. Serializer recives the data from user then it will process it and then create task object from task model then
    #save function will run in the task model and then the database will be updated


