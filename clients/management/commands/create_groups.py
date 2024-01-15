from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    """Command class."""

    help = """ Create Service Command """

    def handle(self, *args, **options):
        groups = ["Admin", "Member"]

        for item in groups:
            group, created = Group.objects.get_or_create(name=item)
            permissions = Permission.objects.all()
            if created:
                if group.name == "Admin":
                    group.permissions.add(*permissions)
                self.stdout.write(self.style.SUCCESS("group created successfully"))
            else:
                self.stdout.write(self.style.SUCCESS("group already exists"))
