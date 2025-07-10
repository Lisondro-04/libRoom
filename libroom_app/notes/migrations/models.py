from django.db import models

class Note(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    title = models.CharField(max_length=255)
    linked_type = models.CharField(max_length=20)  # blg-ch, blg-scn, blg-wrld, glob
    target_id = models.CharField(max_length=20, null=True, blank=True)
    word_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.id}: {self.title}"
