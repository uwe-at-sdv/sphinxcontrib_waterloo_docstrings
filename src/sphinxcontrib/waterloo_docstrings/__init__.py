from importlib.metadata import PackageNotFoundError, version

try:
	__version__ = version("sphinxcontrib-waterloo-docstrings")
except PackageNotFoundError:
	__version__ = "0.0.0"


def setup(app):
	# Lazy import because sphinx is marked as optional dependency
	# in pyproject.toml. The user should actively install sphinx.
	from .extension import setup as extension_setup

	return extension_setup(app)


__all__ = ["__version__", "setup"]
