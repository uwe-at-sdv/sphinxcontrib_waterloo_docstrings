# Unified makefile for the Sphinx theme test projects.

SPHINXOPTS  ?=
SPHINXBUILD ?= sphinx-build
O           ?=

THEMES = alabaster classic furo

.PHONY: help themes $(foreach theme,$(THEMES),html-$(theme) clean-$(theme) help-$(theme))

help:
	@printf '%s\n' \
		'Theme targets:' \
		'  make html-alabaster   make clean-alabaster' \
		'  make html-classic     make clean-classic' \
		'  make html-furo        make clean-furo' \
		'' \
		'Use SPHINXOPTS=... or O=... to pass options to sphinx-build.'

themes: $(foreach theme,$(THEMES),html-$(theme))

define THEME_TARGETS
html-$(1):
	@$$(SPHINXBUILD) -M html "source-$(1)" "build-$(1)" $$(SPHINXOPTS) $$(O)

clean-$(1):
	@$$(SPHINXBUILD) -M clean "source-$(1)" "build-$(1)" $$(SPHINXOPTS) $$(O)

help-$(1):
	@$$(SPHINXBUILD) -M help "source-$(1)" "build-$(1)" $$(SPHINXOPTS) $$(O)
endef

$(foreach theme,$(THEMES),$(eval $(call THEME_TARGETS,$(theme))))
