from ..models import Offers, SelfDescription, Person, Experience, ExperienceDescription, Certificates
from django.shortcuts import get_object_or_404
from typing import List, Dict


class CVGenerator(object):

    def __init__(self, offer_id: int):
        # Retrieve the offer record
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

    def find_all_bricks(self, person_id: int) -> Dict[str, List]:

        experience = Experience.objects.filter(owner__id=person_id)
        bricks = {"Person": [Person(id=person_id)],
                  "SelfDescription": [SelfDescription.objects.filter(owner__id=person_id)]
                  }
        for index, exp in enumerate(experience):
            bricks[f"Experience_{index}"] = exp
            descriptions = list(ExperienceDescription.objects.filter(experience=exp.id))
            if descriptions:
                bricks[f"Experience_{index}_Descriptions"] = descriptions

        bricks["Certificates"] = list(Certificates.objects.filter(owner__id=person_id))

        print(bricks)
        return bricks

    def get_cv(self):
        return self.cv_content
