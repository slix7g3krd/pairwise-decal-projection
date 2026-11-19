import pytest
from render import decal_projection as mod

CASES = [
    ("depth", 'm.depth_along((0.0, 1.0), 2.0) == (0.0, 2.0)'),
    ("normal", 'm.normal_weight(2.0, 3.0) == approx(6.0)'),
    ("bias", 'm.dynamic_bias(1.0, 2.0) == approx(1.2)'),
    ("atlas", 'm.atlas_clamp(0.0, 0.05) == approx(0.05)'),
    ("skinned", 'm.skinned_position((1.0, 2.0), (0.5, 0.5)) == approx((1.5, 2.5))'),
    ("life", 'm.decal_life(5.0, False) == approx(5.0)'),
    ("camera", 'm.camera_key(1, 2) == "1:2"'),
    ("hdr", 'm.hdr_scale(0.5, 2.0) == approx(1.0)'),
    ("grazing", 'm.grazing_fade(45.0, 45.0) == approx(0.0)'),
    ("stencil", 'm.stencil_mask(6, 2) == 2'),
    ("transparent", 'm.transparent_order(1.0, 2.0) is True'),
    ("instance", 'm.instance_transform((0.0, 0.0), (90.0, 0.0)) == approx((90.0, 0.0))'),
    ("cache", 'm.cache_version("m", "v1") == "m:v1"'),
    ("fade", 'm.fade_alpha(2.0, 4.0) == approx(0.5)'),
    ("project", 'm.project_uv(0.5, 2.0) == approx(1.0)')
]

@pytest.mark.parametrize("name,expr", CASES, ids=[c[0] for c in CASES])
def test_contract(name, expr):
    assert eval(expr, {"m": mod, "approx": pytest.approx})
