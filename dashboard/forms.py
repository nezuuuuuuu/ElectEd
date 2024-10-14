from django import forms
from django.contrib import admin
from .models import Candidate, Position, Election

class CandidateAdminForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['name', 'year', 'election', 'position', 'image']

    def __init__(self, *args, **kwargs):
        super(CandidateAdminForm, self).__init__(*args, **kwargs)

        # Dynamically filter positions based on selected election
        if 'election' in self.data:
            try:
                election_id = int(self.data.get('election'))
                self.fields['position'].queryset = Position.objects.filter(election_id=election_id)
            except (ValueError, TypeError):
                self.fields['position'].queryset = Position.objects.none()
        elif self.instance.pk:
            self.fields['position'].queryset = self.instance.election.positions.all()
