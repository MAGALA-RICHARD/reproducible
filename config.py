from apsimNGpy.core.config import set_apsim_bin_path, get_apsim_bin_path, apsim_version
from apsimNGpy.exceptions import ApsimBinPathConfigError
from dotenv import load_dotenv
from pathlib import Path
import os

# load env
load_dotenv()
# get a current bin path
CUR_BIN_PATH = get_apsim_bin_path()

# get bin bath
env_BIN_PATH = os.getenv('APSIM_BIN', '')

# raise if env bin path is not valid

if not os.path.exists(env_BIN_PATH):
    raise ApsimBinPathConfigError('APSIM bin path provided in the .env file is not valid. please try again')

# logic for setting bin if valid
paths = [Path(env_BIN_PATH).resolve(), Path(CUR_BIN_PATH).resolve()]
for index, p in enumerate(paths):
    if not p.is_file():
        if p.stem != 'bin':
            p = p.joinpath('bin')
            paths[index] = p

if paths[0] != paths[1]:
    set_apsim_bin_path(env_BIN_PATH)
