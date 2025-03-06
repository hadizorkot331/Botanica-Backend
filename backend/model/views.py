from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .services.crop_predictor import CropPredictor
from crops.models import Crop
from crops.serializers import CropSerializer


# Create your views here.
class GetDataAPIView(APIView):
    cp = CropPredictor()

    def get(self, request, *args, **kwargs):
        """
        API view that handles getting the prediction and data based on location, and useNPK flag
        View can also accept "data" dictionary if user decides to modify it

        Sample parameters: params={"lat":..., "long":..., "useNPK":True, "data"(optional):...}

        Note: "data" should be in the format {
            "N": 90,
            "P": 40,
            "K": 32,
            "temperature": 24,
            "humidity": 82.03,
            "ph": 7.2,
            "rainfall": 200,
        }

        Note: If user passes soil/weather data, he should always include NPK in the data even if useNPK flag is set to false
        """

        # Extract get parameters
        try:
            lat = request.data.get("lat")
            long = request.data.get("long")
            useNPK = request.data.get("useNPK")
        except KeyError:
            return Response("Incomplete Data", status=status.HTTP_400_BAD_REQUEST)

        try:
            # If data was included in request, use it
            if "data" in request.data.keys():
                feature_data = request.data.get("data")
            else:
                feature_data = self.cp.get_all_data(lat, long)

            predictions = self.cp.predict(feature_data, useNPK=useNPK)
        except TypeError:
            return Response(
                "No Soil / Weather Data OR Bad Data found for this location",
                status=status.HTTP_404_NOT_FOUND,
            )
        except:
            return Response(
                "Something went wrong/Missing Data/Soil or Weather API Down",
                status=status.HTTP_400_BAD_REQUEST,
            )

        # At this point Predictions is a list of dictionaries in the form [ {probability:int, name:string} ]

        for i in range(len(predictions)):
            name = predictions[i]["crop_name"]
            name = name.replace(" ", "")
            crop = Crop.objects.get(name__iexact=name)
            predictions[i]["crop"] = CropSerializer(crop).data

        return Response(
            {"feature_data": feature_data, "predictions": predictions},
            status=status.HTTP_200_OK,
        )
