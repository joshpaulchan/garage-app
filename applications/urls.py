from django.urls import path

from . import views

urlpatterns = [
    path(
        "<str:cluster_id>",
        views.get_applications_for_cluster,
        name="get_applications_for_cluster",
    ),
    path(
        "<str:cluster_id>/deploy",
        views.deploy_applications_to_cluster,
        name="deploy_applications_to_cluster",
    ),
    path(
        "<str:cluster_id>/states",
        views.update_application_states,
        name="update_application_states",
    ),
]
