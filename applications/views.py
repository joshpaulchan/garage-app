from django.http import JsonResponse

from .services import DevstackApplicationService
from .usecases import GetApplicationsForCluserUseCase

# Create your views here.

application_service = DevstackApplicationService()
get_applications_for_cluster_use_case = GetApplicationsForCluserUseCase(
    application_service=application_service
)


def get_applications_for_cluster(request, cluster_id):
    use_case_request = {"cluster_id": cluster_id}
    apps = get_applications_for_cluster_use_case(use_case_request)

    return JsonResponse({"applications": [app.to_dict() for app in apps]})
