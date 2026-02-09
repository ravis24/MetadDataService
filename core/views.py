from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from rest_framework import generics
from .models import Dataset, DataElement
from .serializers import (
    DatasetSerializer,
    DatasetDetailSerializer,
    DataElementSerializer
)


class DatasetAPIView(APIView):

    def get(self, request):
        datasets = Dataset.objects.all()
        serializer = DatasetSerializer(datasets, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DatasetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class DatasetDetailAPIView(APIView):

    def get_object(self, pk):
        try:
            return Dataset.objects.get(pk=pk)
        except Dataset.DoesNotExist:
            return None
    

    def get(self, request, pk):
        dataset = self.get_object(pk)
        if not dataset:
            return Response(
                {"error": "Dataset not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = DatasetDetailSerializer(dataset)
        return Response(serializer.data)
    
    def put(self, request, pk):
        dataset = self.get_object(pk)
        if not dataset:
            return Response(
                {"error": "Dataset not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = DatasetSerializer(dataset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def delete(self, request, pk):
        dataset = self.get_object(pk)
        if not dataset:
            return Response(
                {"error": "Dataset not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        dataset.delete()
        return Response(
            {"message": "Dataset deleted successfully"},
            status=status.HTTP_204_NO_CONTENT
        )


class DataElementAPIView(APIView):

    def get(self, request, dataset_id):
        elements = DataElement.objects.filter(dataset_id=dataset_id)
        serializer = DataElementSerializer(elements, many=True)
        return Response(serializer.data)

    def post(self, request, dataset_id):
        serializer = DataElementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(dataset_id=dataset_id)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )







