from typing import List
from typing import Callable

from logging import Logger
from logging import getLogger

from os import getcwd

from dataclasses import dataclass
from typing import cast

from wx import ACCEL_CTRL
from wx import CommandProcessor
from wx import EVT_MENU_RANGE
from wx import EVT_WINDOW_DESTROY
from wx import FD_FILE_MUST_EXIST
from wx import FD_OPEN
from wx import FH_PATH_SHOW_ALWAYS
from wx import FileHistory
from wx import ID_EXIT
from wx import ID_FILE1
from wx import ID_FILE9
from wx import ID_OPEN
from wx import ID_SELECTALL
from wx import ID_OK
from wx import ID_REDO
from wx import ID_UNDO
from wx import OK
from wx import ICON_ERROR
from wx import DEFAULT_FRAME_STYLE
from wx import EVT_MENU

from wx import FileDialog
from wx import CommandEvent
from wx import Frame
from wx import Menu
from wx import MenuBar

from wx import AcceleratorEntry
from wx import AcceleratorTable

from wx import MessageDialog
from wx import NewIdRef
from wx import WindowDestroyEvent

from pyutv3.FileHistoryConfiguration import FileHistoryConfiguration
from pyutv3.PyutV3UI import PyutV3UI


@dataclass
class RequestResponse:
    cancelled: bool = False
    fileName:  str  = ''


