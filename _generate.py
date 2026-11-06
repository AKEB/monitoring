#!/usr/bin/env python3
"""One-shot static site generator for monitoring-website. Not needed at deploy time."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent


def asset_prefix(disk_rel: str) -> str:
    """Relative prefix from disk path to site root (css/, images/, …)."""
    depth = disk_rel.count("/")
    return "../" * depth if depth else "./"


def logical_of(disk_rel: str) -> str:
    """Path within a language tree (strip leading ru/)."""
    return disk_rel[3:] if disk_rel.startswith("ru/") else disk_rel


def lang_href(logical_rel: str, lang: str) -> str:
    """Href from current page to the same page in the other language."""
    depth = logical_rel.count("/")
    if lang == "en":
        return "../" * depth + "ru/" + logical_rel
    return "../" * (depth + 1) + logical_rel


NAV = {
    "en": [
        ("Features", "docs/features/index.html"),
        ("Docs", "docs/index.html"),
        ("Install", "docs/installation.html"),
        ("Quick Start", "docs/quick-start.html"),
        ("API", "docs/features/api.html"),
    ],
    "ru": [
        ("Возможности", "docs/features/index.html"),
        ("Документация", "docs/index.html"),
        ("Установка", "docs/installation.html"),
        ("Быстрый старт", "docs/quick-start.html"),
        ("API", "docs/features/api.html"),
    ],
}

SIDEBAR = {
    "en": [
        ("Guides", [
            ("Documentation", "docs/index.html"),
            ("Architecture", "docs/architecture.html"),
            ("Installation", "docs/installation.html"),
            ("Quick Start", "docs/quick-start.html"),
            ("Environment variables", "docs/environment.html"),
            ("Using the UI", "docs/usage.html"),
        ]),
        ("Features", [
            ("Overview", "docs/features/index.html"),
            ("Dashboard", "docs/features/dashboard.html"),
            ("Monitors", "docs/features/monitors.html"),
            ("Workers", "docs/features/workers.html"),
            ("Host Agents", "docs/features/agents.html"),
            ("Docker Hosts", "docs/features/docker.html"),
            ("Notifications", "docs/features/notifications.html"),
            ("Maintenance", "docs/features/maintenance.html"),
            ("RBAC & Audit", "docs/features/rbac.html"),
            ("Authentication", "docs/features/auth.html"),
            ("SSL & Events", "docs/features/ssl-events.html"),
            ("API & MCP", "docs/features/api.html"),
        ]),
    ],
    "ru": [
        ("Руководства", [
            ("Документация", "docs/index.html"),
            ("Архитектура", "docs/architecture.html"),
            ("Установка", "docs/installation.html"),
            ("Быстрый старт", "docs/quick-start.html"),
            ("Переменные окружения", "docs/environment.html"),
            ("Интерфейс", "docs/usage.html"),
        ]),
        ("Возможности", [
            ("Обзор", "docs/features/index.html"),
            ("Дашборд", "docs/features/dashboard.html"),
            ("Мониторы", "docs/features/monitors.html"),
            ("Воркеры", "docs/features/workers.html"),
            ("Агенты хостов", "docs/features/agents.html"),
            ("Docker-хосты", "docs/features/docker.html"),
            ("Уведомления", "docs/features/notifications.html"),
            ("Обслуживание", "docs/features/maintenance.html"),
            ("RBAC и аудит", "docs/features/rbac.html"),
            ("Аутентификация", "docs/features/auth.html"),
            ("SSL и события", "docs/features/ssl-events.html"),
            ("API и MCP", "docs/features/api.html"),
        ]),
    ],
}

FOOTER = {
    "en": {
        "copy": "© 2026 Monitoring Project. Dual licensing",
        "license": "AGPLv3 / Commercial",
        "links": [
            ("GitHub", "https://github.com/AKEB/monitoring"),
            ("Docker Hub", "https://hub.docker.com/repository/docker/akeb/monitoring/general"),
            ("Contact", "mailto:vadimakeb@gmail.com"),
            ("License", "LICENSE.md"),
        ],
    },
    "ru": {
        "copy": "© 2026 Monitoring Project. Двойная лицензия",
        "license": "AGPLv3 / Commercial",
        "links": [
            ("GitHub", "https://github.com/AKEB/monitoring"),
            ("Docker Hub", "https://hub.docker.com/repository/docker/akeb/monitoring/general"),
            ("Контакт", "mailto:vadimakeb@gmail.com"),
            ("Лицензия", "LICENSE.md"),
        ],
    },
}


def rel_to(from_rel: str, to_rel: str) -> str:
    from_parts = from_rel.split("/")[:-1]
    to_parts = to_rel.split("/")
    # go up
    up = "../" * len(from_parts)
    return up + "/".join(to_parts) if from_parts else to_rel


def header(lang: str, logical_rel: str, prefix: str) -> str:
    home = rel_to(logical_rel, "index.html")
    other_href = lang_href(logical_rel, lang)
    self_href = logical_rel.rsplit("/", 1)[-1]
    if lang == "en":
        en_href, ru_href = self_href, other_href
    else:
        en_href, ru_href = other_href, self_href

    nav_items = [f'<a href="{rel_to(logical_rel, href)}">{label}</a>' for label, href in NAV[lang]]
    nav = "\n          ".join(nav_items)
    en_cls = ' class="is-active"' if lang == "en" else ""
    ru_cls = ' class="is-active"' if lang == "ru" else ""
    return f"""  <header class="site-header">
    <div class="container">
      <a class="brand" href="{home}">
        <img src="{prefix}images/icon.png" alt="Monitoring" width="36" height="36">
        <span>Monitoring</span>
      </a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-label="Menu">Menu</button>
      <nav class="site-nav">
          {nav}
        <div class="lang-switch">
          <a href="{en_href}"{en_cls}>EN</a>
          <a href="{ru_href}"{ru_cls}>RU</a>
        </div>
      </nav>
    </div>
  </header>"""


def sidebar(lang: str, logical_rel: str) -> str:
    parts = ['      <aside class="docs-sidebar">']
    for section, items in SIDEBAR[lang]:
        parts.append(f"        <h4>{section}</h4>")
        for label, href in items:
            parts.append(f'        <a href="{rel_to(logical_rel, href)}">{label}</a>')
    parts.append("      </aside>")
    return "\n".join(parts)


def footer(lang: str, logical_rel: str) -> str:
    f = FOOTER[lang]
    links = []
    for label, href in f["links"]:
        if href.startswith("http") or href.startswith("mailto:"):
            links.append(f'<a href="{href}">{label}</a>')
        else:
            links.append(f'<a href="{rel_to(logical_rel, href)}">{label}</a>')
    return f"""  <footer class="site-footer">
    <div class="container">
      <p>{f['copy']} (<a href="{rel_to(logical_rel, 'LICENSE.md')}">{f['license']}</a>).</p>
      <div class="footer-links">
        {" | ".join(links)}
      </div>
    </div>
  </footer>"""


def page_shell(
    lang: str,
    disk_rel: str,
    title: str,
    body: str,
    *,
    docs: bool = False,
    description: str = "",
) -> str:
    logical_rel = logical_of(disk_rel)
    prefix = asset_prefix(disk_rel)
    desc = description or title
    head = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{desc}">
  <link rel="shortcut icon" href="{prefix}images/favicon.ico" type="image/x-icon">
  <link rel="stylesheet" href="{prefix}css/site.css">
  <title>{title}</title>
</head>
<body>
"""
    hdr = header(lang, logical_rel, prefix)
    ftr = footer(lang, logical_rel)
    if docs:
        main = f"""  <div class="container docs-layout">
{sidebar(lang, logical_rel)}
    <article class="docs-content">
{body}
    </article>
  </div>
"""
    else:
        main = body
    html = head + hdr + "\n" + main + ftr + f'\n  <script src="{prefix}js/site.js"></script>\n</body>\n</html>\n'
    return html.replace("{{PREFIX}}", prefix)


