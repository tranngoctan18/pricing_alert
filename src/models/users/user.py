import uuid

from src.models.alerts.alert import Alert
from src.common.database import Database
from src.common.utils import Utils
import src.models.users.errors as UserErrors
import src.models.users.constants as UserConstants


class User:
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User {}".format(self.email)

    @staticmethod
    def is_login_valid(email, password):
        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})
        if user_data is None:
            raise UserErrors.UserNotExistsError("Your user does not exist.")
        if not Utils.check_hashed_password(password, user_data['password']):
            raise UserErrors.IncorrectPasswordError("Your password is wrong.")

        return True

    @staticmethod
    def register_user(email, password):
        user_data = User.from_db_by_email(email)

        if user_data is not None:
            raise UserErrors.UserAlreadyRegisterError("Email is already registered.")
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError("Email is invalid.")

        User(email, Utils.hash_password(password)).save_to_db()
        return True

    def save_to_db(self):
        Database.insert("users", self.json())

    def json(self):
        return {"_id": self._id,
                "email": self.email,
                "password": self.password
                }

    @classmethod
    def from_db_by_email(cls, email):
        user_data = Database.find_one(UserConstants.COLLECTION, {"email": email})

        return cls(**user_data) if user_data is not None else None

    @classmethod
    def from_mongo_by_id(cls, _id):
        post_data = Database.find_one(UserConstants.COLLECTION, query={'_id': _id})
        return cls(**post_data)

    def get_alerts(self):
        return Alert.from_db_by_user_email(self.email)
