from mongoengine import (
    Document, IntField, 
    ListField, DynamicField
)

class DistributionConfig(Document):
    distribution = DynamicField()
    groups = ListField()
    index = IntField()

    meta = {
        'collection': 'Configs'
    }