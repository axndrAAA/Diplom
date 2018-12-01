import logging

import numpy as np

from PySide2.QtCore import QObject
from PySide2.QtCore import Signal

from dwta.generator import Generator
from dwta.world import World, WorldArea
from dwta import task, models


LOG = logging.getLogger(__name__)


class Experiment(QObject):

    sigRadiusUpdate = Signal(int)
    sigIdentifyBetaUpdate = Signal(float)
    sigSolutionTypeChanged = Signal(int)
    sigTargetsFound = Signal()

    TARGETS_TASKS = {
        models.Target: task.Attack(),
        models.SearchTarget: task.Search()
    }

    TARGET_MAX_VALUE = 100

    def __init__(self, world, parent=None):
        """

        Args:
            world (World):
        """
        super().__init__(parent)

        self.global_visibility_radius = 200
        self.global_identify_beta = 1.0

        self._agents_params = {
            'visibility_area': models.CircleArea(self.global_visibility_radius),
            # 'max_attack_distance': 10.0,
            'targets_tasks': self.TARGETS_TASKS,
            # 'target_max_value': np.max([t.value for t in targets]),
            'flight_time_total': 10.0,
            'flight_time_left': 9.0,
            'velocity': 140.0,
            'identify_beta': self.global_identify_beta
        }

        self._targets_params = {
            'random': False,
            'value': 5.0
        }

        self.world = world

        self.is_centralized_solution = True
        self.total_assignment_cost = 0.0

        self._gen = Generator(self.world.area)

    @property
    def targets(self):
        return self.world.get_actors(models.Target)

    @property
    def agents(self):
        """

        Returns:
            list of models.Agent
        """
        return self.world.get_actors(models.Agent)

    def add_agents(self, num=1):
        agents = self._gen.many('agent', num, **self._agents_params)
        self.world.add(agents)

    def add_targets(self, num=1):
        targets = self._gen.many('target', num, **self._targets_params)
        self.world.add(targets)

    def shuffle_actors(self, actor_type='all'):
        if actor_type == 'all':
            actors = self.world.actors
        elif actor_type == 'agent':
            actors = self.agents
        elif actor_type == 'target':
            actors = self.targets
        else:
            raise ValueError('Unknown actor_type')

        positions = self._gen.many('position', len(actors))

        self.world.wait_updates = False  # temp disable update signals

        LOG.info(f'Shuffling positions for {actor_type}')
        for actor, position in zip(actors, positions):
            actor.position = position

        self.world.update()
        self.world.wait_updates = True

        # TODO: this disabling and state recovering should be performed in World
        [actor.sigPositionUpdate.emit(actor.position) for actor in actors]

    def set_targets_values(self, new_values=None, random=True):
        if random:
            new_values = np.random.randint(0, self.TARGET_MAX_VALUE,
                                           len(self.targets))
        for target, value in zip(self.targets, new_values):
            target.value = value
        self.update_target_max_value()

    def set_centralized_solution_type(self, value):
        if value == self.is_centralized_solution:
            return

        self.is_centralized_solution = value

        LOG.info(f'Set solution type '
                 f'to {"centralized" if value else "decentralized"}')
        self.sigSolutionTypeChanged.emit(value)

    def update_target_max_value(self):
        max_value = self.get_targets_max_value()
        for agent in self.agents:
            agent.SEARCH_TARGET.value = max_value

    def get_targets_max_value(self):
        if self.targets:
            return np.max([t.value for t in self.targets])
        else:
            return 0

    def find_targets(self):
        if not self.is_centralized_solution:
            LOG.info('Finding targets with decentralized approach')
            for agent in self.agents:
                agent.find_target()
        else:
            LOG.info('Finding targets with centralized approach')

            # create agent with global parameters
            centralized_solver = models.AutonomousUAV(**self._agents_params)

            # gathering all known information in one place
            visible_agents = set()
            identified_targets = set()
            for agent in self.agents:
                visible_agents |= agent.visible_agents
                identified_targets |= agent.identified_targets

            centralized_solver.visible_agents = visible_agents
            centralized_solver.identified_targets = identified_targets

            # TODO: rename more appropriate
            centralized_solver.find_target()

            # broadcast found_assignments to agents, so they can be notified
            # about chosen targets
            for agent in self.agents:
                agent.found_assignments = centralized_solver.found_assignments

        self.find_total_assignment_cost()

        self.sigTargetsFound.emit()

    def find_total_assignment_cost(self):
        # NOTE: not so optimal
        self.total_assignment_cost = 0.0
        for agent in self.agents:
            self.total_assignment_cost += \
                agent.assignment_cost(agent.chosen_target)

    def set_global_visibility_radius(self, value):
        if self.global_visibility_radius == value:
            return

        LOG.debug(f'Global visibility_radius is set to {value}')
        self.global_visibility_radius = value
        for agent in self.agents:
            agent.visibility_area.set_radius(self.global_visibility_radius)
        self._agents_params['visibility_area'].set_radius(value)
        self.sigRadiusUpdate.emit(value)

    def set_global_identify_beta(self, value):
        if self.global_identify_beta == value:
            return

        LOG.debug(f'Global identify_beta is set to {value}')
        self.global_identify_beta = value
        for agent in self.agents:
            agent.identify_beta = value
        self._agents_params['identify_beta'] = value
        self.sigIdentifyBetaUpdate.emit(value)
