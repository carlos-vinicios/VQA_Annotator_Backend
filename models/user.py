from mongoengine import (
    Document, EmailField, 
    StringField
)

class User(Document):
    email = EmailField(unique=True, null=True)
    name = StringField(null=True)
    age = StringField(null=True)
    gender = StringField(null=True)
    education_level = StringField(null=True)
    current_occupation = StringField(null=True)
    occupation_description = StringField(null=True)
    token = StringField(null=True)

    stage = StringField(null=True)

    meta = {
        'collection': 'User'
    }