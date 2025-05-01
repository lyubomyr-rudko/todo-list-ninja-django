from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Task(models.Model):
    """
    Todo task.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100, null=False)
    description = models.TextField()
    complete = models.BooleanField(default=False)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Todo Task"
        verbose_name_plural = "Todo Tasks"
