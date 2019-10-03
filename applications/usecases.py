class ApplicationService:
    def get_applications_for_cluster(self, cluster_id):
        raise NotImplementedError()

    def deploy(self, deploy_targets):
        raise NotImplementedError()


class GetApplicationsForCluserUseCase:
    def __init__(self, application_service: ApplicationService):
        self.application_service = application_service

    def __call__(self, use_case_request):
        cluster_id = use_case_request.get("cluster_id")

        return self.application_service.get_applications_for_cluster(
            cluster_id=cluster_id
        )


class DeployApplicationsUseCase:
    def __init__(self, application_service: ApplicationService):
        self.application_service = application_service

    def __call__(self, use_case_request):
        targets = use_case_request.get("targets")

        response = self.application_service.deploy(deploy_targets=targets)

        return {"targets": []}
