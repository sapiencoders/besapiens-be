import os
from django.db import models
from django.core.exceptions import ValidationError
from markdown import markdown


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    if ext not in ['.md', '.html']:
        raise ValidationError(
            'Unsupported file extension. Only .md or .html files are allowed.')


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    file = models.FileField(upload_to='blog_files/',
                            validators=[validate_file_extension])
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def clean(self):
        if not self.file and not self.content:
            raise ValidationError("Either 'file' or 'content' is required.")

    def save(self, *args, **kwargs):
        if self.file.name.endswith('.md'):
            # Convert markdown content to HTML
            self.content = markdown(self.file.read().decode('utf-8'))
        else:
            # Read HTML content directly
            self.content = self.file.read().decode('utf-8')
        super().save(*args, **kwargs)
