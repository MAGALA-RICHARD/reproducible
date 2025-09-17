# from dotenv import load_dotenv
import logging
from pathlib import Path

from apsimNGpy.core.config import set_apsim_bin_path, get_apsim_bin_path, apsim_version

from config_utils import validate_get_apsim_bin_path, configure_bin_path, logger

logger.info('setting APSIM bin path')

CUR_BIN_PATH = validate_get_apsim_bin_path(get_apsim_bin_path())

configure_bin_path(CUR_BIN_PATH)
