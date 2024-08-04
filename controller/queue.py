from models.annotation import Annotations, Vote
from pymongo import MongoClient
import pandas as pd

class AnnotationQueue:
    
    def __init__(self, 
                 connection_string,
                 files_per_user=40, qtd_cross_files=10, 
                 group_size=3, db_name="DOC_VQA", 
                 collection_name="configs"
                ) -> None:
        self.files = self._load_files()
        self.files_per_user = files_per_user
        self.qtd_cross_files = qtd_cross_files
        self.group_size = group_size 
        
        # Conexão com o MongoDB
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
            
        # Carregar estado do MongoDB
        self._load_state()
    
    def _load_files(self):
        new_dataframe = []
        files = Annotations.objects().only("id", "model")
        df_files = pd.DataFrame([f.to_mongo() for f in files])
        
        model_count = 0
        for i, group in df_files.groupby("model"):
            group = group.sample(frac=1).reset_index(drop=True)
            for j, row in group.iterrows():
                if model_count == 0:
                    new_dataframe.append(row.to_dict())
                else:
                    new_dataframe.insert(j+model_count*j, row.to_dict())
            model_count += 1

        new_dataframe = pd.DataFrame(new_dataframe)
        return new_dataframe["_id"].values

    def _load_state(self):
        state = self.collection.find_one({"tipo": "state"})
        if state:
            self.users = state["users"]
            self.distribution = state["distribution"]
            self.index = state["index"]
        else:
            self.users = []
            self.distribution = {}
            self.index = 0
    
    def _save_state(self):
        state = {
            "type": "state",
            "user": self.users,
            "distribution": self.distribution,
            "index": self.index
        }
        self.collection.update_one(
            {"type": "state"}, 
            {"$set": state}, 
            upsert=True
        )
    
    def add_user_to_queue(self, user_email: str):
        if user_email in self.users:
            raise ValueError(f"{user_email} já está na lista de users.")
        
        self.users.append(user_email)
        self.distribution[user_email] = []
        self._share_file()
        self._save_state()

        for file in self.distribution[user_email]:
            file = Annotations.objects(id=file).first()
            file.user = user_email
            file.save()
    
    def _share_file(self):
        """Cria a distribuição de arquivos para cada usuário da lista"""
        while self.index < len(self.files):
            qtd_groups = len(self.users) // (self.group_size + 1)
            start = qtd_groups * self.group_size
            formed_group = self.users[start : start + self.group_size]
            last_user = None
            for user in formed_group:
                if len(self.distribution[user]) < self.files_per_user:
                    if last_user is not None:
                        #adicionando os arquivos únicos
                        self.distribution[user].extend(self.files[self.index:self.index + (self.files_per_user - self.qtd_cross_files)])
                        self.distribution[user].extend(self.distribution[last_user][-5:]) #copiando os arquivos iguais
                    else:
                        #adicionando os primeiros 20 arquivos aleatórios do grupo
                        self.distribution[user].extend(self.files[self.index:self.index + self.files_per_user])
                    
                    if last_user is not None:
                        self.index += self.files_per_user - self.qtd_cross_files
                    else:
                        self.index += self.files_per_user
                last_user = user                
                
            self._save_state()
            # Verificar se todas as users no grupo atual atingiram o limite de arquivos
            if all(len(self.distribution[p]) >= self.files_per_user for p in formed_group):
                break
    
    def view_distribution(self):
        response = []
        for user, files in self.distribution.items():
            response[user] = {
                "qtd_files": len(files),
                "filenames": files
            }
        
        return response
