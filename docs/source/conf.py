"""
Configuration file for the Sphinx documentation builder.

For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

# pylint: disable=invalid-name

import datetime
import os
import re
import sys

import requests
import tomli

# list all packages
packages = [
    "agent0",
    "chainsync",
    "elfpy",
    "ethpy",
    "pyperdrive",
    "traiderdaive",
]

# indicate where the elfpy Python package lives
package_root = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
sys.path.insert(0, os.path.abspath("."))
for package in packages:
    package_path = os.path.join(
        package_root,
        "lib",
        package,
    )
    sys.path.insert(0, package_path)


# -- Auto notebook index creation --------------------------------------------

example_root_url = "https://delvtech.github.io/elf-simulations-examples/"
rst_outdir = "examples/notebook/"

index_response = requests.get(example_root_url, timeout=5)
# Find all strings in quotes ending in _notebook.html, which should result in all notebook htmls
html_files = re.findall(r"\".*_notebook\.html?\"", index_response.content.decode("utf-8"))

# Remove first and last quotes from strings
html_files = [file[1:-1] for file in html_files]

# Download files to _static
for html_file in html_files:
    notebook_url = example_root_url + html_file
    raw_html = requests.get(notebook_url, timeout=5).content.decode("utf-8")
    out_html_file = "_static/" + html_file
    with open(out_html_file, "w", encoding="UTF-8") as file:
        file.write(raw_html)

if not os.path.exists(rst_outdir):
    os.makedirs(rst_outdir)

# Static page text, needs title at front and path at end
middle_text = """
=================================================

.. raw:: html
    :file: """

# Create an rst file per notebook output
for html_file in html_files:
    raw_name = html_file.split(".")[0]
    title_name = raw_name.replace("_", " ").title()

    with open(rst_outdir + raw_name + ".rst", "w", encoding="UTF-8") as file:
        file.write(title_name + middle_text + "../../_static/" + html_file + "\n")

index_rst_text = """Examples
=================================================

.. toctree::
   :titlesonly:

"""

# Create outer index.rst for examples
for html_file in html_files:
    raw_name = html_file.split(".")[0]
    index_rst_text += "   /" + rst_outdir + raw_name + "\n"

with open("examples/index.rst", "w", encoding="UTF-8") as file:
    file.write(index_rst_text)


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
def _get_project_meta():
    with open(os.path.join(package_root, "pyproject.toml"), mode="rb") as pyproject:
        return tomli.load(pyproject)["project"]


# General information about the project.
pkg_meta = _get_project_meta()
project = str(pkg_meta["name"])
author = ", ".join([person["name"] for person in pkg_meta["authors"]])
organization = "Delv"
copyright = f" {datetime.date.today().year}, {organization}"  # pylint: disable=redefined-builtin

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
# The short X.Y version.
version = str(pkg_meta["version"])
# The full version, including alpha/beta/rc tags.
release = version
github_url = "https://github.com"
github_repo_org = "delvtech"
github_repo_name = "elf-simulations"
github_repo_slug = f"{github_repo_org}/{github_repo_name}"
github_repo_url = f"{github_url}/{github_repo_slug}"
extlinks = {
    "issue": (f"{github_repo_url}/issues/%s", "#%s"),
    "pr": (f"{github_repo_url}/pull/%s", "PR #%s"),
    "commit": (f"{github_repo_url}/commit/%s", "%s"),
}

# The master toctree document.
master_doc = "index"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.napoleon",  # enables Sphinx to understand docstrings in Google format
    "numpydoc",  # enables NumPy docstring format
    "nbsphinx",  # to showcase Jupyter notebooks
    "myst_parser",  # include .md files
    "sphinx.ext.duration",  # gives reading length summaries at build time
    "sphinx.ext.todo",  # support for todo items
    "sphinx.ext.doctest",  # allows one to test code snippets against the python code to ensure synchrony
    "sphinx.ext.autodoc",  # allows rendering of docs automatically from the python code
    "sphinx.ext.autosummary",  # generates documents that contain all the necessary autodoc directives
    "sphinx_autodoc_typehints",  # insert typehints into the final docs
    "sphinx.ext.autosectionlabel",  # allow reference sections using its title
    "autodocsumm",  # display a list of all class methods in table format
    "autoapi.extension",  # auto generates API reference by recursion
    "sphinx.ext.coverage",  # collect documentation coverage stats
]
mathjax3_config = {"chtml": {"displayAlign": "left"}}
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for API document generation -------------------------------------------------
lib_dir = os.path.join("..", "..", "lib")
autoapi_dirs = [os.path.join(lib_dir, package) for package in packages]
autoapi_type = "python"
autoapi_template_dir = os.path.join("_templates", "autoapi")
autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "imported-members",
]
autoapi_keep_files = True
autoapi_add_toctree_entry = True

autodoc_typehints = "signature"
autodoc_member_order = "bysource"
autosectionlabel_prefix_document = True  # Make sure the label target is unique
autoclass_content = "class"

set_type_checking_flag = True
numpydoc_show_class_members = False
always_document_param_types = True
typehints_fully_qualified = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_style = "css/custom.css"
html_theme_options = {"logo_only": True, "display_version": True}
html_short_title = "Documentation"
html_logo = "_static/logo.svg"
html_favicon = "_static/favicon.ico"
html_title = f"{project} v{release} documentation"

language = "en"
today_fmt = "%B %d, %Y"
todo_include_todos = False
