"""去隔行：场序、运动自适应与有理时间码：待实现的核心模块。"""

from __future__ import annotations


def field_order(metadata_order, container_order):
    """按素材标记优先返回场序。"""
    raise NotImplementedError

def motion_score(prev, curr, next):
    """三帧亮度差运动强度。"""
    raise NotImplementedError

def motion_threshold(noise, base):
    """随噪声自适应的运动阈值。"""
    raise NotImplementedError

def timecode_seconds(frames, fps_num, fps_den):
    """有理帧率下的时间码秒数。"""
    raise NotImplementedError

def drop_frame_timecode(frames, fps_num=30000, fps_den=1001):
    """下拉时间码秒数。"""
    raise NotImplementedError

def field_height(frame_height, order):
    """单场高度。"""
    raise NotImplementedError

def convert_color(rgb, src, dst):
    """解隔行前后色彩空间转换。"""
    raise NotImplementedError

def multicam_order(orders, camera_id):
    """多机位场序表查询。"""
    raise NotImplementedError

def resolve_order(metadata_order, container_order, override):
    """场序标记优先级。"""
    raise NotImplementedError

def export_interlaced(progressive, order):
    """导出隔行标记校验结果。"""
    raise NotImplementedError

def weave_fields(top, bottom, order):
    """按场序交织两场。"""
    raise NotImplementedError

def bob_field(field, order):
    """单场行复制。"""
    raise NotImplementedError

def cadence_index(frame):
    """5:2 下拉节奏索引。"""
    raise NotImplementedError

def frame_height(field_height):
    """帧高由场高还原。"""
    raise NotImplementedError

def color_matrix(rgb, matrix):
    """应用 3x3 色彩矩阵。"""
    raise NotImplementedError
