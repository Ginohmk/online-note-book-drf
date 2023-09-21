import dataclasses
from . import models

# For jwt
import datetime
import jwt

# setting
from django.conf import settings


# For type checking of model
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from users.models import User

@dataclasses.dataclass
class UserDataClass:
  first_name: str
  last_name: str
  email: str
  password: str = None
  id: int = None

  @classmethod
  def from_instance(cls, user: "User") -> "UserDataClass":
    return cls(
      first_name = user.first_name,
      last_name = user.last_name,
      email = user.email,
      id = user.id
    )


def create_user(user_dc: "UserDataClass") -> "UserDataClass":
  instance = models.User(
    first_name = user_dc.first_name,
    last_name = user_dc.last_name,
    email= user_dc.email
  )

  if user_dc.password is not None:
    instance.set_password(user_dc.password)

  instance.save()

  return UserDataClass.from_instance(instance)


def check_user_email(email: str) -> 'User':
  user_email = models.User.objects.filter(email = email).first()

  return user_email


def create_token(user_id: int ) -> str:
  payload = dict(
    id = user_id,
    exp = str(datetime.datetime.utcnow() + datetime.timedelta(hours = 24)),
    iot = str(datetime.datetime.utcnow())
  )

  token = jwt.encode(payload, settings.JWT_KEY, algorithm="HS256")

  return token





