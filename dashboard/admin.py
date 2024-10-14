from django.contrib import admin
from .forms import CandidateAdminForm
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
    form = CandidateAdminForm
    list_display = ['name', 'year', 'position', 'election']
    search_fields = ('name',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'position':
            # For initial form load, check if the election is already selected (e.g., in edit mode)
            if request.resolver_match.kwargs.get('object_id'):  # Editing existing candidate
                candidate = Candidate.objects.get(pk=request.resolver_match.kwargs['object_id'])
                kwargs["queryset"] = Position.objects.filter(election=candidate.election)
            else:
                kwargs["queryset"] = Position.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    
    # Ensure that 'position' is available in the form
    def save_model(self, request, obj, form, change):   
        if 'position' in form.cleaned_data:
            obj.position = form.cleaned_data['position']
        super().save_model(request, obj, form, change)

    class Media:
        js = ('admin/js/admin_candidate.js',)

# Register your models here
admin.site.register(Election, ElectionAdmin)
admin.site.register(Position, PositionAdmin) 
admin.site.register(Candidate, CandidateAdmin)
