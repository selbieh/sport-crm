import django_filters


from Academy_class.models import AcademyClass


class AcademyClassFilter(django_filters.FilterSet):
    class Meta:
        model = AcademyClass
        fields = [
            "instructor_id",
            "gender",
            "is_active",
            "age_group",
            "maximum_capacity",
        ]
