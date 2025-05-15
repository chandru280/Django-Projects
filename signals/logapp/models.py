from django.db import models

class LogEntry(models.Model):
    LEVEL_CHOICES = [
        ('DEBUG', 'Debug'),
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('CRITICAL', 'Critical'),
    ]

    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    logger_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255, blank=True, null=True)
    line_number = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.timestamp} [{self.level}] {self.message}"
