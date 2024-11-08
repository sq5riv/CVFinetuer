from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    photo = models.ImageField(upload_to='backend/foto/')

    def __str__(self):
        return str(self.name) + ' ' + str(self.last_name)


class Experience(models.Model):
    COMMERCIAL = "Com"
    EDUCATION = "Edu"
    VOLUNTARY = "Vol"
    PERSONAL = "Per"

    EXP_TYPES = {
        COMMERCIAL: "Commercial",
        EDUCATION: "Educational",
        VOLUNTARY: "Voluntary",
        PERSONAL: "Personal"
    }
    place_name = models.CharField(max_length=50)
    type = models.CharField(
        max_length=3,
        choices=EXP_TYPES
    )
    role = models.CharField(max_length=30)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    owner = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.place_name)


class ExperienceDescription(models.Model):
    experience = models.ForeignKey(
        "Experience",
        on_delete=models.CASCADE,
    )
    description = models.CharField(max_length=2000)


class Certificates(models.Model):
    name = models.CharField(max_length=50)
    issuer = models.CharField(max_length=150)
    issue_date = models.DateField()
    expire_date = models.DateField(null=True, blank=True)
    id_number = models.CharField(max_length=50)
    cert_link = models.URLField(null=True, blank=True)
    notes = models.CharField(max_length=500)
    owner = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
    )
    experience = models.ForeignKey(
        "Experience",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.name)


class Skills(models.Model):
    KNOWLEDGE_LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]

    AUTONOMY_LEVEL_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    name = models.CharField(max_length=100)
    level = models.CharField(
        max_length=20, choices=KNOWLEDGE_LEVEL_CHOICES
    )
    experience_time = models.PositiveIntegerField(help_text="Experience in years")
    autonomy_level = models.CharField(
        max_length=20, choices=AUTONOMY_LEVEL_CHOICES
    )
    notes = models.CharField(max_length=500)
    owner = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.name)


class SelfDescription(models.Model):
    description = models.CharField(max_length=1000)
    owner = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.owner) + ': ' + str(self.description)[:30]


class SkillsCertificates(models.Model):
    skill = models.ForeignKey(
            "Skills",
            on_delete=models.CASCADE,
            )
    certificate = models.ForeignKey(
            "Certificates",
            on_delete=models.CASCADE,
            )


class SkillsExperience(models.Model):
    skill = models.ForeignKey(
            "Skills",
            on_delete=models.CASCADE,
            )
    experience = models.ForeignKey(
            "Experience",
            on_delete=models.CASCADE,
            )


class ExperienceCertificates(models.Model):
    experience = models.ForeignKey(
            "Experience",
            on_delete=models.CASCADE,
            )
    certificate = models.ForeignKey(
            "Certificates",
            on_delete=models.CASCADE,
            )


class Offers(models.Model):
    owner = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
        )
    company_name = models.CharField(max_length=80)
    position = models.CharField(max_length=50)
    offer_link = models.URLField(null=True, blank=True)
    offer = models.CharField(max_length=2000)
    cv = models.CharField(max_length=2000)
