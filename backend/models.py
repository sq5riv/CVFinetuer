from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    photo = models.ImageField(upload_to='backend/foto/')

    def __str__(self):
        return str(self.name) + ' ' + str(self.last_name)

    def __repr__(self):
        return (f"Person(name={self.name!r}, middle_name={self.middle_name!r}, "
                f"last_name={self.last_name!r}, email={self.email!r}")


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

    def __repr__(self):
        return (f"Experience(place_name={self.place_name!r}, "
                f"type={self.EXP_TYPES.get(self.type, 'Unknown')!r}, "
                f"role={self.role!r}, start_date={self.start_date!r}, "
                f"end_date={self.end_date!r},  ")


class ExperienceDescription(models.Model):
    experience = models.ForeignKey(
        "Experience",
        on_delete=models.CASCADE,
    )
    description = models.CharField(max_length=2000)

    def __repr__(self):
        return (f"ExperienceDescription(experience_id={self.experience.id!r}, "
                f"description={self.description!r}...)")


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

    def __repr__(self):
        return (f"Certificates(name={self.name!r}, issuer={self.issuer!r}, "
                f"issue_date={self.issue_date!r}, expire_date={self.expire_date!r}, "
                f"id_number={self.id_number!r}, cert_link={self.cert_link!r}, "
                f"notes={self.notes!r}, owner_id={self.owner.id!r}")


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


class SkillDescription(models.Model):
    description = models.CharField(max_length=1000)
    owner = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.owner) + ': ' + str(self.description)[:30]

    def __repr__(self):
        return str(self.owner) + ': ' + str(self.description)


class SelfDescription(models.Model):
    description = models.CharField(max_length=1000)
    owner = models.ForeignKey(
        "Person",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.owner) + ': ' + str(self.description)[:30]

    def __repr__(self):
        return str(self.owner) + ': ' + str(self.description)


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
    cv = models.CharField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return str(self.company_name) + ' - ' + str(self.position)
