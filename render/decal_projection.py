"""第 61 批：贴花投影修复。

修复点对应：
- depth_along       深度重建：沿表面法线而不是世界坐标投影
- normal_weight     法线混合：乘法混合替代加法，粗糙表面高光方向正确
- dynamic_bias      动态深度偏移：随深度与斜率缩放，消除斜坡/曲面 Z-fighting
- atlas_clamp       图集边界：UV clamp 到格内 inset，边缘透明防邻格渗色
- skinned_position  蒙皮位置：绑定姿势位置 + 当前姿势偏移，角色运动不漂移
- decal_life        生命周期：时间驱动，暂停时冻结而非永久挂起
- camera_key        多相机去重：相机/贴花联合键，分屏不重复叠加
- hdr_scale         HDR 映射：按曝光缩放后再走色调映射
- grazing_fade      掠射淡出：接近掠射角时 alpha 趋零，墙边缘不拉长条
- stencil_mask      模板裁剪：位测试处理几何体裁切与交叠
- transparent_order 透明排序：按深度决定贴花与玻璃的先后，互不吞
- instance_transform 实例变换：每实例独立矩阵，批次间不共享
- cache_version     缓存版本：材质 ID + 贴图版本联合键，换图不命中旧缓存
"""


def depth_along(normal, distance):
    """沿法线重建深度：法线向量乘以距离，返回各轴深度分量。"""
    return tuple(component * distance for component in normal)


def normal_weight(base_z, decal_z):
    """法线混合权重：乘法混合（白盒 1.0 为中性），替代错误的加法混合。"""
    return base_z * decal_z


def dynamic_bias(depth, slope):
    """动态深度偏移：基础深度随斜率放大，陡坡/曲面给更大偏移防 Z-fighting。"""
    return depth * (1.0 + 0.1 * slope)


def atlas_clamp(uv, inset):
    """图集边界 clamp：把 UV 限制在 [inset, 1-inset] 格内，边缘落到透明纹素。"""
    return max(inset, min(1.0 - inset, uv))


def skinned_position(bind, offset):
    """蒙皮贴花位置：绑定姿势位置叠加当前姿势的蒙皮偏移，逐分量相加。"""
    return tuple(bind_component + offset_component
                 for bind_component, offset_component in zip(bind, offset))


def decal_life(life, paused, dt=0.0):
    """贴花生命周期（时间驱动）。

    暂停时冻结剩余寿命；运行时按真实时间步 dt 衰减并钳到 0，
    不再按帧数计数，避免暂停后永久不消失。
    """
    if paused:
        return life
    return max(0.0, life - dt)


def camera_key(camera_id, decal_id):
    """多相机贴花去重键：相机与贴花联合标识，同一贴花在分屏下只渲染一份。"""
    return f"{camera_id}:{decal_id}"


def hdr_scale(color, exposure):
    """HDR 颜色按曝光缩放，结果交给色调映射阶段处理亮部。"""
    return color * exposure


def grazing_fade(angle, min_angle):
    """掠射淡出：入射角达到 min_angle 时淡出为 0，正面（0 度）为 1。"""
    if min_angle <= 0.0:
        return 0.0
    return max(0.0, 1.0 - angle / min_angle)


def stencil_mask(mask, bit):
    """模板裁剪：位与测试贴花模板位是否在当前模板掩码中置位。"""
    return mask & bit


def transparent_order(decal_z, glass_z):
    """透明排序：贴花比玻璃更靠近相机（z 更小）时返回 True，保证远到近排序不互吞。"""
    return decal_z < glass_z


def instance_transform(base, rotation):
    """实例变换：每实例在自己的基础变换上叠加旋转，不共享批次矩阵。"""
    return tuple(base_component + rotation_component
                 for base_component, rotation_component in zip(base, rotation))


def cache_version(material_id, version):
    """贴花缓存键：材质 ID 加贴图版本，换贴图后版本变化即失效旧缓存。"""
    return f"{material_id}:{version}"


def fade_alpha(distance, max_distance):
    """距离淡出：随距离线性衰减到 0，超出最大距离完全透明。"""
    if max_distance <= 0.0:
        return 0.0
    return max(0.0, 1.0 - distance / max_distance)


def project_uv(world_uv, scale):
    """投影 UV 缩放：世界坐标投影值按贴花缩放映射到 UV 空间。"""
    return world_uv * scale
