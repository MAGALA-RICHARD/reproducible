from apsimNGpy.core.config import load_crop_from_disk
import shutil, pathlib

maize = load_crop_from_disk('Maize', out='base.apsimx')
from apsimNGpy.core.apsim import ApsimModel





if __name__ == '__main__':
    for i in range(10):
        shutil.copy(maize, pathlib.Path('__{}__.apsimx'.format(i)).resolve())
