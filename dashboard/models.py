from django.db import models
from django.core.exceptions import ValidationError
from multiselectfield import MultiSelectField
from datetime import date, timedelta

from datetime import datetime

# Active elections
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
        ("ALL", "ALL")
    ]

    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='elections/', null=True, blank=True)
    description = models.TextField(blank=True)
    departments = MultiSelectField(choices=DEPARTMENT_CHOICES, default=['ALL'])  
    open_date = models.DateTimeField(default=datetime.now)  # Correct default value
    close_date = models.DateTimeField(default=datetime.now) 
   

    def __str__(self):
        return f"{self.title} - Departments: {', '.join(self.departments or [])}"

    def clean(self):
        # Validate that at least one department is selected
        if not self.departments:
            raise ValidationError("At least one department must be selected.")
        super().clean()
# Position per election
class Position(models.Model):
    title = models.CharField(max_length=255)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='positions')
    max_selection = models.IntegerField()

    def __str__(self):
        return self.title
# Student model
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
    name = models.CharField(max_length=100)                    # Student name
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, default="NULL")

    def __str__(self):
        return f"{self.name} ({self.department})"  # Display name and department
# Candidate
class Candidate(models.Model):
    YEAR_CHOICES = [
        ("1st Year", "1st Year"),
        ("2nd Year", "2nd Year"),
        ("3rd Year", "3rd Year"),
        ("4th Year", "4th Year"),
    ]

    name = models.CharField(max_length=100)
    partylist = models.CharField(max_length=100,default='')
    year = models.CharField(max_length=20, choices=YEAR_CHOICES, default="1st Year")
    course = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='candidates/', blank=True, null=True)
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='candidates')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='candidates')

    vote_count = models.IntegerField(default=0) 
    platforms = models.TextField(blank=True, null=True)
    is_winner = models.BooleanField(default=False)

    def __str__(self):
        return self.name

from django.core.exceptions import ValidationError

class VoteSlip(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='voteslips')
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='voteslips')
    candidates = models.TextField()  # Store candidate IDs as a comma-separated string

    def __str__(self):
        return f'{self.student} ({self.election})'

    def clean(self):
        if VoteSlip.objects.filter(student=self.student, election=self.election).exists():
            raise ValidationError("Each student can only submit one VoteSlip per election.")
        super().clean()

    def save(self, *args, **kwargs):
        # Ensure each student has only one VoteSlip per election
        if VoteSlip.objects.filter(student=self.student, election=self.election).exists():
            raise ValidationError("Each student can only submit one VoteSlip per election.")

        super().save(*args, **kwargs)  # Save the VoteSlip instance first

        # Convert the candidates string into a list of candidate IDs
        candidate_ids = self.candidates

        # Update the vote counts for each selected candidate
        for candidate_id in candidate_ids:
            candidate = Candidate.objects.get(id=candidate_id)
            candidate.vote_count += 1
        Candidate.objects.bulk_update(Candidate.objects.filter(id__in=candidate_ids), ['vote_count'])