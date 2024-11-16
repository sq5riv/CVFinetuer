from .cv_generator import cv_generator
from django.http import JsonResponse
from django.views import View


class GenerateCV(View):
    """

    """
    @staticmethod
    def get(request):

        cv_content = cv_generator.CVGenerator(offer_id=1).get_cv()

        # Return a response indicating success
        return JsonResponse({"message": "CV generated successfully", "cv": cv_content}, status=200)
