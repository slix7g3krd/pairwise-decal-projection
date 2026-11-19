"""第 61 批：墙面弹孔贴花在斜视角下变成一条拉伸的条纹，换到角色身上又整片悬空..."""

def depth_along(normal, distance):
    """沿法线深度。"""
    raise NotImplementedError("TODO: depth_along")

def normal_weight(base_z, decal_z):
    """法线混合权重。"""
    raise NotImplementedError("TODO: normal_weight")

def dynamic_bias(depth, slope):
    """动态深度偏移。"""
    raise NotImplementedError("TODO: dynamic_bias")

def atlas_clamp(uv, inset):
    """图集边界 clamp。"""
    raise NotImplementedError("TODO: atlas_clamp")

def skinned_position(bind, offset):
    """蒙皮贴花位置。"""
    raise NotImplementedError("TODO: skinned_position")

def decal_life(life, paused):
    """贴花生命周期。"""
    raise NotImplementedError("TODO: decal_life")

def camera_key(camera_id, decal_id):
    """多相机贴花键。"""
    raise NotImplementedError("TODO: camera_key")

def hdr_scale(color, exposure):
    """HDR 颜色缩放。"""
    raise NotImplementedError("TODO: hdr_scale")

def grazing_fade(angle, min_angle):
    """掠射淡出。"""
    raise NotImplementedError("TODO: grazing_fade")

def stencil_mask(mask, bit):
    """模板裁剪。"""
    raise NotImplementedError("TODO: stencil_mask")

def transparent_order(decal_z, glass_z):
    """透明贴花排序。"""
    raise NotImplementedError("TODO: transparent_order")

def instance_transform(base, rotation):
    """实例变换。"""
    raise NotImplementedError("TODO: instance_transform")

def cache_version(material_id, version):
    """贴花缓存键。"""
    raise NotImplementedError("TODO: cache_version")

def fade_alpha(distance, max_distance):
    """距离淡出。"""
    raise NotImplementedError("TODO: fade_alpha")

def project_uv(world_uv, scale):
    """投影 UV 缩放。"""
    raise NotImplementedError("TODO: project_uv")
