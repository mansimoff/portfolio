#!/usr/bin/env python3
"""
build.py — собирает public/index.html из data/portfolio.yaml + templates/index.html.j2.
Копирует static/ (css/js/картинки) в public/ как есть.

Запуск:
    pip install -r requirements.txt
    python build.py
    python -m http.server -d public 8080
"""

import shutil
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markupsafe import Markup

ROOT = Path(__file__).parent
DATA_FILE = ROOT / "data" / "portfolio.yaml"
TEMPLATES_DIR = ROOT / "templates"
STATIC_DIR = ROOT / "static"
OUTPUT_DIR = ROOT / "public"

# Инлайн-SVG-иконки (24x24, stroke-based) — без внешних иконочных библиотек/CDN.
# Markup(...) помечает строку как "безопасный HTML", иначе Jinja2 (autoescape=True)
# экранирует "<svg>" в текст "&lt;svg&gt;" и иконка не отрисуется.
def _icon(path_d: str, *, viewbox: str = "0 0 24 24", extra: str = "") -> Markup:
    return Markup(
        f'<svg viewBox="{viewbox}" fill="none" stroke="currentColor" '
        f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{extra}{path_d}</svg>'
    )


ICONS = {
    "mail": _icon('<path d="M3 5h18v14H3z"/><path d="M3 6l9 7 9-7"/>'),
    "phone": _icon('<path d="M5 4h3l2 5-2.5 1.5a11 11 0 0 0 5 5L14 13l5 2v3a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>'),
    "location": _icon('<path d="M12 21s-7-6.5-7-11a7 7 0 0 1 14 0c0 4.5-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>'),
    "calendar": _icon('<rect x="3" y="5" width="18" height="16" rx="1.5"/><path d="M3 10h18M8 3v4M16 3v4"/>'),
    "github": _icon(
        '<path d="M12 2a10 10 0 0 0-3.16 19.49c.5.09.68-.22.68-.48v-1.7c-2.78.6-3.37-1.34-3.37-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.9 1.52 2.34 1.08 2.91.83.09-.65.35-1.08.63-1.33-2.22-.25-4.56-1.11-4.56-4.95 0-1.1.39-2 1.03-2.7-.1-.25-.45-1.27.1-2.64 0 0 .84-.27 2.75 1.02a9.5 9.5 0 0 1 5 0c1.91-1.3 2.75-1.02 2.75-1.02.55 1.37.2 2.39.1 2.64.64.7 1.03 1.6 1.03 2.7 0 3.85-2.35 4.7-4.58 4.94.36.31.68.92.68 1.85v2.75c0 .27.18.58.69.48A10 10 0 0 0 12 2z"/>'
    ),
    "telegram": _icon('<path d="M21 4L3 11l6 2m12-9l-4 17-8-6m12-11L9 13"/>'),
    "linkedin": _icon(
        '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7 10v7M7 7v.01M12 17v-4.5a2 2 0 0 1 4 0V17"/>'
    ),
    "file": _icon('<path d="M7 2h7l5 5v15H7z"/><path d="M14 2v5h5"/>'),
    "server": _icon('<rect x="3" y="4" width="18" height="6" rx="1"/><rect x="3" y="14" width="18" height="6" rx="1"/><path d="M7 7h.01M7 17h.01"/>'),
    "shield": _icon('<path d="M12 3l7 3v6c0 4.5-3 8-7 9-4-1-7-4.5-7-9V6z"/>'),
    "code": _icon('<path d="M9 8l-4 4 4 4M15 8l4 4-4 4"/>'),
    "brain": _icon('<path d="M9 4a3 3 0 0 0-3 3v1a3 3 0 0 0-1 5.5A3 3 0 0 0 8 18a3 3 0 0 0 1-.17V7a3 3 0 0 0 0-3zM15 4a3 3 0 0 1 3 3v1a3 3 0 0 1 1 5.5A3 3 0 0 1 16 18a3 3 0 0 1-1-.17V7a3 3 0 0 1 0-3z"/>'),
    "school": _icon('<path d="M12 3l10 5-10 5L2 8z"/><path d="M6 10.5V16c0 1.5 3 3 6 3s6-1.5 6-3v-5.5"/>'),
    "briefcase": _icon('<rect x="3" y="7" width="18" height="13" rx="1.5"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>'),
    "close": _icon('<path d="M6 6l12 12M18 6L6 18"/>'),
}


def load_data() -> dict:
    if not DATA_FILE.exists():
        sys.exit(f"Не найден {DATA_FILE}")
    return yaml.safe_load(DATA_FILE.read_text(encoding="utf-8"))


def render_html(data: dict) -> str:
    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=select_autoescape(["html"]),
    )
    template = env.get_template("index.html.j2")
    return template.render(icons=ICONS, **data)


def copy_static() -> None:
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)
    if STATIC_DIR.exists():
        shutil.copytree(STATIC_DIR, OUTPUT_DIR, dirs_exist_ok=True)


def main() -> None:
    data = load_data()
    copy_static()
    html = render_html(data)
    (OUTPUT_DIR / "index.html").write_text(html, encoding="utf-8")
    print(f"OK: собрано в {OUTPUT_DIR}/index.html")


if __name__ == "__main__":
    main()
