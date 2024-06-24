from fastapi import Depends, Security, Path
from services.router import router
from services.auth import get_current_active_user
from schemas.annotation import Vote, Annotation
from typing import List
from controller.annotations import AnnotationsController

@router.get("/vote/next", response_model=Annotation)
def get_page_to_vote(
    _ = Security(get_current_active_user),
    annotations: AnnotationsController = Depends(AnnotationsController)
):
    page = annotations.get_next_vote_metadata()
    return page

@router.post("/vote/{file_id}")
def save_page_votes(
    votes: List[Vote],
    file_id: str = Path(..., description="The ID of the annotation voted"),
    # _ = Security(get_current_active_user),
    annotations: AnnotationsController = Depends(AnnotationsController),
):
    annotations.save_votes(file_id, votes)
    return "saved"