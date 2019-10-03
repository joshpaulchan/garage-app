import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import DeployTarget
from .services import DevstackApplicationService
from .usecases import GetApplicationsForCluserUseCase, DeployApplicationsUseCase

# Create your views here.

application_service = DevstackApplicationService()
get_applications_for_cluster_use_case = GetApplicationsForCluserUseCase(
    application_service=application_service
)
deploy_applications_to_cluster_use_case = DeployApplicationsUseCase(
    application_service=application_service
)


def get_applications_for_cluster(request, cluster_id):
    use_case_request = {"cluster_id": cluster_id}
    apps = get_applications_for_cluster_use_case(use_case_request)

    return JsonResponse({"applications": [app.to_dict() for app in apps]})


@require_POST
@csrf_exempt
def deploy_applications_to_cluster(request, cluster_id):
    body = json.loads(request.body)

    targets = [
        DeployTarget(
            cluster_id=cluster_id,
            application_id=target.get("application_id"),
            version=target.get("version"),
        )
        for target in body.get("targets", [])
    ]

    use_case_request = {"targets": targets}
    response = deploy_applications_to_cluster_use_case(use_case_request)

    return JsonResponse(response)


@require_POST
@csrf_exempt
def update_application_states(request, cluster_id):
    body = json.loads(request.body)

    target_states = []
    for target in body.get("target_states", []):
        try:
            state = StateTarget(
                cluster_id=cluster_id,
                application_id=target.get("application_id"),
                state=ApplicationState[target.get("state")],
            )
            target_states.append(state)
        except KeyError:
            pass

    use_case_request = {"target_states": target_states}
    response = set_application_states_use_case(use_case_request)

    return JsonResponse(response)
