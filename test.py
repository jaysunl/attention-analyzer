from hume import HumeBatchClient
from hume.models.config import FaceConfig

client = HumeBatchClient("Dlu0ioQnAGA3pKAhrGHAswQ2HFJ76jcl5FwZGGpGVAs6gjFu")
filepaths = [
    "faces.zip",
    "david_hume.jpeg",
]
config = FaceConfig()
job = client.submit_job(None, [config], files=filepaths)

print(job)
print("Running...")

details = job.await_complete()
job.download_predictions("predictions.json")
print("Predictions downloaded to predictions.json")
