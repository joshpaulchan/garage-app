from devstack.deploy import Deployment

from .models import Application
from .usecases import ApplicationService


def to_application(devstack_service):
    return Application(id=devstack_service, name=devstack_service)


def group_by(items, key_fn, merge_fn=lambda existing, curr: existing.append(curr)):
    results = {}

    for item in items:
        key = key_fn(item)
        group = results.setdefault(key, [])
        merge_fn(group, item)

    return results


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
        targets_for_cluster = group_by(
            deploy_targets, key_fn=lambda tgt: tgt.cluster_id
        )
        for cluster_id, targets in targets_for_cluster.items():
            cluster = self._get_cluster(cluster_id)
            deploy_request = {t.application_id: t.version for t in targets}
            cluster.deploy(deploy_request=deploy_request)

        return deploy_targets

    def _get_cluster(self, cluster_id):
        if cluster_id not in self.devstack_cache:
            devstack = Deployment(cluster_id)  # cluster_id = devstack_name
            devstack.collect_apps()
            self.devstack_cache[cluster_id] = devstack
        return self.devstack_cache[cluster_id]
