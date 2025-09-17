import sys

from apsimNGpy.core.config import set_apsim_bin_path, get_apsim_bin_path, apsim_version, locate_model_bin_path

# from dotenv import load_dotenv
import logging
from pathlib import Path
import platform

# do not move this file away from the root: reproducible
BASE_DIR = Path(__file__).parent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("app")

logger.info('setting APSIM bin path')
# load env
# load_dotenv()
# get a current bin path
CUR_BIN_PATH = get_apsim_bin_path()  # can return None
CUR_BIN_PATH = Path(CUR_BIN_PATH) if CUR_BIN_PATH and Path(CUR_BIN_PATH).exists() else Path('path/do/not/exist/here')
# locate bin_bath # still can return none, but raise errors related to directory of file not found catch
try:
    CUR_BIN_PATH = locate_model_bin_path(CUR_BIN_PATH)
except (FileNotFoundError, NotADirectoryError):
    # at this point, CUR_BIN_PATH does not exist, and not None
    pass
base_dir = Path(__file__).parent
# get bin bath
# preferred bin path are the compiled one provided in the root of the current directory
set_bin = False

try:
    if platform.system() == 'Windows':
        env_BIN_PATH = locate_model_bin_path(Path(base_dir / r'bin_dist\APSIM2025.8.7844.0\bin'))

    elif platform.system() == 'Darwin':
        env_BIN_PATH = locate_model_bin_path(Path(base_dir / base_dir / r'bin_dist/contents'))

    else:
        env_BIN_PATH = None
except (FileNotFoundError, NotADirectoryError):
    env_BIN_PATH = None

if not env_BIN_PATH:
    # at this point, the bin_path was not found or not supplied based on the OS platform
    pt = str(input('Pre compiled APSIM binaries are missing. Please supply the path of the '
                   'binaries here: '))
    env_BIN_PATH = Path(pt)
    env_BIN_PATH = locate_model_bin_path(env_BIN_PATH)
    if not env_BIN_PATH.exists():
        raise ValueError(f'path {env_BIN_PATH} supplied does not exist ')

if env_BIN_PATH.resolve() != CUR_BIN_PATH.resolve():  # set it once for every session
    set_bin = set_apsim_bin_path(env_BIN_PATH)


version = apsim_version()
if set_bin:
    logger.info(f"{version} successfully loaded to path")
else:
    logger.info(f'APSIM_BIN PATH of version {version} from the previous version is being used')
