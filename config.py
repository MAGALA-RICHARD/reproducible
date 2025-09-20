"""
It is used in all scripts to enforce the distributed APSIM binaries to be set to path
"""
from apsimNGpy.core.config import get_apsim_bin_path

from config_utils import validate_get_apsim_bin_path, configure_bin_path, logger, BASE_DIR, base_dir

logger.info('setting APSIM bin path')

CUR_BIN_PATH = validate_get_apsim_bin_path(get_apsim_bin_path())

configure_bin_path(CUR_BIN_PATH, verbose=True)