def write(rel: str, content: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print("wrote", rel)


# ---------- Content helpers ----------

COMPOSE = """---
services:
  mysql:
    container_name: monitoring-mysql
    image: mysql:latest
    restart: always
    environment:
      TZ: ${TZ:-UTC}
      MYSQL_ROOT_PASSWORD: ${MYSQL_PASSWORD:-RootPassword}
    volumes:
      - ./mysql_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysql", "-h", "127.0.0.1", "-u", "root", "--password=${MYSQL_PASSWORD:-RootPassword}", "-e", "show databases;"]
      start_period: 10s
      interval: 5s
      timeout: 5s
      retries: 55

  memcached:
    container_name: "monitoring-memcached"
    image: memcached
    restart: always
    environment:
      TZ: ${TZ:-UTC}
    command:
      - --conn-limit=1024
      - --memory-limit=32
      - --threads=4

  server:
    container_name: "monitoring-server"
    image: "akeb/monitoring:latest"
    restart: always
    environment:
      TZ: ${TZ:-UTC}
      NGINX_PORT: ${NGINX_PORT:-80}
      MYSQL_HOST: mysql
      MYSQL_PASSWORD: ${MYSQL_PASSWORD:-RootPassword}
      MEMCACHED_HOST: ${MEMCACHED_HOST:-memcached}
      PASSWORD_SALT: ${PASSWORD_SALT:-bHchLzC3B99Ss1213127fdw876EDghc2gkDdtg}
    volumes:
      - ./logs/php/:/var/log/php/:rw
      - ./logs/nginx/:/var/log/nginx/:rw
    ports:
      - "${NGINX_PORT:-80}:80"
    depends_on:
      mysql:
        condition: service_healthy
      memcached:
        condition: service_started
"""

ENV_FILE = """TZ=Europe/London
MYSQL_PASSWORD=YourSecureRootPassword123
NGINX_PORT=80
MEMCACHED_HOST=memcached
PASSWORD_SALT=YourRandomSaltStringHere123456789
"""

WORKER_RUN = """docker run -d \\
  --name monitoring-worker \\
  -e SERVER_HOST=https://your-monitoring-server.com \\
  -e WORKER_KEY_HASH=your_unique_worker_key_here \\
  akeb/monitoring-worker-go:latest
"""

AGENT_RUN = """docker run -d --name monitoring-agent --restart unless-stopped \\
  --net host \\
  -v /var/run/docker.sock:/var/run/docker.sock:ro \\
  -e SERVER_HOST=https://monitoring.example.com/ \\
  -e AGENT_KEY_HASH=... \\
  akeb/monitoring-agent:latest
"""


def pre(code: str) -> str:
    return f'<div class="pre-wrap"><pre><code>{escape(code.rstrip())}</code></pre></div>'


def escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def shot(name: str, caption: str) -> str:
    """Screenshot figure; {{PREFIX}} is replaced with asset_prefix(disk_rel) in page_shell."""
    return f"""<figure class="shot">
  <img src="{{{{PREFIX}}}}screenshots/{name}" alt="{escape(caption)}" loading="lazy">
  <figcaption>{caption}</figcaption>
</figure>"""


def mermaid(diagram: str) -> str:
    return f'<div class="mermaid">\n{diagram.strip()}\n</div>'


# ===================== LANDING =====================

def landing_en() -> str:
    return f"""
  <section class="hero">
    <div class="container">
      <h1>Monitoring</h1>
      <p class="lead">Distributed uptime and host monitoring with a Server, remote Workers, and host Agents. Check HTTP, TCP, Ping, Docker, exporters and server metrics from many regions — and alert without noise.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="docs/installation.html">Install in 5 minutes</a>
        <a class="btn btn-secondary" href="docs/index.html">Read the docs</a>
      </div>
    </div>
  </section>

  <section class="section" id="features">
    <div class="container">
      <h2>What you can do</h2>
      <p class="section-lead">Open any card for a full feature guide with setup steps and screenshots.</p>
      <div class="grid-3">
        <div class="card feature-card"><span class="tag">Core</span><a class="stretched" href="docs/features/monitors.html"><h3>Check types</h3><p>HTTPS, HTTP JSON, TCP, Ping, Docker, External callbacks, node-exporter and host-agent metrics.</p></a></div>
        <div class="card feature-card"><span class="tag">Scale</span><a class="stretched" href="docs/features/workers.html"><h3>Distributed workers</h3><p>Run lightweight Go workers in any network or region for objective availability.</p></a></div>
        <div class="card feature-card"><span class="tag">Hosts</span><a class="stretched" href="docs/features/agents.html"><h3>Host agents</h3><p>CPU, RAM, disks, network, Docker, Proxmox guests and auth events from each server.</p></a></div>
        <div class="card feature-card"><span class="tag">Alerts</span><a class="stretched" href="docs/features/notifications.html"><h3>Smart notifications</h3><p>Telegram, Mattermost, Gotify, MAX, webhooks — with mute, take, resolve actions.</p></a></div>
        <div class="card feature-card"><span class="tag">Access</span><a class="stretched" href="docs/features/rbac.html"><h3>Multi-tenant RBAC</h3><p>Users, groups, folder-inherited ACL, secrets permissions and audit log.</p></a></div>
        <div class="card feature-card"><span class="tag">Integrations</span><a class="stretched" href="docs/features/api.html"><h3>API &amp; MCP</h3><p>Status feed, Management API v2, Swagger UI and MCP tools for automation.</p></a></div>
      </div>
      <p style="margin-top:1.25rem"><a class="btn btn-outline" href="docs/features/index.html">All features →</a></p>
    </div>
  </section>

  <section class="section section-muted" id="architecture">
    <div class="container">
      <h2>Architecture</h2>
      <p class="section-lead">Three roles, one control plane. Details on the <a href="docs/architecture.html">architecture page</a>.</p>
      <div class="arch-components">
        <div class="card"><h3>Server</h3><code>akeb/monitoring</code><p>Web UI, MySQL, API, alerts, ACL.</p></div>
        <div class="card"><h3>Worker</h3><code>akeb/monitoring-worker-go</code><p>Runs checks from remote locations.</p></div>
        <div class="card"><h3>Agent</h3><code>akeb/monitoring-agent</code><p>Pushes host metrics every ~30s.</p></div>
      </div>
      {mermaid('''flowchart LR
  Workers -->|check results| Server
  Agents -->|host metrics| Server
  Server -->|jobs and config| Workers
  Server -->|desired version| Agents
  Server -->|alerts| Notify[Telegram Mattermost Gotify MAX Webhook]
  User[Operators] -->|Web UI / API / MCP| Server''')}
      <p style="text-align:center;margin-top:1.5rem"><img src="{{{{PREFIX}}}}images/architecture.png" alt="Architecture diagram" style="max-width:720px;margin:0 auto;display:block"></p>
    </div>
  </section>

  <section class="section" id="screenshots">
    <div class="container">
      <h2>Product screenshots</h2>
      <p class="section-lead">Live dashboard with uptime bars, response charts and events.</p>
      <div class="grid-2">
        {shot("screenshot_mainpage.png", "Dashboard — monitor tree and statuses")}
        {shot("screenshot_mainpage_monitor.png", "Selected monitor — charts and worker breakdown")}
      </div>
    </div>
  </section>

  <section class="section section-muted">
    <div class="container" style="text-align:center">
      <h2>Start monitoring</h2>
      <p class="section-lead" style="margin-inline:auto">Docker Compose for the server, one container per worker, optional host agents.</p>
      <div class="hero-actions" style="justify-content:center">
        <a class="btn btn-primary" href="docs/installation.html">Installation guide</a>
        <a class="btn btn-outline" href="docs/quick-start.html">Quick start</a>
      </div>
    </div>
  </section>
"""


def landing_ru() -> str:
    return f"""
  <section class="hero">
    <div class="container">
      <h1>Monitoring</h1>
      <p class="lead">Распределённый мониторинг доступности и хостов: сервер, удалённые воркеры и агенты. HTTP, TCP, Ping, Docker, exporter и метрики серверов из разных регионов — с умными алертами без спама.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="docs/installation.html">Установка за 5 минут</a>
        <a class="btn btn-secondary" href="docs/index.html">Документация</a>
      </div>
    </div>
  </section>

  <section class="section" id="features">
    <div class="container">
      <h2>Что умеет система</h2>
      <p class="section-lead">Откройте карточку — подробное описание с настройкой и скриншотами.</p>
      <div class="grid-3">
        <div class="card feature-card"><span class="tag">Ядро</span><a class="stretched" href="docs/features/monitors.html"><h3>Типы проверок</h3><p>HTTPS, HTTP JSON, TCP, Ping, Docker, External, node-exporter и метрики агента.</p></a></div>
        <div class="card feature-card"><span class="tag">Масштаб</span><a class="stretched" href="docs/features/workers.html"><h3>Распределённые воркеры</h3><p>Лёгкие Go-воркеры в любых сетях и регионах для объективной доступности.</p></a></div>
        <div class="card feature-card"><span class="tag">Хосты</span><a class="stretched" href="docs/features/agents.html"><h3>Агенты хостов</h3><p>CPU, RAM, диски, сеть, Docker, гости Proxmox и события auth с каждого сервера.</p></a></div>
        <div class="card feature-card"><span class="tag">Алерты</span><a class="stretched" href="docs/features/notifications.html"><h3>Умные уведомления</h3><p>Telegram, Mattermost, Gotify, MAX, webhook — с действиями mute / take / resolve.</p></a></div>
        <div class="card feature-card"><span class="tag">Доступ</span><a class="stretched" href="docs/features/rbac.html"><h3>RBAC и тенанты</h3><p>Пользователи, группы, ACL с наследованием от папок, секреты и журнал аудита.</p></a></div>
        <div class="card feature-card"><span class="tag">Интеграции</span><a class="stretched" href="docs/features/api.html"><h3>API и MCP</h3><p>Status API, Management API v2, Swagger и MCP-инструменты для автоматизации.</p></a></div>
      </div>
      <p style="margin-top:1.25rem"><a class="btn btn-outline" href="docs/features/index.html">Все возможности →</a></p>
    </div>
  </section>

  <section class="section section-muted" id="architecture">
    <div class="container">
      <h2>Архитектура</h2>
      <p class="section-lead">Три роли, одна панель управления. Подробнее на странице <a href="docs/architecture.html">архитектуры</a>.</p>
      <div class="arch-components">
        <div class="card"><h3>Сервер</h3><code>akeb/monitoring</code><p>Веб-UI, MySQL, API, алерты, ACL.</p></div>
        <div class="card"><h3>Воркер</h3><code>akeb/monitoring-worker-go</code><p>Выполняет проверки из удалённых точек.</p></div>
        <div class="card"><h3>Агент</h3><code>akeb/monitoring-agent</code><p>Отправляет метрики хоста каждые ~30 с.</p></div>
      </div>
      {mermaid('''flowchart LR
  Workers -->|результаты| Server
  Agents -->|метрики хоста| Server
  Server -->|задания| Workers
  Server -->|версия| Agents
  Server -->|алерты| Notify[Telegram Mattermost Gotify MAX Webhook]
  User[Операторы] -->|Web UI / API / MCP| Server''')}
      <p style="text-align:center;margin-top:1.5rem"><img src="{{{{PREFIX}}}}images/architecture.png" alt="Схема архитектуры" style="max-width:720px;margin:0 auto;display:block"></p>
    </div>
  </section>

  <section class="section" id="screenshots">
    <div class="container">
      <h2>Скриншоты</h2>
      <p class="section-lead">Живой дашборд с uptime, графиками и событиями.</p>
      <div class="grid-2">
        {shot("screenshot_mainpage.png", "Дашборд — дерево мониторов и статусы")}
        {shot("screenshot_mainpage_monitor.png", "Выбранный монитор — графики и воркеры")}
      </div>
    </div>
  </section>

  <section class="section section-muted">
    <div class="container" style="text-align:center">
      <h2>Начните мониторинг</h2>
      <p class="section-lead" style="margin-inline:auto">Docker Compose для сервера, по контейнеру на воркер, при необходимости — агенты.</p>
      <div class="hero-actions" style="justify-content:center">
        <a class="btn btn-primary" href="docs/installation.html">Установка</a>
        <a class="btn btn-outline" href="docs/quick-start.html">Быстрый старт</a>
      </div>
    </div>
  </section>
"""


# ===================== DOCS PAGES =====================

DOCS = {}  # page_key -> {en: body, ru: body, title_en, title_ru, desc_en, desc_ru, file}


def add_doc(key: str, file: str, title_en: str, title_ru: str, body_en: str, body_ru: str, desc_en: str = "", desc_ru: str = ""):
    DOCS[key] = {
        "file": file,
        "title_en": title_en,
        "title_ru": title_ru,
        "body_en": body_en,
        "body_ru": body_ru,
        "desc_en": desc_en or title_en,
        "desc_ru": desc_ru or title_ru,
    }


def nav_footer(prev: tuple | None, nxt: tuple | None, lang: str) -> str:
    """prev/nxt are (label, href relative to docs root like architecture.html)"""
    left = ""
    right = ""
    if prev:
        left = f'<a href="{prev[1]}">← {prev[0]}</a>'
    if nxt:
        right = f'<a href="{nxt[1]}">{nxt[0]} →</a>'
    return f'<div class="page-nav"><div>{left}</div><div>{right}</div></div>'


# --- docs index ---
add_doc(
    "docs_index",
    "docs/index.html",
    "Documentation",
    "Документация",
    """
      <h1>Documentation</h1>
      <p class="lead">Everything you need to deploy Monitoring, understand the architecture, and use every feature.</p>
      <div class="grid-2">
        <div class="card"><h3>Guides</h3>
          <ul>
            <li><a href="architecture.html">Architecture</a> — Server, Worker, Agent</li>
            <li><a href="installation.html">Installation</a> — Docker Compose server</li>
            <li><a href="quick-start.html">Quick Start</a> — first worker and monitor</li>
            <li><a href="environment.html">Environment variables</a> — Server, Worker, Agent</li>
            <li><a href="usage.html">Using the UI</a> — daily workflow</li>
          </ul>
        </div>
        <div class="card"><h3>Features</h3>
          <ul>
            <li><a href="features/index.html">Feature map</a></li>
            <li><a href="features/monitors.html">Monitors</a> · <a href="features/workers.html">Workers</a> · <a href="features/agents.html">Agents</a></li>
            <li><a href="features/notifications.html">Notifications</a> · <a href="features/rbac.html">RBAC</a></li>
            <li><a href="features/api.html">API &amp; MCP</a></li>
          </ul>
        </div>
      </div>
      <div class="callout" style="margin-top:1.5rem">
        <strong>Default admin</strong>
        After a fresh install: <code>admin@admin.com</code> / <code>Admin@123</code> — change immediately.
      </div>
    """,
    """
      <h1>Документация</h1>
      <p class="lead">Всё для развёртывания Monitoring, понимания архитектуры и работы с каждой возможностью.</p>
      <div class="grid-2">
        <div class="card"><h3>Руководства</h3>
          <ul>
            <li><a href="architecture.html">Архитектура</a> — сервер, воркер, агент</li>
            <li><a href="installation.html">Установка</a> — Docker Compose</li>
            <li><a href="quick-start.html">Быстрый старт</a> — первый воркер и монитор</li>
            <li><a href="environment.html">Переменные окружения</a> — сервер, воркер, агент</li>
            <li><a href="usage.html">Интерфейс</a> — повседневная работа</li>
          </ul>
        </div>
        <div class="card"><h3>Возможности</h3>
          <ul>
            <li><a href="features/index.html">Карта возможностей</a></li>
            <li><a href="features/monitors.html">Мониторы</a> · <a href="features/workers.html">Воркеры</a> · <a href="features/agents.html">Агенты</a></li>
            <li><a href="features/notifications.html">Уведомления</a> · <a href="features/rbac.html">RBAC</a></li>
            <li><a href="features/api.html">API и MCP</a></li>
          </ul>
        </div>
      </div>
      <div class="callout" style="margin-top:1.5rem">
        <strong>Админ по умолчанию</strong>
        После чистой установки: <code>admin@admin.com</code> / <code>Admin@123</code> — сразу смените пароль.
      </div>
    """,
)

add_doc(
    "architecture",
    "docs/architecture.html",
    "Architecture — Monitoring",
    "Архитектура — Monitoring",
    f"""
      <h1>Architecture</h1>
      <p class="lead">Monitoring is a control plane (Server) plus two kinds of edge processes: Workers that pull check jobs, and Agents that push host telemetry.</p>
      <h2>Components</h2>
      <div class="table-wrap"><table>
        <tr><th>Component</th><th>Image / binary</th><th>Role</th></tr>
        <tr><td>Server</td><td><code>akeb/monitoring</code></td><td>UI, MySQL, Memcached, scheduling, ACL, alerts, APIs</td></tr>
        <tr><td>Worker</td><td><code>akeb/monitoring-worker-go</code></td><td>Executes HTTP/TCP/Ping/Docker/exporter jobs; protocol 2.0+</td></tr>
        <tr><td>Agent</td><td><code>akeb/monitoring-agent</code></td><td>Reports CPU/RAM/disk/net/Docker/Proxmox/auth every ~30s</td></tr>
      </table></div>
      <h2>Data flow</h2>
      {mermaid('''sequenceDiagram
  participant UI as Web_UI
  participant S as Server
  participant W as Worker
  participant A as Agent
  participant N as Notify
  UI->>S: Configure monitors and ACL
  W->>S: get jobs protocol 2.0
  S-->>W: job list
  W->>W: Run checks
  W->>S: state results
  A->>S: report host metrics
  S->>S: Evaluate status events
  S->>N: Alert when thresholds fail
  UI->>S: Live dashboard via WebSocket''')}
      <h2>Storage</h2>
      <ul>
        <li><strong>MySQL</strong> — configuration, events, aggregated metrics</li>
        <li><strong>Memcached</strong> — short-lived caches (e.g. status API)</li>
        <li>Raw check logs are aggregated; old detail is pruned (about 24h)</li>
      </ul>
      <h2>Why workers and agents are separate</h2>
      <p>Workers answer “is the service reachable from this network?”. Agents answer “what is happening on this machine?”. You can run many workers worldwide and many agents on private hosts without opening inbound ports to the Server.</p>
      <div class="page-nav"><div><a href="index.html">← Documentation</a></div><div><a href="installation.html">Installation →</a></div></div>
    """,
    f"""
      <h1>Архитектура</h1>
      <p class="lead">Monitoring — это control plane (сервер) и два типа периферии: воркеры, которые забирают задания проверок, и агенты, которые пушат телеметрию хоста.</p>
      <h2>Компоненты</h2>
      <div class="table-wrap"><table>
        <tr><th>Компонент</th><th>Образ / бинарник</th><th>Роль</th></tr>
        <tr><td>Сервер</td><td><code>akeb/monitoring</code></td><td>UI, MySQL, Memcached, расписание, ACL, алерты, API</td></tr>
        <tr><td>Воркер</td><td><code>akeb/monitoring-worker-go</code></td><td>HTTP/TCP/Ping/Docker/exporter; протокол 2.0+</td></tr>
        <tr><td>Агент</td><td><code>akeb/monitoring-agent</code></td><td>CPU/RAM/диск/сеть/Docker/Proxmox/auth каждые ~30 с</td></tr>
      </table></div>
      <h2>Поток данных</h2>
      {mermaid('''sequenceDiagram
  participant UI as Web_UI
  participant S as Server
  participant W as Worker
  participant A as Agent
  participant N as Notify
  UI->>S: Мониторы и ACL
  W->>S: get jobs protocol 2.0
  S-->>W: список заданий
  W->>W: Проверки
  W->>S: state результаты
  A->>S: report метрики
  S->>S: События статусов
  S->>N: Алерты
  UI->>S: Дашборд WebSocket''')}
      <h2>Хранение</h2>
      <ul>
        <li><strong>MySQL</strong> — конфигурация, события, агрегаты</li>
        <li><strong>Memcached</strong> — короткоживущие кэши</li>
        <li>Сырые логи агрегируются; детали чистятся примерно за 24 часа</li>
      </ul>
      <h2>Зачем разделять воркеры и агенты</h2>
      <p>Воркеры отвечают: «доступен ли сервис из этой сети?». Агенты — «что происходит на машине?». Можно держать много воркеров по миру и агентов на закрытых хостах без входящих портов к серверу.</p>
      <div class="page-nav"><div><a href="index.html">← Документация</a></div><div><a href="installation.html">Установка →</a></div></div>
    """,
)

add_doc(
    "installation",
    "docs/installation.html",
    "Installation — Monitoring",
    "Установка — Monitoring",
    f"""
      <h1>Server installation</h1>
      <p class="lead">Deploy the Monitoring server with Docker Compose: MySQL, Memcached and the server image.</p>
      <h2>1. Project directory</h2>
      {pre("mkdir monitoring-server\\ncd monitoring-server")}
      <h2>2. Environment file</h2>
      <p>Create <code>.env</code> (change the password and salt):</p>
      {pre(ENV_FILE)}
      <div class="callout warn"><strong>Security</strong>Use a long random <code>PASSWORD_SALT</code> and a strong MySQL password. Never commit <code>.env</code>.</div>
      <h2>3. docker-compose.yml</h2>
      {pre(COMPOSE)}
      <h2>4. Start</h2>
      {pre("docker compose up -d")}
      <p>Open <code>http://your-server-ip</code> (or the host/port you mapped).</p>
      <h2>First login</h2>
      <ul>
        <li>Email: <code>admin@admin.com</code></li>
        <li>Password: <code>Admin@123</code></li>
      </ul>
      <p>Optional: configure SMTP, Telegram bot token, OpenID/OAuth via environment variables — see <a href="environment.html">Environment variables</a> and <a href="features/auth.html">Authentication</a>.</p>
      <div class="callout"><strong>Workers &amp; agents without Docker</strong>Download ready binaries from GitHub Releases (no Go build on the server) — see <a href="features/workers.html">Workers</a> and <a href="features/agents.html">Host agents</a>.</div>
      <div class="page-nav"><div><a href="architecture.html">← Architecture</a></div><div><a href="quick-start.html">Quick Start →</a></div></div>
    """,
    f"""
      <h1>Установка сервера</h1>
      <p class="lead">Развёртывание через Docker Compose: MySQL, Memcached и образ сервера.</p>
      <h2>1. Каталог проекта</h2>
      {pre("mkdir monitoring-server\\ncd monitoring-server")}
      <h2>2. Файл окружения</h2>
      <p>Создайте <code>.env</code> (смените пароль и соль):</p>
      {pre(ENV_FILE)}
      <div class="callout warn"><strong>Безопасность</strong>Длинная случайная <code>PASSWORD_SALT</code> и сильный пароль MySQL. Не коммитьте <code>.env</code>.</div>
      <h2>3. docker-compose.yml</h2>
      {pre(COMPOSE)}
      <h2>4. Запуск</h2>
      {pre("docker compose up -d")}
      <p>Откройте <code>http://your-server-ip</code> (или ваш порт).</p>
      <h2>Первый вход</h2>
      <ul>
        <li>E-mail: <code>admin@admin.com</code></li>
        <li>Пароль: <code>Admin@123</code></li>
      </ul>
      <p>Опционально: SMTP, Telegram, OpenID/OAuth — см. <a href="environment.html">переменные окружения</a> и <a href="features/auth.html">Аутентификацию</a>.</p>
      <div class="callout"><strong>Воркер и агент без Docker</strong>Готовые бинарники скачиваются с GitHub Releases (без сборки Go на сервере) — см. <a href="features/workers.html">Воркеры</a> и <a href="features/agents.html">Агенты</a>.</div>
      <div class="page-nav"><div><a href="architecture.html">← Архитектура</a></div><div><a href="quick-start.html">Быстрый старт →</a></div></div>
    """,
)

add_doc(
    "quickstart",
    "docs/quick-start.html",
    "Quick Start — Monitoring",
    "Быстрый старт — Monitoring",
    f"""
      <h1>Quick start</h1>
      <p class="lead">From a running server to the first green check in a few minutes.</p>
      <ol class="steps">
        <li><strong>Open the UI</strong> and sign in as admin.</li>
        <li><strong>Create a worker</strong> under Workers → Create. Copy <code>WORKER_KEY_HASH</code>.</li>
        <li><strong>Start the worker</strong> on any host that can reach your server:{pre(WORKER_RUN)}</li>
        <li><strong>Create a monitor</strong> — Monitors → Create → HTTPS, set URL, interval, assign the worker, save.</li>
        <li><strong>Add a notify channel</strong> (optional) — Telegram / Mattermost / Gotify / MAX / Webhook — and attach it to the monitor.</li>
      </ol>
      {shot("screenshot_workers.png", "Workers list")}
      {shot("screenshot_createMonitor_1.png", "Create monitor")}
      <p>Prefer a host binary instead of Docker? Download <code>monitoring-worker-linux-amd64</code> (or <code>arm64</code>) from <a href="https://github.com/AKEB/monitoring-worker-go/releases">GitHub Releases</a> — full systemd steps on <a href="features/workers.html">Workers</a>.</p>
      <p>First results usually appear within a minute. Next: <a href="usage.html">Using the UI</a> or <a href="features/agents.html">host agents</a>.</p>
      <div class="page-nav"><div><a href="installation.html">← Installation</a></div><div><a href="usage.html">Using the UI →</a></div></div>
    """,
    f"""
      <h1>Быстрый старт</h1>
      <p class="lead">От запущенного сервера до первой зелёной проверки за несколько минут.</p>
      <ol class="steps">
        <li><strong>Откройте UI</strong> и войдите как admin.</li>
        <li><strong>Создайте воркер</strong> Workers → Create. Скопируйте <code>WORKER_KEY_HASH</code>.</li>
        <li><strong>Запустите воркер</strong> на хосте с доступом к серверу:{pre(WORKER_RUN)}</li>
        <li><strong>Создайте монитор</strong> — Monitors → Create → HTTPS, URL, интервал, назначьте воркер.</li>
        <li><strong>Добавьте канал уведомлений</strong> (по желанию) и привяжите к монитору.</li>
      </ol>
      {shot("screenshot_workers.png", "Список воркеров")}
      {shot("screenshot_createMonitor_1.png", "Создание монитора")}
      <p>Нужен бинарник вместо Docker? Скачайте <code>monitoring-worker-linux-amd64</code> (или <code>arm64</code>) с <a href="https://github.com/AKEB/monitoring-worker-go/releases">GitHub Releases</a> — шаги systemd на странице <a href="features/workers.html">Воркеры</a>.</p>
      <p>Первые результаты обычно за минуту. Дальше: <a href="usage.html">интерфейс</a> или <a href="features/agents.html">агенты</a>.</p>
      <div class="page-nav"><div><a href="installation.html">← Установка</a></div><div><a href="usage.html">Интерфейс →</a></div></div>
    """,
)

add_doc(
    "usage",
    "docs/usage.html",
    "Using the UI — Monitoring",
    "Интерфейс — Monitoring",
    f"""
      <h1>Using the UI</h1>
      <p class="lead">Day-to-day operations on the dashboard and admin screens.</p>
      <h2>Dashboard</h2>
      <ul>
        <li>Folder tree of monitors you can read; collapse state is remembered</li>
        <li>Status badges and 24h availability %</li>
        <li>Filter by Success / Error / Warning / Unknown / Maintenance; search by title</li>
        <li>WebSocket background refresh for the list and the selected monitor</li>
        <li>On mobile: bottom nav toggles List vs Data panes</li>
      </ul>
      {shot("screenshot_mainpage.png", "Main dashboard")}
      <h2>Monitor detail</h2>
      <ul>
        <li>Uptime bar (24h segments)</li>
        <li>Response-time or metric charts (30m–24h), per worker when applicable</li>
        <li>Events table (status transitions)</li>
        <li>Theme follows system light/dark</li>
      </ul>
      {shot("screenshot_mainpage_monitor.png", "Monitor detail with charts")}
      <h2>Admin areas</h2>
      <p>Permission-gated menus: Workers, Monitors, Notify, Signatures, Dockers, Servers, Maintenances, Users/Groups/Permissions/Logs, API tokens under Settings.</p>
      <div class="page-nav"><div><a href="quick-start.html">← Quick Start</a></div><div><a href="environment.html">Environment →</a></div></div>
    """,
    f"""
      <h1>Интерфейс</h1>
      <p class="lead">Повседневная работа с дашбордом и админкой.</p>
      <h2>Дашборд</h2>
      <ul>
        <li>Дерево папок и мониторов с правами на чтение; сворачивание запоминается</li>
        <li>Бейджи статуса и availability за 24 часа</li>
        <li>Фильтр Success / Error / Warning / Unknown / Maintenance; поиск по имени</li>
        <li>Фоновое обновление по WebSocket</li>
        <li>На мобильном: переключение List / Data</li>
      </ul>
      {shot("screenshot_mainpage.png", "Главный дашборд")}
      <h2>Карточка монитора</h2>
      <ul>
        <li>Uptime-полоса за 24 часа</li>
        <li>Графики времени ответа или метрик (30м–24ч)</li>
        <li>Таблица событий</li>
        <li>Тема следует системной light/dark</li>
      </ul>
      {shot("screenshot_mainpage_monitor.png", "Детали монитора")}
      <h2>Админка</h2>
      <p>По правам: Workers, Monitors, Notify, Signatures, Dockers, Servers, Maintenances, пользователи/группы/права/логи, API-токены в Settings.</p>
      <div class="page-nav"><div><a href="quick-start.html">← Быстрый старт</a></div><div><a href="environment.html">Окружение →</a></div></div>
    """,
)

WORKER_DOWNLOAD_INSTALL = """# Pick the latest tag on https://github.com/AKEB/monitoring-worker-go/releases
# Use linux-arm64 on Raspberry Pi / ARM hosts.
VER=v2.3.0
ARCH=amd64   # or arm64

sudo mkdir -p /opt/monitoring-worker
sudo curl -fsSL -o /opt/monitoring-worker/monitoring-worker \\
  "https://github.com/AKEB/monitoring-worker-go/releases/download/${VER}/monitoring-worker-linux-${ARCH}"
sudo chmod 755 /opt/monitoring-worker/monitoring-worker

# Optional checksum check:
# curl -fsSL -o /tmp/monitoring-worker.sha256 \\
#   "https://github.com/AKEB/monitoring-worker-go/releases/download/${VER}/monitoring-worker-linux-${ARCH}.sha256"
# echo "$(cat /tmp/monitoring-worker.sha256)  /opt/monitoring-worker/monitoring-worker" | sha256sum -c -

sudo tee /opt/monitoring-worker/.env >/dev/null <<'EOF'
TZ=Europe/Moscow
SERVER_HOST=https://monitoring.example.com/
WORKER_KEY_HASH=paste_worker_key_here
PROTOCOL_VERSION=2.0
AUTO_UPDATE=true
EOF

sudo tee /etc/systemd/system/monitoring-worker.service >/dev/null <<'EOF'
[Unit]
Description=Monitoring worker
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=/opt/monitoring-worker
ExecStart=/opt/monitoring-worker/monitoring-worker
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now monitoring-worker
journalctl -u monitoring-worker -f
"""

WORKER_BUILD = """# Only if you need a custom build — prefer GitHub Releases on servers.
go build -buildvcs=false -o monitoring-worker ./cmd/worker/
GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go build -buildvcs=false -o monitoring-worker-linux-amd64 ./cmd/worker/
GOOS=linux GOARCH=arm64 CGO_ENABLED=0 go build -buildvcs=false -o monitoring-worker-linux-arm64 ./cmd/worker/
"""

AGENT_DOWNLOAD_INSTALL = """# Pick the latest tag on https://github.com/AKEB/monitoring-agent/releases
VER=v1.2.0
ARCH=amd64   # or arm64

sudo mkdir -p /opt/monitoring-agent
sudo curl -fsSL -o /opt/monitoring-agent/monitoring-agent \\
  "https://github.com/AKEB/monitoring-agent/releases/download/${VER}/monitoring-agent-linux-${ARCH}"
sudo chmod 755 /opt/monitoring-agent/monitoring-agent

# Optional checksum check:
# curl -fsSL -o /tmp/monitoring-agent.sha256 \\
#   "https://github.com/AKEB/monitoring-agent/releases/download/${VER}/monitoring-agent-linux-${ARCH}.sha256"
# echo "$(cat /tmp/monitoring-agent.sha256)  /opt/monitoring-agent/monitoring-agent" | sha256sum -c -

sudo tee /opt/monitoring-agent/.env >/dev/null <<'EOF'
TZ=Europe/Moscow
SERVER_HOST=https://monitoring.example.com/
AGENT_KEY_HASH=paste_agent_key_here
REPORT_INTERVAL_SEC=30
AUTO_UPDATE=true
EOF

sudo tee /etc/systemd/system/monitoring-agent.service >/dev/null <<'EOF'
[Unit]
Description=Monitoring host agent
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/monitoring-agent
ExecStart=/opt/monitoring-agent/monitoring-agent
Restart=always
RestartSec=5
EnvironmentFile=-/opt/monitoring-agent/.env

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now monitoring-agent
journalctl -u monitoring-agent -f
"""

AGENT_BUILD = """# Only if you need a custom build — prefer GitHub Releases on servers.
go build -buildvcs=false -o monitoring-agent ./cmd/agent/
GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go build -buildvcs=false -o monitoring-agent-linux-amd64 ./cmd/agent/
GOOS=linux GOARCH=arm64 CGO_ENABLED=0 go build -buildvcs=false -o monitoring-agent-linux-arm64 ./cmd/agent/
"""

add_doc(
    "environment",
    "docs/environment.html",
    "Environment variables — Monitoring",
    "Переменные окружения — Monitoring",
    f"""
      <h1>Environment variables</h1>
      <p class="lead">Complete reference for the Server container, Go Worker and Host Agent. Defaults match the current code / <code>.env.example</code> files.</p>
      <div class="callout"><strong>Where to set them</strong>Server: Compose <code>environment</code> / <code>.env</code>. Worker and Agent: process env or a <code>.env</code> file next to the binary (or in the working directory). See also <a href="features/workers.html">Workers</a> and <a href="features/agents.html">Agents</a> for binary installs.</div>

      <h2 id="server">Server (<code>akeb/monitoring</code>)</h2>
      <h3>Core</h3>
      <div class="table-wrap"><table>
        <tr><th>Variable</th><th>Default</th><th>Description</th></tr>
        <tr><td><code>TZ</code></td><td><code>UTC</code></td><td>Timezone</td></tr>
        <tr><td><code>PASSWORD_SALT</code></td><td>—</td><td>Required salt for password hashing — use a long random string</td></tr>
        <tr><td><code>NGINX_PORT</code></td><td><code>80</code></td><td>Published HTTP port in Compose samples</td></tr>
        <tr><td><code>APP_DEBUG</code></td><td><code>false</code></td><td>Application debug mode</td></tr>
        <tr><td><code>APP_SIGNIN_ACTIVE</code></td><td><code>true</code></td><td>Allow email/password sign-in</td></tr>
        <tr><td><code>APP_SIGNUP_ACTIVE</code></td><td><code>true</code></td><td>Allow self-registration</td></tr>
        <tr><td><code>APP_BASE_URL</code></td><td>empty</td><td>Public absolute URL (scheme+host) for redirects/emails; empty = detect from request</td></tr>
        <tr><td><code>TRUST_PROXY</code></td><td><code>false</code></td><td>Trust <code>X-Real-IP</code> / <code>X-Forwarded-*</code> only behind a known reverse proxy</td></tr>
        <tr><td><code>DESIRED_AGENT_VERSION</code></td><td>empty</td><td>Fallback target agent version (GitHub tag) if not set in Admin → Servers</td></tr>
        <tr><td><code>DESIRED_WORKER_VERSION</code></td><td>empty</td><td>Fallback target worker version if not set in Admin → Workers</td></tr>
      </table></div>
      <h3>MySQL</h3>
      <div class="table-wrap"><table>
        <tr><th>Variable</th><th>Default</th><th>Description</th></tr>
        <tr><td><code>MYSQL_HOST</code></td><td><code>localhost</code></td><td>MySQL host</td></tr>
        <tr><td><code>MYSQL_PORT</code></td><td><code>3306</code></td><td>MySQL port</td></tr>
        <tr><td><code>MYSQL_USERNAME</code></td><td><code>root</code></td><td>MySQL user</td></tr>
        <tr><td><code>MYSQL_PASSWORD</code></td><td>—</td><td>MySQL password</td></tr>
        <tr><td><code>MYSQL_DB_NAME</code></td><td><code>monitoring</code></td><td>Database name</td></tr>
        <tr><td><code>MYSQL_DEBUG</code></td><td><code>false</code></td><td>SQL debug logs</td></tr>
        <tr><td><code>MYSQL_DONT_USE_SLAVE</code></td><td><code>true</code></td><td>Disable read replica</td></tr>
        <tr><td><code>MYSQL_SLAVE_HOST</code></td><td><code>MYSQL_HOST</code></td><td>Replica host</td></tr>
        <tr><td><code>MYSQL_SLAVE_PORT</code></td><td><code>MYSQL_PORT</code></td><td>Replica port</td></tr>
        <tr><td><code>MYSQL_SLAVE_USERNAME</code></td><td><code>MYSQL_USERNAME</code></td><td>Replica user</td></tr>
        <tr><td><code>MYSQL_SLAVE_PASSWORD</code></td><td><code>MYSQL_PASSWORD</code></td><td>Replica password</td></tr>
        <tr><td><code>MYSQL_SLAVE_DB_NAME</code></td><td><code>MYSQL_DB_NAME</code></td><td>Replica database</td></tr>
      </table></div>
      <h3>Memcached</h3>
      <div class="table-wrap"><table>
        <tr><th>Variable</th><th>Default</th><th>Description</th></tr>
        <tr><td><code>MEMCACHED_HOST</code></td><td>empty</td><td>Memcached host (required in Compose: <code>memcached</code>)</td></tr>
        <tr><td><code>MEMCACHED_PORT</code></td><td><code>11211</code></td><td>Memcached port</td></tr>
      </table></div>
      <h3>SMTP</h3>
      <div class="table-wrap"><table>
        <tr><th>Variable</th><th>Default</th><th>Description</th></tr>
        <tr><td><code>SMTP_HOST</code></td><td>empty</td><td>SMTP host (password reset, mail)</td></tr>
        <tr><td><code>SMTP_PORT</code></td><td><code>25</code></td><td>SMTP port</td></tr>
        <tr><td><code>SMTP_USERNAME</code></td><td>empty</td><td>SMTP user</td></tr>
        <tr><td><code>SMTP_PASSWORD</code></td><td>empty</td><td>SMTP password</td></tr>
        <tr><td><code>SMTP_TLS</code></td><td><code>false</code></td><td>STARTTLS</td></tr>
        <tr><td><code>SMTP_SSL</code></td><td><code>false</code></td><td>Implicit SSL</td></tr>
      </table></div>
      <h3>OpenID Connect</h3>
      <div class="table-wrap"><table>
        <tr><th>Variable</th><th>Default</th><th>Description</th></tr>
        <tr><td><code>OPENIDCONNECT_PROVIDER</code></td><td>empty</td><td>OIDC provider URL</td></tr>
        <tr><td><code>OPENIDCONNECT_CLIENT_ID</code></td><td>empty</td><td>Client id</td></tr>
        <tr><td><code>OPENIDCONNECT_CLIENT_SECRET</code></td><td>empty</td><td>Client secret</td></tr>
        <tr><td><code>OPENIDCONNECT_BUTTON</code></td><td>empty</td><td>Login button label</td></tr>
        <tr><td><code>OPENIDCONNECT_SCOPE</code></td><td><code>email profile openid</code></td><td>Scopes</td></tr>
        <tr><td><code>OPENIDCONNECT_REGISTER</code></td><td><code>true</code></td><td>Allow auto-register on first login</td></tr>
      </table></div>
      <h3>OAuth</h3>
      <div class="table-wrap"><table>
        <tr><th>Variable</th><th>Default</th><th>Description</th></tr>
        <tr><td><code>OAUTH_CLIENT_ID</code></td><td>empty</td><td>OAuth client id</td></tr>
        <tr><td><code>OAUTH_CLIENT_SECRET</code></td><td>empty</td><td>Client secret</td></tr>
        <tr><td><code>OAUTH_AUTHORIZATION_ENDPOINT</code></td><td>empty</td><td>Authorize URL</td></tr>
        <tr><td><code>OAUTH_TOKEN_ENDPOINT</code></td><td>empty</td><td>Token URL</td></tr>
        <tr><td><code>OAUTH_USERINFO_ENDPOINT</code></td><td>empty</td><td>Userinfo URL</td></tr>
        <tr><td><code>OAUTH_BUTTON</code></td><td>empty</td><td>Login button label</td></tr>
        <tr><td><code>OAUTH_SCOPE</code></td><td><code>self_profile</code></td><td>Scopes</td></tr>
        <tr><td><code>OAUTH_REGISTER</code></td><td><code>true</code></td><td>Allow auto-register</td></tr>
      </table></div>
      <h3>Telegram (server-side bot / proxy)</h3>
      <div class="table-wrap"><table>
        <tr><th>Variable</th><th>Default</th><th>Description</th></tr>
        <tr><td><code>TELEGRAM_BOT_TOKEN</code></td><td>empty</td><td>Optional global bot token (channels can also store their own)</td></tr>
        <tr><td><code>TELEGRAM_PROXY_SOCKS5</code></td><td><code>true</code></td><td>Use SOCKS5 for Telegram proxy</td></tr>
        <tr><td><code>TELEGRAM_PROXY_HOST</code></td><td>empty</td><td>Proxy host</td></tr>
        <tr><td><code>TELEGRAM_PROXY_PORT</code></td><td><code>8080</code></td><td>Proxy port</td></tr>
        <tr><td><code>TELEGRAM_PROXY_USERNAME</code></td><td>empty</td><td>Proxy user</td></tr>
        <tr><td><code>TELEGRAM_PROXY_PASSWORD</code></td><td>empty</td><td>Proxy password</td></tr>
      </table></div>

      <h2 id="worker">Worker (<code>monitoring-worker-go</code>)</h2>
      <div class="table-wrap"><table>
        <tr><th>Variable</th><th>Default</th><th>Description</th></tr>
        <tr><td><code>SERVER_HOST</code></td><td>—</td><td><strong>Required.</strong> Monitoring base URL (trailing slash added if missing)</td></tr>
        <tr><td><code>WORKER_KEY_HASH</code></td><td>—</td><td><strong>Required.</strong> Key from Admin → Workers</td></tr>
        <tr><td><code>TZ</code></td><td><code>UTC</code></td><td>Timezone</td></tr>
        <tr><td><code>PROTOCOL_VERSION</code></td><td><code>2.0</code></td><td>Must be 2.0+ (server ≥ v2.1)</td></tr>
        <tr><td><code>WORKER_THREADS</code></td><td><code>10</code></td><td>Concurrent check threads</td></tr>
        <tr><td><code>JOBS_GET_TIMEOUT</code></td><td><code>30</code></td><td>Seconds between job polls</td></tr>
        <tr><td><code>LOOP_TIMEOUT</code></td><td><code>200000</code></td><td>Main loop delay (microseconds)</td></tr>
        <tr><td><code>RESPONSE_SEND_TIMEOUT</code></td><td><code>5</code></td><td>Seconds between result POSTs</td></tr>
        <tr><td><code>LOGS_WRITE_TIMEOUT</code></td><td><code>10</code></td><td>Seconds between log flushes</td></tr>
        <tr><td><code>PROXY_HOST</code></td><td>empty</td><td>Optional outbound proxy for checks</td></tr>
        <tr><td><code>PROXY_TYPE</code></td><td>empty</td><td>Proxy type (HTTP / SOCKS5 as in cURL)</td></tr>
        <tr><td><code>WORKER_VERSION</code></td><td>ldflags / <code>local</code></td><td>Reported version (env overrides build ldflags)</td></tr>
        <tr><td><code>DEBUG</code></td><td><code>false</code></td><td>Verbose worker logs</td></tr>
        <tr><td><code>CURL_DEBUG</code></td><td><code>false</code></td><td>HTTP check request logging</td></tr>
        <tr><td><code>DOCKER_DEBUG</code></td><td><code>false</code></td><td>Docker Engine API debug lines</td></tr>
        <tr><td><code>IMMEDIATE_ERROR_RETRY</code></td><td><code>true</code></td><td><code>true</code> = retry failed job on next loop tick (PHP-compatible); <code>false</code> = wait <code>repeat_seconds</code></td></tr>
        <tr><td><code>AUTO_UPDATE</code></td><td><code>true</code></td><td>Apply <code>data.update</code> from server (binary replace)</td></tr>
        <tr><td><code>UPDATE_FROM_GITHUB</code></td><td><code>true</code></td><td>Allow only <code>github.com/AKEB/monitoring-worker-go</code> release URLs</td></tr>
      </table></div>
      <p>In Docker prefer image tags and set <code>AUTO_UPDATE=false</code>.</p>

      <h2 id="agent">Agent (<code>monitoring-agent</code>)</h2>
      <div class="table-wrap"><table>
        <tr><th>Variable</th><th>Default</th><th>Description</th></tr>
        <tr><td><code>SERVER_HOST</code></td><td>—</td><td><strong>Required.</strong> Monitoring base URL</td></tr>
        <tr><td><code>AGENT_KEY_HASH</code></td><td>—</td><td><strong>Required.</strong> Key from Admin → Servers</td></tr>
        <tr><td><code>TZ</code></td><td><code>UTC</code></td><td>Timezone</td></tr>
        <tr><td><code>REPORT_INTERVAL_SEC</code></td><td><code>30</code></td><td>Push interval (clamped 15–600)</td></tr>
        <tr><td><code>AGENT_VERSION</code></td><td>ldflags / <code>local</code></td><td>Reported version</td></tr>
        <tr><td><code>DEBUG</code></td><td><code>false</code></td><td>Verbose stderr</td></tr>
        <tr><td><code>COLLECT_DOCKER</code></td><td><code>true</code></td><td>Docker container inventory</td></tr>
        <tr><td><code>COLLECT_PROXMOX</code></td><td><code>true</code></td><td>Proxmox VE QEMU/LXC inventory</td></tr>
        <tr><td><code>COLLECT_AUTH</code></td><td><code>true</code></td><td>Auth log delta (SSH/sudo)</td></tr>
        <tr><td><code>COLLECT_PROCESSES</code></td><td><code>true</code></td><td>Process snapshot</td></tr>
        <tr><td><code>PROCESS_TOP_N</code></td><td><code>20</code></td><td>Top processes by CPU (5–100)</td></tr>
        <tr><td><code>AUTO_UPDATE</code></td><td><code>true</code></td><td>Honor update payload from report API</td></tr>
        <tr><td><code>UPDATE_FROM_GITHUB</code></td><td><code>true</code></td><td>Allow only <code>github.com/AKEB/monitoring-agent</code> release URLs</td></tr>
      </table></div>

      <div class="page-nav"><div><a href="usage.html">← Using the UI</a></div><div><a href="features/index.html">Features →</a></div></div>
    """,
    f"""
      <h1>Переменные окружения</h1>
      <p class="lead">Полный справочник для сервера, Go-воркера и агента. Значения по умолчанию — из кода и <code>.env.example</code>.</p>
      <div class="callout"><strong>Где задавать</strong>Сервер: Compose <code>environment</code> / <code>.env</code>. Воркер и агент: env процесса или файл <code>.env</code> рядом с бинарником. См. также <a href="features/workers.html">Воркеры</a> и <a href="features/agents.html">Агенты</a>.</div>

      <h2 id="server">Сервер (<code>akeb/monitoring</code>)</h2>
      <h3>Ядро</h3>
      <div class="table-wrap"><table>
        <tr><th>Переменная</th><th>По умолчанию</th><th>Описание</th></tr>
        <tr><td><code>TZ</code></td><td><code>UTC</code></td><td>Часовой пояс</td></tr>
        <tr><td><code>PASSWORD_SALT</code></td><td>—</td><td>Соль для хешей паролей — длинная случайная строка</td></tr>
        <tr><td><code>NGINX_PORT</code></td><td><code>80</code></td><td>Порт HTTP в примерах Compose</td></tr>
        <tr><td><code>APP_DEBUG</code></td><td><code>false</code></td><td>Режим отладки</td></tr>
        <tr><td><code>APP_SIGNIN_ACTIVE</code></td><td><code>true</code></td><td>Вход по e-mail/паролю</td></tr>
        <tr><td><code>APP_SIGNUP_ACTIVE</code></td><td><code>true</code></td><td>Самостоятельная регистрация</td></tr>
        <tr><td><code>APP_BASE_URL</code></td><td>пусто</td><td>Публичный URL (scheme+host) для редиректов/писем</td></tr>
        <tr><td><code>TRUST_PROXY</code></td><td><code>false</code></td><td>Доверять <code>X-Forwarded-*</code> только за известным proxy</td></tr>
        <tr><td><code>DESIRED_AGENT_VERSION</code></td><td>пусто</td><td>Целевая версия агента, если не задана в UI</td></tr>
        <tr><td><code>DESIRED_WORKER_VERSION</code></td><td>пусто</td><td>Целевая версия воркера, если не задана в UI</td></tr>
      </table></div>
      <h3>MySQL</h3>
      <div class="table-wrap"><table>
        <tr><th>Переменная</th><th>По умолчанию</th><th>Описание</th></tr>
        <tr><td><code>MYSQL_HOST</code></td><td><code>localhost</code></td><td>Хост MySQL</td></tr>
        <tr><td><code>MYSQL_PORT</code></td><td><code>3306</code></td><td>Порт</td></tr>
        <tr><td><code>MYSQL_USERNAME</code></td><td><code>root</code></td><td>Пользователь</td></tr>
        <tr><td><code>MYSQL_PASSWORD</code></td><td>—</td><td>Пароль</td></tr>
        <tr><td><code>MYSQL_DB_NAME</code></td><td><code>monitoring</code></td><td>Имя БД</td></tr>
        <tr><td><code>MYSQL_DEBUG</code></td><td><code>false</code></td><td>Отладка SQL</td></tr>
        <tr><td><code>MYSQL_DONT_USE_SLAVE</code></td><td><code>true</code></td><td>Не использовать реплику</td></tr>
        <tr><td><code>MYSQL_SLAVE_*</code></td><td>как master</td><td>Параметры read-replica (HOST/PORT/USERNAME/PASSWORD/DB_NAME)</td></tr>
      </table></div>
      <h3>Memcached</h3>
      <div class="table-wrap"><table>
        <tr><th>Переменная</th><th>По умолчанию</th><th>Описание</th></tr>
        <tr><td><code>MEMCACHED_HOST</code></td><td>пусто</td><td>Хост Memcached</td></tr>
        <tr><td><code>MEMCACHED_PORT</code></td><td><code>11211</code></td><td>Порт</td></tr>
      </table></div>
      <h3>SMTP</h3>
      <div class="table-wrap"><table>
        <tr><th>Переменная</th><th>По умолчанию</th><th>Описание</th></tr>
        <tr><td><code>SMTP_HOST</code></td><td>пусто</td><td>SMTP-хост</td></tr>
        <tr><td><code>SMTP_PORT</code></td><td><code>25</code></td><td>Порт</td></tr>
        <tr><td><code>SMTP_USERNAME</code> / <code>SMTP_PASSWORD</code></td><td>пусто</td><td>Учётные данные</td></tr>
        <tr><td><code>SMTP_TLS</code> / <code>SMTP_SSL</code></td><td><code>false</code></td><td>STARTTLS / implicit SSL</td></tr>
      </table></div>
      <h3>OpenID Connect и OAuth</h3>
      <p>Набор <code>OPENIDCONNECT_*</code> (PROVIDER, CLIENT_ID/SECRET, BUTTON, SCOPE, REGISTER) и <code>OAUTH_*</code> (CLIENT_ID/SECRET, AUTHORIZATION/TOKEN/USERINFO_ENDPOINT, BUTTON, SCOPE, REGISTER). Подробности — в английской таблице выше и в <a href="features/auth.html">Аутентификации</a>.</p>
      <h3>Telegram</h3>
      <div class="table-wrap"><table>
        <tr><th>Переменная</th><th>По умолчанию</th><th>Описание</th></tr>
        <tr><td><code>TELEGRAM_BOT_TOKEN</code></td><td>пусто</td><td>Опциональный глобальный токен бота</td></tr>
        <tr><td><code>TELEGRAM_PROXY_SOCKS5</code></td><td><code>true</code></td><td>SOCKS5 для proxy</td></tr>
        <tr><td><code>TELEGRAM_PROXY_HOST</code> / <code>PORT</code></td><td>пусто / <code>8080</code></td><td>Адрес proxy</td></tr>
        <tr><td><code>TELEGRAM_PROXY_USERNAME</code> / <code>PASSWORD</code></td><td>пусто</td><td>Учётка proxy</td></tr>
      </table></div>

      <h2 id="worker">Воркер (<code>monitoring-worker-go</code>)</h2>
      <div class="table-wrap"><table>
        <tr><th>Переменная</th><th>По умолчанию</th><th>Описание</th></tr>
        <tr><td><code>SERVER_HOST</code></td><td>—</td><td><strong>Обязательно.</strong> URL сервера</td></tr>
        <tr><td><code>WORKER_KEY_HASH</code></td><td>—</td><td><strong>Обязательно.</strong> Ключ из Admin → Workers</td></tr>
        <tr><td><code>TZ</code></td><td><code>UTC</code></td><td>Часовой пояс</td></tr>
        <tr><td><code>PROTOCOL_VERSION</code></td><td><code>2.0</code></td><td>Только 2.0+</td></tr>
        <tr><td><code>WORKER_THREADS</code></td><td><code>10</code></td><td>Потоки проверок</td></tr>
        <tr><td><code>JOBS_GET_TIMEOUT</code></td><td><code>30</code></td><td>Интервал опроса заданий (сек)</td></tr>
        <tr><td><code>LOOP_TIMEOUT</code></td><td><code>200000</code></td><td>Задержка цикла (мкс)</td></tr>
        <tr><td><code>RESPONSE_SEND_TIMEOUT</code></td><td><code>5</code></td><td>Интервал отправки результатов (сек)</td></tr>
        <tr><td><code>LOGS_WRITE_TIMEOUT</code></td><td><code>10</code></td><td>Интервал записи логов (сек)</td></tr>
        <tr><td><code>PROXY_HOST</code> / <code>PROXY_TYPE</code></td><td>пусто</td><td>Исходящий proxy для проверок</td></tr>
        <tr><td><code>WORKER_VERSION</code></td><td>ldflags / <code>local</code></td><td>Версия в API</td></tr>
        <tr><td><code>DEBUG</code> / <code>CURL_DEBUG</code> / <code>DOCKER_DEBUG</code></td><td><code>false</code></td><td>Логи воркера / HTTP / Docker API</td></tr>
        <tr><td><code>IMMEDIATE_ERROR_RETRY</code></td><td><code>true</code></td><td>Сразу повторять упавшую задачу (как PHP)</td></tr>
        <tr><td><code>AUTO_UPDATE</code> / <code>UPDATE_FROM_GITHUB</code></td><td><code>true</code></td><td>Автообновление бинарника с GitHub</td></tr>
      </table></div>
      <p>В Docker лучше обновлять тегом образа и ставить <code>AUTO_UPDATE=false</code>.</p>

      <h2 id="agent">Агент (<code>monitoring-agent</code>)</h2>
      <div class="table-wrap"><table>
        <tr><th>Переменная</th><th>По умолчанию</th><th>Описание</th></tr>
        <tr><td><code>SERVER_HOST</code></td><td>—</td><td><strong>Обязательно.</strong> URL сервера</td></tr>
        <tr><td><code>AGENT_KEY_HASH</code></td><td>—</td><td><strong>Обязательно.</strong> Ключ из Admin → Servers</td></tr>
        <tr><td><code>TZ</code></td><td><code>UTC</code></td><td>Часовой пояс</td></tr>
        <tr><td><code>REPORT_INTERVAL_SEC</code></td><td><code>30</code></td><td>Интервал отчёта (15–600)</td></tr>
        <tr><td><code>AGENT_VERSION</code></td><td>ldflags / <code>local</code></td><td>Версия в API</td></tr>
        <tr><td><code>DEBUG</code></td><td><code>false</code></td><td>Подробный stderr</td></tr>
        <tr><td><code>COLLECT_DOCKER</code></td><td><code>true</code></td><td>Инвентарь Docker</td></tr>
        <tr><td><code>COLLECT_PROXMOX</code></td><td><code>true</code></td><td>Гости Proxmox VE</td></tr>
        <tr><td><code>COLLECT_AUTH</code></td><td><code>true</code></td><td>Дельта auth-лога</td></tr>
        <tr><td><code>COLLECT_PROCESSES</code></td><td><code>true</code></td><td>Снимок процессов</td></tr>
        <tr><td><code>PROCESS_TOP_N</code></td><td><code>20</code></td><td>Топ процессов по CPU (5–100)</td></tr>
        <tr><td><code>AUTO_UPDATE</code> / <code>UPDATE_FROM_GITHUB</code></td><td><code>true</code></td><td>Автообновление с GitHub</td></tr>
      </table></div>

      <div class="page-nav"><div><a href="usage.html">← Интерфейс</a></div><div><a href="features/index.html">Возможности →</a></div></div>
    """,
)

# Features index + all feature pages
add_doc(
    "feat_index",
    "docs/features/index.html",
    "Features — Monitoring",
    "Возможности — Monitoring",
    """
      <h1>Features</h1>
      <p class="lead">Complete map of product capabilities. Each page includes configuration notes and related screenshots where available.</p>
      <div class="grid-2">
        <div class="card"><h3><a href="dashboard.html">Dashboard</a></h3><p>Live tree, filters, charts, WebSocket updates.</p></div>
        <div class="card"><h3><a href="monitors.html">Monitors</a></h3><p>All check types, folders, fail modes, intervals.</p></div>
        <div class="card"><h3><a href="workers.html">Workers</a></h3><p>Remote checkers, keys, auto-update.</p></div>
        <div class="card"><h3><a href="agents.html">Host agents</a></h3><p>Server metrics, Proxmox, Docker, install.</p></div>
        <div class="card"><h3><a href="docker.html">Docker hosts</a></h3><p>TLS Engine API endpoints for container checks.</p></div>
        <div class="card"><h3><a href="notifications.html">Notifications</a></h3><p>Channels, actions, signatures, in-app.</p></div>
        <div class="card"><h3><a href="maintenance.html">Maintenance</a></h3><p>Planned windows with folder inheritance.</p></div>
        <div class="card"><h3><a href="rbac.html">RBAC &amp; audit</a></h3><p>ACL, groups, secrets, impersonate, logs.</p></div>
        <div class="card"><h3><a href="auth.html">Authentication</a></h3><p>Password, OpenID, OAuth, 2FA, SMTP.</p></div>
        <div class="card"><h3><a href="ssl-events.html">SSL &amp; events</a></h3><p>Certificate expiry alerts and event store.</p></div>
        <div class="card"><h3><a href="api.html">API &amp; MCP</a></h3><p>Status API, Management v2, Swagger, MCP.</p></div>
      </div>
    """,
    """
      <h1>Возможности</h1>
      <p class="lead">Полная карта функций продукта. На каждой странице — настройка и скриншоты.</p>
      <div class="grid-2">
        <div class="card"><h3><a href="dashboard.html">Дашборд</a></h3><p>Дерево, фильтры, графики, WebSocket.</p></div>
        <div class="card"><h3><a href="monitors.html">Мониторы</a></h3><p>Типы проверок, папки, fail modes.</p></div>
        <div class="card"><h3><a href="workers.html">Воркеры</a></h3><p>Удалённые проверки, ключи, автообновление.</p></div>
        <div class="card"><h3><a href="agents.html">Агенты</a></h3><p>Метрики хоста, Proxmox, Docker.</p></div>
        <div class="card"><h3><a href="docker.html">Docker-хосты</a></h3><p>TLS Engine API для контейнеров.</p></div>
        <div class="card"><h3><a href="notifications.html">Уведомления</a></h3><p>Каналы, действия, подписи.</p></div>
        <div class="card"><h3><a href="maintenance.html">Обслуживание</a></h3><p>Окна работ с наследованием.</p></div>
        <div class="card"><h3><a href="rbac.html">RBAC и аудит</a></h3><p>ACL, группы, секреты, логи.</p></div>
        <div class="card"><h3><a href="auth.html">Аутентификация</a></h3><p>Пароль, OpenID, OAuth, 2FA.</p></div>
        <div class="card"><h3><a href="ssl-events.html">SSL и события</a></h3><p>Истечение сертификатов и события.</p></div>
        <div class="card"><h3><a href="api.html">API и MCP</a></h3><p>Status, Management v2, Swagger, MCP.</p></div>
      </div>
    """,
)

add_doc(
    "dashboard",
    "docs/features/dashboard.html",
    "Dashboard — Monitoring",
    "Дашборд — Monitoring",
    f"""
      <h1>Dashboard</h1>
      <p class="lead">The home screen is a live view of every monitor you are allowed to read.</p>
      <h2>Capabilities</h2>
      <ul>
        <li>Nested folders with remembered collapse state</li>
        <li>Status badges and 24-hour availability percentage</li>
        <li>Multi-select status filter and title search</li>
        <li>WebSocket-driven refresh for list and selected monitor</li>
        <li>Uptime bar, response-time / metric charts (ECharts), worker breakdown, events</li>
        <li>Auto light/dark theme matching the OS</li>
      </ul>
      {shot("screenshot_mainpage.png", "Dashboard list")}
      {shot("screenshot_mainpage_monitor.png", "Selected monitor")}
      <div class="page-nav"><div><a href="index.html">← Features</a></div><div><a href="monitors.html">Monitors →</a></div></div>
    """,
    f"""
      <h1>Дашборд</h1>
      <p class="lead">Главный экран — живое представление всех мониторов, доступных на чтение.</p>
      <h2>Возможности</h2>
      <ul>
        <li>Вложенные папки с запоминанием сворачивания</li>
        <li>Бейджи статуса и availability за 24 часа</li>
        <li>Мультифильтр по статусу и поиск по названию</li>
        <li>Обновление списка и карточки по WebSocket</li>
        <li>Uptime, графики (ECharts), разбивка по воркерам, события</li>
        <li>Автотема light/dark</li>
      </ul>
      {shot("screenshot_mainpage.png", "Список на дашборде")}
      {shot("screenshot_mainpage_monitor.png", "Выбранный монитор")}
      <div class="page-nav"><div><a href="index.html">← Возможности</a></div><div><a href="monitors.html">Мониторы →</a></div></div>
    """,
)

add_doc(
    "monitors",
    "docs/features/monitors.html",
    "Monitors — Monitoring",
    "Мониторы — Monitoring",
    f"""
      <h1>Monitors</h1>
      <p class="lead">Monitors are the checks (or folders) that define what Monitoring watches and how it alerts.</p>
      <h2>Organization</h2>
      <ul>
        <li><strong>Folders</strong> — hierarchy; ACL and maintenance inherit to children</li>
        <li>Enable/disable per monitor; copy monitor in admin UI</li>
        <li>Assign workers and notify channels (ACL-filtered)</li>
        <li><strong>Fail modes</strong>: notify when any / majority (≥50%) / all assigned workers fail</li>
        <li>Interval, timeout, re-alert cadence; optional signatures; <code>api_enabled</code> for Status API</li>
      </ul>
      <h2>Check types</h2>
      <div class="table-wrap"><table>
        <tr><th>Type</th><th>What it does</th></tr>
        <tr><td>HTTPS / HTTP</td><td>URL check: status codes, redirects, headers, proxy, SSL verify, timeout. Optional response header <code>Log</code> for custom alert text</td></tr>
        <tr><td>HTTP JSON</td><td>HTTP plus <code>json_path</code> and expected value/type; same optional <code>Log</code> response header</td></tr>
        <tr><td>TCP</td><td>Host:port connectivity</td></tr>
        <tr><td>Ping</td><td>ICMP reachability</td></tr>
        <tr><td>Docker</td><td>Container status via configured Docker Engine API</td></tr>
        <tr><td>External</td><td>Push/callback via public <code>/api/external/{{hash}}/</code>; optional <code>Log</code> header or <code>?log=</code> / <code>?message=</code></td></tr>
        <tr><td>node-exporter disk/memory</td><td>Prometheus exporter scrapes with % thresholds</td></tr>
        <tr><td>Server offline</td><td>Agent heartbeat age (minutes)</td></tr>
        <tr><td>Server CPU / memory / disk / container</td><td>Thresholds from agent metrics</td></tr>
        <tr><td>Server net RX / TX</td><td>Bandwidth thresholds in Mbps</td></tr>
      </table></div>
      <h2 id="custom-log">Custom error text via <code>Log</code></h2>
      <p>HTTPS, HTTP JSON and External can attach a human-readable message that appears in events and notifications as <code>Log: …</code>.</p>
      <h3>HTTPS / HTTP JSON (checked resource → worker)</h3>
      <p>The endpoint under check returns an optional response header named exactly <code>Log</code>. The worker copies it into <code>response_error</code> (prefixed with <code>Log: </code>, sanitized, truncated). If present, it overrides other <code>response_error</code> text for that check (including HTTP JSON messages). The server stores it on the monitor as <code>external_log</code> on FAIL and uses it in fail alerts.</p>
      {pre('''HTTP/1.1 500 Internal Server Error
Log: upstream timeout on payment-api
''')}
      <h3>External (callback → server)</h3>
      <p>On <code>GET /api/external/{{hash}}/?status=ok|fail</code> (also accepts synonyms like <code>error</code>/<code>down</code>/<code>0</code> for fail), pass custom text with priority:</p>
      <ol>
        <li>HTTP request header <code>Log</code></li>
        <li>Query <code>?log=…</code></li>
        <li>Query <code>?message=…</code> (alias)</li>
      </ol>
      {pre('''# Header
curl -H 'Log: disk full on backup' \\
  'https://monitoring.example.com/api/external/<64hex>/?status=fail'

# Query parameter
curl 'https://monitoring.example.com/api/external/<64hex>/?status=fail&log=disk%20full'
''')}
      <p>Without custom text, fail alerts use a default like <code>External status: fail</code>. The last log is kept for heartbeat-style re-alerts.</p>
      {shot("screenshot_monitors.png", "Monitors admin")}
      {shot("screenshot_createMonitor_1.png", "Create monitor (1)")}
      {shot("screenshot_createMonitor_2.png", "Create monitor (2)")}
      <div class="page-nav"><div><a href="dashboard.html">← Dashboard</a></div><div><a href="workers.html">Workers →</a></div></div>
    """,
    f"""
      <h1>Мониторы</h1>
      <p class="lead">Мониторы — проверки (или папки), которые определяют, что смотрит система и как алертит.</p>
      <h2>Организация</h2>
      <ul>
        <li><strong>Папки</strong> — иерархия; ACL и maintenance наследуются вниз</li>
        <li>Включение/выключение; копирование в админке</li>
        <li>Назначение воркеров и каналов уведомлений</li>
        <li><strong>Fail modes</strong>: any / majority (≥50%) / all</li>
        <li>Интервал, таймаут, повтор алерта; signatures; <code>api_enabled</code> для Status API</li>
      </ul>
      <h2>Типы проверок</h2>
      <div class="table-wrap"><table>
        <tr><th>Тип</th><th>Назначение</th></tr>
        <tr><td>HTTPS / HTTP</td><td>URL: коды, редиректы, заголовки, proxy, SSL verify. Опциональный response-заголовок <code>Log</code> для текста алерта</td></tr>
        <tr><td>HTTP JSON</td><td>HTTP + <code>json_path</code> и ожидаемое значение; тот же заголовок <code>Log</code></td></tr>
        <tr><td>TCP</td><td>Доступность host:port</td></tr>
        <tr><td>Ping</td><td>ICMP</td></tr>
        <tr><td>Docker</td><td>Статус контейнера через Docker Engine API</td></tr>
        <tr><td>External</td><td>Push через <code>/api/external/{{hash}}/</code>; заголовок <code>Log</code> или <code>?log=</code> / <code>?message=</code></td></tr>
        <tr><td>node-exporter disk/memory</td><td>Скрейп exporter с порогами %</td></tr>
        <tr><td>Server offline</td><td>Возраст heartbeat агента</td></tr>
        <tr><td>Server CPU / memory / disk / container</td><td>Пороги по метрикам агента</td></tr>
        <tr><td>Server net RX / TX</td><td>Пороги Mbps</td></tr>
      </table></div>
      <h2 id="custom-log">Свой текст ошибки через <code>Log</code></h2>
      <p>HTTPS, HTTP JSON и External могут передать понятное сообщение — в событиях и алертах оно видно как <code>Log: …</code>.</p>
      <h3>HTTPS / HTTP JSON (проверяемый ресурс → воркер)</h3>
      <p>Ответ проверяемого URL может содержать заголовок ровно <code>Log</code>. Воркер кладёт его в <code>response_error</code> (с префиксом <code>Log: </code>, очистка и обрезка). Если заголовок есть, он перекрывает другой текст ошибки этой проверки (в т.ч. сообщения HTTP JSON). Сервер сохраняет его в <code>external_log</code> при FAIL и использует в алертах.</p>
      {pre('''HTTP/1.1 500 Internal Server Error
Log: upstream timeout on payment-api
''')}
      <h3>External (callback → сервер)</h3>
      <p>На <code>GET /api/external/{{hash}}/?status=ok|fail</code> (для fail также <code>error</code>/<code>down</code>/<code>0</code>) текст передаётся с приоритетом:</p>
      <ol>
        <li>HTTP-заголовок запроса <code>Log</code></li>
        <li>Query <code>?log=…</code></li>
        <li>Query <code>?message=…</code> (алиас)</li>
      </ol>
      {pre('''# Заголовок
curl -H 'Log: disk full on backup' \\
  'https://monitoring.example.com/api/external/<64hex>/?status=fail'

# Параметр
curl 'https://monitoring.example.com/api/external/<64hex>/?status=fail&log=disk%20full'
''')}
      <p>Без своего текста fail даёт сообщение вроде <code>External status: fail</code>. Последний log сохраняется для повторных heartbeat-алертов.</p>
      {shot("screenshot_monitors.png", "Админка мониторов")}
      {shot("screenshot_createMonitor_1.png", "Создание монитора (1)")}
      {shot("screenshot_createMonitor_2.png", "Создание монитора (2)")}
      <div class="page-nav"><div><a href="dashboard.html">← Дашборд</a></div><div><a href="workers.html">Воркеры →</a></div></div>
    """,
)

add_doc(
    "workers",
    "docs/features/workers.html",
    "Workers — Monitoring",
    "Воркеры — Monitoring",
    f"""
      <h1>Workers</h1>
      <p class="lead">Workers are remote Go processes that pull jobs from the server and return check results (protocol 2.0+).</p>
      <h2>Management</h2>
      <ul>
        <li>CRUD with title, last activity, protocol/worker version</li>
        <li>Timeouts: jobs get, loop, response send, logs write; thread count</li>
        <li><code>WORKER_KEY_HASH</code> secret (regenerate gated by secrets permission)</li>
        <li>Assign monitors and Docker hosts</li>
        <li>Restart flag for next sync; desired version for GitHub auto-update</li>
      </ul>
      <h2>Run with Docker</h2>
      {pre(WORKER_RUN)}
      <p>Set <code>AUTO_UPDATE=false</code> in Docker images if you prefer image tags over binary self-replace.</p>
      <h2>Run without Docker — download binary from GitHub</h2>
      <p>No Go toolchain on the server. Assets: <code>monitoring-worker-linux-amd64</code> / <code>linux-arm64</code> (+ <code>.sha256</code>) from <a href="https://github.com/AKEB/monitoring-worker-go/releases">AKEB/monitoring-worker-go releases</a>. Set <code>VER</code> to the latest tag.</p>
      {pre(WORKER_DOWNLOAD_INSTALL)}
      <p>The worker loads <code>.env</code> from the working directory or next to the binary. Full variables: <a href="../environment.html#worker">Environment → Worker</a>.</p>
      <h3>Optional: build from source</h3>
      <p>Only if you need a custom binary — not required for production hosts.</p>
      {pre(WORKER_BUILD)}
      {shot("screenshot_workers.png", "Workers admin")}
      <div class="page-nav"><div><a href="monitors.html">← Monitors</a></div><div><a href="agents.html">Host agents →</a></div></div>
    """,
    f"""
      <h1>Воркеры</h1>
      <p class="lead">Воркеры — удалённые Go-процессы: забирают задания и отдают результаты (протокол 2.0+).</p>
      <h2>Управление</h2>
      <ul>
        <li>CRUD: название, активность, версии протокола/воркера</li>
        <li>Таймауты и число потоков</li>
        <li>Секрет <code>WORKER_KEY_HASH</code></li>
        <li>Привязка мониторов и Docker-хостов</li>
        <li>Restart и целевая версия для автообновления с GitHub</li>
      </ul>
      <h2>Запуск в Docker</h2>
      {pre(WORKER_RUN)}
      <p>В Docker лучше <code>AUTO_UPDATE=false</code> и обновление тегом образа.</p>
      <h2>Без Docker — скачать бинарник с GitHub</h2>
      <p>На сервере не нужен Go. Файлы: <code>monitoring-worker-linux-amd64</code> / <code>linux-arm64</code> (+ <code>.sha256</code>) в <a href="https://github.com/AKEB/monitoring-worker-go/releases">релизах AKEB/monitoring-worker-go</a>. Подставьте актуальный тег в <code>VER</code>.</p>
      {pre(WORKER_DOWNLOAD_INSTALL)}
      <p>Воркер читает <code>.env</code> из рабочей директории или рядом с бинарником. Полный список: <a href="../environment.html#worker">Окружение → Воркер</a>.</p>
      <h3>Опционально: сборка из исходников</h3>
      <p>Только если нужен свой бинарник — на проде обычно не требуется.</p>
      {pre(WORKER_BUILD)}
      {shot("screenshot_workers.png", "Админка воркеров")}
      <div class="page-nav"><div><a href="monitors.html">← Мониторы</a></div><div><a href="agents.html">Агенты →</a></div></div>
    """,
)

add_doc(
    "agents",
    "docs/features/agents.html",
    "Host agents — Monitoring",
    "Агенты хостов — Monitoring",
    f"""
      <h1>Host agents</h1>
      <p class="lead">The <code>monitoring-agent</code> binary pushes host telemetry to the server about every 30 seconds.</p>
      <h2>What it reports</h2>
      <ul>
        <li>Host identity, uptime, virtualization</li>
        <li>CPU (cores, load, usage %), memory/swap, disks, network (IPs, bps)</li>
        <li>Docker containers when the socket is available</li>
        <li>Proxmox VE QEMU/LXC guests when <code>/etc/pve</code> exists</li>
        <li>Auth log delta (SSH/sudo), top processes</li>
      </ul>
      <h2>Server UI</h2>
      <p>Admin → Servers → Create yields <code>AGENT_KEY_HASH</code>. Edit page shows live charts, Proxmox guests, auth events, key rotate, desired agent version / update now.</p>
      <h2>Install with Docker</h2>
      {pre(AGENT_RUN)}
      <h2>Install without Docker — download binary from GitHub</h2>
      <p>No Go on the host. Assets: <code>monitoring-agent-linux-amd64</code> / <code>linux-arm64</code> (+ <code>.sha256</code>) from <a href="https://github.com/AKEB/monitoring-agent/releases">AKEB/monitoring-agent releases</a>. Works on Proxmox, Debian, Raspberry Pi, LXC.</p>
      {pre(AGENT_DOWNLOAD_INSTALL)}
      <p>Full variables: <a href="../environment.html#agent">Environment → Agent</a>.</p>
      <h3>Optional: build from source</h3>
      <p>Only for custom builds — not needed on production servers.</p>
      {pre(AGENT_BUILD)}
      <h2>Derived monitors</h2>
      <p>Create Server-* monitor types bound to a registered server for offline/CPU/RAM/disk/container/net alerts.</p>
      <div class="page-nav"><div><a href="workers.html">← Workers</a></div><div><a href="docker.html">Docker hosts →</a></div></div>
    """,
    f"""
      <h1>Агенты хостов</h1>
      <p class="lead">Бинарник <code>monitoring-agent</code> пушит телеметрию хоста на сервер примерно каждые 30 секунд.</p>
      <h2>Что отдаёт</h2>
      <ul>
        <li>Идентичность хоста, uptime, виртуализация</li>
        <li>CPU, память/swap, диски, сеть</li>
        <li>Docker-контейнеры при доступном сокете</li>
        <li>Гости Proxmox VE при наличии <code>/etc/pve</code></li>
        <li>События auth, топ процессов</li>
      </ul>
      <h2>UI сервера</h2>
      <p>Admin → Servers → Create даёт <code>AGENT_KEY_HASH</code>. На карточке — графики, Proxmox, auth, ротация ключа, целевая версия.</p>
      <h2>Установка в Docker</h2>
      {pre(AGENT_RUN)}
      <h2>Без Docker — скачать бинарник с GitHub</h2>
      <p>Go на хосте не нужен. Файлы: <code>monitoring-agent-linux-amd64</code> / <code>linux-arm64</code> (+ <code>.sha256</code>) в <a href="https://github.com/AKEB/monitoring-agent/releases">релизах AKEB/monitoring-agent</a>. Подходит для Proxmox, Debian, Raspberry Pi, LXC.</p>
      {pre(AGENT_DOWNLOAD_INSTALL)}
      <p>Полный список переменных: <a href="../environment.html#agent">Окружение → Агент</a>.</p>
      <h3>Опционально: сборка из исходников</h3>
      <p>Только для кастомной сборки — на серверах обычно не нужна.</p>
      {pre(AGENT_BUILD)}
      <h2>Производные мониторы</h2>
      <p>Типы Server-* привязываются к зарегистрированному серверу.</p>
      <div class="page-nav"><div><a href="workers.html">← Воркеры</a></div><div><a href="docker.html">Docker-хосты →</a></div></div>
    """,
)

add_doc(
    "docker",
    "docs/features/docker.html",
    "Docker hosts — Monitoring",
    "Docker-хосты — Monitoring",
    """
      <h1>Docker hosts</h1>
      <p class="lead">Register Docker Engine API endpoints so workers can check container state over TLS.</p>
      <h2>Configuration</h2>
      <ul>
        <li>Host address and port</li>
        <li>TLS CA / client cert / key (PEM write-only; API only exposes <code>tls_present</code>)</li>
        <li>Optional <code>tls_server_name</code> when the IP does not match the certificate DNS</li>
        <li>Link which workers may poll the host</li>
        <li>Enable/disable + ACL</li>
      </ul>
      <p>Docker-type monitors pick a container name from AJAX lists. Interval/timeout can follow the Docker host settings.</p>
      <div class="page-nav"><div><a href="agents.html">← Host agents</a></div><div><a href="notifications.html">Notifications →</a></div></div>
    """,
    """
      <h1>Docker-хосты</h1>
      <p class="lead">Регистрация endpoints Docker Engine API, чтобы воркеры проверяли контейнеры по TLS.</p>
      <h2>Настройка</h2>
      <ul>
        <li>Адрес и порт</li>
        <li>TLS CA / client cert / key (PEM только на запись)</li>
        <li>Опционально <code>tls_server_name</code>, если IP не совпадает с DNS в сертификате</li>
        <li>Какие воркеры опрашивают хост</li>
        <li>Включение/выключение и ACL</li>
      </ul>
      <p>Мониторы типа Docker выбирают контейнер из AJAX-списка.</p>
      <div class="page-nav"><div><a href="agents.html">← Агенты</a></div><div><a href="notifications.html">Уведомления →</a></div></div>
    """,
)

add_doc(
    "notifications",
    "docs/features/notifications.html",
    "Notifications — Monitoring",
    "Уведомления — Monitoring",
    """
      <h1>Notifications</h1>
      <p class="lead">Alert channels deliver status changes with interactive actions and optional signatures.</p>
      <h2>Channels</h2>
      <div class="table-wrap"><table>
        <tr><th>Channel</th><th>Notes</th></tr>
        <tr><td>Telegram</td><td>Bot token + chat; optional SOCKS/HTTP proxy via env; action buttons</td></tr>
        <tr><td>Mattermost</td><td>Server URL + token; channel or @user; actions</td></tr>
        <tr><td>Gotify</td><td>Server URL, app token, priority</td></tr>
        <tr><td>MAX</td><td>Bot token + receiver; interactive buttons</td></tr>
        <tr><td>Webhook</td><td>HTTP POST; optional basic auth; Alertmanager-style firing/resolved payload</td></tr>
      </table></div>
      <h2>Alert actions</h2>
      <p>Resolve, Take, Mute, Unmute, Call, OK. Mute suppresses repeats until the monitor is green again. Callbacks hit <code>/api/alert-action/...</code>.</p>
      <h2>Other</h2>
      <ul>
        <li>Test send from notify edit (needs write + secrets)</li>
        <li>Signatures — reusable footer blocks on alerts</li>
        <li>In-app / browser notifications for subscribed UI sessions</li>
        <li><code>notify_secrets</code> ACL gates tokens and URLs</li>
      </ul>
      <div class="page-nav"><div><a href="docker.html">← Docker hosts</a></div><div><a href="maintenance.html">Maintenance →</a></div></div>
    """,
    """
      <h1>Уведомления</h1>
      <p class="lead">Каналы алертов со статусными изменениями, действиями и подписями.</p>
      <h2>Каналы</h2>
      <div class="table-wrap"><table>
        <tr><th>Канал</th><th>Заметки</th></tr>
        <tr><td>Telegram</td><td>Бот + chat; proxy; кнопки действий</td></tr>
        <tr><td>Mattermost</td><td>URL + token; канал или @user</td></tr>
        <tr><td>Gotify</td><td>URL, app token, priority</td></tr>
        <tr><td>MAX</td><td>Бот + receiver; кнопки</td></tr>
        <tr><td>Webhook</td><td>HTTP POST; payload в стиле Alertmanager</td></tr>
      </table></div>
      <h2>Действия</h2>
      <p>Resolve, Take, Mute, Unmute, Call, OK. Mute глушит повторы до зелёного статуса.</p>
      <h2>Ещё</h2>
      <ul>
        <li>Тестовая отправка</li>
        <li>Signatures — подвал алерта</li>
        <li>In-app / browser notifications</li>
        <li>ACL <code>notify_secrets</code></li>
      </ul>
      <div class="page-nav"><div><a href="docker.html">← Docker-хосты</a></div><div><a href="maintenance.html">Обслуживание →</a></div></div>
    """,
)

add_doc(
    "maintenance",
    "docs/features/maintenance.html",
    "Maintenance — Monitoring",
    "Обслуживание — Monitoring",
    """
      <h1>Maintenance</h1>
      <p class="lead">Schedule planned windows so checks show Maintenance instead of noisy failures.</p>
      <ul>
        <li>Title, <code>start_time</code> / <code>finish_time</code> (finish ≥ start)</li>
        <li>Attach any monitors you can read; folders inherit to children</li>
        <li>Status appears on the dashboard and in the Status API</li>
        <li>ACL: access + <code>create_maintenance</code></li>
      </ul>
      <p>UI: <code>/maintenances/</code> (user-facing, not only admin).</p>
      <div class="page-nav"><div><a href="notifications.html">← Notifications</a></div><div><a href="rbac.html">RBAC →</a></div></div>
    """,
    """
      <h1>Обслуживание</h1>
      <p class="lead">Плановые окна: статус Maintenance вместо ложных аварий.</p>
      <ul>
        <li>Название, <code>start_time</code> / <code>finish_time</code></li>
        <li>Привязка мониторов; папки наследуются детьми</li>
        <li>Статус на дашборде и в Status API</li>
        <li>ACL и <code>create_maintenance</code></li>
      </ul>
      <p>UI: <code>/maintenances/</code>.</p>
      <div class="page-nav"><div><a href="notifications.html">← Уведомления</a></div><div><a href="rbac.html">RBAC →</a></div></div>
    """,
)

add_doc(
    "rbac",
    "docs/features/rbac.html",
    "RBAC & audit — Monitoring",
    "RBAC и аудит — Monitoring",
    f"""
      <h1>RBAC &amp; audit</h1>
      <p class="lead">Fine-grained access control for every major object, with folder inheritance and a full audit trail.</p>
      <h2>Subjects</h2>
      <p><code>monitor</code>, <code>worker</code>, <code>notify</code>, <code>maintenance</code>, <code>docker</code>, <code>signature</code>, <code>server</code>, plus Framework <code>user</code>/<code>group</code>.</p>
      <h2>Levels</h2>
      <ul>
        <li>Read / Write / Delete</li>
        <li>ACCESS_READ / ACCESS_WRITE / ACCESS_CHANGE for managing ACL itself</li>
        <li><code>create_*</code> permissions per entity type</li>
        <li>Secrets: worker key, notify secrets, server <code>agent_key_hash</code></li>
      </ul>
      <h2>Users &amp; groups</h2>
      <p>Admin CRUD, group membership, per-object permissions UI at <code>/admin/permissions/{{subject}}/{{id}}/</code>, impersonate, audit logs.</p>
      {shot("screenshot_permissions.png", "Permissions")}
      {shot("screenshot_addNewPermission.png", "Add permission")}
      <div class="page-nav"><div><a href="maintenance.html">← Maintenance</a></div><div><a href="auth.html">Authentication →</a></div></div>
    """,
    f"""
      <h1>RBAC и аудит</h1>
      <p class="lead">Детальные права на объекты, наследование от папок и журнал аудита.</p>
      <h2>Субъекты</h2>
      <p><code>monitor</code>, <code>worker</code>, <code>notify</code>, <code>maintenance</code>, <code>docker</code>, <code>signature</code>, <code>server</code>, а также <code>user</code>/<code>group</code>.</p>
      <h2>Уровни</h2>
      <ul>
        <li>Read / Write / Delete</li>
        <li>ACCESS_* для управления ACL</li>
        <li><code>create_*</code> на типы сущностей</li>
        <li>Секреты: ключ воркера, notify, <code>agent_key_hash</code></li>
      </ul>
      <h2>Пользователи и группы</h2>
      <p>CRUD, членство в группах, UI прав, impersonate, audit logs.</p>
      {shot("screenshot_permissions.png", "Права")}
      {shot("screenshot_addNewPermission.png", "Добавление права")}
      <div class="page-nav"><div><a href="maintenance.html">← Обслуживание</a></div><div><a href="auth.html">Аутентификация →</a></div></div>
    """,
)

add_doc(
    "auth",
    "docs/features/auth.html",
    "Authentication — Monitoring",
    "Аутентификация — Monitoring",
    """
      <h1>Authentication</h1>
      <p class="lead">Sign-in options are controlled by environment variables on the server.</p>
      <div class="table-wrap"><table>
        <tr><th>Method</th><th>Env / notes</th></tr>
        <tr><td>Email + password</td><td><code>APP_SIGNIN_ACTIVE</code>; signup via <code>APP_SIGNUP_ACTIVE</code></td></tr>
        <tr><td>Forgot password</td><td>SMTP settings (<code>SMTP_*</code>)</td></tr>
        <tr><td>OpenID Connect</td><td><code>OPENIDCONNECT_*</code> provider, client, scopes, optional auto-register</td></tr>
        <tr><td>Generic OAuth</td><td><code>OAUTH_*</code> auth/token/userinfo endpoints</td></tr>
        <tr><td>2FA</td><td>Framework settings (disable path in profile)</td></tr>
      </table></div>
      <p>UI uses session cookies. Management/Status APIs use personal Bearer tokens and ignore cookies.</p>
      <div class="page-nav"><div><a href="rbac.html">← RBAC</a></div><div><a href="ssl-events.html">SSL &amp; events →</a></div></div>
    """,
    """
      <h1>Аутентификация</h1>
      <p class="lead">Способы входа задаются переменными окружения сервера.</p>
      <div class="table-wrap"><table>
        <tr><th>Способ</th><th>Env / заметки</th></tr>
        <tr><td>E-mail + пароль</td><td><code>APP_SIGNIN_ACTIVE</code>; регистрация — <code>APP_SIGNUP_ACTIVE</code></td></tr>
        <tr><td>Сброс пароля</td><td>SMTP (<code>SMTP_*</code>)</td></tr>
        <tr><td>OpenID Connect</td><td><code>OPENIDCONNECT_*</code></td></tr>
        <tr><td>OAuth</td><td><code>OAUTH_*</code></td></tr>
        <tr><td>2FA</td><td>Настройки Framework</td></tr>
      </table></div>
      <p>UI — сессионные cookie. API — персональные Bearer-токены.</p>
      <div class="page-nav"><div><a href="rbac.html">← RBAC</a></div><div><a href="ssl-events.html">SSL и события →</a></div></div>
    """,
)

add_doc(
    "ssl",
    "docs/features/ssl-events.html",
    "SSL & events — Monitoring",
    "SSL и события — Monitoring",
    """
      <h1>SSL &amp; events</h1>
      <h2>SSL expiry</h2>
      <ul>
        <li>HTTPS / HTTP JSON can verify certificates and hostnames</li>
        <li>Workers report <code>cert_expire</code>; cron notifies on day thresholds 15/7/6/5/4/3/2/1</li>
        <li>Once per day per monitor; notify channels + in-app subscribers; signatures appended</li>
        <li>Exposed in Status API as <code>ssl_expire_time</code> / <code>ssl_expire_at</code></li>
      </ul>
      <h2>Events</h2>
      <ul>
        <li>Status transitions stored in <code>monitoring_events</code> with hash deduplication</li>
        <li>Shown on the home feed and per-monitor (~2 day window)</li>
        <li>Raw logs aggregated; detail retention about 24 hours</li>
      </ul>
      <div class="page-nav"><div><a href="auth.html">← Authentication</a></div><div><a href="api.html">API &amp; MCP →</a></div></div>
    """,
    """
      <h1>SSL и события</h1>
      <h2>Истечение SSL</h2>
      <ul>
        <li>HTTPS / HTTP JSON — verify сертификата и имени</li>
        <li>Воркеры отдают <code>cert_expire</code>; cron шлёт алерты за 15/7/…/1 день</li>
        <li>Не чаще раза в сутки; каналы + in-app; подписи</li>
        <li>В Status API: <code>ssl_expire_*</code></li>
      </ul>
      <h2>События</h2>
      <ul>
        <li>Переходы статусов в <code>monitoring_events</code></li>
        <li>На главной и в карточке монитора (~2 дня)</li>
        <li>Агрегация логов; детали ~24 часа</li>
      </ul>
      <div class="page-nav"><div><a href="auth.html">← Аутентификация</a></div><div><a href="api.html">API и MCP →</a></div></div>
    """,
)

add_doc(
    "api",
    "docs/features/api.html",
    "API & MCP — Monitoring",
    "API и MCP — Monitoring",
    """
      <h1>API &amp; MCP</h1>
      <p class="lead">Automate Monitoring with personal tokens, REST, Swagger and an MCP endpoint.</p>
      <h2>API tokens</h2>
      <p>Settings → API: create/revoke tokens (<code>mnt_…</code>). Send as <code>Authorization: Bearer</code> or <code>X-Api-Token</code>. Rights equal the token owner; secrets redacted without permission.</p>
      <h2>User Status API</h2>
      <p><code>GET /api/v1/status/</code> — opt-in monitors only (<code>api_enabled</code>). Returns up/down/maintenance/unknown, availability windows, SSL expiry, workers, maintenances. Cached ~20s with rate limits.</p>
      <h2>Management API v2</h2>
      <p>REST CRUD for monitors, notify, signatures, workers, maintenances, dockers, servers; users/groups read-only; logs by date; permissions GET/PUT. Interactive docs: <code>/api/docs/</code> (OpenAPI <code>/api/docs/openapi.json</code>).</p>
      <h2>MCP</h2>
      <p><code>POST /mcp/</code> JSON-RPC; tools mirror v2 plus <code>api_docs</code>. Suitable for Cursor-style remote MCP configs.</p>
      <h2>Other endpoints</h2>
      <ul>
        <li>External callback: public hash URLs for External monitors; optional <code>Log</code> header or <code>?log=</code> / <code>?message=</code> (see <a href="monitors.html#custom-log">Monitors → Log</a>)</li>
        <li>Agent report: <code>POST /api/agent/report/</code></li>
        <li>Alert-action callbacks for messenger buttons</li>
      </ul>
      <p>Deep protocol notes: <a href="https://github.com/AKEB/monitoring">server docs</a> (<code>WORKER_API.md</code>, <code>USER_API.md</code>, <code>MANAGEMENT_API.md</code>, <code>AGENT_API.md</code>).</p>
      <div class="page-nav"><div><a href="ssl-events.html">← SSL &amp; events</a></div><div><a href="../index.html">Docs home →</a></div></div>
    """,
    """
      <h1>API и MCP</h1>
      <p class="lead">Автоматизация через токены, REST, Swagger и MCP.</p>
      <h2>API-токены</h2>
      <p>Settings → API: токены <code>mnt_…</code> как <code>Authorization: Bearer</code> или <code>X-Api-Token</code>. Права = владелец токена.</p>
      <h2>User Status API</h2>
      <p><code>GET /api/v1/status/</code> — только мониторы с <code>api_enabled</code>. Статусы, availability, SSL, воркеры, maintenance.</p>
      <h2>Management API v2</h2>
      <p>CRUD сущностей, права, логи. Swagger: <code>/api/docs/</code>.</p>
      <h2>MCP</h2>
      <p><code>POST /mcp/</code> — инструменты как у v2 плюс <code>api_docs</code>.</p>
      <h2>Прочее</h2>
      <ul>
        <li>External callback: заголовок <code>Log</code> или <code>?log=</code> / <code>?message=</code> (см. <a href="monitors.html#custom-log">Мониторы → Log</a>)</li>
        <li>Agent report</li>
        <li>Alert-action callbacks</li>
      </ul>
      <p>Детали протоколов — в репозитории сервера (<code>*_API.md</code>).</p>
      <div class="page-nav"><div><a href="ssl-events.html">← SSL и события</a></div><div><a href="../index.html">К документации →</a></div></div>
    """,
)


def main() -> None:
    write(
        "index.html",
        page_shell(
            "en",
            "index.html",
            "Monitoring — Distributed Monitoring System",
            landing_en(),
            description="Distributed uptime and host monitoring with Server, Workers and Agents.",
        ),
    )
    write(
        "ru/index.html",
        page_shell(
            "ru",
            "ru/index.html",
            "Monitoring — распределённая система мониторинга",
            landing_ru(),
            description="Распределённый мониторинг доступности и хостов.",
        ),
    )

    for meta in DOCS.values():
        f = meta["file"]
        write(
            f,
            page_shell(
                "en",
                f,
                meta["title_en"],
                meta["body_en"],
                docs=True,
                description=meta["desc_en"],
            ),
        )
        write(
            "ru/" + f,
            page_shell(
                "ru",
                "ru/" + f,
                meta["title_ru"],
                meta["body_ru"],
                docs=True,
                description=meta["desc_ru"],
            ),
        )

    print("done", len(list(ROOT.rglob("*.html"))), "html files")


if __name__ == "__main__":
    main()
