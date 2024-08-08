import os
from models.annotation import Annotations, Vote
from fastapi import HTTPException

from env import EnvironmentVariables
BACKEND_ENV = EnvironmentVariables()

class AnnotationsController:

    def resize_proportionally(self, original_width: int, original_height: int, new_width: int):
        """
        Calculate the proportional resized dimensions for an image.

        :param original_width: The original width of the image.
        :param original_height: The original height of the image.
        :param new_width: The new width to resize the image to.
        :return: A tuple containing the new width and the new height.
        """
        if original_width <= 0 or original_height <= 0 or new_width <= 0:
            raise ValueError("All dimensions must be greater than zero")

        # Calculate the aspect ratio
        aspect_ratio = original_height / original_width

        # Calculate the new height maintaining the aspect ratio
        new_height = int(new_width * aspect_ratio)

        return new_width, new_height

    def parse_bboxes(self, annotation):
        """Gera as bounding boxes que serão exibidas no front"""
        annotation = annotation.to_mongo().to_dict()
        annotation["file_id"] = str(annotation.pop("_id"))
        
        for qa_annotation in annotation["questions"]:
            for bbox in qa_annotation["answer_bboxes"]:
                bbox[0] = bbox[0] / annotation["page_size"]["width"]
                bbox[2] = bbox[2] / annotation["page_size"]["width"]
                bbox[1] = bbox[1] / annotation["page_size"]["height"]
                bbox[3] = bbox[3] / annotation["page_size"]["height"]
        new_width, new_height = self.resize_proportionally(
            annotation["page_size"]["width"], annotation["page_size"]["height"], 1400
        )
        annotation["page_size"]["width"], annotation["page_size"]["height"] = new_width, new_height
        return annotation

    def list_annotations_metadata(self, user):
        response = []
        anns = Annotations.objects(user__in=[user.email])
        if len(anns) == 0:
            raise HTTPException(
                status_code=404,
                detail="Não foram encontrados arquivos anotados."
            )
        
        for ann in anns:
            annotated = [False] * len(ann.questions)
            for i, question in enumerate(ann.questions):
                for vote in question.votes:
                    if vote.model == user.email:
                        annotated[i] = True
                        break
            
            if all(annotated):
                response.append(self.parse_bboxes(ann))

        return response

    def get_annotation_metadata(self, user):
        response = None
        anns = Annotations.objects(user__in=[user.email])
            
        for ann in anns:
            annotated = [False] * len(ann.questions)
            for i, question in enumerate(ann.questions):
                for vote in question.votes:
                    if vote.model == user.email:
                        annotated[i] = True
                        break
            
            if not all(annotated):
                response = self.parse_bboxes(ann)
                break
        
        if response is None:
            raise HTTPException(
                status_code=404,
                detail="Não foram encontrados mais nenhum arquivo para anotação."
            )

        return response

    def get_annotation(self, file_id, user):
        ann = Annotations.objects(id=file_id, user__in=[user.email]).first()
        if ann is None:
            raise HTTPException(
                status_code=404,
                detail="O arquivo não foi encontrado."
            )
        
        return self.parse_bboxes(ann)
    
    def get_report_path(self, file_id):
        annotation = Annotations.objects.get(id=file_id)
        year = annotation.filename.split("_")[1]
        filename = f"demonstrativo_{year}.pdf"
        return os.path.join(
            BACKEND_ENV.REPORTS_PATH, 
            annotation.ticker, 
            filename
        )

    def save_evaluation(self, file_id, evaluations, user):
        annotation = Annotations.objects.get(id=file_id)

        for evaluation, question in zip(evaluations, annotation.questions):
            final_eval = evaluation.model_dump()
            final_eval["model"] = user.email
            index = -1
            for i, vote in enumerate(question.votes):
                if vote.model == user.email:
                    index = i
                    break
            if index == -1:
                #adiciona uma nova avaliação
                question.votes.append(Vote(**final_eval))
                annotation.review_counts += 1
            else:
                #atualiza uma avaliação realizada
                question.votes[index] = Vote(**final_eval)
        
        annotation.save()
