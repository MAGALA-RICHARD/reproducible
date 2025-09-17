import platform
import logging
from apsimNGpy.core.config import locate_model_bin_path, set_apsim_bin_path, apsim_version
from apsimNGpy.exceptions import ApsimBinPathConfigError
from pathlib import Path

# do not move this file away from the root: reproducible
BASE_DIR = Path(__file__).parent

base_dir = Path(__file__).parent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("app")


def validate_get_apsim_bin_path(bin_path: str):
    CUR_BIN_PATH = bin_path
    CUR_BIN_PATH = Path(CUR_BIN_PATH) if CUR_BIN_PATH and Path(CUR_BIN_PATH).exists() else Path(
        'path/do/not/exist/here')
    # locate bin_bath # still can return none, but raise errors related to directory of file not found catch
    try:
        CUR_BIN_PATH = locate_model_bin_path(CUR_BIN_PATH)
    except (FileNotFoundError, NotADirectoryError):
        # at this point, CUR_BIN_PATH does not exist,but not None
        pass
    return CUR_BIN_PATH


def configure_bin_path(current_bin, os_platform=platform.system(), prefered=None):
    """
       Configure the APSIM NG *bin* directory for this process (reproducible capsule).

    This helper validates any already-configured path (`current_bin`) and, if needed,
    attempts to locate and set a usable APSIM **bin** directory. Resolution order:

    1) If `prefered` (sic) is provided: resolve with `locate_model_bin_path(prefered)`.
    2) Else choose an OS-specific repo default:
       - Windows  ->  <BASE_DIR>/bin_dist/APSIM2025.8.7844.0/bin
       - macOS    ->  <BASE_DIR>/bin_dist/contents
       - Linux/*  ->  no default (caller should pass `prefered`)
    3) If a candidate path is found and differs from the validated current path,
       set it via `set_apsim_bin_path(...)`.

    The function is **non-interactive** (no prompts), suitable for CI/tests. It logs
    what it did and returns `True` when a valid bin is available (either newly set
    or reusing an existing path).

    Parameters
    ------------------------

     current_bin : str | pathlib.Path | None The currently configured APSIM bin directory (e.g.,
    from `get_apsim_bin_path()`), or `None` if not set. Validated via `validate_get_apsim_bin_path`.

     os_platform: (str). This will be detected automatically no need to supply it. it is not included here for testing
    default=platform.system() Platform identifier used to choose built-in defaults. Expected values include
    "Windows" and "Darwin". Other values receive no built-in default.

    prefered : str | pathlib.Path | None (Spelling
    kept for backward compatibility.) A preferred bin directory to try first. When provided, it is resolved with
    `locate_model_bin_path` and this function raises NotADirecotry errror. preferred could be provided only if the
    platform is linnux or user wants to test other apsim versions. or the compiled one in the current have some issues

    Returns
    -------
    bool
        `True` if a valid APSIM bin path is available after this call (either newly set
        or an existing, validated path reused). No other truthy/falsey values are used.

    Raises
    ------
    ApsimBinPathConfigError
        If no valid APSIM bin directory can be determined (e.g., no default exists for
        this platform and `prefered` was not supplied, or supplied path cannot be located).
    FileNotFoundError, NotADirectoryError, which may propagate from `locate_model_bin_path(prefered)
       when the preferred path is invalid.

    Side Effects
    ------------
    - May call `set_apsim_bin_path(path)` to update the process-level APSIM bin.
    - Emits INFO/ERROR log messages describing the outcome (configured, reused, or failed).

    Notes
    -----
    - `BASE_DIR` must be defined at module scope; macOS default expects
      `<BASE_DIR>/bin_dist/contents`. On Linux (and other OS strings), pass `prefered`.
    - The function enforces a "set once per session" rule: it only calls
      `set_apsim_bin_path` when the resolved candidate differs from the validated current.
    - Designed for reproducible capsules: no user input, deterministic search order.

    Examples
    --------
    >>> # Use a repo-bundled Windows binary (explicit preferred path):
    >>> ok = configure_bin_path(
    ...     current_bin=get_apsim_bin_path(),
    ...     prefered=Path(BASE_DIR) / "bin_dist" / "APSIM2025.8.7844.0" / "bin"
    ... )
    >>> if not ok:
    ...     raise RuntimeError("APSIM bin not available")

    >>> # macOS default (if you ship contents in the repo); otherwise pass prefered:
    >>> ok = configure_bin_path(current_bin=get_apsim_bin_path(), os_platform="Darwin")

    >>> # Robust usage: handle failure explicitly
    >>> try:
    ...     configure_bin_path(current_bin=get_apsim_bin_path(), prefered="/opt/APSIM/bin")
    ... except ApsimBinPathConfigError as e:
    ...     logger.error("Could not configure APSIM bin: %s", e)
    ...     raise


    """
    CUR_BIN_PATH = validate_get_apsim_bin_path(current_bin)
    set_bin = False
    if prefered:
        env_BIN_PATH = locate_model_bin_path(prefered)
    else:
        try:
            if os_platform == "Windows":
                env_BIN_PATH = locate_model_bin_path(Path(base_dir / r'bin_dist\APSIM2025.8.7844.0\bin'))

            elif os_platform == 'Darwin':
                env_BIN_PATH = locate_model_bin_path(Path(base_dir / base_dir / r'bin_dist/contents'))

            else:
                env_BIN_PATH = None
        except (FileNotFoundError, NotADirectoryError):
            env_BIN_PATH = None

    if env_BIN_PATH:

        if env_BIN_PATH.resolve() != CUR_BIN_PATH.resolve():  # set it once for every session
            set_bin = set_apsim_bin_path(env_BIN_PATH)

        if set_bin:
            # We just set env_BIN_PATH successfully
            logger.info("APSIM Configure with bin path: → %s", str(env_BIN_PATH))
            return True
        elif CUR_BIN_PATH and CUR_BIN_PATH.exists():
            # No change; reusing an already-set path
            logger.info("loading APSIM with existing bin path: → %s:", str(CUR_BIN_PATH))
            return True
        else:
            # Nothing configured and no valid previous path
            logger.error("APSIM bin path is  not yet configured. Set APSIM_BIN path explicitly using "
                         "config_utils.configure_bin_path(prefered= 'your path'", )
    else:
        raise ApsimBinPathConfigError('APSIM bin path is not configured. Please install apsim or compile from github '
                                      'and provided the required bin path')
