#!/usr/bin/env python3
"""
Coworker Labs site builder.
Renders Jinja2 templates in src/ with YAML data from src/_data/.
Outputs static HTML to _site/.
"""

import os
import shutil
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

SRC     = os.path.join(os.path.dirname(__file__), "src")
DATA    = os.path.join(SRC, "_data")
OUT     = os.path.join(os.path.dirname(__file__), "_site")

PAGES = [
    ("index.html",         "index.html"),
    ("professionals.html", "professionals.html"),
    ("organizations.html", "organizations.html"),
    ("about.html",         "about.html"),
]

# ── helpers ──────────────────────────────────────────────────────────────────

def load_yaml(name):
    path = os.path.join(DATA, name)
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)

def copy_tree(src_dir, dst_dir):
    if os.path.exists(dst_dir):
        shutil.rmtree(dst_dir)
    shutil.copytree(src_dir, dst_dir)

# ── build ─────────────────────────────────────────────────────────────────────

def build():
    # fresh output dir
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

    # load all data
    ctx = {
        "site":          load_yaml("site.yaml"),
        "homepage":      load_yaml("homepage.yaml"),
        "professionals": load_yaml("professionals.yaml"),
        "organizations": load_yaml("organizations.yaml"),
        "about":         load_yaml("about.yaml"),
    }

    # Jinja2 env — loader points at src/ so {% extends %} paths work as written
    env = Environment(
        loader=FileSystemLoader(SRC),
        autoescape=False,
        trim_blocks=True,
        lstrip_blocks=True,
    )

    # render pages
    for src_template, out_name in PAGES:
        tmpl = env.get_template(src_template)
        html = tmpl.render(**ctx)
        out_path = os.path.join(OUT, out_name)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  ✓  {out_name}")

    # copy static assets
    assets_src = os.path.join(SRC, "assets")
    assets_dst = os.path.join(OUT, "assets")
    if os.path.exists(assets_src):
        shutil.copytree(assets_src, assets_dst)
        print("  ✓  assets/")

    # copy admin (Decap CMS)
    admin_src = os.path.join(SRC, "admin")
    admin_dst = os.path.join(OUT, "admin")
    if os.path.exists(admin_src):
        shutil.copytree(admin_src, admin_dst)
        print("  ✓  admin/")

    print(f"\nBuild complete → {OUT}")

if __name__ == "__main__":
    build()
