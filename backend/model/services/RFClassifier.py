import pandas as pd
import joblib
from pathlib import Path

script_dir = Path(__file__).resolve().parent

pickle_path = script_dir / 'Crop_RandomForest_Classifier_V1.pkl'

pickle_data = joblib.load(pickle_path)

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

        zipped_list = list(zip(predictions.tolist(), labels))
        zipped_list.sort(reverse=True)
        zipped_predictions = list(
            {"probability": probability, "crop_name": crop_name}
            for probability, crop_name in zipped_list
        )
        return zipped_predictions