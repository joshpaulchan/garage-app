from django.urls import path

from . import views

urlpatterns = [
    path(
        "<str:cluster_id>",
        views.get_applications_for_cluster,
        name="get_applications_for_cluster",
    )
]
