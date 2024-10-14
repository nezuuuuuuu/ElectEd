from django.contrib import admin
from .models import Election, Position, Candidate


class PositionInline(admin.TabularInline):
    model = Position
    extra = 1  # Number of empty forms to display for adding new positions

    # Optional: Customize the displayed fields in the inline admin
    fields = ('title', 'election')  # Display title and associated election

class ElectionAdmin(admin.ModelAdmin):
    inlines = [PositionInline]

    # Optional: Customize list display for Election admin
    list_display = ('title', 'description')  # Display title and description in the election list

class PositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_election_title')  # Display position title and election title
    search_fields = ('title',)  # Allow searching by position title

    def get_election_title(self, obj):
        return obj.election.title if obj.election else 'No Election'

    get_election_title.short_description = 'Election'  # Set a short description for the column

class CandidateAdmin(admin.ModelAdmin):
    list_display = ['name', 'year', 'position', 'election']
    search_fields = ('name',)

# Register your models here
admin.site.register(Election, ElectionAdmin)
admin.site.register(Position, PositionAdmin)  # Register with custom admin
admin.site.register(Candidate, CandidateAdmin)
