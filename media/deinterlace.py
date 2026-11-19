"""去隔行核心：场序、运动自适应与有理时间码。

约定：
- 场序取值 'top'（上场优先）/ 'bottom'（下场优先）。
- 场序标记优先级：素材元数据 > 容器标记 > 手动覆盖兜底。
- 时间码一律用有理帧率 (fps_num/fps_den) 计算，避免 29.97 累计漂移。
"""

from __future__ import annotations

TOP = 'top'
BOTTOM = 'bottom'

# 线性 <-> sRGB 使用的伽马指数
_SRGB_GAMMA = 2.4


def field_order(metadata_order, container_order):
    """按素材标记优先返回场序：素材元数据优先于容器标记。"""
    if metadata_order is not None:
        return metadata_order
    return container_order


def motion_score(prev, curr, next):
    """三帧亮度差运动强度：|curr-prev| 与 |next-curr| 的逐元素绝对差之和。"""
    score = 0
    for p, c in zip(prev, curr):
        score += abs(c - p)
    for c, n in zip(curr, next):
        score += abs(n - c)
    return score


def motion_threshold(noise, base):
    """随噪声自适应的运动阈值：噪声越大阈值越高，慢镜头不被误判为静止。"""
    return base + 4.0 * noise


def timecode_seconds(frames, fps_num, fps_den):
    """有理帧率下的时间码秒数：frames * fps_den / fps_num。"""
    return frames * fps_den / fps_num


def drop_frame_timecode(frames, fps_num=30000, fps_den=1001):
    """下拉（drop-frame）素材的真实秒数，按有理帧率换算，不按帧号取整。"""
    return frames * fps_den / fps_num


def field_height(frame_height, order):
    """单场高度：帧高的一半，与帧高严格分离，不与帧高混用。"""
    return frame_height // 2


def convert_color(rgb, src, dst):
    """解隔行前后色彩空间转换，保证链路中色彩空间一致。"""
    if src == dst:
        return tuple(rgb)
    if src == 'linear' and dst == 'srgb':
        return tuple(c ** (1.0 / _SRGB_GAMMA) for c in rgb)
    if src == 'srgb' and dst == 'linear':
        return tuple(c ** _SRGB_GAMMA for c in rgb)
    raise ValueError(f'unsupported color conversion: {src} -> {dst}')


def multicam_order(orders, camera_id):
    """多机位场序表查询：每个机位按自己的场序，切换时不沿用上一机位。"""
    return orders[camera_id]


def resolve_order(metadata_order, container_order, override):
    """场序标记优先级：素材元数据 > 容器标记 > 手动覆盖。"""
    for order in (metadata_order, container_order, override):
        if order is not None:
            return order
    return None


def export_interlaced(progressive, order):
    """导出隔行标记校验：逐行素材不得再标记为隔行，返回 (隔行标记, 场序)。"""
    if progressive:
        return (False, order)
    return (True, order)


def weave_fields(top, bottom, order):
    """按场序交织两场：'top' 上场行在前，'bottom' 下场行在前。"""
    first, second = (top, bottom) if order == TOP else (bottom, top)
    out = []
    for a, b in zip(first, second):
        out.append(a)
        out.append(b)
    return tuple(out)


def bob_field(field, order):
    """单场行复制：每场行复制一次，补齐整帧高度。"""
    out = []
    for line in field:
        out.append(line)
        out.append(line)
    return tuple(out)


def cadence_index(frame):
    """5:2 下拉节奏索引：帧号对 5 取模。"""
    return frame % 5


def frame_height(field_height):
    """帧高由场高还原：场高的两倍。"""
    return field_height * 2


def color_matrix(rgb, matrix):
    """应用 3x3 色彩矩阵：out[i] = sum(matrix[i][j] * rgb[j])。"""
    r, g, b = rgb
    return tuple(
        float(m[0] * r + m[1] * g + m[2] * b)
        for m in matrix
    )
