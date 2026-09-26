"""成片检查器 — 用 ffprobe 核对成片是否符合脚本要求。

用法:
    python video_checker.py --video final.mp4 --expected-duration 25 --tolerance 3
"""
import argparse
import json
import subprocess
import sys


def ffprobe(video_path: str) -> dict:
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_format", "-show_streams", video_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe 失败: {result.stderr}")
    return json.loads(result.stdout)


def check(video_path: str, expected_duration: float, tolerance: float) -> list:
    info = ffprobe(video_path)
    issues = []

    duration = float(info["format"]["duration"])
    if abs(duration - expected_duration) > tolerance:
        issues.append(
            f"[时长] 实际 {duration:.1f}s,脚本要求 {expected_duration}s(±{tolerance}s),超出容差"
        )

    video_streams = [s for s in info["streams"] if s["codec_type"] == "video"]
    if not video_streams:
        issues.append("[视频流] 未检测到视频轨道")
    else:
        v = video_streams[0]
        w, h = int(v["width"]), int(v["height"])
        if h <= w:
            issues.append(f"[比例] 分辨率 {w}x{h} 不是竖屏,TikTok 要求 9:16 竖屏")
        else:
            ratio = w / h
            if abs(ratio - 9 / 16) > 0.05:
                issues.append(f"[比例] 分辨率 {w}x{h} 不接近标准 9:16")

    audio_streams = [s for s in info["streams"] if s["codec_type"] == "audio"]
    if not audio_streams:
        issues.append("[音频] 未检测到音轨,请确认是否需要口播/背景音乐")

    return issues


def main():
    parser = argparse.ArgumentParser(description="检查成片是否符合脚本要求")
    parser.add_argument("--video", required=True, help="成片文件路径")
    parser.add_argument("--expected-duration", type=float, required=True, help="脚本要求时长(秒)")
    parser.add_argument("--tolerance", type=float, default=3.0, help="时长容差(秒)")
    args = parser.parse_args()

    issues = check(args.video, args.expected_duration, args.tolerance)
    if not issues:
        print("✅ 成片符合脚本要求")
    else:
        print("❌ 发现以下问题:")
        for i in issues:
            print(f"  - {i}")
        sys.exit(1)


if __name__ == "__main__":
    main()
