import logging
from typing import Sequence

from devstack.deploy import Deployment

from .models import Application, ApplicationState, StateTarget
from .usecases import ApplicationService

logger = logging.getLogger()


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
    SUPPORTED_STATE_OPERATIONS = {ApplicationState.RESTARTING}

    def __init__(self):
        self.devstack_cache = {}
        self.applications_for_cluster_cache = {}

    def get_applications_for_cluster(self, cluster_id):
        applications = self._get_or_save_applications_in_cluster(cluster_id)

        return applications

    def deploy(self, deploy_targets):
        targets_for_cluster = group_by(
            deploy_targets, key_fn=lambda tgt: tgt.cluster_id
        )
        for cluster_id, targets in targets_for_cluster.items():
            cluster = self._get_cluster(cluster_id)
            deploy_request = {t.application_id: t.version for t in targets}
            cluster.deploy(deploy_request=deploy_request)

        return deploy_targets

    def update_states(self, state_targets: Sequence[StateTarget]):
        targets_for_cluster = group_by(state_targets, key_fn=lambda tgt: tgt.cluster_id)

        for cluster_id, targets in targets_for_cluster.items():
            cluster = self._get_cluster(cluster_id)

            for target in targets:
                if target.state in self.SUPPORTED_STATE_OPERATIONS:
                    self._apply_state_operation(cluster, cluster_id, target)
                else:
                    logger.log(f"Unsupported operation:{target}")

        return state_targets

    def _get_or_save_applications_in_cluster(self, cluster_id):
        if cluster_id in self.applications_for_cluster_cache:
            return self.applications_for_cluster_cache.get(cluster_id)

        cluster = self._get_cluster(cluster_id)
        services_and_versions = cluster.get_versions(current_only=True)

        applications_in_cluster = []
        for service_name, version in services_and_versions:
            applications_in_cluster.append(
                Application(id=service_name, name=service_name, version=version)
            )

        self.applications_for_cluster_cache[cluster_id] = applications_in_cluster

        return applications_in_cluster

    def _get_cluster(self, cluster_id):
        if cluster_id not in self.devstack_cache:
            devstack = Deployment(cluster_id)  # cluster_id = devstack_name
            devstack.collect_apps()
            self.devstack_cache[cluster_id] = devstack
        return self.devstack_cache[cluster_id]

    def _apply_state_operation(self, cluster, cluster_id, target_state):
        if target_state.state == ApplicationState.RESTARTING:
            # "Restart" by deploying the same version as currently deployed
            applications = self._get_or_save_applications_in_cluster(cluster_id)
            app = next(
                filter(lambda app: app.id == target_state.application_id, applications),
                None,
            )
            cluster.deploy(deploy_request={target_state.application_id: app.version})
