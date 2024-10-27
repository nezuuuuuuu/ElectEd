from django.db import models
from django.core.exceptions import ValidationError
from multiselectfield import MultiSelectField


# Create your models here.

#Active elections
class Election(models.Model):
    DEPARTMENT_CHOICES = [
    ("CS", "Computer Science"),
    ("IT", "Information Technology"),
    ("CE", "Civil Engineering"),
    ("EE", "Electrical Engineering"),
    ("ME", "Mechanical Engineering"),
    ("BS", "Business Studies"),
    ("HRM", "Hospitality and Restaurant Management"),
    ("AB", "Accountancy"),
    ("ED", "Education"),
    ("Nursing", "Nursing"),
    ("Architecture", "Architecture"),
    ("Marine", "Marine Engineering"),
    ("Chemistry", "Chemistry"),
    ("Biology", "Biology"),
    ("Physics", "Physics"),
    ("Math", "Mathematics"),
    ("Communication", "Communication Arts"),
    ("Arts", "Fine Arts"),
    ("Music", "Music"),
    ("Law", "Law"),
    ("ALL","ALL")
    ]
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='elections/', null=True, blank=True)
    description = models.TextField(blank=True)
    departments = MultiSelectField(choices=DEPARTMENT_CHOICES, default=['ALL'])  

    def __str__(self):
        return f"{self.title} - Departments: {', '.join(self.departments)}"   
#Position Per election
class Position(models.Model):
    title = models.CharField(max_length=255)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='positions')

    def __str__(self):
        return self.title
    
#candidate
class Candidate(models.Model):
    YEAR_CHOICES = [
        ("1st Year", "1st Year"),
        ("2nd Year", "2nd Year"),
        ("3rd Year", "3rd Year"),
        ("4th Year", "4th Year"),
    ]

    name = models.CharField(max_length=100)
    year = models.CharField(max_length=20, choices=YEAR_CHOICES, default="1st Year")
    image = models.ImageField(upload_to='candidates/', blank=True, null=True)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='candidates')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='candidates')
    vote_count = models.IntegerField(default=0)  # New field to track vote count

    def __str__(self):
        return self.name
    
class Student(models.Model):
    DEPARTMENT_CHOICES = [
    ("CS", "Computer Science"),
    ("IT", "Information Technology"),
    ("CE", "Civil Engineering"),
    ("EE", "Electrical Engineering"),
    ("ME", "Mechanical Engineering"),
    ("BS", "Business Studies"),
    ("HRM", "Hospitality and Restaurant Management"),
    ("AB", "Accountancy"),
    ("ED", "Education"),
    ("Nursing", "Nursing"),
    ("Architecture", "Architecture"),
    ("Marine", "Marine Engineering"),
    ("Chemistry", "Chemistry"),
    ("Biology", "Biology"),
    ("Physics", "Physics"),
    ("Math", "Mathematics"),
    ("Communication", "Communication Arts"),
    ("Arts", "Fine Arts"),
    ("Music", "Music"),
    ("Law", "Law"),
    ]

    student_id = models.CharField(max_length=10, unique=True)  # Unique student ID
    name = models.CharField(max_length=100)                     # Student name
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, default="NULL")

    def __str__(self):
        return f"{self.name} ({self.department})"  # Display name and department
    
class VoteSlip(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='voteslip')                    # Student name
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='voteslip')
    votes = models.CharField(max_length=20, default="NULL")

    def __str__(self):
        return f'{self.student} ({self.election})'