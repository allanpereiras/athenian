import pandas as pd
from django.db import models
from django.utils.text import slugify
from django_extensions.db.models import TimeStampedModel


class CSVFile(TimeStampedModel):
    """Uploaded CSV file model"""

    name = models.CharField(max_length=100)
    file = models.FileField(upload_to="csvfiles/")

    def __str__(self) -> str:
        return self.name

    def delete(self, *args, **kwargs):
        """
        Overriding delete method to delete the CSV file as well.
        """
        if self.file:
            self.file.delete()
        super().delete(*args, **kwargs)

    @property
    def read_to_dataframe(self):
        """
        Load the CSV file and return a pandas DataFrame object.
        """
        return pd.read_csv(self.file.path)


class Data(TimeStampedModel):
    """Data model / Table schema for dashboard data"""

    review_time = models.IntegerField()
    team = models.CharField(max_length=50)
    date = models.DateField()
    merge_time = models.IntegerField()
    from_csv = models.ForeignKey(CSVFile, on_delete=models.CASCADE, related_name="data")

    class Meta:
        verbose_name_plural = "Data"

    def __str__(self) -> str:
        return f"{self.id}"


class Dashboard(TimeStampedModel):
    """A Dashboard aggregate visualizations and data sources.
    Can be shared with other users via its permalink value.
    """

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    permalink = models.CharField(max_length=255, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.permalink:
            # Generate permalink if it doesn't exist
            self.permalink = self.generate_unique_permalink()
        super().save(*args, **kwargs)

    def generate_unique_permalink(self) -> str:
        """
        Generate a unique permalink using the model's name field.
        """
        base_permalink = slugify(self.name)
        unique_permalink = base_permalink
        num = 1

        while Dashboard.objects.filter(permalink=unique_permalink).exists():
            # Append a number to the permalink if it's not unique
            unique_permalink = f"{base_permalink}-{num}"
            num += 1

        return unique_permalink

    def __str__(self) -> str:
        return self.name


class VisualizationType(models.TextChoices):
    """Visualization types"""

    BAR = "bar", "Bar"
    LINE = "line", "Line"
    PIE = "pie", "Pie"
    SCATTER = "scatter", "Scatter"


class Visualization(TimeStampedModel):
    """Visualization model"""

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    type = models.CharField(max_length=15, choices=VisualizationType.choices)
    from_csv = models.ForeignKey(
        CSVFile, on_delete=models.PROTECT, related_name="visualizations"
    )
    dashboard = models.ForeignKey(
        Dashboard, on_delete=models.CASCADE, related_name="visualizations"
    )

    def __str__(self) -> str:
        return self.name
