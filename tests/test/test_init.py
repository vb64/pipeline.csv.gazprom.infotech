"""Package pipeline_csv_gazprom_infotech tests.

make test T=test_init.py
"""
from pipeline_gazprom_infotech.ipl import Infotech, LineObj as LineObjAttr
from pipeline_gazprom_infotech.codes import Tube as TubeType, Feature

from pipeline_csv.csvfile.row import Row
from pipeline_csv.csvfile.tubes import Tube
from pipeline_csv.csvfile.defect import Defect
from pipeline_csv.csvfile import Stream
from pipeline_csv import TypeHorWeld, DefektSide

from pipeline_csv.oegiv import Row as CsvRow, TypeDefekt, TypeMarker, File as CsvFile

from . import TestBase


class TestInit(TestBase):
    """Module __init__.py."""

    def test_get_diam_infotech(self):
        """Check get_diam_infotech function."""
        from pipeline_csv_gazprom_infotech import get_diam_infotech

        assert get_diam_infotech(1, 2, {}) is None

    def test_add_diam_change(self):
        """Check add_diam_change function."""
        from pipeline_csv_gazprom_infotech import add_diam_change

        row = Row.as_diam(100, 1400, 100)
        assert add_diam_change(None, row, {}) == 0

    def test_get_seam2(self):
        """Check get_seam2 function."""
        pipe = Tube(Row.as_weld(100, custom_number='1'), Stream(), "")
        pipe.seams = []
        pipe.add_object(Row.as_seam(
          pipe.dist + 10,
          TypeHorWeld.SECOND,
          '1,10', '7,10'
        ))
        assert pipe.typ == TypeHorWeld.SECOND
        assert pipe.seam2.as_minutes == 430

    def test_it_size(self):
        """Check it_size function."""
        from pipeline_csv_gazprom_infotech import it_size

        assert it_size(None) == ""
        assert it_size(0) == ""
        assert it_size("0") == ""
        assert it_size("0.0") == ""

    def test_add_pipe(self):
        """Check add_pipe function."""
        import pipeline_csv_gazprom_infotech

        ldict = {}
        ddict = {}
        save = pipeline_csv_gazprom_infotech.pipe_type
        pipeline_csv_gazprom_infotech.pipe_type = lambda pipe: TubeType.ODNOSHOV

        xml = Infotech()
        pipe = Tube(Row.as_weld(100, custom_number='1'), Stream(), "")
        pipe.thick = '105'
        pipe.length = 100
        obj_dict = {}
        assert pipeline_csv_gazprom_infotech.add_pipe(
          pipe, xml, obj_dict, ldict, ddict, None, None
        ) is not None
        assert len(obj_dict) > 0

        pipeline_csv_gazprom_infotech.pipe_type = save

    def test_add_defect(self):
        """Check add_defect function."""
        from pipeline_csv_gazprom_infotech import add_defect

        pipe = Tube(CsvRow.as_weld(100, custom_number='1'), Stream(), "")
        row = CsvRow.as_defekt(
          110,
          TypeDefekt.CORROZ, DefektSide.UNKNOWN,
          None, None, None, None, None, None, None, ""
        )
        assert add_defect(None, Defect(row, pipe), {}, {}, None) == 0

    def test_add_lineobject(self):
        """Check add_lineobject function."""
        from pipeline_csv_gazprom_infotech import add_lineobject

        xml = Infotech()
        obj = CsvRow.as_lineobj(100, TypeMarker.OTVOD, "xxx", 0, "")
        assert add_lineobject(xml, obj, {}, {}, None) == 0

        obj.object_name = "xxx"
        trans_dict = {
          TypeMarker.OTVOD: Feature.OTVOD_VREZKA,
        }

        def custom_handler(xml_item, custom_data):
            """Handle custom data."""
            xml_item.attrib[LineObjAttr.Rem] = custom_data

        assert add_lineobject(xml, obj, {}, trans_dict, custom_handler) == 1

    def test_pipe_type(self):
        """Check pipe_type function."""
        from pipeline_csv_gazprom_infotech import pipe_type

        pipe = Tube(
          Row.as_weld(100, custom_number='1'),
          Stream(),
          ""
        )
        assert not pipe.seams
        assert pipe_type(pipe) == TubeType.UNKNOWN

        pipe.seams = [Row.as_seam(101, TypeHorWeld.NO_WELD, None, None)]
        assert pipe_type(pipe) == TubeType.BEZSHOV

        pipe.seams = [Row.as_seam(101, TypeHorWeld.UNKNOWN, None, None)]
        assert pipe_type(pipe) == TubeType.UNKNOWN

        pipe.seams = [Row.as_seam(101, TypeHorWeld.SPIRAL, None, None)]
        assert pipe_type(pipe) == TubeType.SPIRAL

        pipe.seams = [
          Row.as_seam(101, TypeHorWeld.HORIZONTAL, None, None),
          Row.as_seam(102, TypeHorWeld.HORIZONTAL, None, None),
        ]
        assert pipe_type(pipe) == TubeType.DVUSHOV

    def test_translate(self):
        """Check translate function."""
        from pipeline_csv_gazprom_infotech import translate

        csv_data = CsvFile.from_file(self.fixture("iv.csv"), diameter=1400)
        xml = Infotech()
        ldict = {
          TypeMarker.OTVOD: Feature.OTVOD_VREZKA,
          TypeMarker.MARKER: Feature.MARKER,
          TypeMarker.MAGNET: Feature.MARKER_MAGN,
          TypeMarker.TROYNIK: Feature.TROYNIK,
          TypeMarker.VALVE: Feature.VALVE,
        }
        ddict = {
          TypeDefekt.CORROZ: Feature.CORROZ,
          TypeDefekt.MECHANIC: Feature.MECHANICAL_DEFEKT,
          TypeDefekt.DENT: Feature.DENT,
        }

        assert translate(csv_data, xml, ldict, ddict, None, None) == (41, 64, 5)
