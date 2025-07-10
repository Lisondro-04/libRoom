from django.db import models

class Note(models.Model):
    NOTE_TYPES = [
        ('blg-ch', 'Chapter'),
        ('blg-scn', 'Scene'),
        ('blg-wrld', 'Worldbuilding'),
        ('glob', 'Global'),
    ]

    id = models.CharField(primary_key=True, max_length=10, editable=False)
    title = models.CharField(max_length=200)
    linked_type = models.CharField(max_length=10, choices=NOTE_TYPES)
    linked_target_id = models.CharField(max_length=50, null=True, blank=True)
    content = models.TextField()
    word_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.word_count = len(self.content.split())
        if not self.id:
            last_note = Note.objects.order_by('-id').first()
            if last_note:
                last_id = int(last_note.id.split('-')[1])
                self.id = f"nt-{last_id+1:03d}"
            else:
                self.id = "nt-001"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.id})"
