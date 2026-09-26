"""视频剪辑工具 — ffmpeg 常用操作封装:竖屏裁剪 / 加字幕 / 加水印 / 掐头去尾。

用法:
    python video_editor.py crop-vertical --input in.mp4 --output out.mp4
    python video_editor.py add-subtitle --input in.mp4 --srt cap.srt --output out.mp4
    python video_editor.py add-watermark --input in.mp4 --logo logo.png --output out.mp4
    python video_editor.py trim --input in.mp4 --start 2 --end 27 --output out.mp4
"""
import argparse
import subprocess


def run(cmd: list):
    print("$ " + " ".join(cmd))
    subprocess.run(cmd, check=True)


def crop_vertical(input_path: str, output_path: str, target_w: int = 1080, target_h: int = 1920):
    vf = (
        f"scale={target_w}:-2,"
        f"crop={target_w}:{target_h}"
    )
    run(["ffmpeg", "-y", "-i", input_path, "-vf", vf, "-c:a", "copy", output_path])


def add_subtitle(input_path: str, srt_path: str, output_path: str):
    vf = f"subtitles={srt_path}:force_style='FontSize=18,Alignment=2'"
    run(["ffmpeg", "-y", "-i", input_path, "-vf", vf, "-c:a", "copy", output_path])


def add_watermark(input_path: str, logo_path: str, output_path: str, position: str = "bottom-right"):
    positions = {
        "bottom-right": "W-w-20:H-h-20",
        "bottom-left": "20:H-h-20",
        "top-right": "W-w-20:20",
        "top-left": "20:20",
    }
    overlay = positions.get(position, positions["bottom-right"])
    run([
        "ffmpeg", "-y", "-i", input_path, "-i", logo_path,
        "-filter_complex", f"overlay={overlay}",
        output_path,
    ])


def trim(input_path: str, start: float, end: float, output_path: str):
    run([
        "ffmpeg", "-y", "-i", input_path,
        "-ss", str(start), "-to", str(end),
        "-c:v", "libx264", "-c:a", "aac",
        output_path,
    ])


def main():
    parser = argparse.ArgumentParser(description="ffmpeg 视频剪辑工具")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("crop-vertical", help="裁剪为 9:16 竖屏")
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--width", type=int, default=1080)
    p.add_argument("--height", type=int, default=1920)

    p = sub.add_parser("add-subtitle", help="烧录字幕")
    p.add_argument("--input", required=True)
    p.add_argument("--srt", required=True)
    p.add_argument("--output", required=True)

    p = sub.add_parser("add-watermark", help="添加水印")
    p.add_argument("--input", required=True)
    p.add_argument("--logo", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--position", default="bottom-right",
                   choices=["bottom-right", "bottom-left", "top-right", "top-left"])

    p = sub.add_parser("trim", help="掐头去尾")
    p.add_argument("--input", required=True)
    p.add_argument("--start", type=float, required=True)
    p.add_argument("--end", type=float, required=True)
    p.add_argument("--output", required=True)

    args = parser.parse_args()

    if args.command == "crop-vertical":
        crop_vertical(args.input, args.output, args.width, args.height)
    elif args.command == "add-subtitle":
        add_subtitle(args.input, args.srt, args.output)
    elif args.command == "add-watermark":
        add_watermark(args.input, args.logo, args.output, args.position)
    elif args.command == "trim":
        trim(args.input, args.start, args.end, args.output)


if __name__ == "__main__":
    main()
