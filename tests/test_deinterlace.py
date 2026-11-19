import pytest

from media import deinterlace as mod

CASES = [
    pytest.param('field_order', ('top', 'bottom'), 'top', False, id='01_material_field_order'),
    pytest.param('motion_score', ([0, 0], [1, 0], [1, 1]), 2, False, id='02_motion_score'),
    pytest.param('motion_threshold', (0.01, 0.1), 0.14, True, id='03_adaptive_motion_threshold'),
    pytest.param('timecode_seconds', (30000, 30000, 1001), 1001.0, True, id='04_rational_timecode'),
    pytest.param('drop_frame_timecode', (17982,), 599.9994, True, id='05_drop_frame_timecode'),
    pytest.param('field_height', (1080, 'top'), 540, False, id='06_field_height'),
    pytest.param('convert_color', ((0.5, 0.5, 0.5), 'linear', 'srgb'), (0.7491535384383408, 0.7491535384383408, 0.7491535384383408), True, id='07_linear_to_srgb'),
    pytest.param('multicam_order', ({'camA': 'top', 'camB': 'bottom'}, 'camB'), 'bottom', False, id='08_multicam_order_table'),
    pytest.param('resolve_order', (None, 'top', 'bottom'), 'top', False, id='09_order_priority'),
    pytest.param('export_interlaced', (True, 'top'), (False, 'top'), False, id='10_export_marker'),
    pytest.param('weave_fields', ([1, 2], [3, 4], 'top'), (1, 3, 2, 4), False, id='11_weave_top_first'),
    pytest.param('bob_field', ([1, 2], 'top'), (1, 1, 2, 2), False, id='12_bob_field'),
    pytest.param('cadence_index', (7,), 2, False, id='13_cadence_index'),
    pytest.param('frame_height', (540,), 1080, False, id='14_frame_from_field_height'),
    pytest.param('color_matrix', ((1.0, 0.0, 0.0), ((1, 0, 0), (0, 1, 0), (0, 0, 1))), (1.0, 0.0, 0.0), True, id='15_color_matrix'),
]


def assert_close(actual, expected):
    if isinstance(expected, tuple):
        assert isinstance(actual, tuple) and len(actual) == len(expected)
        for a, e in zip(actual, expected):
            assert_close(a, e)
    elif isinstance(expected, list):
        assert isinstance(actual, list) and len(actual) == len(expected)
        for a, e in zip(actual, expected):
            assert_close(a, e)
    elif isinstance(expected, dict):
        assert actual.keys() == expected.keys()
        for key in expected:
            assert_close(actual[key], expected[key])
    else:
        assert actual == pytest.approx(expected)


@pytest.mark.parametrize("func_name,args,expected,approx", CASES)
def test_deinterlace_contract(func_name, args, expected, approx):
    func = getattr(mod, func_name)
    result = func(*args)
    if approx:
        assert_close(result, expected)
    else:
        assert result == expected
