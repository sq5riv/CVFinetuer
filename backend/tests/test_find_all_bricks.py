import json
import os
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date
from django.test import TestCase
from backend.models import (
    Person, Experience, ExperienceDescription, Certificates, Skills,
    SkillDescription, SelfDescription, Offers
)
from backend.cv_generator.cv_generator import CVGenerator


class SerializationTests(TestCase):

    def setUp(self):
        # Create a Person instance
        self.person = Person.objects.create(
            name="John",
            middle_name="Doe",
            last_name="Smith",
            email="john.doe@example.com",
            photo=SimpleUploadedFile("test.jpg", b"file_content")
        )

        # Create Experience instances
        self.experience = Experience.objects.create(
            place_name="Test Company",
            type=Experience.COMMERCIAL,
            role="Software Engineer",
            start_date=date(2020, 1, 1),
            end_date=date(2023, 1, 1),
            owner=self.person
        )

        # Create ExperienceDescription instance
        self.experience_description = ExperienceDescription.objects.create(
            experience=self.experience,
            description="Worked on several high-profile projects."
        )

        # Create Certificates instance
        self.certificate = Certificates.objects.create(
            name="Certified Tester",
            issuer="Test Institute",
            issue_date=date(2022, 5, 1),
            expire_date=None,
            id_number="12345",
            cert_link="http://example.com/certificate",
            notes="Completed with distinction",
            owner=self.person,
            experience=self.experience
        )

        # Create Skills instance
        self.skill = Skills.objects.create(
            name="Python Programming",
            level="expert",
            experience_time=5,
            autonomy_level="high",
            notes="Expert in Python",
            owner=self.person
        )

        # Create SkillDescription instance
        self.skill_description = SkillDescription.objects.create(
            skill=self.skill,
            description="Proficient in Python 3.x and frameworks."
        )

        # Create SelfDescription instance
        self.self_description = SelfDescription.objects.create(
            description="Dedicated and skilled software developer.",
            owner=self.person
        )

        # Create Offers instance
        self.offer = Offers.objects.create(
            owner=self.person,
            company_name="TechCorp",
            position="Lead Developer",
            offer_link="http://example.com/offer",
            offer="Join our team and work on exciting projects.",
            cv=None
        )

    def test_person_to_json(self):
        serialized = json.loads(self.person.to_json())
        self.assertEqual(serialized["name"], "John")
        self.assertEqual(serialized["middle_name"], "Doe")
        self.assertEqual(serialized["last_name"], "Smith")
        self.assertEqual(serialized["email"], "john.doe@example.com")
        self.assertTrue(serialized["photo"].endswith(".jpg"))

    def test_experience_to_json(self):
        serialized = json.loads(self.experience.to_json())
        self.assertEqual(serialized["place_name"], "Test Company")
        self.assertEqual(serialized["type"], "Commercial")
        self.assertEqual(serialized["role"], "Software Engineer")
        self.assertEqual(serialized["start_date"], "2020-01-01")
        self.assertEqual(serialized["end_date"], "2023-01-01")

    def test_experience_description_to_json(self):
        serialized = json.loads(self.experience_description.to_json())
        self.assertEqual(serialized["description"], "Worked on several high-profile projects.")
        self.assertEqual(serialized["experience_id"], self.experience.id)

    def test_certificates_to_json(self):
        serialized = json.loads(self.certificate.to_json())
        self.assertEqual(serialized["name"], "Certified Tester")
        self.assertEqual(serialized["issuer"], "Test Institute")
        self.assertEqual(serialized["issue_date"], "2022-05-01")
        self.assertEqual(serialized["cert_link"], "http://example.com/certificate")

    def test_skills_to_json(self):
        serialized = json.loads(self.skill.to_json())
        self.assertEqual(serialized["name"], "Python Programming")
        self.assertEqual(serialized["level"], "Expert")
        self.assertEqual(serialized["autonomy_level"], "High")

    def test_skill_description_to_json(self):
        serialized = json.loads(self.skill_description.to_json())
        self.assertEqual(serialized["description"], "Proficient in Python 3.x and frameworks.")
        self.assertEqual(serialized["skill_name"], "Python Programming")

    def test_self_description_to_json(self):
        serialized = json.loads(self.self_description.to_json())
        self.assertEqual(serialized["description"], "Dedicated and skilled software developer.")
        self.assertEqual(serialized["owner_id"], self.person.id)

    def test_offers_to_json(self):
        serialized = json.loads(self.offer.to_json())
        self.assertEqual(serialized["company_name"], "TechCorp")
        self.assertEqual(serialized["position"], "Lead Developer")
        self.assertEqual(serialized["offer_link"], "http://example.com/offer")

    def test_find_all_bricks(self):
        # Call the function
        result = CVGenerator.find_all_bricks(self.person.id)

        # Validate the structure and contents
        self.assertIn("Person", result)
        self.assertIn("SelfDescription", result)
        self.assertIn("Experience_0", result)
        self.assertIn("Certificates", result)
        self.assertIn("Skill_0", result)
        self.assertIn("Skill_0_Descriptions", result)

        # Check the values
        self.assertEqual(json.loads(result["Person"])["name"], self.person.name)
        self.assertEqual(json.loads(result["Person"])["email"], self.person.email)
        self.assertEqual(result["Experience_0"].place_name, "Test Company")
        self.assertEqual(result["Certificates"][0].name, "Certified Tester")
        self.assertEqual(result["Skill_0"].name, "Python Programming")
        self.assertEqual(result["Skill_0_Descriptions"][0].description, "Proficient in Python 3.x and frameworks.")

    def tearDown(self):
        # Remove the uploaded file after each test
        if self.person.photo and os.path.isfile(self.person.photo.path):
            os.remove(self.person.photo.path)
