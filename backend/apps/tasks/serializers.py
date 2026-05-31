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
     #as in model we calculated it buy in here we are showing 
     #it in api section when user access api/task those two will show with task fields
    is_overdue = serializers.BooleanField(read_only=True)
    total_xp = serializers.IntegerField(read_only=True)
    #ModelSerializer only looks for dababase coloum it ignores python method and property
    #so that's why we need to specifiy them

