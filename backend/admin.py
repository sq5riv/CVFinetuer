from django.contrib import admin
from backend.models import Person, Experience, ExperienceDescription, Certificates, Skills, SelfDescription, \
    SkillsExperience, ExperienceCertificates, SkillsCertificates, Offers
# Register your models here.


class ProjectAdmin(admin.ModelAdmin):
    pass


admin.site.register(Person, ProjectAdmin)
admin.site.register(Experience, ProjectAdmin)
admin.site.register(ExperienceDescription, ProjectAdmin)
admin.site.register(Certificates, ProjectAdmin)
admin.site.register(Skills, ProjectAdmin)
admin.site.register(SelfDescription, ProjectAdmin)
admin.site.register(SkillsCertificates, ProjectAdmin)
admin.site.register(SkillsExperience, ProjectAdmin)
admin.site.register(ExperienceCertificates, ProjectAdmin)
admin.site.register(Offers, ProjectAdmin)
