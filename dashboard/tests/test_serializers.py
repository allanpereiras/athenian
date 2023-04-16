from typing import Dict

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from ..models import CSVFile, Data
from ..serializers import CSVFileSerializer, CSVSummarySerializer


class CSVFileSerializerTest(TestCase):
    def test_create_csv_file(self) -> None:
        csv_content = b"review_time,team,date,merge_time\n1,team1,2022-04-10,2\n3,team2,2022-04-11,4\n"
        csv_file = SimpleUploadedFile("test.csv", csv_content, content_type="text/csv")
        data: Dict[str, SimpleUploadedFile] = {"file": csv_file}
        serializer = CSVFileSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        csv_file = serializer.save()
        self.assertIsInstance(csv_file, CSVFile)
        self.assertEqual(csv_file.name, "test.csv")
        self.assertIsNotNone(csv_file.file)

    def test_create_csv_file_with_invalid_data(self) -> None:
        data: Dict[str, str] = {"invalid_field": "invalid_data"}

        serializer = CSVFileSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("file", serializer.errors)


class CSVSummarySerializerTest(TestCase):
    def setUp(self) -> None:
        self.maxDiff = None  # Show full diff in case of failure
        csv_content = b"review_time,team,date,merge_time\n1,team1,2022-04-10,2\n3,team2,2022-04-11,4\n"
        csv_file = SimpleUploadedFile("test.csv", csv_content, content_type="text/csv")
        self.csv_file_obj = CSVFile.objects.create(name="test.csv", file=csv_file)

        self.data = Data.objects.create(
            from_csv=self.csv_file_obj,
            team="test_team",
            review_time=10,
            merge_time=20,
            date="2022-04-10",
        )

    def tearDown(self) -> None:
        if self.csv_file_obj.file:
            self.csv_file_obj.file.delete()

    def test_csv_summary_serializer(self) -> None:
        # Serialize the CSVFile object using the CSVSummarySerializer
        serializer = CSVSummarySerializer(self.csv_file_obj)
        # Check the serialized data
        expected_data: Dict[str, str] = {
            "id": self.csv_file_obj.id,
            "file": self.csv_file_obj.file.url,
            "name": "test.csv",
            "data_count": 1,
            "summary_stats": {
                "avg_review_time": self.data.review_time,
                "avg_merge_time": self.data.merge_time,
                "min_review_time": self.data.review_time,
                "min_merge_time": self.data.merge_time,
                "max_review_time": self.data.review_time,
                "max_merge_time": self.data.merge_time,
            },
            "created": self.csv_file_obj.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "modified": self.csv_file_obj.modified.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }
        self.assertDictEqual(serializer.data, expected_data)
