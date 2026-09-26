"""发布文案生成器 — 生成印尼语 TikTok 标题+正文+话题标签。

用法:
    python copywriting_generator.py --product "Serum Vitamin C" --angle "before/after"
"""
import argparse

TITLE_TEMPLATES = {
    "before/after": "Baru {days} hari udah keliatan hasilnya! 😱 #{product_tag}",
    "pain_point": "Solusi buat kalian yang sering ngalamin masalah ini 👇",
    "myth_bust": "Ternyata cara pake {product} yang bener itu gini!",
}

BODY_TEMPLATE = """{title}

Beneran deh, {product} ini worth it banget buat dicoba.
Yang masih ragu, langsung aja check keranjang kuning ya! 🛒

{hashtags}
"""

BASE_HASHTAGS = ["#fyp", "#viral", "#tiktokshop", "#racuntiktok"]


def slugify_tag(product: str) -> str:
    return "".join(product.split()).lower()


def generate_hashtags(product: str, extra: list) -> str:
    tags = BASE_HASHTAGS + [f"#{slugify_tag(product)}"] + [f"#{t}" for t in extra]
    return " ".join(dict.fromkeys(tags))  # 去重保序


def generate(product: str, angle: str, extra_tags: list) -> str:
    template = TITLE_TEMPLATES.get(angle, TITLE_TEMPLATES["pain_point"])
    title = template.format(product=product, product_tag=slugify_tag(product), days=7)
    hashtags = generate_hashtags(product, extra_tags)
    return BODY_TEMPLATE.format(title=title, product=product, hashtags=hashtags)


def main():
    parser = argparse.ArgumentParser(description="生成印尼语 TikTok 发布文案")
    parser.add_argument("--product", required=True)
    parser.add_argument("--angle", default="pain_point", choices=list(TITLE_TEMPLATES.keys()))
    parser.add_argument("--tags", nargs="*", default=[], help="额外话题标签(不带 #)")
    args = parser.parse_args()

    print(generate(args.product, args.angle, args.tags))


if __name__ == "__main__":
    main()
