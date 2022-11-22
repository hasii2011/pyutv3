
from typing import cast

from logging import Logger
from logging import getLogger

from wx import CLIP_CHILDREN
from wx import EVT_TREE_SEL_CHANGED
from wx import ID_ANY
from wx import TR_HAS_BUTTONS
from wx import TR_HIDE_ROOT

from wx import Frame
from wx import Notebook
from wx import SplitterWindow
from wx import TreeCtrl

from wx import TreeEvent

from wx import TreeItemId


class PyutV3UI:
    """
    This class is a container class that create user interface components
    in the parent frame
    """

    def __init__(self, topLevelFrame: Frame):

        self._topLevelFrame: Frame = topLevelFrame
        self.logger:         Logger = getLogger(__name__)

        self._splitter:    SplitterWindow = cast(SplitterWindow, None)
        self._projectTree: TreeCtrl       = cast(TreeCtrl, None)
        self._notebook:    Notebook       = cast(Notebook, None)

        self._projectsRoot: TreeItemId   = cast(TreeItemId, None)

        self._initializeUIElements()

        self._notebookCurrentPage: int = -1

    def _initializeUIElements(self):
        """
        Instantiate all the UI elements
        """
        self._splitter     = SplitterWindow(parent=self._topLevelFrame, id=ID_ANY)
        self._projectTree  = TreeCtrl(parent=self._splitter, id=ID_ANY, style=TR_HIDE_ROOT | TR_HAS_BUTTONS)
        self._notebook     = Notebook(parent=self._splitter, id=ID_ANY, style=CLIP_CHILDREN)

        self._splitter.SetMinimumPaneSize(20)
        self._splitter.SplitVertically(self._projectTree, self._notebook, 160)

        self._projectsRoot = self._projectTree.AddRoot("Ozzee")

        # Callbacks
        # self._parent.Bind(EVT_NOTEBOOK_PAGE_CHANGED, self._onNotebookPageChanged)
        self._topLevelFrame.Bind(EVT_TREE_SEL_CHANGED, self._onProjectTreeSelChanged)
        # self._projectTree.Bind(EVT_TREE_ITEM_RIGHT_CLICK, self.__onProjectTreeRightClick)

    def _syncPageFrameAndNotebook(self, frame):
        for i in range(self._notebook.GetPageCount()):
            pageFrame = self._notebook.GetPage(i)
            if pageFrame is frame:
                self._notebook.SetSelection(i)
                break

    def _onProjectTreeSelChanged(self, event: TreeEvent):
        """
        Callback for tree node selection changed

        Args:
            event:
        """
        itm:      TreeItemId   = event.GetItem()
        self.logger.debug(f'Clicked on: {itm=}')

    def __syncPageFrameAndNotebook(self, frame):

        for i in range(self._notebook.GetPageCount()):
            pageFrame = self._notebook.GetPage(i)
            if pageFrame is frame:
                self._notebook.SetSelection(i)
                break
