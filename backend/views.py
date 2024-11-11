from django.http import JsonResponse
from django.views import View
from .models import Offers
from django.shortcuts import get_object_or_404


class GenerateCV(View):
    def get(self, request):
        # Retrieve the offer record
        offer = get_object_or_404(Offers, id='1')

        # Simple logic to generate CV content (this could be more complex)
        cv_content = f"""
        CV for {offer.owner}:
        Company Name: {offer.company_name}
        Position: {offer.position}
        Offer Details: {offer.offer}
        Link to Offer: {offer.offer_link if offer.offer_link else 'N/A'}
        """

        # Save the generated CV to the database
        offer.cv = cv_content
        offer.save()

        # Return a response indicating success
        return JsonResponse({"message": "CV generated successfully", "cv": cv_content}, status=200)
