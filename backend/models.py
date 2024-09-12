from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    gender = models.BinaryField(blank=True)
    photo = models.ImageField()


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
    end_date = models.DateField(blank=True)
    description = models.CharField(max_length=500)
    owner = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.place_name


class Certificates(models.Model):
    name = models.CharField(max_length=50)
    issuer = models.CharField(max_length=150)
    issue_date = models.DateField()
    expire_date = models.DateField(blank=True)
    id_number = models.CharField(max_length=50)
    cert_link = models.CharField()
    notes = models.CharField()
    owner = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
    )


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
    knowledge_level = models.CharField(
        max_length=20, choices=KNOWLEDGE_LEVEL_CHOICES
    )
    experience_time = models.PositiveIntegerField(help_text="Experience in years")
    autonomy_level = models.CharField(
        max_length=20, choices=AUTONOMY_LEVEL_CHOICES
    )
    notes = models.CharField()
    owner = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class SelfDescription(models.Model):
    description = models.CharField()
    owner = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
    )


class SkillsCertificates(models.Model):
    skill = models.ForeignKey(
            "Skill",
            on_delete=models.CASCADE,
            )
    certificate = models.ForeignKey(
            "Certificates",
            on_delete=models.CASCADE,
            )


class SkillsExperience(models.Model):
    skill = models.ForeignKey(
            "Skill",
            on_delete=models.CASCADE,
            )
    certificate = models.ForeignKey(
            "Experience",
            on_delete=models.CASCADE,
            )
