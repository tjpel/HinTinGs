from django.db import models
import uuid

# Create your models here.
class Question(models.Model):
    """
    A model to handle a Question.
    Fields:
    - text: The actual String representation of question 
    """

    # define fields
    text = models.CharField(max_length = 500)

class SourceDocument(models.Model):
    """
    A model to store document embeddings
    Fields:
    - id:           uuid 
    - name:         original filename
    - content:      document text
    - embedding:    embeddings list stored as json
    - created_at:   datetime of creation
    """

    id = models.UUIDField(default=uuid.uuid4, primary_key=True)

    name = models.CharField(max_length=255)
    content = models.TextField()

    embedding = models.JSONField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} | uploaded at: {self.created_at}'

    
class File(models.Model):
    """
    A model to take in a uploaded .md File
    Fields:
        - file: the file
    """

    file = models.FileField(upload_to='quants/Notion_DB/')
    filename = models.CharField(max_length=255, blank=True)
    time_added = models.DateTimeField(auto_now_add = True)

    def save(self, *args, **kwargs):
        if not self.filename:
            cleaned = self.file.name.split('/')[-1]
            self.filename = cleaned
        super().save(*args, **kwargs)
