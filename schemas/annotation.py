from pydantic import BaseModel
from typing import List, Optional


class PageDimension(BaseModel):
    width: int
    height: int


class Usage(BaseModel):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int


class QuestionVote(BaseModel):
    coherence: int
    objectivity: int
    relevance: int
    overall: Optional[int] = 1


class AnswerVote(BaseModel):
    accuracy: int = 1
    overall: Optional[int] = 1

# class Vote(BaseModel):
#   question : QuestionVote
#   answer   : AnswerVote
#   model    : str


class Vote(BaseModel):
    coherent: bool
    relevant: bool
    correct: bool
    model: str


class QAs(BaseModel):
    question: str
    answer: str
    answer_bboxes: List[List[float]]


class VisualizationAnnotation(BaseModel):
    filename: str


class Annotation(BaseModel):
    file_id: Optional[str] = ''
    filename: str
    ticker: str
    model: str
    page: int
    page_size: PageDimension
    questions: List[QAs]
