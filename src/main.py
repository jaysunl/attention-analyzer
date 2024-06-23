import os

from hume import HumeBatchClient
from hume.models.config import FaceConfig
from separate import separate_faces

'''
Separate the faces, then perform emotion inference on each face
'''
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

if __name__ == "__main__":
	main()


