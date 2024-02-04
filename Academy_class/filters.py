import django_filters


from Academy_class.models import AcademyClass


class AcademyClassFilter(django_filters.FilterSet):
    current_date = django_filters.DateFilter(method="filter_current_date")

    def filter_current_date(self, queryset, name, value):
        return queryset.filter(dates__contains=[value])

    class Meta:
        model = AcademyClass
        fields = [
            "instructor_id",
            "gender",
            "is_active",
            "age_group",
            "maximum_capacity",
            "current_date",
        ]
