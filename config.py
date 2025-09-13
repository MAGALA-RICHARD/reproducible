from apsimNGpy.core.config import set_apsim_bin_path, get_apsim_bin_path, apsim_version
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
CUR_BIN_PATH = get_apsim_bin_path()

base_dir = Path(__file__).parent
# get bin bath
if platform.system() == 'Windows':
    env_BIN_PATH = Path(base_dir/r'bin_dist\APSIM2025.8.7844.0\bin')
elif platform.system() == 'Darwin':
    env_BIN_PATH = Path(base_dir / base_dir/r'bin_dist/contents')
else:
    pt = str(input('pre compiled binaries are not provide for this operating system. please supply the path of the binaries here: '))
    env_BIN_PATH = Path(pt)
    if not env_BIN_PATH.exists():
        raise NotImplementedError('path supplied does not exist ')
set_bin = set_apsim_bin_path(env_BIN_PATH)

version = apsim_version()
if set_bin:
    logger.info(f"{version} successfully loaded to path")



