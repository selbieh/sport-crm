import base64
import random
import string
import uuid

from django.core.files.base import ContentFile
from rest_framework import serializers


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


class Base64ImageField(serializers.FileField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            img_form, img_str = data.split(";base64,")
            ext = img_form.split("/")[-1]
            unique_id = uuid.uuid4()
            image = ContentFile(
                base64.b64decode(img_str), name=f"{unique_id.urn[9:]}.{ext}"
            )

            return super(Base64ImageField, self).to_internal_value(image)
        return super(Base64ImageField, self).to_internal_value(data)