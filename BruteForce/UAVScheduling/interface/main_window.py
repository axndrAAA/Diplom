import logging

import numpy as np

from UAVScheduling.experiment import Experiment
from dwta.models import CircleArea, AutonomousUAV
from dwta.state import Position2D
from dwta.interface.graphics_scene import MyScene
from dwta.interface.models import TargetsModel
from dwta.interface.utils import loadUiType


LOG = logging.getLogger(__name__)


# Define main window class from template
WindowTemplate, TemplateBaseClass = loadUiType('interface/mainwindow.ui')


class MainWindow(TemplateBaseClass):

    def __init__(self, experiment, *args, **kwargs):
        """

        Args:
            experiment (Experiment):
            *args:
            **kwargs:
        """
        super().__init__(*args, **kwargs)

        self._experiment = experiment
        self._agents_to_generate = 5
        self._targets_to_generate = 10

        self.ui = WindowTemplate()
        self.ui.setupUi(self)

        self._scene = MyScene(self._experiment.world)
        self.ui.graphicsView.setScene(self._scene)
        self._scene.add_grid()

        self.connect_slots()
        self.set_initial_values()

        self._probability_line = None
        self._init_identify_probability_distribution_plot()

        self.setup_views()

    def set_initial_values(self):
        # visibility radius
        min_visibility_radius = 10
        max_visibility_radius = 10000
        self.ui.visibilityRadiusSlider.setMinimum(min_visibility_radius)
        self.ui.visibilityRadiusSlider.setMaximum(max_visibility_radius)
        self.ui.visibilityRadiusSlider.setValue(
            self._experiment.global_visibility_radius)

        # identify beta
        self.ui.identifyBetaLabel.setNum(self._experiment.global_identify_beta)

        # dimensions
        max_width = 10000
        self.ui.widthSpinBox.setMaximum(max_width)
        self.ui.widthSpinBox.setValue(self._experiment.world.area.width)

        max_height = 10000
        self.ui.heightSpinBox.setMaximum(max_height)
        self.ui.heightSpinBox.setValue(self._experiment.world.area.height)

        # actors
        max_agents_to_generate = 100
        self.ui.agentsToGenerateSpinBox.setMaximum(max_agents_to_generate)
        self.ui.agentsToGenerateSpinBox.setValue(self._agents_to_generate)

        max_targets_to_generate = 500
        self.ui.targetsToGenerateSpinBox.setMaximum(max_targets_to_generate)
        self.ui.targetsToGenerateSpinBox.setValue(self._targets_to_generate)

        self.update_selected_actor()

        self.ui.centralizedSolutionCheckBox.setChecked(
            self._experiment.is_centralized_solution)

        self.update_total_assignment_cost()

    def connect_slots(self):
        # visibility radius
        self.ui.visibilityRadiusSlider.valueChanged.connect(
            self._experiment.set_global_visibility_radius)

        self._experiment.sigRadiusUpdate.connect(
            self.ui.visibilityRadiusSlider.setValue)

        # identify beta
        self.ui.identifyBetaSlider.valueChanged.connect(
            self.update_identify_beta)

        # NOTE:connecting both signals from Experiment
        self._experiment.sigIdentifyBetaUpdate.connect(
            self.plot_identify_probability_distribution)

        self._experiment.sigRadiusUpdate.connect(
            self.plot_identify_probability_distribution)

        # dimensions
        self.ui.widthSpinBox.valueChanged.connect(
            self._experiment.world.area.set_width)

        self._experiment.world.area.sigWidthChanged.connect(
            self.ui.widthSpinBox.setValue)

        self.ui.heightSpinBox.valueChanged.connect(
            self._experiment.world.area.set_height)

        self._experiment.world.area.sigHeightChanged.connect(
            self.ui.heightSpinBox.setValue)

        self._connect_generate_slots()

        self._scene.selectionChanged.connect(self.update_selected_actor)

        self._connect_experiment_slots()

    def _connect_generate_slots(self):
        # actors spin boxes
        self.ui.agentsToGenerateSpinBox.valueChanged.connect(
            self.set_agents_to_generate)

        self.ui.targetsToGenerateSpinBox.valueChanged.connect(
            self.set_targets_to_generate)

        # actors push buttons
        self.ui.generateAgentsPushButton.released.connect(
            self.generate_agents)

        self.ui.generateTargetsPushButton.released.connect(
            self.generate_targets)

        self.ui.removeAllAgentsPushButton.released.connect(
            self.remove_all_agents)

        self.ui.removeAllTargetsPushButton.released.connect(
            self.remove_all_targets)

    def _connect_experiment_slots(self):
        self.ui.worldUpdatePushButton.released.connect(
            self._experiment.world.update)

        self.ui.findTargetsPushButton.released.connect(
            self._experiment.find_targets)

        self.ui.shuffleAgentPositionsPushButton.released.connect(
            self.shuffle_agent_positions)

        self.ui.shuffleTargetPositionsPushButton.released.connect(
            self.shuffle_target_positions)

        self.ui.shuffleAllPositionsPushButton.released.connect(
            self.shuffle_all_positions)

        # centralized solution checkbox
        self.ui.centralizedSolutionCheckBox.stateChanged.connect(
            self._experiment.set_centralized_solution_type)

        self._experiment.sigSolutionTypeChanged.connect(
            self.ui.centralizedSolutionCheckBox.setChecked)

        self._experiment.sigTargetsFound.connect(
            self.update_total_assignment_cost)

        self.ui.randomTargetValuesPushButton.released.connect(
            self.random_targets_values)

    def setup_views(self):
        targets_model = TargetsModel(self._experiment.world)
        self.ui.tableView.setModel(targets_model)

    # slots
    def generate_agents(self):
        self._experiment.add_agents(self._agents_to_generate)

    def generate_targets(self):
        self._experiment.add_targets(self._targets_to_generate)

    def set_agents_to_generate(self, value):
        self._agents_to_generate = value

    def set_targets_to_generate(self, value):
        self._targets_to_generate = value

    def remove_all_agents(self):
        self._experiment.world.remove(self._experiment.airports)

    def remove_all_targets(self):
        self._experiment.world.remove(self._experiment.targets)

    def remove_selected_actor(self):
        selected_item = self._scene.selected_item
        if selected_item:
            self._experiment.world.remove_actor(selected_item.actor)

    def shuffle_agent_positions(self):
        self._experiment.shuffle_actors('agent')

    def shuffle_target_positions(self):
        self._experiment.shuffle_actors('targetCluster')

    def shuffle_all_positions(self):
        self._experiment.shuffle_actors('all')

    def update_total_assignment_cost(self):
        total_assignment_cost = f'{self._experiment.total_assignment_cost:.2}'
        self.ui.totalAssignmentCostLabel.setText(total_assignment_cost)

    def random_targets_values(self):
        self._experiment.set_targets_values(random=True)

    def update_identified_targets_list(self):

        LOG.debug('Updating ListWidget of identified targets '
                  'for selected Agent')

        # blockSignals and setUpdatesEnabled are needed to prevent flickering
        # because of rapid updates of QListWidget, see:
        # https://bitbucket.org/zivadynamics/ziva-vfx-utils/pull-requests/4/feature-vfx-244-make-uizivauirun/diff
        self.blockSignals(True)
        self.setUpdatesEnabled(False)

        list_widget = self.ui.identifiedTargetsListWidget
        list_widget.clear()

        selected_item = self._scene.selected_item
        if selected_item and isinstance(selected_item.actor, AutonomousUAV):
            agent = selected_item.actor
            targets = [str(target) for target in agent.identified_targets]
            list_widget.addItems(sorted(targets))

        self.setUpdatesEnabled(True)
        self.blockSignals(False)

    def update_selected_actor(self):
        selected_item = self._scene.selected_item
        if selected_item:
            actor = selected_item.actor
            self.ui.selectedActorTypeLabel.setText(actor.name)
            self.ui.selectedActorIdLabel.setText(str(actor.id))
            self.ui.selectedActorDetailsLabel.setText(actor.details or
                                                      'No details')

            self.update_selected_actor_position(actor.position)

            # track position only for selected actor
            actor.sigPositionUpdate.connect(self.update_selected_actor_position)

            if isinstance(actor, AutonomousUAV):
                actor.sigNewTargetsIdentified.connect(
                    self.update_identified_targets_list)
        else:
            self.ui.selectedActorTypeLabel.setText('No Type')
            self.ui.selectedActorIdLabel.setText('No Id')
            self.ui.selectedActorDetailsLabel.setText('No details')
            self.update_selected_actor_position(Position2D(0, 0))

        self.update_identified_targets_list()

    def update_selected_actor_position(self, position):
        self.ui.selectedActorXLabel.setText(f'{position.x:.2f}')
        self.ui.selectedActorYLabel.setText(f'{position.y:.2f}')

    def update_identify_beta(self, value):
        new_value = value / self.ui.identifyBetaSlider.maximum()
        self._experiment.set_global_identify_beta(new_value)

        self.ui.identifyBetaLabel.setNum(new_value)

    # NOTE: this could be hidden in subclass on CanvasPlot
    def plot_identify_probability_distribution(self):

        # NOTE: we assume, that all airports are the same, thus we pick first
        #  of them as a reference
        if self._experiment.airports:
            agent = self._experiment.airports[0]
        else:
            # create stub agent
            # NOTE: not optimal at all!
            visibility_area = CircleArea(
                self._experiment.global_visibility_radius)
            identify_beta = self._experiment.global_identify_beta

            agent = AutonomousUAV(Position2D(0, 0),
                                  visibility_area=visibility_area,
                                  identify_beta=identify_beta)

        max_distance = agent.visibility_area.value

        distances = np.linspace(0, max_distance)
        y = agent.probability_identify_distribution(distances)

        canvas = self.ui.identifyProbabilityDistributionPlot
        if self._probability_line:
            # Update existing line
            self._probability_line.set_xdata(distances)
            self._probability_line.set_ydata(y)

            canvas.ax.set_xlim(0, max_distance)
        else:
            # Generate new line to perform updates on it
            # NOTE: Axes.plot returns a tuple of line objects
            self._probability_line = canvas.ax.plot(distances, y)[0]
        canvas.draw()

    def _init_identify_probability_distribution_plot(self):
        canvas = self.ui.identifyProbabilityDistributionPlot
        canvas.ax.grid(color='0.9')
        canvas.ax.set_title('Identify Probability Distribution')
        canvas.ax.set_xlabel('distance, m')

        canvas.ax.set_xlim(0, 1.0)
        canvas.ax.set_ylim(0, 1.1)

        canvas.fig.subplots_adjust(left=0.15, bottom=0.15,
                                   right=0.90, top=0.90)

        # initial plot
        self.plot_identify_probability_distribution()

