from mongoengine import connect
from env import EnvironmentVariables
BACKEND_ENV = EnvironmentVariables()

connect(host=BACKEND_ENV.MONGODB_URI)