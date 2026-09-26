"""封面制作工具 — 从视频抽帧并叠加标题文字,生成封面图。

用法:
    python cover_designer.py --video final.mp4 --time 2.0 --title "SERUM VIRAL INI!" --output cover.jpg
"""
import argparse
import subprocess
import tempfile
import os

from PIL import Image, ImageDraw, ImageFont


def extract_frame(video_path: str, timestamp: float, frame_path: str):
    cmd = [
        "ffmpeg", "-y", "-ss", str(timestamp), "-i", video_path,
        "-frames:v", "1", "-q:v", "2", frame_path,
    ]
    subprocess.run(cmd, check=True)


def overlay_title(frame_path: str, title: str, output_path: str, font_path: str = None):
    img = Image.open(frame_path).convert("RGB")
    draw = ImageDraw.Draw(img)

    font_size = int(img.width * 0.09)
    try:
        font = ImageFont.truetype(font_path or "DejaVuSans-Bold.ttf", font_size)
    except OSError:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), title, font=font)
    text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (img.width - text_w) / 2
    y = img.height * 0.75

    outline = 4
    for dx in range(-outline, outline + 1):
        for dy in range(-outline, outline + 1):
            draw.text((x + dx, y + dy), title, font=font, fill="black")
    draw.text((x, y), title, font=font, fill="white")

    img.save(output_path, quality=95)


def make_cover(video_path: str, timestamp: float, title: str, output_path: str):
    with tempfile.TemporaryDirectory() as tmp:
        frame_path = os.path.join(tmp, "frame.jpg")
        extract_frame(video_path, timestamp, frame_path)
        overlay_title(frame_path, title, output_path)


def main():
    parser = argparse.ArgumentParser(description="从视频抽帧生成封面图")
    parser.add_argument("--video", required=True, help="视频文件路径")
    parser.add_argument("--time", type=float, default=1.0, help="抽帧时间点(秒)")
    parser.add_argument("--title", required=True, help="封面标题文字")
    parser.add_argument("--output", required=True, help="输出封面图路径")
    args = parser.parse_args()

    make_cover(args.video, args.time, args.title, args.output)
    print(f"封面已生成: {args.output}")


if __name__ == "__main__":
    main()
