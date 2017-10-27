from passlib.hash import pbkdf2_sha512
import re

class Utils():


    @staticmethod
    def hash_password(password):
        """
        Hases a password using pbkdf2_sha512
        :param password: The sha512 password from login/register form
        :return: a sha512 > pbkdf2_sha512 encrypted password
        """
        return pbkdf2_sha512.encrypt(password)



    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        Checks that the password user sent matches that of the database.
        The database password is encrypted more than the user's password at this stage.
        :param password: sha512-hashed password
        :param hashed_password: pbkdf2_sha512 encrypted password
        :return: True if password matches, False otherwise
        """
        return pbkdf2_sha512.verify(password, hashed_password)


    @staticmethod
    def email_is_valid(email):
        email_address_matcher = re.compile(r'^[\w\.]+@[\w\.]+$') # hello.

        return True if email_address_matcher.match(email) else False