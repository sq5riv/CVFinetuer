from ..models import Offers, SelfDescription, Person, Experience, ExperienceDescription, Certificates,\
    Skills, SkillDescription
from django.shortcuts import get_object_or_404
from typing import List, Dict


class CVGenerator(object):

    def __init__(self, offer_id: int):

        offer = get_object_or_404(Offers, id=offer_id)

        self.find_all_bricks(person_id=offer.owner.id)
        # Simple logic to generate CV content (this could be more complex)
        self.cv_content = f"""
                CV for {offer.owner}:
                Company Name: {offer.company_name}
                Position: {offer.position}
                Offer Details: {offer.offer}
                Link to Offer: {offer.offer_link if offer.offer_link else 'N/A'}
                """

        # Save the generated CV to the database
        offer.cv = self.cv_content
        offer.save()

    @staticmethod
    def find_all_bricks(person_id: int) -> Dict[str, List]:

        bricks = {"Person": [Person(id=person_id)],
                  "SelfDescription": [SelfDescription.objects.filter(owner__id=person_id)]
                  }
        experience = Experience.objects.filter(owner__id=person_id)
        for index, exp in enumerate(experience):
            bricks[f"Experience_{index}"] = exp
            descriptions = list(ExperienceDescription.objects.filter(experience=exp.id))
            if descriptions:
                bricks[f"Experience_{index}_Descriptions"] = descriptions

        bricks["Certificates"] = list(Certificates.objects.filter(owner__id=person_id))
        skills = Skills.objects.filter(owner__id=person_id)
        for index, skill in enumerate(skills):
            bricks[f"Skill_{index}"] = skill
            descriptions = list(SkillDescription.objects.filter(skill_id=skill.id))
            if descriptions:
                bricks[f"Skill_{index}_Descriptions"] = descriptions

        return bricks

    def get_cv(self):
        return self.cv_content
