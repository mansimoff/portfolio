# portfolio

Классическое портфолио: сайдбар с фото/контактами + 5 табов (About, Resume,
Portfolio, Certificates, Contact), переключаемых без перезагрузки страницы.
Архитектура — та же, что в твоём резюме: один YAML-файл → HTML через `build.py`.

Хостится как **project page**: `https://<username>.github.io/portfolio/`
(в отличие от резюме — оно user page, в корне домена). Поэтому все пути в
проекте относительные (`style.css`, не `/style.css`) — не трогай это при
правках, иначе сайт сломается именно в GitHub Pages (локально через
`python -m http.server` разницы не заметишь).

## Быстрый старт

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python build.py
python -m http.server -d public 8080   # http://localhost:8080
```

Settings → Pages → Source → **GitHub Actions** в репозитории `portfolio`.

## Структура

```
data/portfolio.yaml      — ВСЕ данные: контакты, опыт, скиллы, проекты, сертификаты
templates/index.html.j2  — HTML-шаблон (Jinja2)
static/
  style.css                — дизайн (ivory/бордовый, Fraunces+Work Sans)
  script.js                 — табы, фильтр портфолио, лайтбокс, мобильный сайдбар
  assets/
    photo.jpg                 — твоё фото
    favicon.svg
    projects/*.jpg             — обложки проектов
    certificates/*.jpg          — сканы/фото сертификатов
build.py                 — сборщик: yaml + шаблон → public/index.html
check_syntax.py          — синтаксис-чек (yaml/py/css/jinja/html), см. resume-site
scripts/make_placeholder.py — генератор картинки-заглушки с подписью
public/                  — СГЕНЕРИРОВАННЫЙ результат, не редактируется руками
```

## Как добавить/заменить фото

Любое изображение — просто файл по пути, указанному в `portfolio.yaml`.
Форматы: jpg/png, рекомендую jpg для фото (меньше вес).

- **Твоё фото** (сайдбар): `static/assets/photo.jpg`, квадратное, от 400×400px.
  Путь в yaml: `photo: "assets/photo.jpg"`.
- **Обложка проекта**: клади в `static/assets/projects/`, пропорция 4:3
  (например 800×600) — так не будет обрезаться криво. Путь в `projects[].image`.
- **Скан сертификата**: клади в `static/assets/certificates/`, квадратное
  или близкое к нему (например 500×500 или 600×450) — в сетке они квадратные.
  Путь в `certificate_groups[].entries[].image`.

Нет реального изображения, но нужно что-то, чтобы макет не выглядел дырявым:

```bash
python scripts/make_placeholder.py static/assets/certificates/it-2.jpg "Linux Essentials" 500 500
```

Впиши путь из вывода в `portfolio.yaml` — потом просто заменишь файл на
настоящий скан, путь менять не придётся.

## Как добавить сертификат

В `data/portfolio.yaml`, в нужную группу `certificate_groups`:

```yaml
  - group: "IT и профессиональные курсы"
    entries:
      - title: "Linux Essentials"
        issuer: "Cisco Networking Academy"
        year: "2024"
        image: "assets/certificates/linux-essentials.jpg"
```

Новая категория — просто новый блок `- group: "..."` с собственным `entries`.
Порядок групп на странице = порядок в списке.

## Как добавить проект в Portfolio

```yaml
projects:
  - title: "Название"
    category: "Automation"     # должна быть в project_categories, иначе не попадёт в фильтр
    image: "assets/projects/my-project.jpg"
    description: "Коротко, 1-2 предложения"
    url: "https://github.com/you/repo"   # можно пусто — тогда карточка не кликабельна
```

Новая категория фильтра — допиши её в `project_categories` в начале файла.

## Как добавить ещё один сервис/карточку в "What I'm doing"

```yaml
about:
  services:
    - icon: "code"   # доступны: server, shield, code, brain, school, briefcase, file
      title: "Название"
      description: "Описание в одно предложение"
```

Нужна иконка, которой нет в списке — добавь SVG в словарь `ICONS` в начале
`build.py` (скопируй по образцу существующих, `_icon("<path d='...'/>")`) и
используй её ключ в `icon:`.

## Дизайн-система

Все цвета/шрифты/отступы — в `:root` в начале `static/style.css`. Акцент —
бордовый (`--accent: #7a2e3a`), заголовки — Fraunces (serif), текст — Work Sans.
Тёмная тема переключается автоматически по `prefers-color-scheme` в браузере.

Сознательно НЕ переиспользует палитру резюме (там — тёмный терминал/янтарь) —
два сайта обращаются к разной части твоей идентичности, визуально должны
читаться как разные проекты, а не клоны друг друга.

## Проверка синтаксиса перед пушем

```bash
python check_syntax.py            # yaml/py/css/jinja
python build.py
python check_syntax.py --html     # + собранный HTML
```
CI (`lint` → `build` → `deploy`) делает то же самое автоматически при каждом push.

## Что можно / нельзя трогать руками

**Можно и нужно:** `data/portfolio.yaml`, картинки в `static/assets/`.
**Можно, но аккуратно:** `templates/index.html.j2`, `static/style.css`,
`static/script.js` — структура/дизайн/поведение.
**Нельзя:** `public/` — генерируется заново при каждой сборке, любые
правки там исчезнут.
