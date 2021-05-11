from enum import Enum
from PIL import ExifTags

basic_xml_fmt = """
<?xml version="1.0" encoding="UTF-8"?>
<x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="XMP Core 4.4.0-Exiv2">
 <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
  <rdf:Description rdf:about=""
    xmlns:exif="http://ns.adobe.com/exif/1.0/"
    xmlns:xmp="http://ns.adobe.com/xap/1.0/"
    xmlns:xmpMM="http://ns.adobe.com/xap/1.0/mm/"
    xmlns:darktable="http://darktable.sf.net/"
   exif:DateTimeOriginal="{}"
   xmp:Rating="{}"
   xmpMM:DerivedFrom="{}"
   darktable:import_timestamp="{}"
   darktable:change_timestamp="-1"
   darktable:export_timestamp="-1"
   darktable:print_timestamp="-1"
   darktable:xmp_version="4"
   darktable:raw_params="0"
   darktable:auto_presets_applied="0"
   darktable:history_end="0"
   darktable:iop_order_version="1">
   <darktable:masks_history>
    <rdf:Seq/>
   </darktable:masks_history>
   <darktable:history>
    <rdf:Seq/>
   </darktable:history>
  </rdf:Description>
 </rdf:RDF>
</x:xmpmeta>
"""

EXTENSIONS = {'.tif', '.tiff', '.bmp', '.jpg', '.jpeg', '.png', '.raw', '.arw', '.nef', '.erf', '.pef', '.orf'}
RAW_EXTENSIONS = {'.erf', '.raw', '.arw', '.erf', '.pef', '.orf'}
ReverseExifTags = {v: k for k, v in ExifTags.TAGS.items()}

ROTATION_CODES = {0x1: 0, 0x3: 180, 0x6: 270, 0x8: 90}

FLASH_CODES = {
    0x0: 'No Flash',
    0x1: 'Fired',
    0x5: 'Fired, Return not detected',
    0x7: 'Fired, Return detected',
    0x8: 'On, Did not fire',
    0x9: 'On, Fired',
    0xd: 'On, Return not detected',
    0xf: 'On, Return detected',
    0x10: 'Off, Did not fire',
    0x14: 'Off, Did not fire, Return not detected',
    0x18: 'Auto, Did not fire',
    0x19: 'Auto, Fired',
    0x1d: 'Auto, Fired, Return not detected',
    0x1f: 'Auto, Fired, Return detected',
    0x20: 'No flash function',
    0x30: 'Off, No flash function',
    0x41: 'Fired, Red-eye reduction',
    0x45: 'Fired, Red-eye reduction, Return not detected',
    0x47: 'Fired, Red-eye reduction, Return detected',
    0x49: 'On, Red-eye reduction',
    0x4d: 'On, Red-eye reduction, Return not detected',
    0x4f: 'On, Red-eye reduction, Return detected',
    0x50: 'Off, Red-eye reduction',
    0x58: 'Auto, Did not fire, Red-eye reduction',
    0x59: 'Auto, Fired, Red-eye reduction',
    0x5d: 'Auto, Fired, Red-eye reduction, Return not detected',
    0x5f: 'Auto, Fired, Red-eye reduction, Return detected',
}

WHITE_BALANCE_CODES = {
    0x0: 'Auto',
    0x1: 'Manual'
}

COLOR_SPACE = {
    0x1: 'sRGB',
    0x2: 'Adobe RGB',
    0xfffd: 'Wide Gamut RGB',
    0xfffe: 'ICC Profile',
    0xffff: 'Uncalibrated',
}


class ExifKeys(Enum):
    MAKE = 'Make'
    MODEL = 'Model'
    DATE_TIME = 'DateTime'
    ORIENTATION = 'Orientation'
    FLASH = 'Flash'
    LENS_MAKE = 'LensMake'
    LENS_MODEL = 'LensModel'
    FOCAL_LENGTH = 'FocalLength'
    F_NUMBER = 'FNumber'
    ISO = 'ISOSpeedRatings'
    SHUTTER_SPEED = 'ExposureTime'
    WHITE_BALANCE = 'WhiteBalance'
    IMAGE_WIDTH = 'ExifImageWidth'
    IMAGE_HEIGHT = 'ExifImageHeight'
    COLOR_SPACE = 'ColorSpace'


