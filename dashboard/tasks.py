

from celery import shared_task
from dashboard.models import CSVFile, Data


@shared_task()
def ingest_csv(csv_instance: int) -> int:
    """Ingest CSV file data into Data model"""
    csv_file = CSVFile.objects.get(pk=csv_instance)
    data_objs = [
        Data(
            review_time=row["review_time"],
            team=row["team"],
            date=row["date"],
            merge_time=row["merge_time"],
            from_csv=csv_file,
        )
        for _, row in csv_file.read_to_dataframe.iterrows()
    ]
    Data.objects.bulk_create(data_objs)
    return len(data_objs)