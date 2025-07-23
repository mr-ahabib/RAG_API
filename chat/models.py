from django.db import models

class ChatHistory(models.Model):
    user_id = models.CharField(max_length=100)  # to identify different users (optional)
    question = models.TextField()
    answer = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} - {self.question[:50]}"
