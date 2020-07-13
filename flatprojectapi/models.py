from django.db import models
from django.core.validators import FileExtensionValidator

class Status(models.Model):
    description = models.CharField(max_length=30)

    def __str__(self):
        return self.description

class Branches(models.Model):
    description = models.CharField(max_length=30)

    def __str__(self):
        return self.description

class Merges(models.Model):
    default_error_messages = {
        'required': 'This field is required',
    }

    title = models.CharField(max_length=30, error_messages=default_error_messages)
    description = models.TextField(error_messages=default_error_messages)
    base_branch = models.ForeignKey(Branches, on_delete=models.CASCADE, default=1, related_name='branch_1')
    compare_branch = models.ForeignKey(Branches, on_delete=models.CASCADE, default=1, related_name='branch_2')
    author = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=100, null=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, default=1, related_name='status')

    def __str__(self):
        return self.title

