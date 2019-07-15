# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2016-2019 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Jupyter Notebook previewer."""

from __future__ import absolute_import, unicode_literals

import nbformat
from flask import render_template
from nbconvert import HTMLExporter

from ..utils import sanitize_html


def render(file):
    """Generate the result HTML."""
    with file.open() as fp:
        content = fp.read()

    notebook = nbformat.reads(content.decode('utf-8'), as_version=4)

    # Note, we are not using the nbconvert provided HTML sanitizer
    # (nbconvert.preprocessors.sanitize.SanitizeHTML), as it does not catch
    # some special cases of XSS attacks (see example application for examples).
    html_exporter = HTMLExporter()
    html_exporter.template_file = 'basic'
    (body, resources) = html_exporter.from_notebook_node(notebook)
    return sanitize_html(body), resources


def can_preview(file):
    """Determine if file can be previewed."""
    return file.is_local() and file.has_extensions('.ipynb')


def preview(file):
    """Render the IPython Notebook."""
    body, resources = render(file)
    default_jupyter_nb_style = resources['inlining']['css'][1]
    return render_template(
        'invenio_previewer/ipynb.html',
        file=file,
        content=body,
        inline_style=default_jupyter_nb_style
    )
