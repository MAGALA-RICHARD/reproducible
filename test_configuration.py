import platform
import shutil
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
        with tempfile.TemporaryDirectory() as td:
            bin_d = Path(td) / "bin_test_dir"
            bin_d.mkdir(parents=True, exist_ok=True)

            # Create minimal markers so _is_valid_bin_dir(bin_d) will pass
            if platform.system() == "Windows":
                (bin_d / "Models.exe").write_text("")  # empty file is fine for the test
                (bin_d / "Models.dll").touch()
            else:
                (bin_d / "Models").mkdir(exist_ok=True)  # folder commonly present
                (bin_d / "Models.dll").touch()

            # Act: prefer this directory; current_bin intentionally None/invalid

            ans = configure_bin_path(current_bin=None, prefered=bin_d)
            # Assert
            self.assertIsNotNone(ans, msg="configure_apsim_bin returned None")

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
            configure_bin_path(current_bin="", prefered=None, os_platform='linnux')

    def test_configure_bin_path_when_os_is_macOS(self):
        """test that configure_bin_path is set correctly when os is MacOS, just test if the current bin path is valid
        """
        with self.assertRaises(ApsimBinPathConfigError):
            # because internally set_apsim_bin_path apply the appropriate logic to each OS platform, this will raise
            # an ApsimBinPathConfigError, but it helps in not selecting the wrong dir for each platform
            ans = configure_bin_path(current_bin="", prefered=None, os_platform='Darwin')


if __name__ == '__main__':
    unittest.main(verbosity=2)
