from rest_framework.views import APIView
from rest_framework.response import Response
from .services.crop_predictor import CropPredictor


# Create your views here.
class PredictAPIView(APIView):
    classifier = CropPredictor()

    def get(self, request, *args, **kwargs):
        lat = request.data.get("lat")
        long = request.data.get("long")
        # print("DATAAAAAA:", data)
        predictions = self.classifier.predict(lat, long)
        return Response(predictions)
