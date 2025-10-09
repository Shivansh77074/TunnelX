# """
# Face Recognition Service for SecureSession
# """
# import face_recognition
# from PIL import Image
# import numpy as np
# from io import BytesIO

# class FaceService:
#     """Face recognition service for biometric authentication."""

#     def __init__(self):
#         self.tolerance = 0.6
#         self.model = 'hog'  # or 'cnn' for better accuracy but slower

#     def extract_face_encoding(self, image_data: bytes) -> list:
#         """Extract face encoding from image data."""
#         try:
#             # Load image
#             image = face_recognition.load_image_file(BytesIO(image_data))

#             # Get face encodings
#             face_encodings = face_recognition.face_encodings(image, model=self.model)

#             if len(face_encodings) == 0:
#                 raise ValueError("No face found in image")
#             elif len(face_encodings) > 1:
#                 raise ValueError("Multiple faces found in image")

#             return face_encodings[0].tolist()

#         except Exception as e:
#             raise ValueError(f"Face processing failed: {str(e)}")

#     def compare_faces(self, known_encoding: list, test_encoding: list) -> bool:
#         """Compare two face encodings."""
#         try:
#             known_np = np.array(known_encoding)
#             test_np = np.array(test_encoding)

#             matches = face_recognition.compare_faces([known_np], test_np, tolerance=self.tolerance)
#             return matches[0]

#         except Exception as e:
#             print(f"Face comparison error: {e}")
#             return False

#     def validate_image(self, image_data: bytes) -> bool:
#         """Validate if image is suitable for face recognition."""
#         try:
#             # Check if image can be loaded
#             image = Image.open(BytesIO(image_data))

#             # Check image size (minimum requirements)
#             if image.width < 100 or image.height < 100:
#                 return False

#             # Check if image format is supported
#             if image.format not in ['JPEG', 'PNG', 'BMP']:
#                 return False

#             return True

#         except Exception:
#             return False
