from fastapi import Depends, Security, Path
from services.router import router
from services.auth import get_current_active_user
from schemas.annotation import Vote, Annotation
from typing import List
from controller.annotations import AnnotationsController

@router.get("/evaluation/list", response_model=List[Annotation])
def get_pages_to_evaluate(
    user = Security(get_current_active_user),
    annotations: AnnotationsController = Depends(AnnotationsController)
):
    page = annotations.list_annotations_metadata(user)
    return page

@router.get("/evaluation/next", response_model=Annotation)
def get_page_to_evaluate(
    user = Security(get_current_active_user),
    annotations: AnnotationsController = Depends(AnnotationsController)
):
    page = annotations.get_annotation_metadata(user)
    return page

@router.post("/evaluation/{file_id}")
def save_page_evaluation(
    votes: List[Vote],
    file_id: str = Path(..., description="The ID of the annotation voted"),
    _ = Security(get_current_active_user),
    annotations: AnnotationsController = Depends(AnnotationsController),
):
    annotations.save_evaluation(file_id, votes)
    return "saved"