from django.contrib import admin
from .forms import CandidateAdminForm
from .models import Election, Position, Candidate, Student, VoteSlip
from django.templatetags.static import static
from django.utils.html import format_html

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
    get_election_title.short_description = 'Election'

class CandidateAdmin(admin.ModelAdmin):
    form = CandidateAdminForm
    list_display = ['display_image_with_name', 'year', 'position', 'election', 'vote_count']
    search_fields = ('name',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Dynamically filter the position choices based on the selected election
        if db_field.name == 'position':
            if 'election' in request.POST:
                election_id = request.POST.get('election')
                kwargs["queryset"] = Position.objects.filter(election_id=election_id)
            elif request.resolver_match.kwargs.get('object_id'):
                # Editing an existing candidate
                candidate = Candidate.objects.get(pk=request.resolver_match.kwargs['object_id'])
                kwargs["queryset"] = Position.objects.filter(election=candidate.election)
            else:
                kwargs["queryset"] = Position.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def display_image_with_name(self, obj):
        if obj.image:
            return format_html(
                '<div style="display: flex; align-items: center;">'
                '<img src="{}" style="height: 50px; width: 50px; border-radius: 25px; margin-right: 10px;"/>'
                '<span>{}</span>'
                '</div>',
                obj.image.url, obj.name)
        return "(No image)"
    display_image_with_name.short_description = 'Image Preview'

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
    list_display = ('student', 'election', 'display_candidates')
    search_fields = ('student__name', 'election__title')
    list_filter = ('election',)

    def display_candidates(self, obj):
        # Display a comma-separated list of candidate names in the VoteSlip
        return ", ".join([candidate.name for candidate in obj.candidates.all()])
    display_candidates.short_description = 'Voted Candidates'


admin.site.register(VoteSlip, VoteSlipAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Election, ElectionAdmin)
admin.site.register(Position, PositionAdmin) 
admin.site.register(Candidate, CandidateAdmin)
