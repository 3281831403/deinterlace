# 去隔行：场序、运动自适应与有理时间码

隔行素材场序经常反：不按素材标记、混合场产生重影、阈值写死、29.97 时间码漂移、丢帧复制错场、分辨率切换场高帧高混用。本仓库固定场序与时间基。

- 领域：游戏、图形与多媒体
- 子方向：音视频处理
- 语言/框架：Python 3, pytest
- 初始状态：15 个参数化用例全部失败

## 目录结构

```
README.md
conftest.py
.gitignore
media/__init__.py
media/deinterlace.py
tests/test_deinterlace.py
```

## 需要修复的 10 个问题

1. 按素材场序标记决定上场/下场优先，不靠容器猜测
2. 运动自适应去隔行，快速横向运动不把两场揉成重影
3. 运动阈值随噪声与镜头自适应，慢镜头不被当静止
4. 时间码按有理数帧率计算，29.97 下拉不累计漂移
5. 丢帧时保持场序，不直接复制上一场造成错位
6. 场高与帧高分开处理，分辨率切换不拉伸半帧
7. 解隔行前后统一色彩空间，肤色不发绿
8. 多机位维护各自场序表，切换不闪
9. 硬件解码与容器场标记冲突时按明确优先级
10. 导出时校验逐行/隔行标记，避免播放器二次解隔行

## 15 条验收契约

    01. material field order — `field_order`
    02. motion score — `motion_score`
    03. adaptive motion threshold — `motion_threshold`
    04. rational timecode — `timecode_seconds`
    05. drop frame timecode — `drop_frame_timecode`
    06. field height — `field_height`
    07. linear to srgb — `convert_color`
    08. multicam order table — `multicam_order`
    09. order priority — `resolve_order`
    10. export marker — `export_interlaced`
    11. weave top first — `weave_fields`
    12. bob field — `bob_field`
    13. cadence index — `cadence_index`
    14. frame from field height — `frame_height`
    15. color matrix — `color_matrix`

## 当前状态

`media/deinterlace.py` 只保留函数签名与文档字符串，所有函数体统一
`raise NotImplementedError`。`tests/test_deinterlace.py` 使用一个
`@pytest.mark.parametrize` 装载 15 条契约，初始全部失败且没有 collection error。

```bash
python -m pytest -q
```

预期输出包含 `15 failed`。实现 `media/deinterlace.py` 后，15 条契约应全部通过。
