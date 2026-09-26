"""数据分析工具 — 汇总视频/达人数据(通常由 FastMoss MCP 查询结果导出为 JSON),生成复盘报告。

FastMoss 的达人/商品/视频数据通过 Claude 会话里的 FastMoss MCP 工具查询获取,
本脚本负责把查询结果(JSON)整理成结构化的中文复盘报告,不直接请求 FastMoss API。

用法:
    python data_analyzer.py --input videos.json --output report.md

输入 JSON 格式示例(每条视频一个对象):
    [
      {"title": "...", "views": 120000, "likes": 3200, "comments": 80,
       "shares": 45, "duration": 24, "post_date": "2026-09-01"}
    ]
"""
import argparse
import json


def load_videos(path: str) -> list:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def engagement_rate(v: dict) -> float:
    views = v.get("views", 0)
    if not views:
        return 0.0
    interactions = v.get("likes", 0) + v.get("comments", 0) + v.get("shares", 0)
    return interactions / views * 100


def build_report(videos: list) -> str:
    if not videos:
        return "无数据"

    ranked = sorted(videos, key=lambda v: v.get("views", 0), reverse=True)
    total_views = sum(v.get("views", 0) for v in videos)
    avg_engagement = sum(engagement_rate(v) for v in videos) / len(videos)

    lines = [
        "# 视频数据复盘报告",
        "",
        f"- 视频总数: {len(videos)}",
        f"- 总播放量: {total_views:,}",
        f"- 平均互动率: {avg_engagement:.2f}%",
        "",
        "## 播放量 Top 5",
        "",
        "| 标题 | 播放量 | 互动率 | 发布日期 |",
        "|---|---|---|---|",
    ]
    for v in ranked[:5]:
        lines.append(
            f"| {v.get('title', '-')} | {v.get('views', 0):,} | "
            f"{engagement_rate(v):.2f}% | {v.get('post_date', '-')} |"
        )

    lines += ["", "## 观察建议", ""]
    best = ranked[0]
    lines.append(f"- 表现最好的是《{best.get('title', '-')}》,可分析其钩子/选题角度并复用到后续脚本。")
    low_engagement = [v for v in videos if engagement_rate(v) < avg_engagement * 0.5]
    if low_engagement:
        lines.append(f"- 有 {len(low_engagement)} 条视频互动率明显低于均值,建议检查钩子与 CTA 设计。")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="生成视频数据复盘报告")
    parser.add_argument("--input", required=True, help="视频数据 JSON 文件路径")
    parser.add_argument("--output", help="报告输出路径(markdown),不填则打印到终端")
    args = parser.parse_args()

    videos = load_videos(args.input)
    report = build_report(videos)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"报告已生成: {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
