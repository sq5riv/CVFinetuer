from django.test import TestCase
from backend.models import (
    Person, SelfDescription, Experience, ExperienceDescription, Certificates, Skills, SkillDescription
)
from backend.cv_generator.cv_generator import CVGenerator
import os
import json


class TestFindAllBricks(TestCase):

    def setUp(self):
        # Create a Person
        self.person = Person.objects.create(
            name="John",
            middle_name="M",
            last_name="Doe",
            email="john.doe@example.com",
        )

        # Create SelfDescriptions
        self.self_description = SelfDescription.objects.create(
            owner=self.person,
            description="This is a test self-description."
        )

        # Create Experiences
        self.experience = Experience.objects.create(
            place_name="Test Company",
            type="Com",
            role="Developer",
            start_date="2020-01-01",
            end_date="2021-01-01",
            owner=self.person
        )

        # Create ExperienceDescriptions
        self.experience_description = ExperienceDescription.objects.create(
            experience=self.experience,
            description="This is a test experience description."
        )

        # Create Certificates
        self.certificate = Certificates.objects.create(
            name="Test Certificate",
            issuer="Test Issuer",
            issue_date="2020-01-01",
            expire_date="2023-01-01",
            id_number="123456",
            cert_link="https://example.com",
            notes="Test notes.",
            owner=self.person
        )

        # Create Skills
        self.skill = Skills.objects.create(
            name="Test Skill",
            level="advanced",
            experience_time=5,
            autonomy_level="high",
            notes="Test skill notes.",
            owner=self.person
        )

        # Create SkillDescriptions
        self.skill_description = SkillDescription.objects.create(
            skill=self.skill,
            description="This is a test skill description."
        )

    def test_find_all_bricks(self):
        # Call the function
        result = CVGenerator.find_all_bricks(person_id=self.person.id)

        # Verify the result
        self.assertEqual(len(result), 7)  # Adjust based on the expected number of bricks

        # Check Person Brick
        person_brick = next(brick for brick in result if brick.label == "Person")

        self.assertEqual(json.loads(person_brick.data)["name"], self.person.name)

        # Check SelfDescription Brick
        self_description_brick = next(brick for brick in result if brick.label == "SelfDescription")
        self.assertEqual(json.loads(self_description_brick.data)["description"], self.self_description.description)

        # Check Experience Bricks
        experience_brick = next(brick for brick in result if brick.label.startswith("Experience_"))
        self.assertEqual(json.loads(experience_brick.data)["place_name"], self.experience.place_name)

        experience_description_brick = next(
            brick for brick in result if brick.label.endswith("_Descriptions")
        )
        self.assertEqual(
            json.loads(experience_description_brick.data)["description"],
            self.experience_description.description
        )

        # Check Certificate Bricks
        certificate_brick = next(brick for brick in result if brick.label.startswith("certificate_"))
        self.assertEqual(json.loads(certificate_brick.data)["name"], self.certificate.name)

        # Check Skill Bricks
        skill_brick = next(brick for brick in result if brick.label.startswith("Skill_"))
        self.assertEqual(json.loads(skill_brick.data)["name"], self.skill.name)

        skill_description_brick = next(
            brick for brick in result if brick.label.endswith("_Description")
        )
        self.assertEqual(
            json.loads(skill_description_brick.data)["description"],
            self.skill_description.description
        )

    def tearDown(self):
        # Remove the uploaded file after each test
        if self.person.photo and os.path.isfile(self.person.photo.path):
            os.remove(self.person.photo.path)
