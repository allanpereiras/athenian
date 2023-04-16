from django.contrib import admin

from .models import CSVFile, Dashboard, Data, Visualization


@admin.register(CSVFile)
class CSVFileAdmin(admin.ModelAdmin):
    list_display = ("id", "created", "modified", "name", "file")
    list_filter = ("created", "modified")
    search_fields = ("name",)


@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "created",
        "modified",
        "review_time",
        "team",
        "date",
        "merge_time",
        "from_csv",
    )
    list_filter = ("created", "modified", "date", "from_csv")


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    list_display = ("id", "created", "modified", "name", "description", "permalink")
    list_filter = ("created", "modified")
    search_fields = ("name", "description", "permalink")


@admin.register(Visualization)
class VisualizationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "type",
        "name",
        "description",
        "from_csv",
        "dashboard",
        "created",
        "modified",
    )
    list_filter = ("type", "created", "modified", "from_csv", "dashboard")
    search_fields = ("name", "description", "permalink")
