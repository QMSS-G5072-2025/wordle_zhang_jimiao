import os
import sys
sys.path.insert(0, os.path.abspath("C:/Users/Jimiao Zhang/QMSS5072_package/wordle_jz4007/src"))

project = "Wordle jz4007"
author = "Jimiao Zhang"
release = "0.1.0"

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "furo"

