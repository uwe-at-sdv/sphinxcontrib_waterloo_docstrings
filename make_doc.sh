#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

pushd doc
make clean && make html

mkdir -p doc-json
waterlint render-json --out-dir doc-json/ --out-prefix wtrl-sphinx-no-examples --flavour rfc-2119 --basedir ../src --obj sphinxcontrib.waterloo_docstrings.extension --include-qid-prefix sphinxcontrib.waterloo_docstrings

waterlint add-example-json --in doc-json/wtrl-sphinx-no-examples.wtrl.core.rfc-2119.json --examples doc-json/examples.json --out doc-json/wtrl-sphinx.wtrl.core.rfc-2119.json

mkdir -p doc-html5
waterlint render-html5 --in doc-json/wtrl-sphinx.wtrl.core.rfc-2119.json --header-html doc-html5/wtrl-sphinx-header.html --additional-css doc-html5/css/wtrl-sphinx-header.css --out doc-html5/wtrl-sphinx.wtrl.core.rfc-2119.html
popd
