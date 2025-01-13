from django.db import models
from accounts.models import CustomUser

class Activities(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="activities")
    data = models.TextField(max_length=100, blank=False)  # Ensure no blank data is allowed
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Activities"  # Ensure admin shows the plural form correctly
        ordering = ["-created_date"]  # Sort by newest activities first

    def __str__(self):
        return f"Activity by {self.user.username} at {self.created_date.strftime('%Y-%m-%d %H:%M:%S')}"
