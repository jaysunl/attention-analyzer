import os
import json

from hume import HumeBatchClient
from hume.models.config import FaceConfig
from separate import separate_faces
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('Agg')

def get_relevant_emotions(json_file):
	emotions_map = {}
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
							emotions_map[filename] = {}
							for emotion in emotions:
								if emotion['name'] in target_emotions:
									emotions_map[filename][emotion['name']] = emotion['score']
									# print(f"{emotion['name']}: {emotion['score']}")
							# print()
	return emotions_map

def gen_plot(data):
	emotions = list(data[next(iter(data))].keys())
	filenames = list(data.keys())

	# Convert data to array for plotting
	values = np.array([[data[filename][emotion] for emotion in emotions] for filename in filenames])

	# Bar width and positions
	bar_width = 0.12
	positions = np.arange(len(emotions))

	# Colors
	colors = plt.cm.get_cmap('tab20', len(filenames))

	# Plotting
	fig = plt.figure(figsize=(14, 8))
	ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

	for i, filename in enumerate(filenames):
		ax.bar(positions + i * bar_width, values[i], bar_width, label=filename, color=colors(i))

	# Formatting
	ax.set_xlabel('Emotions')
	ax.set_ylabel('Scores')
	ax.set_title('Emotion Scores for Different Faces')
	ax.set_xticks(positions + bar_width * (len(filenames) - 1) / 2)
	ax.set_xticklabels(emotions, rotation=45, ha='right')
	ax.legend()

	# Making it pretty
	plt.grid(axis='y', linestyle='--', alpha=0.7)
	plt.tight_layout()
	image_file = 'emotion_scores.png'
	# Save the plot as an image file
	plt.savefig(image_file)

	# Display plot
	# plt.show()
	return image_file

def pipeline(input_image_path):
	separate_faces(input_image_path)
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
	emotions_map = get_relevant_emotions("predictions.json")
	image_file = gen_plot(emotions_map)
	return image_file 



