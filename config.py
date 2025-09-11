from apsimNGpy.core.config import set_apsim_bin_path, get_apsim_bin_path, apsim_version
from dotenv import load_dotenv
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("app")

logger.info('setting APSIM bin path')
# load env
load_dotenv()
# get a current bin path
CUR_BIN_PATH = get_apsim_bin_path()

base_dir = Path(__file__).parent
# get bin bath
env_BIN_PATH = Path(base_dir/r'bin_dist\APSIM2025.8.7844.0\bin')

set_bin = set_apsim_bin_path(env_BIN_PATH)

version = apsim_version()
if set_bin:
    logger.info(f"{version} successfully loaded to path")



