from django.db import models

# Create your models here.

#Active elections
class Election(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='elections/', null=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
    
#Position Per election
class Position(models.Model):
    title = models.CharField(max_length=255)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='positions')

    def __str__(self):
        return self.title
    
#candidate
class Candidate(models.Model):
    name = models.CharField(max_length=100)
    year = models.CharField(max_length=20, default="1st Year")
    image = models.ImageField(upload_to='candidates/', blank=True, null=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='candidates')
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='candidates')

    def __str__(self):
        return self.name
