from services.router import router

from models.annotation import Annotations
from models.configs import DistributionConfig
from models.user import User

users = User.objects()
config = DistributionConfig.objects().first()

group_index = 0
for user in users[1:]:
    group_id = config.groups[group_index]
    files = Annotations.objects(group_id__in=[group_id])
    for f in files:
        try:
            f.user.append(user.email)
            f.save()
        except:
            print("Falha no arquivo:", f.filename)
    group_index += 1

print(group_index)