from apsimNGpy.core.config import set_apsim_bin_path, get_apsim_bin_path
from dotenv import load_dotenv

# load env
load_dotenv()
# get a current bin path
CUR_BIN_PATH = get_apsim_bin_path()

# get bin bath
env_BIN_PATH = 'APSIM2025.8.7844.0'

set_apsim_bin_path(env_BIN_PATH)
