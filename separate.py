import face_recognition
from PIL import Image

def save_faces(image_path, output_dir):
    image = face_recognition.load_image_file(image_path)
    
    face_locations = face_recognition.face_locations(image)
    
    pil_image = Image.open(image_path)
    
    for i, face_location in enumerate(face_locations):
        top, right, bottom, left = face_location
        face_image = pil_image.crop((left, top, right, bottom))
        
        face_image.save(f"{output_dir}/face_{i+1}.jpg")

def separate_faces():
    input_image_path = "/home/jsliang@AD.UCSD.EDU/attention-analyzer/image.jpg"
    output_directory = "output_faces"

    save_faces(input_image_path, output_directory)
