from mongoengine import (
    DynamicDocument, EmbeddedDocument, 
    IntField, StringField, EmbeddedDocumentField,
    ListField, FloatField, EmbeddedDocumentListField
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

class EvaluationVote(EmbeddedDocument):
    coherence = IntField(required=True)
    objectivity = IntField(required=True)
    overall = IntField(required=True)
    accuracy = IntField()

class Vote(EmbeddedDocument):
    overall = IntField(required=True)
    question = EmbeddedDocumentField(EvaluationVote, required=True)
    answer = EmbeddedDocumentField(EvaluationVote, required=True)
    model = StringField(required=True)

class QAs(EmbeddedDocument):
    question = StringField(required=True)
    answer = StringField(required=True)
    region = StringField()
    text = StringField()
    answer_bboxes = ListField(ListField(IntField()), required=True)
    votes = EmbeddedDocumentListField(Vote, required=True)

class Annotations(DynamicDocument):
    filename = StringField(required=True)
    extracted_filename = StringField(required=True)
    ticker = StringField(required=True)
    model = StringField(required=True)
    page = IntField(required=True)
    page_size = EmbeddedDocumentField(PageDimension, required=True)
    questions = EmbeddedDocumentListField(QAs, required=True)
    cost = EmbeddedDocumentField(Usage, null=True)
    review_counts = IntField()
    
    meta = {
        'collection': 'Annotations1_1'
    }