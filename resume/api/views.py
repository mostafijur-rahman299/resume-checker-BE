import fitz  # PyMuPDF
import tempfile
import os
import spacy
from docx import Document
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from resume.resume_parser import ResumeParser


class ResumeUploadView(APIView):
    parser_classes = (MultiPartParser,)

    def extract_text(self, file_path, file_type):
        try:
            if file_type == 'pdf':
                # Open the uploaded PDF using PyMuPDF
                doc = fitz.open(file_path)
                extracted_text = ""
                for page in doc:
                    extracted_text += page.get_text()
            elif file_type == 'docx':
                # Open the uploaded DOCX using python-docx
                doc = Document(file_path)
                extracted_text = ""
                for para in doc.paragraphs:
                    extracted_text += para.text

            return True, extracted_text

        except Exception as e:
            return False, str(e)

        finally:
            # Clean up the temporary file after processing
            if os.path.exists(file_path):
                os.remove(file_path)

    def process_text(self, text):
        # Create the ResumeParser instance
        parser = ResumeParser()

        # Process the text to get a spaCy doc object
        doc = parser.process_text(text)

        # Extract structured data
        return parser.extract_data(doc)


    def post(self, request):
        file = request.FILES.get('file')

        if not file:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        file_type = file.name.split('.')[-1].lower()
        if file_type not in ['pdf', 'docx']:
            return Response({'error': 'Unsupported file type'}, status=status.HTTP_400_BAD_REQUEST)

        # Save the file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix='.' + file_type) as temp_file:
            for chunk in file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name
        
        success, response = self.extract_text(temp_file_path, file_type)
        if not success:
            return Response({'error': response}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        resume_data = self.process_text(response)

        return Response({'extracted_text': resume_data}, status=status.HTTP_200_OK)        
