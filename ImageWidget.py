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
from PySide2.QtGui import QPalette, QGuiApplication, QWheelEvent, QResizeEvent
from PySide2.QtUiTools import QUiLoader
from PIL.ImageQt import ImageQt
from PIL import Image
import math

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

class ImageWidget(QScrollArea):

    def __init__(self):
        super(ImageWidget, self).__init__()
        self.image = None   # type: Image.Image
        self.qimage = None  # type: QImage
        # self.scale_factor = 1.0
        self.image_label = QLabel()
        self.image_label.setScaledContents(True)
        self.image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.history = list()


        self.setWidget(self.image_label)
        self.image_path = None  # type: Path
        self.setVisible(True)
        self.image_label.setVisible(True)
        self.scale_factor = 1.0

        # self.setFixedSize(1000, 600)

    def scaleImage(self, factor):
        self.scale_factor *= factor
        log.debug(f'scalefactor {self.scale_factor}')
        self.image_label.resize(self.scale_factor * self.image_label.pixmap().size())

        self.adjustScrollBar(self.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.verticalScrollBar(), factor)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                               + ((factor - 1) * scrollBar.pageStep() / 2)))

    def update_(self, image: Image):
        self.qimage = ImageQt(image)
        self.image_label.setPixmap(QPixmap.fromImage(self.qimage))
        log.info(f'Pixmap size: {self.image_label.pixmap().size()}')

    def rotate(self, value: int):
        image = self.image.rotate(value, expand=1)
        # image.show()
        self.update_(image)

    def setImage(self, newImage: QImage):
        self.qimage = newImage
        if self.qimage.colorSpace().isValid():
            self.qimage.convertToColorSpace(QColorSpace.SRgb)
        self.image_label.setPixmap(QPixmap.fromImage(self.qimage))
        self.image_label.adjustSize()
        self.scale_factor = 1.0

    def loadFile(self, file_name):
        new_image = Image.open(file_name)  #type: Image.Image
        if not new_image:
            return False
        self.image = new_image  # type: Image.Image
        self.setImage(ImageQt(new_image))
        self.image_path = Path(file_name)
        log.debug(f'Loading image with size of: {self.image.width}, {self.image.height}')

        return True

    def zoomIn(self):
        self.scaleImage(1.25)

    def zoomOut(self):
        self.scaleImage(0.8)

    def normalSize(self):
        self.image_label.adjustSize()
        self.scale_factor = 1.0

    def fitToWindow(self, fit: bool):
        self.setWidgetResizable(fit)
        if not fit:
            self.normalSize()

    def wheelEvent(self, event: QWheelEvent) -> None:
        num_pixels = event.pixelDelta()
        num_degrees = 1 - (event.angleDelta().y() / 800)
        if self.image and event.modifiers() == Qt.ControlModifier:
            self.scaleImage(num_degrees)
            log.debug(f'numpixel {num_pixels} numDegrees {num_degrees}')

    def resizeEvent(self, event: QResizeEvent) -> None:
        log.debug(f'resize {event.size()}')
        old = self.image_label.pixmap().size()
        w,h = event.size().width(), event.size().height()
        img_w, img_h = old.width(), old.height()
        new_size = self.resize_((img_w, img_h), (w, h))
        log.debug(f'new: {new_size} old: {old}')
        self.image_label.resize(new_size[0], new_size[1])


    def resize_(self, img_size, self_size):
        x, y = map(math.floor, self_size)
        if x >= img_size[0] and y >= img_size[1]:
            return

        def round_aspect(number, key):
            return max(min(math.floor(number), math.ceil(number), key=key), 1)

        # preserve aspect ratio
        aspect = img_size[0] / img_size[1]
        if x / y >= aspect:
            x = round_aspect(y * aspect, key=lambda n: abs(aspect - n / y))
        else:
            y = round_aspect(
                x / aspect, key=lambda n: 0 if n == 0 else abs(aspect - x / n)
            )
        size = (x, y)
        return size

mariann = '/home/mate/Pictures/2021_04_28_Mariann/DSC09738.JPG'
moon = '/home/mate/Pictures/2021_04_27_Supermoon/dark/DSC09721.jpg'

if __name__ == '__main__':
    app = QApplication([])
    window = QMainWindow()
    widget = ImageWidget()
    widget.loadFile(moon)
    widget.rotate(90)
    widget.fitToWindow(False)
    # widget.show()
    window.setCentralWidget(widget)
    window.resize(QGuiApplication.primaryScreen().availableSize() * 3 / 5)
    window.show()
    sys.exit(app.exec_())