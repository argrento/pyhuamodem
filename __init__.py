"""puhuamodem provides user friendly interface to advanced features of 3g modems.
Modules:
    errors - exceptions and error-handling methods,
    huamodem - the Modem() class and it's dependencies.
"""

__version__ = '0.1'

import huamodem.errors
from huamodem.huamodem import Modem