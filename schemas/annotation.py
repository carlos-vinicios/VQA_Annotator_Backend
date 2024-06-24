from pydantic import BaseModel
from typing import List, Optional

class PageDimension(BaseModel):
    width  : int
    height : int

class Usage(BaseModel):
    completion_tokens : int
    prompt_tokens     : int
    total_tokens      : int

class EvaluationVote(BaseModel):
  coherence   : int
  objectivity : int
  accuracy    : Optional[int] = 0
  overall     : Optional[int] = 0

class Vote(BaseModel):
  overall  : int
  question : EvaluationVote
  answer   : EvaluationVote
  model    : str

class QAs(BaseModel):
    question      : str
    answer        : str
    answer_bboxes : List[List[float]]

class Annotation(BaseModel):
    file_id             : Optional[str] = ''
    filename            : str
    extracted_filename  : str
    ticker              : str
    model               : str
    page                : int
    page_size           : PageDimension
    questions           : List[QAs]