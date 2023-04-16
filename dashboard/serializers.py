from django.db import models
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from rest_framework import serializers

from .models import CSVFile, Dashboard, Visualization
from .tasks import ingest_csv


class CSVFileSerializer(serializers.ModelSerializer):
    """
    Serializer to handle CSV file uploads.
    """

    name = serializers.CharField(read_only=True)

    class Meta:
        model = CSVFile
        fields = "__all__"

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="file",
                location=OpenApiParameter.QUERY,
                description="CSV file to be uploaded",
                required=True,
                type=OpenApiTypes.BINARY,
            )
        ]
    )
    def create(self, validated_data: dict) -> CSVFile:
        """
        Handle CSV file upload and create Data instances for each row
        """
        csv_file = validated_data["file"]
        # Create CSVFile object
        csv_instance = CSVFile.objects.create(name=csv_file.name, file=csv_file)

        ingest_csv.delay(csv_instance.pk)  # call the Celery task (async)

        return csv_instance


class CSVSummarySerializer(serializers.ModelSerializer):
    """
    Serializer to handle CSV file summary stats.
    """

    data_count = serializers.SerializerMethodField()
    summary_stats = serializers.SerializerMethodField()

    class Meta:
        model = CSVFile
        fields = "__all__"

    def get_data_count(self, obj: CSVFile) -> int:
        """Related Data count"""
        return obj.data.count()

    def get_summary_stats(self, obj: CSVFile) -> dict:
        """Summary statistics for related Data"""
        return obj.data.aggregate(
            avg_review_time=models.Avg("review_time"),
            avg_merge_time=models.Avg("merge_time"),
            min_review_time=models.Min("review_time"),
            min_merge_time=models.Min("merge_time"),
            max_review_time=models.Max("review_time"),
            max_merge_time=models.Max("merge_time"),
        )


class VisualizationSerializer(serializers.ModelSerializer):
    """Serializer for Visualization model
    Used to create new visualization objects for a dashboard
    """

    class Meta:
        model = Visualization
        fields = "__all__"


class DashboardSerializer(serializers.ModelSerializer):
    """Serializer for Dashboard model
    Used to create new dashboard objects, and to retrieve existing ones
    Dashboards can be retrieved by its permalink
    """

    permalink = serializers.CharField(read_only=True)

    class Meta:
        model = Dashboard
        fields = "__all__"