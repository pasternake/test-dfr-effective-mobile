from django.db import models

class Resource(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Action(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Permission(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('resource', 'action')

    def __str__(self):
        return f"{self.resource.code}.{self.action.code}"

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    permissions = models.ManyToManyField(Permission, related_name='roles')

    def __str__(self):
        return self.name
