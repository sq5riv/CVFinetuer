from django.test import TestCase
from backend.models import Person, SelfDescription, Experience, ExperienceDescription, Certificates, Skills, \
    SkillDescription
from backend.cv_generator.cv_generator import CVGenerator


class FindAllBricksTest(TestCase):
    def setUp(self):
        # Create a sample person
        self.person = Person.objects.create(
            name="John",
            middle_name="A.",
            last_name="Doe",
            email="john.doe@example.com"
        )

        # Create sample SelfDescription
        SelfDescription.objects.create(
            owner=self.person,
            description="An experienced developer with expertise in Python."
        )

        # Create sample Experience
        exp = Experience.objects.create(
            place_name="Tech Company",
            type=Experience.COMMERCIAL,
            role="Software Engineer",
            start_date="2020-01-01",
            end_date="2022-01-01",
            owner=self.person
        )

        # Create sample ExperienceDescription
        ExperienceDescription.objects.create(
            experience=exp,
            description="Worked on various software projects."
        )

        # Create sample Certificate
        Certificates.objects.create(
            name="Python Certification",
            issuer="Certifying Body",
            issue_date="2021-06-01",
            id_number="123456",
            owner=self.person
        )

        # Create sample Skills
        skill = Skills.objects.create(
            name="Python Programming",
            level="Advanced",
            experience_time=5,
            owner=self.person
        )

        # Create sample SkillDescription
        SkillDescription.objects.create(
            skill=skill,
            description="Proficient in Python for web development."
        )

    def test_find_all_bricks(self):
        # Call the function with the person_id of the sample data
        bricks = CVGenerator.find_all_bricks(self.person.id)

        # Check the 'Person' key
        self.assertIn("Person", bricks)
        self.assertEqual(bricks["Person"][0], self.person)

        # Check the 'SelfDescription' key
        self.assertIn("SelfDescription", bricks)
        self.assertTrue(bricks["SelfDescription"])

        # Check 'Experience_0' key
        self.assertIn("Experience_0", bricks)
        self.assertEqual(bricks["Experience_0"].place_name, "Tech Company")

        # Check 'Experience_0_Descriptions' key
        self.assertIn("Experience_0_Descriptions", bricks)
        self.assertTrue(bricks["Experience_0_Descriptions"])

        # Check 'Certificates' key
        self.assertIn("Certificates", bricks)
        self.assertTrue(bricks["Certificates"])

        # Check 'Skill_0' key
        self.assertIn("Skill_0", bricks)
        self.assertEqual(bricks["Skill_0"].name, "Python Programming")

        # Check 'Skill_0_Descriptions' key
        self.assertIn("Skill_0_Descriptions", bricks)
        self.assertTrue(bricks["Skill_0_Descriptions"])