class PyutV3Frame(Frame):

    FRAME_ID:      int = 0xDeadBeef
    WINDOW_WIDTH:  int = 1200
    WINDOW_HEIGHT: int = 600

    def __init__(self, parent=None, wxId=FRAME_ID, size=(WINDOW_WIDTH, WINDOW_HEIGHT)):

        super().__init__(parent=parent, id=wxId,  size=size, style=DEFAULT_FRAME_STYLE, title='Test Scaffold for Plugins')

        self.logger:           Logger = getLogger(__name__)
        self._loadXmlFileWxId: int    = NewIdRef()

        self._status = self.CreateStatusBar()
        self._status.SetStatusText('Ready!')

        # self._eventEngine: EventEngine = EventEngine(listeningWindow=self)
        self._scaffoldUI:  PyutV3UI  = PyutV3UI(topLevelFrame=self)

        self._fileHistory: FileHistory = FileHistory(idBase=ID_FILE1)
        self._fileHistory.SetMenuPathStyle(style=FH_PATH_SHOW_ALWAYS)

        self._commandProcessor: CommandProcessor = CommandProcessor()

        self._fileMenu: Menu = cast(Menu, None)
        self._editMenu: Menu = cast(Menu, None)

        self._createApplicationMenuBar()

        self.__setupKeyboardShortCuts()

        self.Bind(EVT_WINDOW_DESTROY, self._cleanupFileHistory)

    # noinspection PyUnusedLocal
    def Close(self, force=False):
        self.Destroy()

    # noinspection PyUnusedLocal
    def _cleanupFileHistory(self, event: WindowDestroyEvent):
        """
        A little extra cleanup is required for the FileHistory control;
        Take time to persist the file history
        Args:
            event:
        """
        fileHistoryConfiguration: FileHistoryConfiguration = FileHistoryConfiguration(appName='pyutV3',
                                                                                      vendorName='ElGatoMalo',
                                                                                      localFilename='pyutRecentFiles.ini')
        #
        # On OS X this gets stored in ~/Library/Preferences
        # Nothing I did to the FileHistoryConfiguration object seemed to change that
        self._fileHistory.Save(config=fileHistoryConfiguration)

        del self._fileHistory
        self._fileMenu.Destroy()

    def loadXmlFile(self, fqFileName: str):
        """

        Args:
            fqFileName: full qualified file name
        """
        # self._loadXmlFile(fqFileName=fqFileName)
        pass

    def _createApplicationMenuBar(self):

        self._loadXmlFileWxId = NewIdRef()

        self._newClassDiagramWxId:    int = NewIdRef()
        self._newUseCaseDiagramWxId:  int = NewIdRef()
        self._newSequenceDiagramWxId: int = NewIdRef()

        menuBar:   MenuBar = MenuBar()
        fileMenu:  Menu = Menu()
        editMenu:  Menu = Menu()

        fileMenu  = self._makeFileMenu(fileMenu)
        editMenu  = self._makeEditMenu(editMenu)

        menuBar.Append(fileMenu, 'File')
        menuBar.Append(editMenu, 'Edit')

        self.SetMenuBar(menuBar)

        self.Bind(EVT_MENU, self.Close, id=ID_EXIT)

        # Set to class protected variables
        self._fileMenu = fileMenu
        self._editMenu = editMenu

    def _makeFileMenu(self, fileMenu: Menu) -> Menu:

        newDiagramSubMenu: Menu = self._makeNewDiagramSubMenu()

        fileMenu.AppendSubMenu(newDiagramSubMenu, 'New')
        fileMenu.Append(ID_OPEN)
        fileMenu.Append(self._loadXmlFileWxId, 'Load Xml Diagram')

        self._fileHistory.UseMenu(fileMenu)
        fileHistoryConfiguration: FileHistoryConfiguration = FileHistoryConfiguration(appName='pyutV3',
                                                                                      vendorName='ElGatoMalo',
                                                                                      localFilename='pyutRecentFiles.ini')
        entryCount: int = fileHistoryConfiguration.GetNumberOfEntries()
        file1:      str = fileHistoryConfiguration.Read('file1')
        self.logger.info(f'{entryCount=} - {file1=}')
        self._fileHistory.Load(fileHistoryConfiguration)

        self.Bind(EVT_MENU, self._onFileOpen,    id=ID_OPEN)
        self.Bind(EVT_MENU, self._onLoadXmlFile, id=self._loadXmlFileWxId)
        self._bindRecentlyOpenedFileIds()

        return fileMenu

    def _bindRecentlyOpenedFileIds(self):
        """
        Assumes
        * We use the base ID Start
        * They are sequential in the definition file
        """
        self.Bind(
            EVT_MENU_RANGE, self._onOpenRecent, id=ID_FILE1, id2=ID_FILE9
            )

    def _makeNewDiagramSubMenu(self) -> Menu:
        subMenu: Menu = Menu()

        subMenu.Append(self._newClassDiagramWxId,    'Class Diagram')
        subMenu.Append(self._newUseCaseDiagramWxId,  'Use Case Diagram')
        subMenu.Append(self._newSequenceDiagramWxId, 'Sequence Diagram')

        return subMenu

    def _makeEditMenu(self, editMenu: Menu) -> Menu:

        editMenu.Append(ID_UNDO)
        editMenu.Append(ID_REDO)
        editMenu.Append(ID_SELECTALL)

        self.Bind(EVT_MENU, self._onUndo, id=ID_UNDO)
        self.Bind(EVT_MENU, self._onRedo, id=ID_REDO)

        self._commandProcessor.SetEditMenu(editMenu)

        return editMenu

    # noinspection PyUnusedLocal
    def _onFileOpen(self, event: CommandEvent):

        dlg: FileDialog = FileDialog(self, message="Choose a file", wildcard="*.put", style=FD_OPEN)
        if dlg.ShowModal() == ID_OK:
            # Only allowed single file loads
            filenames: List[str] = dlg.GetPaths()
            self.logger.info(f'Opened file name: {filenames[0]}')
            self._fileHistory.AddFileToHistory(filename=filenames[0])
        dlg.Destroy()

    # noinspection PyUnusedLocal
    def _onLoadXmlFile(self, event: CommandEvent):

        self._displayError(message='Use the import plugin')

    def _onOpenRecent(self, event: CommandEvent):
        fileNum: int = event.GetId() - ID_FILE1
        path:    str = self._fileHistory.GetHistoryFile(fileNum)

        self.logger.info(f'{event=} - filename: {path}')

        # add it back to the history; then it will be moved up the list
        self._fileHistory.AddFileToHistory(path)

    # noinspection PyUnusedLocal
    def _onUndo(self, event: CommandEvent):
        self.logger.info(f'Invoked Undo')

    # noinspection PyUnusedLocal
    def _onRedo(self, event: CommandEvent):
        self.logger.info(f'Invoked Redo')

    def _askForXMLFileToImport(self) -> RequestResponse:
        """
        TODO: This belongs in another class

        Called to ask for a file to import

        Returns:  The request response named tuple
        """
        dlg = FileDialog(None, "Choose a file", getcwd(), "", "*.xml", FD_OPEN | FD_FILE_MUST_EXIST)

        response: RequestResponse = RequestResponse()
        if dlg.ShowModal() != ID_OK:
            dlg.Destroy()
            response.cancelled = True
        else:
            fileNames: List[str] = dlg.GetPaths()
            file:      str       = fileNames[0]

            response.cancelled = False
            response.fileName = file

        return response

    def __makeSubMenuEntry(self, subMenu: Menu, wxId: int, pluginName: str, callback: Callable) -> Menu:

        subMenu.Append(wxId, pluginName)
        self.Bind(EVT_MENU, callback, id=wxId)

        return subMenu

    def __setupKeyboardShortCuts(self):
        lst = [
            (ACCEL_CTRL, ord('l'), self._loadXmlFileWxId),
            (ACCEL_CTRL, ord('a'), ID_SELECTALL),
            ]
        acc = []
        for el in lst:
            (el1, el2, el3) = el
            acc.append(AcceleratorEntry(el1, el2, el3))
        accel_table = AcceleratorTable(acc)
        self.SetAcceleratorTable(accel_table)

    def _displayError(self, message: str):

        booBoo: MessageDialog = MessageDialog(parent=None, message=message, caption='Error', style=OK | ICON_ERROR)
        booBoo.ShowModal()
