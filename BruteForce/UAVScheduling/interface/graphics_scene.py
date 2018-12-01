import logging

from PySide2.QtWidgets import QGraphicsScene, QMenu
from PySide2.QtCore import Qt

from dwta.interface.grid_item import GridItem
from dwta.world import World
from dwta.views import create_view, ActorView


LOG = logging.getLogger(__name__)


class MyScene(QGraphicsScene):

    def __init__(self, world, parent=None):
        """

        Args:
            world (World):
            parent:
        """
        super().__init__(parent)

        self._world = world
        self._world.sigActorAdded.connect(self.add_actor)
        self._world.sigActorRemoved.connect(self.remove_actor)

        self._world.area.sigChanged.connect(self.setSceneRect)
        self.setSceneRect(self._world.area.area)

        world_area_view = create_view(self._world.area)
        self.addItem(world_area_view)

        self._last_selected = None
        self.selectionChanged.connect(self.update_selection)

        self._grids = []

        self._index = {}
        """Mapping from added actors to their views. Added for convenience."""

    def contextMenuEvent(self, event):
        super().contextMenuEvent(event)
        if self.selected_item:
            menu = QMenu()
            delete_actor_action = menu.addAction('Delete Actor')
            delete_actor_action.triggered.connect(self.remove_selected_actor)
            menu.exec_(event.screenPos())

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == Qt.MouseButton.RightButton:
            # NOTE: we use mousePressEvent instead of mouseReleaseEvent,
            #  because the last one is intercepting by contextMenuEvent

            actor_views = [x for x in self.items(event.scenePos())
                           if isinstance(x, ActorView)]
            if actor_views:
                topmost_actor = actor_views[0]  # TODO: temp
                topmost_actor.setSelected(True)
            elif self.selected_item:
                # clear selection
                self.selected_item.setSelected(False)

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Delete and self.selected_item:
            self.remove_selected_actor()

    # NOTE: we assume, that add_actor and remove_actor would be called after
    #  World method. So, we do not perform World.update() here
    def add_actor(self, actor):
        actor_view = create_view(actor)
        self.addItem(actor_view)
        self._index[actor] = actor_view

        LOG.debug(f'ActorView for {actor} added')

        self.redraw_grid_under_item(self._index[actor])

    def remove_actor(self, actor):
        self.removeItem(self._index[actor])

        LOG.debug(f'ActorView for {actor} removed')

        # redraw surrounding area
        self.redraw_grid_under_item(self._index[actor])
        del self._index[actor]

    def remove_selected_actor(self):
        self._world.remove_actor(self._last_selected.actor)

    @property
    def selected_item(self):
        return self._last_selected

    def update_selection(self):
        """Restricts selection to only one item at time."""
        # see: https://stackoverflow.com/a/26224738/10380652

        if (len(self.selectedItems()) == 1 and
                self.selectedItems()[0] == self._last_selected):
            # selected ourselves
            return

        if self._last_selected and self._last_selected.isSelected():
            # NOTE: setSelected will call update_selection again! sometimes?
            # remove selection if selected, this change item state
            self._last_selected.setSelected(False)

        if self._last_selected:
            # redraw previous selection after state changed
            self.redraw_grid_under_item(self._last_selected)

            # if we have previous selection, forget it. if afterwards no new
            # item was selected, we simply finish selection update we
            # consistent state
            self._last_selected = None

        if not self.selectedItems():
            # nothing to select
            return

        self._last_selected = self.selectedItems()[0]
        # redraw new selection
        self.redraw_grid_under_item(self._last_selected)

    def add_grid(self):
        """Add zoomable grid to this Scene.

        NOTE: this take effect only when there's at least one view
         attached to Scene
        """
        self.remove_grid()
        for view in self.views():
            grid = GridItem(view)
            self._grids.append(grid)
            self.addItem(grid)

    def remove_grid(self):
        for grid in self._grids:
            self.removeItem(grid)
        self._grids = []

    def redraw_grid_under_item(self, item):
        LOG.debug(f'Redrawing grid under {type(item).__name__} '
                  f'at pos {item.pos()}. Bounding rect = {item.boundingRect()}')

        # some changes doesn't force GridItem to redraw. for example,
        #  there appear white squares behind newly added items. thus we need
        #  to call this method
        # for grid in self._grids:
        #     grid.update(item.boundingRect())

        # FIXME: temporally we schedule redraw on whole visible area
        #  of the scene, because AgentView markers has property
        #  ItemIgnoresTransformations and thus we doesn't properly deal with
        #  resize of boundingRect
        for view in self.views():
            self.update(view.sceneRect())
