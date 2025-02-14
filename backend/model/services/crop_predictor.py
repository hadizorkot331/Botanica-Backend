import requests
from datetime import datetime
from . import RFClassifier


class CropPredictor:
    classifier = RFClassifier.RFModel()
    soil_api_url = "https://api.openepi.io/soil/property"
    historical_weather_api_url = "https://archive-api.open-meteo.com/v1/archive"

    def estimate_P(self, n, cec, ph):
        return 0.02 + 0.5 * n + 0.03 * cec - 0.1 * (ph - 6.5)

    def estimate_K(self, n, cec, ph):
        return 0.05 + 0.2 * n + 0.05 * cec + 0.1 * (ph - 6.5)

    def get_soil_data(self, lat, long):
        response = requests.get(
            self.soil_api_url,
            params={
                "lat": lat,
                "lon": long,
                "depths": "5-15cm",
                "properties": ["bdod", "cec", "nitrogen", "phh2o"],
                "values": "mean",
            },
        )

        data = response.json()
        dic = {}
        for layer in data["properties"]["layers"]:
            code = layer["code"]
            mean = layer["depths"][0]["values"]["mean"] / 10
            dic[code] = mean

        k = self.estimate_K(dic["nitrogen"], dic["cec"], dic["phh2o"])
        p = self.estimate_P(dic["nitrogen"], dic["cec"], dic["phh2o"])

        results = {
            "N": dic["nitrogen"],
            "P": p,
            "K": k,
            "ph": dic["phh2o"],
        }

        return results

    def get_weather_data(self, lat, long):
        # Get delta for a year
        current_year = datetime.now().year
        start_date = f"{current_year - 1}-01-01"
        end_date = f"{current_year - 1}-12-31"

        # Parameters for weather data
        params = {
            "latitude": lat,
            "longitude": long,
            "start_date": start_date,
            "end_date": end_date,
            "daily": [
                "precipitation_sum",
                "temperature_2m_mean",
                "relative_humidity_2m_mean",
            ],
            "timezone": "auto",
        }

        response = requests.get(self.historical_weather_api_url, params=params)
        data = response.json()

        # Extract data
        precipitation = data["daily"]["precipitation_sum"]
        temperature = data["daily"]["temperature_2m_mean"]
        humidity = data["daily"]["relative_humidity_2m_mean"]

        # Calculate total rainfall, average temperature, and average humidity
        annual_rainfall = sum(precipitation) / 10
        average_temperature = sum(temperature) / len(temperature)
        average_humidity = sum(humidity) / len(humidity)

        return {
            "temperature": average_temperature,
            "humidity": average_humidity,
            "rainfall": annual_rainfall,
        }

    def get_ordered_soil_and_weather_data(self, soil_dict, weather_dict):
        return {
            "N": soil_dict["N"],
            "P": soil_dict["P"],
            "K": soil_dict["K"],
            "temperature": weather_dict["temperature"],
            "humidity": weather_dict["humidity"],
            "ph": soil_dict["ph"],
            "rainfall": weather_dict["rainfall"],
        }

    def get_all_data(self, lat, long):
        soil_dict = self.get_soil_data(lat, long)
        weather_dict = self.get_weather_data(lat, long)

        return self.get_ordered_soil_and_weather_data(soil_dict, weather_dict)

    def predict(self, data, useNPK=True):
        # print(data)
        return self.classifier.get_prediction_probabilities(data, useNPK=useNPK)


# cp = CropPredictor()
# print(cp.predict(cp.get_all_data(35.113234, 34.212334), useNPK=True))
