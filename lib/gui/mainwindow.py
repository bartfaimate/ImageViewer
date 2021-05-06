#!/usr/bin/python3

import sys
from PySide2 import QtCore
from PySide2.QtGui import QColorSpace, QImage, QImageWriter, QKeySequence, QPixmap, QImageReader
from PySide2.QtWidgets import QAction, QApplication, QDialog, QFileDialog, QLabel, QMessageBox, QMainWindow, QScrollArea
from PySide2.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton
from PySide2.QtWidgets import QWidget, QSizePolicy
from PySide2.QtCore import QDir, QStandardPaths, QStringListModel, Qt
from PySide2.QtGui import QPalette, QGuiApplication
jpg = '/home/mate/develop/python/ImageSorter/__test_images__/darktable/DSC06979.JPG'

class Window(QMainWindow):
    
    def __init__(self):
        super().__init__()
        # self.setGeometry(100,100,800,600)
        self.setWindowTitle("QuickView")
        self.imageLabel = QLabel()
        self.scrollArea = QScrollArea()
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored);
        self.imageLabel.setScaledContents(True);

        self.scrollArea.setBackgroundRole(QPalette.Dark);
        self.scrollArea.setWidget(self.imageLabel);
        self.scrollArea.setVisible(False);
        self.setCentralWidget(self.scrollArea);

        self.createActions()

        self.resize(QGuiApplication.primaryScreen().availableSize() * 3 / 5);

    def loadFile(self, file_name):
        
        reader = QImageReader(file_name)
        reader.setAutoTransform(True)
        newImage = reader.read()
        if newImage.isNull() :
            QMessageBox.information(self, 'Warning',
                                 f'Cannot load image {file_name}')
            return False
        return True

    def setImage(self, newImage):
        image = newImage;
        if image.colorSpace().isValid():
            image.convertToColorSpace(QColorSpace.SRgb);
        self.imageLabel.setPixmap(QPixmap.fromImage(image));
        self.scaleFactor = 1.0;

        self.scrollArea.setVisible(True)
        self.printAct.setEnabled(True)
        self.fitToWindowAct.setEnabled(True)
        self.updateActions()

        if not self.fitToWindowAct.isChecked():
            self.imageLabel.adjustSize();

    def saveFile(self, fileName):
        writer = QImageWriter(fileName)

        if not writer.write(self.image) :
            QMessageBox.information(self, QGuiApplication.applicationDisplayName(),
                                 "Cannot write {}: {}".format(
                                     QDir.toNativeSeparators(fileName)),
                                     writer.errorString()
                                     )
            return False
        message = 'Wrote "{}"'.format(QDir.toNativeSeparators(fileName))
        self.statusBar().showMessage(message);
        return True;
    
    def initializeImageFileDialog(self, dialog, acceptMode):
        self.firstDialog = True;

        if self.firstDialog:
            self.firstDialog = False
            picturesLocations = QStandardPaths.standardLocations(QStandardPaths.PicturesLocation)
            dialog.setDirectory( picturesLocations[-1] if not picturesLocations else QDir.currentPath() )

        mimeTypeFilters = []
        supportedMimeTypes = QImageReader.supportedMimeTypes() if acceptMode == QFileDialog.AcceptOpen else QImageWriter.supportedMimeTypes()
        for mimeTypeName in supportedMimeTypes:
            mimeTypeFilters.append(mimeTypeName)
        mimeTypeFilters.sort()
        dialog.setMimeTypeFilters(mimeTypeFilters);
        dialog.selectMimeTypeFilter("image/jpeg");
        if acceptMode == QFileDialog.AcceptSave:
            dialog.setDefaultSuffix("jpg")

    def open(self):
        dialog = QFileDialog(self, "Open File");
        self.initializeImageFileDialog(dialog, QFileDialog.AcceptOpen);

        while dialog.exec_() == QDialog.Accepted and not self.loadFile(dialog.selectedFiles()[0]):
            pass

    def saveAs(self):
        dialog =QFileDialog(self, "Save File As");
        self.initializeImageFileDialog(dialog, QFileDialog.AcceptSave);

        while dialog.exec_() == QDialog.Accepted and not self.saveFile(dialog.selectedFiles()[0]):
            pass

    

    def copy(self):
        QGuiApplication.clipboard().setImage(self.image);

    def clipboardImage(self):
        if mimeData := QGuiApplication.clipboard().mimeData():
            if mimeData.hasImage():
                image = mimeData.imageData()
            if not image.isNull():
                return image;
        
        return QImage()

    def paste(self):
        newImage = self.clipboardImage()
        if newImage.isNull(): 
            self.statusBar().showMessage("No image in clipboard")
        else:
            self.setImage(newImage);
            self.setWindowFilePath('');
            message = ("Obtained image from clipboard, {}x{}, Depth: {}").format(
                newImage.width(), newImage.height(), newImage.depth()
                )
            self.statusBar().showMessage(message);

    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)

    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0
    
    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow);
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

        self.editMenu = self.menuBar().addMenu("&Edit");

        copyAct = self.editMenu.addAction("&Copy", self.copy)
        copyAct.setShortcut(QKeySequence.Copy);
        copyAct.setEnabled(False);

        # QAction *pasteAct = editMenu->addAction(tr("&Paste"), this, &ImageViewer::paste);
        # pasteAct->setShortcut(QKeySequence::Paste);

        # QMenu *viewMenu = menuBar()->addMenu(tr("&View"));

        # zoomInAct = viewMenu->addAction(tr("Zoom &In (25%)"), this, &ImageViewer::zoomIn);
        # zoomInAct->setShortcut(QKeySequence::ZoomIn);
        # zoomInAct->setEnabled(false);

        # zoomOutAct = viewMenu->addAction(tr("Zoom &Out (25%)"), this, &ImageViewer::zoomOut);
        # zoomOutAct->setShortcut(QKeySequence::ZoomOut);
        # zoomOutAct->setEnabled(false);

        # normalSizeAct = viewMenu->addAction(tr("&Normal Size"), this, &ImageViewer::normalSize);
        # normalSizeAct->setShortcut(tr("Ctrl+S"));
        # normalSizeAct->setEnabled(false);

        # viewMenu->addSeparator();

        # fitToWindowAct = viewMenu->addAction(tr("&Fit to Window"), this, &ImageViewer::fitToWindow);
        # fitToWindowAct->setEnabled(false);
        # fitToWindowAct->setCheckable(true);
        # fitToWindowAct->setShortcut(tr("Ctrl+F"));

    

    def updateActions(self):
        self.saveAsAct.setEnabled(not self.image.isNull());
        self.copyAct.setEnabled(not self.image.isNull());
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked());
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked());
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked());

    def scaleImage(self, factor):
        self.scaleFactor *= factor;
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap(Qt.ReturnByValue).size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor);
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor);

        self.zoomInAct.setEnabled(self.scaleFactor < 3.0);
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.333);
    
    def adjustScrollBar(self, scrollBar,factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                            + ((factor - 1) * scrollBar.pageStep()/2)))

if __name__ == '__main__':
    
    
    # Create the application object
    app = QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec_())


