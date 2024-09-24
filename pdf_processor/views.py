from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import ExtractedData
from .serializers import ExtractedDataSerializer
import nltk
from pdfminer.high_level import extract_text

class PDFUploadView(APIView):
    def post(self, request, *args, **kwargs):
        pdf_file = request.FILES.get('file')
        email = request.data.get('email')

        if not pdf_file or not email:
            return Response({'error': 'File or email missing'}, status=status.HTTP_400_BAD_REQUEST)

        # Extract text from PDF
        text = extract_text(pdf_file)

        # NLTK processing to find nouns and verbs
        words = nltk.word_tokenize(text)
        tagged_words = nltk.pos_tag(words)

        nouns = [word for word, pos in tagged_words if pos.startswith('NN')]
        verbs = [word for word, pos in tagged_words if pos.startswith('VB')]

        extracted_data = {
            'email': email,
            'nouns': ', '.join(nouns),
            'verbs': ', '.join(verbs),
        }

        # Save extracted data
        serializer = ExtractedDataSerializer(data=extracted_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
