import random
import string


def upload_avatar(instance, filename):
    return "users/{0}/{1}".format(instance.id, filename)


MALE = "Male"
FEMALE = "Female"

GENDER_CHOICES = [
    (MALE, "Male"),
    (FEMALE, "Female"),
]

SYSTEM_ADMIN = "System_admin"
CUSTOMER = "Customer"
ACCOUNTANT = "Accountant"

ROLE_CHOICES = [
    (SYSTEM_ADMIN, "System_admin"),
    (CUSTOMER, "Customer"),
    (ACCOUNTANT, "Accountant"),
]


def generate_random_password():
    password_length = 8
    password = "".join(
        random.choices(string.ascii_letters + string.digits, k=password_length)
    )
    return password
