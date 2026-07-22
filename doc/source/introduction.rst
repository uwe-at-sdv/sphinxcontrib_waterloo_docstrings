.. _chapter_introduction:

Introduction
============

What This Extension Does
------------------------

This package provides a Sphinx extension for rendering
`Waterloo Docstrings <https://github.com/uwe-at-sdv/sdv_doc_waterloo>`_ as HTML
documentation. It adds directives for inserting Waterloo docstrings into a
Sphinx document and roles for rendering Waterloo's semantic inline markup.

During rendering, the extension resolves Python objects, reads their docstrings,
parses the Waterloo structure, validates the result, and converts the validated
docstring into Docutils nodes. If something goes wrong, the extension can show
diagnostics directly in the generated document and also report them through the
Sphinx build log.


Why Waterloo Docstrings
-----------------------

Waterloo Docstrings define a structured docstring format for Python projects.
The format focuses on machine-verifiable normativity: requirements and
guarantees are not merely written as prose, but anchored in explicitly defined
sections, subsections, and normativity keywords.

This matters when documentation is consumed by both humans and tools. A human
reader should see readable reference documentation. A tool, validator, or LLM
should be able to inspect the same source text and recover enough structure to
reason about contracts, parameters, return values, examples, and cross
references.

The normative Waterloo documentation describes the format in detail and shows
examples of valid docstrings:

`Waterloo Docstrings documentation <https://uwe-at-sdv.github.io/sdv_doc_waterloo/>`_


Design Goals
------------

The extension is designed as a rendering layer for Waterloo Docstrings, not as
a separate documentation format. Its main goals are:

* Render validated Waterloo docstrings into ordinary Sphinx/Docutils nodes.
* Keep semantic markup visible in the HTML output without turning it into
  purely typographic decoration.
* Report resolver, parser, and validator diagnostics close to the source
  directive that triggered them.
* Stay reasonably theme-neutral, so the generated output can follow the visual
  language of the active Sphinx theme.
* Preserve a practical authoring workflow: write Python docstrings, validate
  them with Waterloo validation tools, and render them through Sphinx.

The extension deliberately leaves the normative definition of the docstring
format to the Waterloo documentation. This package focuses on how validated
Waterloo docstrings are embedded into a Sphinx project.


What This Extension Is Not
--------------------------

This extension is not the normative definition of the Waterloo Docstring
format. The rules for valid sections, subsections, indentation, scopes,
normativity keywords, and diagnostics belong to the Waterloo documentation and
the Waterloo validation tools.

The directive names are intentionally close to :wtrl_mod:`sphinx.ext.autodoc`:
both systems resolve Python objects and generate Sphinx documentation from
their docstrings. The difference is that this extension does not interpret
arbitrary Python docstrings. It expects Waterloo docstrings, validates their
structure, and renders their semantic content.

In particular, this package does not try to infer missing documentation from
Python signatures or source code. If a docstring is missing, malformed, or
invalid, the renderer reports that problem instead of silently inventing
documentation.


How It Fits Into Waterloo
-------------------------

This package is one output layer in the broader Waterloo toolchain. The core
Waterloo package defines the docstring model, parses Waterloo text, validates
the structure, and provides diagnostics that can be consumed by humans or
tools.

Other parts of the toolchain focus on different output targets: structured JSON
for machine consumers, interactive HTML for browsing generated documentation,
and MCP access for LLM-assisted workflows. This Sphinx extension focuses on a
different integration point: it embeds validated Waterloo docstrings into a
normal Sphinx project, so they can be combined with hand-written prose,
cross-references, themes, and the rest of the Sphinx ecosystem.


Project Status
--------------

The extension is type-checked regularly with :wtrl_cmd:`mypy`. The checked
source files are:

.. literalinclude:: type_checking_files.txt
	:language: none

The current type-checking status is:

.. literalinclude:: type_checking_report.txt
	:language: none

The :wtrl_lit:`mypy` configuration used for this report is:

.. literalinclude:: ../../mypy.ini
	:language: ini

Known type-checking exceptions are listed here:

.. literalinclude:: type_checking_exceptions.txt
	:language: none


Dependencies
------------

The package depends on :wtrl_pkg:`sdv-doc-waterloo`, which provides the
Waterloo parser, validator, diagnostics, and rendering helpers used by this
extension.

The Sphinx dependency itself is provided as an optional extra in the package
metadata. This keeps the dependency relationship explicit: the extension code
depends on the Waterloo core package, while a project that actually builds
Sphinx documentation also needs Sphinx installed in the build environment.

Installation details are covered in :ref:`Getting Started <chapter_getting_started>`.
