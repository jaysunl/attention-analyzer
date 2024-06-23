import os
import json

from hume import HumeBatchClient
from hume.models.config import FaceConfig
from separate import separate_faces

def get_relevant_emotions(json_file):
	with open(json_file, 'r') as f:
		data = json.load(f)

	target_emotions = ["Concentration", "Contemplation", "Boredom", "Determination", 
					"Confusion", "Distress", "Doubt", "Interest", "Calmness"]

	for entry in data:
		filename = entry['source']['filename']
		predictions = entry['results']['predictions']
		
		if predictions:
			face_predictions = predictions[0]['models']['face']
			
			grouped_predictions = face_predictions['grouped_predictions']
			
			if grouped_predictions:
				for grouped_prediction in grouped_predictions:
					predictions = grouped_prediction['predictions']
					
					for prediction in predictions:
						emotions = prediction['emotions']
						if emotions:
							print(f"Filename: {filename}")
							for emotion in emotions:
								if emotion['name'] in target_emotions:
									print(f"{emotion['name']}: {emotion['score']}")
							print()

def main():
	separate_faces()
	client = HumeBatchClient("Dlu0ioQnAGA3pKAhrGHAswQ2HFJ76jcl5FwZGGpGVAs6gjFu")
	filepaths = []
	directory = "output_faces"
	for filename in os.listdir(directory):
		filepath = os.path.join(directory, filename)
		filepaths.append(filepath)
	config = FaceConfig()
	job = client.submit_job(None, [config], files=filepaths)

	print(job)
	print("Running...")

	details = job.await_complete()
	job.download_predictions("predictions.json")
	print("Predictions downloaded to predictions.json")
	get_relevant_emotions("predictions.json")

if __name__ == "__main__":
	main()


