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

    """List and create datasets."""

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

    """Retrieve, update, or delete a dataset."""

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

    """Manage data elements belonging to a dataset with filtering support."""

    def get_dataset(self, dataset_id):
        try:
            return Dataset.objects.get(pk=dataset_id)
        except Dataset.DoesNotExist:
            return None

    def get(self, request, dataset_id):
        dataset = self.get_dataset(dataset_id)
        if not dataset:
            return Response(
                {"error": "Dataset not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        elements = DataElement.objects.filter(dataset=dataset)

        # 🔍 Filtering Support
        name = request.GET.get("name")
        data_type = request.GET.get("data_type")
        is_required = request.GET.get("is_required")
        is_pii = request.GET.get("is_pii")

        if name:
            elements = elements.filter(name__icontains=name)

        if data_type:
            elements = elements.filter(data_type=data_type)

        if is_required is not None:
            elements = elements.filter(
                is_required=is_required.lower() == "true"
            )

        if is_pii is not None:
            elements = elements.filter(
                is_pii=is_pii.lower() == "true"
            )

        serializer = DataElementSerializer(elements, many=True)
        return Response(serializer.data)

    def post(self, request, dataset_id):
        dataset = self.get_dataset(dataset_id)
        if not dataset:
            return Response(
                {"error": "Dataset not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = DataElementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(dataset=dataset)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )









