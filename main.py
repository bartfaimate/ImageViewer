# This Python file uses the following encoding: utf-8
import sys
import os
from pathlib import Path
import logging
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtGui import QColorSpace, QImage, QImageWriter, QKeySequence, QPixmap, QImageReader
from PySide2.QtWidgets import QAction, QApplication, QDialog, QFileDialog, QLabel, QMessageBox, QMainWindow, QScrollArea
from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton
from PySide2.QtWidgets import QWidget, QSizePolicy
from PySide2.QtCore import QDir, QStandardPaths, QStringListModel, Qt, QFile
from PySide2.QtGui import QPalette, QGuiApplication, QWheelEvent
from PySide2.QtUiTools import QUiLoader
from PIL.ImageQt import ImageQt
from PIL.Image import Image


logging.basicConfig(level=logging.DEBUG)


class ImageViewer(QMainWindow):

    def __init__(self):
        super(ImageViewer, self).__init__()
        # self.ui = self.load_ui()
        self.image = None   # type: Image

        self.center_widget = QWidget()
        self.vertical_layout = QVBoxLayout()
        self.img_label = QLabel()
        self.img_label.setBackgroundRole(QPalette.Base)
#        self.img_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored);

        self.img_label.setScaledContents(True)
        self.scroll_area = QScrollArea()

        self.scroll_area.setWidget(self.img_label)
        self.scroll_area.setBackgroundRole(QPalette.Dark)
        self.scroll_area.setVisible(True)
        self.img_label.setVisible(True)
        self.resize(QGuiApplication.primaryScreen().availableSize() * 3 / 5)

        self.vertical_layout.addWidget(self.scroll_area)
        self.center_widget.setLayout(self.vertical_layout)
        self.setCentralWidget(self.center_widget)

        self.scaleFactor = 1.0
        self.createActions()

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        ui = loader.load(ui_file, self)
        ui_file.close()
        logging.debug('ui loaded')
        return ui

    def initializeImageFileDialog(self, dialog, acceptMode):
        self.firstDialog = True

        if self.firstDialog:
            self.firstDialog = False
            picturesLocations = QStandardPaths.standardLocations(QStandardPaths.PicturesLocation)
            dialog.setDirectory(picturesLocations[-1] if not picturesLocations else QDir.currentPath() )

        mimeTypeFilters = []
        supportedMimeTypes = QImageReader.supportedMimeTypes() if acceptMode == QFileDialog.AcceptOpen else QImageWriter.supportedMimeTypes()
        for mimeTypeName in supportedMimeTypes:
            mimeTypeFilters.append(mimeTypeName)
        mimeTypeFilters.sort()
        dialog.setMimeTypeFilters(mimeTypeFilters)
        dialog.selectMimeTypeFilter("image/jpeg")
        if acceptMode == QFileDialog.AcceptSave:
            dialog.setDefaultSuffix("jpg")

    def loadFile(self, file_name):
        reader = QImageReader(file_name)
        reader.setAutoTransform(True)
        newImage = reader.read()
        if newImage.isNull():
            QMessageBox.information(self, 'Warning',
                                    f'Cannot load image {file_name}')
            return False
        
        self.setImage(newImage)

        self.setWindowFilePath(file_name)

        message = f'Opened "{file_name}", {self.image.width()}x{self.image.height()}, Depth: {self.image.depth()}'
        self.statusBar().showMessage(message)
        return True

    def setImage(self, newImage):
        self.image = newImage
        if self.image.colorSpace().isValid():
            self.image.convertToColorSpace(QColorSpace.SRgb)
        self.img_label.setPixmap(QPixmap.fromImage(self.image))
        
        self.scaleFactor = 1.0

        # self.scroll_area.setVisible(True)
        # printAct->setEnabled(true)
        self.fitToWindowAct.setEnabled(True)
        self.updateActions()

        if not self.fitToWindowAct.isChecked():
            self.img_label.adjustSize()

    def open(self):
        dialog = QFileDialog(self, "Open File")
        self.initializeImageFileDialog(dialog, QFileDialog.AcceptOpen)

        while dialog.exec_() == QDialog.Accepted and not self.loadFile(dialog.selectedFiles()[0]):
            pass
        logging.info(f'Opening...{dialog.selectedFiles()}')

    def saveAs(self):
        dialog = QFileDialog(self, "Save File As")
        self.initializeImageFileDialog(dialog, QFileDialog.AcceptSave)

        while dialog.exec_() == QDialog.Accepted and not self.saveFile(dialog.selectedFiles()[0]):
            pass

    def copy(self):
        QGuiApplication.clipboard().setImage(self.image)

    def clipboardImage(self):
        if mimeData := QGuiApplication.clipboard().mimeData():
            if mimeData.hasImage():
                image = mimeData.imageData()
            if not image.isNull():
                return image

        return QImage()

    def paste(self):
        newImage = self.clipboardImage()
        if newImage.isNull():
            self.statusBar().showMessage("No image in clipboard")
        else:
            self.setImage(newImage)
            self.setWindowFilePath('')
            message = ("Obtained image from clipboard, {}x{}, Depth: {}").format(
                newImage.width(), newImage.height(), newImage.depth()
                )
            self.statusBar().showMessage(message)

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        print(self.img_label.pixmap().size())
        self.img_label.resize(self.scaleFactor * self.img_label.pixmap().size())

        self.adjustScrollBar(self.scroll_area.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scroll_area.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.111)
    
    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)

    def normalSize(self):
        self.img_label.adjustSize()
        self.scaleFactor = 1.0

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scroll_area.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()
        self.updateActions()

    def createActions(self):
        self.fileMenu = self.menuBar().addMenu("&File")

        self.openAct = self.fileMenu.addAction("&Open...", self.open)
        self.openAct.setShortcut(QKeySequence.Open)

        self.saveAsAct = self.fileMenu.addAction("&Save As...", self.saveAs)
        self.saveAsAct.setEnabled(False)

        self.fileMenu.addSeparator()

        self.exitAct = self.fileMenu.addAction("E&xit", self.close)
        self.exitAct.setShortcut("Ctrl+Q")

        self.editMenu = self.menuBar().addMenu("&Edit")

        self.copyAct = self.editMenu.addAction("&Copy", self.copy)
        self.copyAct.setShortcut(QKeySequence.Copy)
        self.copyAct.setEnabled(False)

        viewMenu = self.menuBar().addMenu("&View")

        self.zoomInAct = viewMenu.addAction("Zoom &In (25%)", self.zoomIn)
        self.zoomInAct.setShortcut(QKeySequence.ZoomIn)
        self.zoomInAct.setEnabled(False)

        self.zoomOutAct = viewMenu.addAction("Zoom &Out (25%)", self.zoomOut)
        self.zoomOutAct.setShortcut(QKeySequence.ZoomOut)
        self.zoomOutAct.setEnabled(False)

        self.normalSizeAct = viewMenu.addAction("&Normal Size", self.normalSize)
        self.normalSizeAct.setShortcut("Ctrl+S")
        self.normalSizeAct.setEnabled(False)

        viewMenu.addSeparator()

        self.fitToWindowAct = viewMenu.addAction("&Fit to Window", self.fitToWindow)
        self.fitToWindowAct.setEnabled(False)
        self.fitToWindowAct.setCheckable(True)
        self.fitToWindowAct.setShortcut("Ctrl+F")

    def updateActions(self):
        self.saveAsAct.setEnabled(not self.image.isNull())
        self.copyAct.setEnabled(not self.image.isNull())
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())
    
    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                            + ((factor - 1) * scrollBar.pageStep()/2)))

    def wheelEvent(self, event: QWheelEvent) -> None:
        num_pixels = event.pixelDelta()
        num_degrees = event.angleDelta() / 8
        if self.image and event.modifiers() == Qt.ControlModifier:
           self.scaleImage(num_degrees / 20)
        # print(f'numpixel {numPixels} numDegrees {numDegrees}')




if __name__ == "__main__":
    app = QApplication([])
    widget = ImageViewer()
    widget.show()
    sys.exit(app.exec_())
