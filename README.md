# TikTok Indonesia 短视频内容流水线

面向印尼市场 TikTok 短视频的内容生产工具集,覆盖从拍摄脚本到发布文案、数据复盘的全流程。

## 功能模块

| 模块 | 文件 | 说明 |
|---|---|---|
| 拍摄脚本生成 | `shoot_script_generator.py` | 按产品/选题生成印尼语拍摄脚本(钩子+分镜+口播+CTA) |
| 成片检查 | `video_checker.py` | 用 ffprobe 检测成片是否符合脚本要求(时长/比例/首屏钩子等) |
| 视频剪辑 | `video_editor.py` | ffmpeg 封装:竖屏化裁剪、加字幕、加水印、掐头去尾 |
| 封面制作 | `cover_designer.py` | 从视频抽帧并叠加标题文字,产出封面图 |
| 发布文案生成 | `copywriting_generator.py` | 生成印尼语标题+正文+话题标签 |
| 数据分析 | `data_analyzer.py` | 结合 FastMoss MCP 数据(达人/商品/视频)整理复盘报告 |

## 环境依赖

```bash
pip install -r requirements.txt
```

需要系统安装 `ffmpeg`(用于 `video_editor.py` / `video_checker.py` / `cover_designer.py` 抽帧)。

## 典型流程

1. `shoot_script_generator.py` 生成脚本 → 现场拍摄
2. 成片剪辑完成后,`video_checker.py` 核对是否符合脚本(时长/比例/关键镜头)
3. `video_editor.py` 做后期处理(竖屏裁剪/字幕/水印)
4. `cover_designer.py` 出封面图
5. `copywriting_generator.py` 生成发布文案
6. 发布后用 `data_analyzer.py` + FastMoss MCP 工具做数据复盘
