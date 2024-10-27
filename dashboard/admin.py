from django.contrib import admin
from .forms import CandidateAdminForm
from .models import Election, Position, Candidate, Student,VoteSlip
from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from elected.admin import admin_site

class PositionInline(admin.TabularInline):
    model = Position
    extra = 1  
    fields = ('title', 'election')  

class ElectionAdmin(admin.ModelAdmin):
    inlines = [PositionInline]

    list_display = ('title', 'description') 

class PositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_election_title') 
    search_fields = ('title',)  


    def get_election_title(self, obj):
        return obj.election.title if obj.election else 'No Election'

    get_election_title.short_description = 'Election'  # Set a short description for the column

class CandidateAdmin(admin.ModelAdmin):
    form = CandidateAdminForm
    list_display = ['name', 'year', 'position', 'election','vote_count']
    search_fields = ('name',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'position':
            if request.resolver_match.kwargs.get('object_id'):  # Editing existing candidate
                candidate = Candidate.objects.get(pk=request.resolver_match.kwargs['object_id'])
                kwargs["queryset"] = Position.objects.filter(election=candidate.election)
            else:
                kwargs["queryset"] = Position.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    
    def save_model(self, request, obj, form, change):   
        if 'position' in form.cleaned_data:
            obj.position = form.cleaned_data['position']
        super().save_model(request, obj, form, change)

    class Media:
        js = ('admin/js/admin_candidate.js',)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name', 'department')  
    search_fields = ('name', 'student_id', 'department')  

class VoteSlipAdmin(admin.ModelAdmin):
    list_display = ('student', 'election', 'votes')
    
    search_fields = ('student__name', 'election__title')
    
    list_filter = ('election',)

admin_site.register(VoteSlip, VoteSlipAdmin)
admin_site.register(Student, StudentAdmin)
admin_site.register(Election, ElectionAdmin)
admin_site.register(Position, PositionAdmin) 
admin_site.register(Candidate, CandidateAdmin)

