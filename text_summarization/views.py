from django.shortcuts import render
from matplotlib.pyplot import text
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import TextSerializer, InputSerializer
from . import models
from rest_framework import status

class TextInstanceGetView(GenericAPIView):
   # permission_classes = (IsAuthenticated,)
    serializer_class = TextSerializer
    
    def get(self, request):
        text = models.text.objects.all().order_by('created_at')
        if len(text)== 0:
            return Response(list(), status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.serializer_class(text, many=True)
            self.queryset = serializer
        return Response(serializer.data, status = status.HTTP_200_OK)
        

class TextDeleteOneView(GenericAPIView):
    #permission_classes = (IsAuthenticated,)

    def delete(self, request, text_id):
        text = models.text.objects.get(id = text_id)
        if text:
            text.delete()
        else:
            return Response("No video found! " + str(text),status=status.HTTP_400_BAD_REQUEST)
        return Response("Deleted!",status=status.HTTP_201_CREATED)

       
class TextGetOneView(GenericAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = TextSerializer
    def get(self, request, text_id):
        text = models.text.objects.get(id = text_id)
        serializer = self.serializer_class(text, many=False)
        return Response(serializer.data)

class TextUploadView(GenericAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = TextSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('error', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TextUpdateView(GenericAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = TextSerializer
    def post(self,request, text_id):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            text = models.text.objects.get(id = text_id)
            text.raw_text = serializer.data['raw_text']
            text.summary = serializer.data['summary']
            text.labels = serializer.data['labels']
            text.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('error', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class InputView(GenericAPIView):
    serializer_class = InputSerializer

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            raw_text = serializer.data['raw_text']
            # perform AI 
            summary = 'haha'
            lable_list = ['happy']
            lable = ' '.join(str(e) for e in lable_list)
            data = {
                "raw_text": raw_text,
                "summary": summary,
                "labels": lable
            }
            text_serializer = TextSerializer(data = data)
            if text_serializer.is_valid():
                text_serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response("Created Successfully", status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)