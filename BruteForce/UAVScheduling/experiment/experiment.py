import logging

import numpy as np

from PySide2.QtCore import QObject
from PySide2.QtCore import Signal

from UAVScheduling.auxillary.generator import Generator
from UAVScheduling.experiment.world import World, WorldArea
from UAVScheduling.models import models


LOG = logging.getLogger(__name__)


class Experiment(QObject):


    def __init__(self, world, parent=None):
        """

        Args:
            world (World):
        """
        super().__init__(parent)

        self.global_visibility_radius = 200

        self._target_cluster_params = {
            'random': False,
            'value': 5.0
        }

        self.world = world

        self.total_assignment_cost = 0.0

        self._gen = Generator(self.world.area)

    @property
    def target_clusters(self):
        return self.world.get_objects(models.TargetCluster)

    def add_target_clusters(self, num=1):
        target_clusters = self._gen.many('targetCluster', num, **self._target_cluster_params)
        self.world.add(target_clusters)

    def set_targets_values(self, new_values=None, random=True):
        if random:
            new_values = np.random.randint(0, self.TARGET_MAX_VALUE,
                                           len(self.targets))
        for target, value in zip(self.targets, new_values):
            target.value = value
        self.update_target_max_value()


    def update_target_max_value(self):
        max_value = self.get_targets_max_value()
        for agent in self.airports:
            agent.SEARCH_TARGET.value = max_value

    def get_targets_max_value(self):
        if self.targets:
            return np.max([t.value for t in self.targets])
        else:
            return 0

    def find_targets(self):
        if not self.is_centralized_solution:
            LOG.info('Finding targets with decentralized approach')
            for agent in self.airports:
                agent.find_target()
        else:
            LOG.info('Finding targets with centralized approach')

            # create agent with global parameters
            centralized_solver = models.AutonomousUAV(**self._agents_params)

            # gathering all known information in one place
            visible_agents = set()
            identified_targets = set()
            for agent in self.airports:
                visible_agents |= agent.visible_agents
                identified_targets |= agent.identified_targets

            centralized_solver.visible_agents = visible_agents
            centralized_solver.identified_targets = identified_targets

            # TODO: rename more appropriate
            centralized_solver.find_target()

            # broadcast found_assignments to airports, so they can be notified
            # about chosen targets
            for agent in self.airports:
                agent.found_assignments = centralized_solver.found_assignments

        self.find_total_assignment_cost()

        self.sigTargetsFound.emit()

    def find_total_assignment_cost(self):
        # NOTE: not so optimal
        self.total_assignment_cost = 0.0
        for agent in self.airports:
            self.total_assignment_cost += \
                agent.assignment_cost(agent.chosen_target)

    def set_global_visibility_radius(self, value):
        if self.global_visibility_radius == value:
            return

        LOG.debug(f'Global visibility_radius is set to {value}')
        self.global_visibility_radius = value
        for agent in self.airports:
            agent.visibility_area.set_radius(self.global_visibility_radius)
        self._agents_params['visibility_area'].set_radius(value)
        self.sigRadiusUpdate.emit(value)

    def set_global_identify_beta(self, value):
        if self.global_identify_beta == value:
            return

        LOG.debug(f'Global identify_beta is set to {value}')
        self.global_identify_beta = value
        for agent in self.airports:
            agent.identify_beta = value
        self._agents_params['identify_beta'] = value
        self.sigIdentifyBetaUpdate.emit(value)
