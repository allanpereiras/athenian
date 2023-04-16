from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import generics, parsers

from . import models, serializers


@extend_schema(
    tags=["CSV Upload"],
    request={
        "multipart/form-data": {
            "type": "object",
            "properties": {
                "file": {"type": "string", "format": "binary"},
            },
        }
    },
)
class CSVUploadView(generics.CreateAPIView):
    """
    View to handle CSV file uploads via POST requests.
    """

    parser_class = (parsers.FileUploadParser, parsers.MultiPartParser)
    serializer_class = serializers.CSVFileSerializer


class CSVSummaryView(generics.RetrieveAPIView):
    """
    View to handle CSV file summary stats via GET requests.
    """

    serializer_class = serializers.CSVSummarySerializer
    queryset = models.CSVFile.objects.all()
    lookup_fields = ["id"]

    @extend_schema(
        description="Retrieve the summary statistics of a CSV file",
        parameters=[
            OpenApiParameter(
                name="id",
                type=int,
                location=OpenApiParameter.PATH,
                description="ID of the CSV file to retrieve summary stats for",
            )
        ],
        responses={200: serializers.CSVSummarySerializer},
        tags=["CSV Summary"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@extend_schema(
    tags=["Visualization"]
)
class VisualizationsAPIView(generics.CreateAPIView):
    serializer_class = serializers.VisualizationSerializer


@extend_schema(
    tags=["Dashboards"]
)
class DashboardAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.DashboardSerializer
    queryset = models.Dashboard.objects.all()
    lookup_fields = ["id", "permalink"]
