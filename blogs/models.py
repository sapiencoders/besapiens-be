import os
from django.db import models
from django.core.exceptions import ValidationError
from markdown import markdown


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    if ext not in ['.md', '.html']:
        raise ValidationError(
            'Unsupported file extension. Only .md or .html files are allowed.')


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)
    notes = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    banner_url = models.CharField(max_length=250, blank=True, null=True)
    categories = models.ManyToManyField(Category)
    content = models.TextField(blank=True)
    file = models.FileField(upload_to='blog_files/',
                            validators=[validate_file_extension])
    active = models.BooleanField(default=False)
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
        elif self.file.name.endswith('.html'):
            # Read HTML content directly
            self.content = self.file.read().decode('utf-8')
        self.content = self.content.replace('\n', '')
        super().save(*args, **kwargs)


class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.name} on {self.post.title}"
