from devstack.deploy import Deployment

from .models import Application
from .usecases import ApplicationService


def to_application(devstack_service):
    return Application(id=devstack_service, name=devstack_service)


class DevstackApplicationService(ApplicationService):
    def __init__(self):
        self.devstack_cache = {}

    def get_applications_for_cluster(self, cluster_id):
        devstack = self._get_cluster(cluster_id)
        services_and_versions = devstack.get_versions(current_only=True)

        return list(
            map(
                lambda service_and_version: to_application(service_and_version[0]),
                services_and_versions,
            )
        )

    def deploy(self, deploy_targets):
        print(f"deploying targets: {deploy_targets}")

        return deploy_targets

    def _get_cluster(self, cluster_id):
        if cluster_id not in self.devstack_cache:
            devstack = Deployment(cluster_id)  # cluster_id = devstack_name
            devstack.collect_apps()
            self.devstack_cache[cluster_id] = devstack
        return self.devstack_cache[cluster_id]
