from django.contrib import admin
from .forms import CandidateAdminForm
from .models import Election, Position, Candidate, Student
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from elected.admin import admin_site

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

class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name', 'department')  # Display these fields in the list view
    search_fields = ('name', 'student_id', 'department')  # Allow searching by these fields

    # Optional: Customize the form layout or fields if needed
    # form = StudentAdminForm  # Uncomment if you have a custom form for the Student model

# Register the Student model with the custom admin class
admin_site.register(Student, StudentAdmin)

# Register your models here
admin_site.register(Election, ElectionAdmin)
admin_site.register(Position, PositionAdmin) 
admin_site.register(Candidate, CandidateAdmin)

