"""拍摄脚本生成器 — 按产品/选题生成印尼语 TikTok 短视频拍摄脚本。

用法:
    python shoot_script_generator.py --product "Serum Vitamin C" --angle "before/after" --duration 25
"""
import argparse
import textwrap
from dataclasses import dataclass, field


@dataclass
class Scene:
    timecode: str
    shot: str
    vo_id: str  # 口播文案(印尼语)


@dataclass
class ShootScript:
    product: str
    angle: str
    duration: int
    hook: str
    scenes: list = field(default_factory=list)
    cta: str = ""

    def render(self) -> str:
        lines = [
            f"=== 拍摄脚本: {self.product} ===",
            f"卖点角度: {self.angle}  |  目标时长: {self.duration}s",
            "",
            "【钩子 (0-3s)】",
            self.hook,
            "",
            "【分镜】",
        ]
        for s in self.scenes:
            lines.append(f"  [{s.timecode}] 镜头: {s.shot}")
            lines.append(f"         口播(ID): {s.vo_id}")
        lines += ["", "【CTA (结尾)】", self.cta]
        return "\n".join(lines)


HOOK_TEMPLATES = {
    "before/after": "Gila, cuma {days} hari udah keliatan bedanya!",
    "pain_point": "Kalian juga sering ngalamin masalah ini nggak sih?",
    "myth_bust": "Ternyata selama ini kita salah pake {product}!",
}

CTA_TEMPLATES = [
    "Klik keranjang kuning sekarang, stok terbatas!",
    "Follow buat tips lainnya, dan cek link di bio ya!",
    "Comment 'INFO' kalo mau tau harganya!",
]


def build_scenes(duration: int) -> list:
    n = 3 if duration <= 20 else 4
    step = duration // (n + 1)
    scenes = []
    starts = [step * i for i in range(1, n + 1)]
    templates = [
        ("Close-up produk di tangan", "Ini dia bahan rahasianya."),
        ("Demo pemakaian langsung", "Gampang banget, tinggal oles aja."),
        ("Reaksi wajah/testimoni", "Beneran kerasa hasilnya!"),
        ("Perbandingan sebelum-sesudah", "Liat sendiri bedanya di sini."),
    ]
    for i, start in enumerate(starts):
        end = start + step
        shot, vo = templates[i % len(templates)]
        scenes.append(Scene(timecode=f"{start:02d}-{end:02d}s", shot=shot, vo_id=vo))
    return scenes


def generate(product: str, angle: str, duration: int) -> ShootScript:
    hook_template = HOOK_TEMPLATES.get(angle, HOOK_TEMPLATES["pain_point"])
    hook = hook_template.format(product=product, days=7)
    scenes = build_scenes(duration)
    cta = CTA_TEMPLATES[0]
    return ShootScript(product=product, angle=angle, duration=duration, hook=hook, scenes=scenes, cta=cta)


def main():
    parser = argparse.ArgumentParser(description="生成印尼语 TikTok 拍摄脚本")
    parser.add_argument("--product", required=True, help="产品/选题名称")
    parser.add_argument("--angle", default="pain_point", choices=list(HOOK_TEMPLATES.keys()))
    parser.add_argument("--duration", type=int, default=25, help="目标视频时长(秒)")
    args = parser.parse_args()

    script = generate(args.product, args.angle, args.duration)
    print(script.render())


if __name__ == "__main__":
    main()
