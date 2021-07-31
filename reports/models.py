from profiles.models import Profile
from django.db import models
from django.urls import reverse



class Report(models.Model):
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to='reports', blank=True)
    remarks = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


    def get_absolute_url(self):
        return reverse("reports:detail", kwargs={"pk": self.pk})
    
    class Meta:
        ordering=('-created',)