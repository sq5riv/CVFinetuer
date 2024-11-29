from ..models import Offers, SelfDescription, Person, Experience, ExperienceDescription, Certificates,\
    Skills, SkillDescription
from django.shortcuts import get_object_or_404
from typing import List
from .brick import Brick


class CVGenerator(object):

    def __init__(self, offer_id: int):

        offer = get_object_or_404(Offers, id=offer_id)

        self.bricks = self.find_all_bricks(person_id=offer.owner.id)
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
    def find_all_bricks(person_id: int) -> List:
        brick_list = [Brick(label="Person", data=Person.objects.get(id=person_id).to_json())]
        brick_list.extend([Brick(label="SelfDescription", data=desc.to_json()) for desc in
                           SelfDescription.objects.filter(owner__id=person_id)])
        experience = Experience.objects.filter(owner__id=person_id)
        for index, exp in enumerate(experience):
            brick_list.append(Brick(label=f"Experience_{index}", data=exp.to_json()))
            descriptions = list(ExperienceDescription.objects.filter(experience=exp.id))
            if descriptions:
                brick_list.extend([Brick(label=f"Experience_{index}_Descriptions", data=desc.to_json())
                                   for desc in descriptions])
        brick_list.extend([Brick(f"certificate_{index}", cert.to_json())
                           for index, cert in enumerate(list(Certificates.objects.filter(owner__id=person_id)))])
        skills = Skills.objects.filter(owner__id=person_id)
        for index, skill in enumerate(skills):
            brick_list.append(Brick(label=f"Skill_{index}", data=skill.to_json()))
            descriptions = list(SkillDescription.objects.filter(skill_id=skill.id))
            if descriptions:
                brick_list.extend([Brick(label=f"Skill_{index}_Description", data=desc.to_json())
                                   for desc in descriptions])

        return brick_list

    def get_cv(self):
        return self.cv_content
