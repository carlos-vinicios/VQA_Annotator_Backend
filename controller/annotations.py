import os
from models.annotation import Annotations, Vote

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

    def overall_rate(self, question, vote):
        q_weight = 1
        a_weight = 1 if len(question.answer_bboxes) > 0 else 0.5
        overall_q = sum([v * q_weight for v in vote['question'].values()]) / len(vote['question'].values())
        overall_a = sum([v * a_weight for v in vote['answer'].values()]) / len(vote['answer'].values())

        return round(overall_q, 2), round(overall_a, 2)

    def get_next_vote_metadata(self):
        ann = Annotations.objects(review_counts__lte=3).first()
        ann = ann.to_mongo().to_dict()
        ann["file_id"] = str(ann.pop("_id"))
        for qa_ann in ann["questions"]:
            for bbox in qa_ann["answer_bboxes"]:
                bbox[0] = bbox[0] / ann["page_size"]["width"]
                bbox[2] = bbox[2] / ann["page_size"]["width"]
                bbox[1] = bbox[1] / ann["page_size"]["height"]
                bbox[3] = bbox[3] / ann["page_size"]["height"]
        new_width, new_height = self.resize_proportionally(
            ann["page_size"]["width"], ann["page_size"]["height"], 1400
        )
        ann["page_size"]["width"], ann["page_size"]["height"] = new_width, new_height
        return ann
    
    def get_report_path(self, file_id):
        annotation = Annotations.objects.get(id=file_id)
        return os.path.join(
            BACKEND_ENV.REPORTS_PATH, 
            annotation.ticker, 
            annotation.filename
        )

    def save_votes(self, file_id, votes):
        annotation = Annotations.objects.get(id=file_id)

        for vote, question in zip(votes, annotation.questions):
            final_vote = vote.model_dump()
            del final_vote['question']['accuracy'] #removendo campo padrão do Pydantic
            del final_vote['question']['overall'] #removendo campo padrão do Pydantic
            del final_vote['answer']['overall'] #removendo campo padrão do Pydantic
            
            overall_q, overall_a = self.overall_rate(question, final_vote)
            final_vote['question']['overall'] = overall_q
            final_vote['answer']['overall'] = overall_a
            
            question.votes.append(Vote(**final_vote))
        annotation.review_counts += 1
        annotation.save()
