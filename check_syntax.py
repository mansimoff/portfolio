#!/usr/bin/env python3
"""
check_syntax.py — быстрая проверка СИНТАКСИСА (не стиля) перед сборкой/деплоем.
Тот же подход, что в resume-site. Детали и ограничения (почему tinycss2/tidy
не ловят незакрытые скобки/теги "как положено") — см. комментарии ниже.

Запуск:
    pip install -r requirements.txt
    python check_syntax.py            # yaml/py/css/jinja — до build.py
    python check_syntax.py --html     # + public/*.html — после build.py
"""

import argparse
import glob
import re
import subprocess
import sys
from pathlib import Path

import tinycss2
import yaml
from jinja2 import Environment, TemplateSyntaxError

errors: list[str] = []


def check_yaml() -> None:
    for f in sorted(glob.glob("data/*.yaml")):
        try:
            yaml.safe_load(Path(f).read_text(encoding="utf-8"))
        except yaml.YAMLError as e:
            errors.append(f"[YAML] {f}:\n{e}")


def check_python() -> None:
    for f in sorted(glob.glob("*.py")) + sorted(glob.glob("scripts/*.py")):
        result = subprocess.run([sys.executable, "-m", "py_compile", f], capture_output=True, text=True)
        if result.returncode != 0:
            errors.append(f"[PY] {f}:\n{result.stderr.strip()}")


def check_css() -> None:
    # CSS обязан по спецификации "долечивать" незакрытые блоки на EOF —
    # поэтому балансируем скобки вручную (вне строк/комментариев), а не
    # полагаемся только на spec-compliant парсер.
    for f in sorted(glob.glob("static/*.css")):
        content = Path(f).read_text(encoding="utf-8")
        stripped = re.sub(r"/\*.*?\*/", "", content, flags=re.S)
        stripped = re.sub(r'"(?:[^"\\]|\\.)*"', '""', stripped)
        stripped = re.sub(r"'(?:[^'\\]|\\.)*'", "''", stripped)

        depth = 0
        for ch in stripped:
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth < 0:
                    errors.append(f"[CSS] {f}: лишняя закрывающая '}}' (скобки не сбалансированы)")
                    break
        else:
            if depth != 0:
                errors.append(f"[CSS] {f}: не хватает {depth} закрывающей(их) '}}' — скобки не сбалансированы")

        rules = tinycss2.parse_stylesheet(content, skip_comments=True, skip_whitespace=True)
        for rule in rules:
            if rule.type == "error":
                errors.append(f"[CSS] {f} (offset {rule.source_line}:{rule.source_column}):\n{rule.message}")


def check_jinja_templates() -> None:
    env = Environment()
    for f in sorted(glob.glob("templates/*.j2")):
        source = Path(f).read_text(encoding="utf-8")
        try:
            env.parse(source)
        except TemplateSyntaxError as e:
            errors.append(f"[JINJA] {f}:{e.lineno}:\n{e.message}")


def check_rendered_html() -> None:
    files = sorted(glob.glob("public/**/*.html", recursive=True))
    if not files:
        errors.append("[HTML] public/ пуст — запусти build.py перед --html")
        return
    for f in files:
        result = subprocess.run(["tidy", "-q", "-errors", f], capture_output=True, text=True)
        # 0 — чисто, 1 — есть warnings (не блокируем — tidy шумит на loading="lazy",
        # svg stroke/fill и т.п., это легитимный HTML5/SVG, просто старая версия tidy
        # его не знает), 2+ — реальная поломка разметки.
        if result.returncode >= 2:
            errors.append(f"[HTML] {f}:\n{result.stderr.strip()}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--html", action="store_true")
    args = parser.parse_args()

    check_yaml()
    check_python()
    check_css()
    check_jinja_templates()
    if args.html:
        check_rendered_html()

    if errors:
        print("\n\n".join(errors), file=sys.stderr)
        print(f"\n--- {len(errors)} ошибка(ок) ---", file=sys.stderr)
        sys.exit(1)

    print("OK: синтаксис всех проверенных файлов корректен")


if __name__ == "__main__":
    main()
