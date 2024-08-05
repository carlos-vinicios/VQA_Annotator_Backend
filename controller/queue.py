from models.annotation import Annotations
from models.configs import DistributionConfig
import threading

class AnnotationQueue:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:  # This is the only difference
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def add_user_to_queue(self, user_email: str):
        config = DistributionConfig.objects().first()

        group_id = config.groups[config.index]
        files = Annotations.objects(group_id__in=[group_id])
        for f in files:
            f.user.append(user_email)
            f.save()

        #atualizando o index
        config.index += 1
        config.save()
    
    def view_distribution(self):
        response = []
        for user, files in self.distribution.items():
            response[user] = {
                "qtd_files": len(files),
                "filenames": files
            }
        
        return response
