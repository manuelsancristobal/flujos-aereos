"""Copia archivos al repo Jekyll local: datos, HTML, CSS y JS para ArcLayer."""

import logging
import shutil
from src.config import (
    PROCESSED_DATA_DIR,
    JEKYLL_DATA_DIR,
    JEKYLL_CSS_DIR,
    JEKYLL_JS_DIR,
    JEKYLL_PAGE,
    JEKYLL_PROJECT_MD,
    JEKYLL_PROJECTS_DIR,
    JEKYLL_REPO,
    VIZ_DIR,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

def deploy():
    """Copia archivos al repo Jekyll. El push es manual."""
    if not JEKYLL_REPO.exists():
        logger.error(f"Repositorio Jekyll no encontrado en: {JEKYLL_REPO}")
        return

    # 1. JSONs de datos
    if PROCESSED_DATA_DIR.exists():
        JEKYLL_DATA_DIR.mkdir(parents=True, exist_ok=True)
        count = 0
        for f in PROCESSED_DATA_DIR.glob("*.json"):
            shutil.copy2(f, JEKYLL_DATA_DIR / f.name)
            count += 1
        logger.info(f"Copiados {count} archivos de datos → {JEKYLL_DATA_DIR}")

    # 2. CSS
    css_src = VIZ_DIR / "assets" / "css" / "style.css"
    if css_src.exists():
        JEKYLL_CSS_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copy2(css_src, JEKYLL_CSS_DIR / css_src.name)
        logger.info(f"Copiado CSS → {JEKYLL_CSS_DIR}")

    # 3. JS
    js_src = VIZ_DIR / "assets" / "js" / "map.js"
    if js_src.exists():
        JEKYLL_JS_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copy2(js_src, JEKYLL_JS_DIR / js_src.name)
        logger.info(f"Copiado JS → {JEKYLL_JS_DIR}")

    # 4. HTML (index.html) -> viz.html en el repo
    html_src = VIZ_DIR / "index.html"
    if html_src.exists():
        JEKYLL_PAGE.parent.mkdir(parents=True, exist_ok=True)
        # IMPORTANTE: En el HTML copiado, las rutas de assets deben ser relativas al nuevo destino
        # Si JEKYLL_PAGE es /proyectos/arclayer/viz.html, 
        # y assets están en /proyectos/arclayer/assets/js/map.js
        # Las rutas en el HTML (assets/js/map.js) ya son relativas y funcionan si se mantiene la estructura.
        shutil.copy2(html_src, JEKYLL_PAGE)
        logger.info(f"Copiado index.html → {JEKYLL_PAGE}")

    # 5. Markdown del proyecto
    if JEKYLL_PROJECT_MD.exists():
        JEKYLL_PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copy2(JEKYLL_PROJECT_MD, JEKYLL_PROJECTS_DIR / JEKYLL_PROJECT_MD.name)
        logger.info(f"Sincronizado proyecto .md → {JEKYLL_PROJECTS_DIR}")

    logger.info("Deploy completado localmente. Recuerda hacer git push en el repo de tu portafolio.")

if __name__ == "__main__":
    deploy()
