"""
Tests for APSIM NG binary path configuration (config_utils.py)
==============================================================

Purpose
-------
Exercise edge cases and platform-specific logic in the configuration helpers that
locate and validate the APSIM NG executables/libraries.

Covers
------
- ``validate_get_apsim_bin_path(None)`` should return a ``Path`` placeholder that
  may not exist (signals "unset" rather than crashing).
- ``validate_get_apsim_bin_path(get_apsim_bin_path())`` should resolve to an
  existing path on a correctly configured system.
- ``configure_bin_path(...)`` behavior under multiple scenarios:
  * preferred path is ``None`` (falls back to current/auto-detected),
  * current path is ``None`` (selects a valid path or returns a safe value),
  * preferred path provided and structurally valid → accepted,
  * preferred path missing required executables → raises ``ApsimBinPathConfigError``.
- Unsupported platform guard: passing an unknown ``os_platform`` raises ``ApsimBinPathConfigError``.
- Cross-platform branch: when running on Windows, asking for macOS (``'Darwin'``)
  logic with an empty current bin path is expected to raise
  ``ApsimBinPathConfigError`` (protects against selecting incompatible layouts).

Test strategy
-------------
- Uses a temporary directory that mimics an APSIM bin layout:
  * Windows: creates stub ``Models.exe`` and ``Models.dll``.
  * Unix-like: creates a ``Models/`` folder and a stub ``Models.dll``.
- No actual binaries are executed; presence checks are structural only.
- Original configuration is restored at the end of tests that modify state.

Prerequisites
-------------
- ``config_utils.py`` exporting:
  ``validate_get_apsim_bin_path``, ``configure_bin_path``, ``logger``,
  and ``ApsimBinPathConfigError``.
- ``apsimNGpy.core.config.get_apsim_bin_path`` available.
- Python ``unittest`` standard library.

How to run
----------
From the repository root (or the directory containing this file):

.. code-block:: bash

   python -m unittest -v path/to/this_test_file.py

Notes
-----
- These tests do not require network or APSIM execution—only filesystem access.
- If your environment uses nonstandard APSIM layouts, adjust the "marker" files
  in the temporary bin to align with your validator’s requirements.
"""

import platform
import tempfile
import unittest
from config_utils import validate_get_apsim_bin_path, configure_bin_path, logger, ApsimBinPathConfigError
from apsimNGpy.core.config import get_apsim_bin_path
from pathlib import Path


class TestConfiguration(unittest.TestCase):
    def setUp(self) -> None:
        self.get_apsim_bin_path_none = None

    def test_validate_get_apsim_bin_path_when_none(self):
        ans = validate_get_apsim_bin_path(self.get_apsim_bin_path_none)
        self.assertIsInstance(ans, Path)
        if isinstance(ans, Path):
            self.assertFalse(ans.exists())

    def test_configure_bin_path_when_not_None(self):
        ans = validate_get_apsim_bin_path(get_apsim_bin_path())
        self.assertTrue(ans.exists())

    def test_configure_bin_path_when_prefered_is_none(self):
        ans = configure_bin_path(get_apsim_bin_path(), prefered=None)
        self.assertTrue(ans, msg=f" configure_bin_path failed when preferred bin is none")

    def test_configure_bin_path_when_current_bin_is_none(self):
        ans = configure_bin_path(current_bin=None, prefered=None)
        self.assertTrue(ans, msg=f" configure_bin_path failed when current bin is none")

    def test_configure_bin_path_when_current_preferred(self):
        """test that configure_bin_path is set correctly when preferred is provided"""
        # Arrange: create a throwaway bin dir that "looks" like an APSIM bin
        current = get_apsim_bin_path()
        with tempfile.TemporaryDirectory() as td:
            bin_d = Path(td) / "bin_test_dir"
            bin_d.mkdir(parents=True, exist_ok=True)

            # Create minimal markers so _is_valid_bin_dir(bin_d) will pass
            if platform.system() == "Windows":
                (bin_d / "Models.exe").write_text(
                    "")  # empty file is fine for the test, but there is a cath it will provide invalid dir later
                (bin_d / "Models.dll").touch()
            else:
                (bin_d / "Models").mkdir(exist_ok=True)  # folder commonly present
                (bin_d / "Models.dll").touch()

            # Act: prefer this directory; current_bin intentionally None/invalid

            ans = configure_bin_path(current_bin=None, prefered=bin_d)
            # Assert
            self.assertIsNotNone(ans, msg="configure_apsim_bin returned None")
            # 3 lastly reset back to normal
            cc = configure_bin_path(current_bin=current, prefered=None)
            if cc is not None:
                logger.info(f"bin path configured back after testing another dir")
            else:
                logger.info(f"bin path reset failed")

    def test_configure_bin_path_when_current_preferred_has_no_executables(self):
        """test that configure_bin_path is set correctly when preferred is provided"""
        # Arrange: create a throwaway bin dir that "looks" like an APSIM bin
        with self.assertRaises(ApsimBinPathConfigError):
            with tempfile.TemporaryDirectory() as td:
                bin_d = Path(td) / "bin_test_dir"
                bin_d.mkdir(parents=True, exist_ok=True)
                ans = configure_bin_path(current_bin=None, prefered=bin_d)
                # Assert
                self.assertIsNotNone(ans, msg="configure_apsim_bin returned None")

    def test_configure_bin_path_when_os_is_not_supported(self):
        """test that configure_bin_path is set correctly when os is not supported. we expect an ApsimBinPathConfigError,
         only if the preferred path is none of current_bin is none
        """
        with self.assertRaises(ApsimBinPathConfigError):
            configure_bin_path(current_bin="", prefered=None, os_platform='linux')

    def test_configure_bin_path_when_os_is_macOS(self):
        """test that configure_bin_path is set correctly when os is MacOS, just test if the current bin path is valid
        """
        if platform.system() == 'Windows':
            with self.assertRaises(ApsimBinPathConfigError):
                # because internally set_apsim_bin_path apply the appropriate logic to each OS platform, this will raise
                # an ApsimBinPathConfigError, but it helps in not selecting the wrong dir for each platform
                configure_bin_path(current_bin="", prefered=None, os_platform='Darwin')


if __name__ == '__main__':
    unittest.main(verbosity=0)
