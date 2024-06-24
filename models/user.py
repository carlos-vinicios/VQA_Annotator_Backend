from mongoengine import (
    Document, EmailField, 
    StringField
)

class User(Document):
    email = EmailField(unique=True, null=True)
    token = StringField(null=True)
    stage = StringField(null=True)

    meta = {
        'collection': 'User'
    }