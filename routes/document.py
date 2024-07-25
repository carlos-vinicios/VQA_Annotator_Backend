from fastapi import Depends, Security, HTTPException, Path
from fastapi.responses import FileResponse
from services.router import router
from services.auth import get_current_active_user
from schemas.annotation import VisualizationAnnotation, Annotation
from controller.annotations import AnnotationsController

@router.get("/document/{file_id}", response_class=FileResponse)
def get_page_to_vote(
    # _ = Security(get_current_active_user),
    annotation: AnnotationsController = Depends(AnnotationsController),
    file_id: str = Path(..., description="The ID of the PDF file to download")
):
    try:
        file_path = annotation.get_report_path(file_id)
        return FileResponse(file_path, media_type='application/pdf', filename="document.pdf")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="PDF file not found")
    
@router.get("/document/visualization/{filename}/{gen_model}", response_model=Annotation)
def get_page_to_vote(
    user = Security(get_current_active_user),
    annotations: AnnotationsController = Depends(AnnotationsController),
    filename: str = Path(..., description="Name of the file to visualization"),
    gen_model: str = Path(..., description="Name of the QA generation model")
):
    page = annotations.get_annotation(filename, gen_model, user)
    return page