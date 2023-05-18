#! /bin/sh
# Pip freeze the installed packages into constraints.txt.
# Note that pip/setuptools/wheel are excluded by pip unless we call it with --all.
# We are happy to follow pip's lead here.
# We also exclude zc.buildout and our dummy plonecoredev package.
# And we exclude editable packages.
bin/pip freeze --exclude-editable --exclude plonecoredev --exclude zc.buildout > constraints.txt
