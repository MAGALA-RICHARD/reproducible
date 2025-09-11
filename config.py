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


# load env
load_dotenv()
# get a current bin path
CUR_BIN_PATH = get_apsim_bin_path()

# get bin bath
env_BIN_PATH = Path(r'./dist/APSIM_2025.8.7844.0').resolve()

set_apsim_bin_path(env_BIN_PATH)

version = apsim_version()
logger.info(f"{version} successfully loaded to path")



