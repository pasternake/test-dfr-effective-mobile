from django.core.management.base import BaseCommand
from permissions.models import Resource, Action, Permission, Role
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate initial test data'

    def handle(self, *args, **kwargs):
        # Create Resources
        doc_res, _ = Resource.objects.get_or_create(name='Document', code='document')
        
        # Create Actions
        read_act, _ = Action.objects.get_or_create(name='Read', code='read')
        create_act, _ = Action.objects.get_or_create(name='Create', code='create')
        
        # Create Permissions
        doc_read, _ = Permission.objects.get_or_create(resource=doc_res, action=read_act)
        doc_create, _ = Permission.objects.get_or_create(resource=doc_res, action=create_act)
        
        # Create Roles
        admin_role, _ = Role.objects.get_or_create(name='Admin')
        admin_role.permissions.add(doc_read, doc_create)
        
        viewer_role, _ = Role.objects.get_or_create(name='Viewer')
        viewer_role.permissions.add(doc_read)
        
        # Create Users
        admin_user, created = User.objects.get_or_create(email='admin@example.com')
        if created:
            admin_user.set_password('admin123')
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
            admin_user.roles.add(admin_role)
            self.stdout.write(self.style.SUCCESS('Created admin user'))
        else:
             self.stdout.write(self.style.SUCCESS('Admin user already exists'))
            
        viewer_user, created = User.objects.get_or_create(email='viewer@example.com')
        if created:
            viewer_user.set_password('viewer123')
            viewer_user.save()
            viewer_user.roles.add(viewer_role)
            self.stdout.write(self.style.SUCCESS('Created viewer user'))
        else:
             self.stdout.write(self.style.SUCCESS('Viewer user already exists'))
            
        self.stdout.write(self.style.SUCCESS('Successfully populated test data'))
