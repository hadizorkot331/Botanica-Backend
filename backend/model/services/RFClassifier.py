import pandas as pd
import joblib


pickle_data = joblib.load(
    "/Users/hadizorkot/Documents/AUB/Sem 4/CMPS 271/Botanica/backend/model/services/Crop_RandomForest_Classifier_V1.pkl"
)

labels = pickle_data["numbers_to_labels"].values()
classifier = pickle_data["model"]
classifier_no_NPK = pickle_data["model_no_NPK"]


class RFModel:
    def get_prediction_probabilities(self, data, useNPK=True):
        if useNPK:
            predictions = classifier.predict_proba(pd.DataFrame(data, index=[0]))[0]
        else:
            data.pop("N")
            data.pop("P")
            data.pop("K")
            predictions = classifier_no_NPK.predict_proba(
                pd.DataFrame(data, index=[0])
            )[0]
        zipped_predictions = list(zip(predictions.tolist(), labels))
        zipped_predictions.sort(reverse=True)
        return zipped_predictions


# test_data = {
#     "N": 90,
#     "P": 40,
#     "K": 32,
#     "temperature": 24,
#     "humidity": 82.03,
#     "ph": 7.2,
#     "rainfall": 200,
# }
# p = Predictor()
# prediction = p.predict(test_data)
# print(prediction)
