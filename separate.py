import face_recognition
from PIL import Image
#import cv2

def save_faces(image_path, output_dir):
    try:
        image = face_recognition.load_image_file(image_path)

        # if len(image.shape) == 2:
        #     image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)    
        # elif len(image.shape) == 3 and image.shape[2] == 4:
        #     image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    
        face_locations = face_recognition.face_locations(image)
        
        pil_image = Image.open(image_path)
        
        for i, face_location in enumerate(face_locations):
            top, right, bottom, left = face_location
            face_image = pil_image.crop((left, top, right, bottom))
            
            face_image.save(f"{output_dir}/face_{i+1}.jpg")
        print(f"Saved {len(face_locations)} from {image_path} to {output_dir}")
    
    except Exception as e:
        print(f"Error processing {image_path}: {e}")

def separate_faces():
    input_image_path = "image.jpg"
    output_directory = "output_faces"

    save_faces(input_image_path, output_directory)
