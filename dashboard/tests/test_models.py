from datetime import date

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from ..models import CSVFile, Dashboard, Data


class CSVFileModelTest(TestCase):
    def setUp(self) -> None:
        self.csv_file = SimpleUploadedFile(
            name="test.csv",
            content=b"review_time,team,date,merge_time\n1,team1,2022-04-10,2\n3,team2,2022-04-11,4\n",
            content_type="text/csv",
        )
        self.csv_file_obj = CSVFile.objects.create(name="test.csv", file=self.csv_file)

    def tearDown(self) -> None:
        if self.csv_file_obj.file:
            self.csv_file_obj.file.delete()

    def test_csv_file_str_method(self) -> None:
        self.assertEqual(str(self.csv_file_obj), "test.csv")

    def test_csv_file_delete_method(self) -> None:
        if self.csv_file_obj.file:
            self.csv_file_obj.file.storage.delete(self.csv_file_obj.file.name)
        self.csv_file_obj.delete()
        self.assertFalse(self.csv_file_obj.id)

    def test_csv_file_read_to_dataframe_property(self) -> None:
        df = self.csv_file_obj.read_to_dataframe
        self.assertEqual(len(df), 2)
        self.assertListEqual(
            list(df.columns), ["review_time", "team", "date", "merge_time"]
        )


class DataModelTest(TestCase):
    def setUp(self) -> None:
        self.csv_file = CSVFile.objects.create(
            name="test.csv",
            file=SimpleUploadedFile(
                name="test.csv",
                content=b"review_time,team,date,merge_time\n1,team1,2022-04-10,2\n3,team2,2022-04-11,4\n",
                content_type="text/csv",
            ),
        )
        self.data = Data.objects.create(
            review_time=1,
            team="team1",
            date=date(2022, 4, 10),
            merge_time=2,
            from_csv=self.csv_file,
        )

    def tearDown(self) -> None:
        self.csv_file.delete()
        self.data.delete()

    def test_data_model(self) -> None:
        self.assertEqual(str(self.data), f"{self.data.id}")
        self.assertEqual(self.data.review_time, 1)
        self.assertEqual(self.data.team, "team1")
        self.assertEqual(self.data.date, date(2022, 4, 10))
        self.assertEqual(self.data.merge_time, 2)
        self.assertEqual(self.data.from_csv, self.csv_file)


class DashboardModelTest(TestCase):
    def setUp(self) -> None:
        self.dashboard = Dashboard.objects.create(
            name="test dashboard", description="test description"
        )

    def tearDown(self) -> None:
        self.dashboard.delete()

    def test_dashboard_model(self) -> None:
        self.assertEqual(str(self.dashboard), "test dashboard")
        self.assertEqual(self.dashboard.name, "test dashboard")
        self.assertEqual(self.dashboard.description, "test description")
