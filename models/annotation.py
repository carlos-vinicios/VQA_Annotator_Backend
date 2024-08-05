from mongoengine import (
    DynamicDocument, EmbeddedDocument, 
    IntField, StringField, EmbeddedDocumentField,
    ListField, FloatField, EmbeddedDocumentListField,
    BooleanField
)

class PageDimension(EmbeddedDocument):
    width = IntField(required=True)
    height = IntField(required=True)

class Prices(EmbeddedDocument):
    input = FloatField(required=True)
    output = FloatField(required=True)

class Usage(EmbeddedDocument):
    output_tokens = IntField(required=True)
    prompt_tokens = IntField(required=True)
    prices = EmbeddedDocumentField(Prices)
    total = IntField(required=True)

# class EvaluationVote(EmbeddedDocument):
#     relevance = IntField()
#     coherence = IntField()
#     objectivity = IntField()
#     overall = IntField()
#     accuracy = IntField()

# class Vote(EmbeddedDocument):
#     question = EmbeddedDocumentField(EvaluationVote, required=True)
#     answer = EmbeddedDocumentField(EvaluationVote, required=True)
#     model = StringField(required=True)

class Vote(EmbeddedDocument):
    coherent = BooleanField()
    relevant = BooleanField()
    correct = BooleanField()
    model = StringField(required=True)

    meta = {'strict': False}

class QAs(EmbeddedDocument):
    question = StringField(required=True)
    answer = StringField(required=True)
    region = StringField()
    text = StringField()
    answer_bboxes = ListField(ListField(IntField()))
    votes = EmbeddedDocumentListField(Vote)

class Annotations(DynamicDocument):
    filename = StringField(required=True)
    # extracted_filename = StringField(required=True)
    ticker = StringField(required=True)
    model = StringField(required=True)
    page = IntField(required=True)
    page_size = EmbeddedDocumentField(PageDimension, required=True)
    questions = EmbeddedDocumentListField(QAs, required=True)
    cost = EmbeddedDocumentField(Usage, null=True)
    review_counts = IntField()
    user = ListField()
    
    meta = {
        'collection': 'FinalAnnotations'
    }