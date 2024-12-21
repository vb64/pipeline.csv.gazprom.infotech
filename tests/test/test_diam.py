"""Package pipeline_csv_gazprom_infotech tests.

make test T=test_diam.py
"""
from . import TestBase


class TestDiam(TestBase):
    """Module diam.py."""

    def test_get_code(self):
        """Check get_code method."""
        from pipeline_csv_gazprom_infotech.diam import DiamChange, D_1400, D_1200

        diam = DiamChange("xxx", "zzz", D_1400, D_1200)
        assert diam.get_code(1400, 1200) == ("xxx", "zzz")
        assert diam.get_code(700, 500) is None
