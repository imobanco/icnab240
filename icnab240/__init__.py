from .controllers import create_santander_cnab  # noqa
from .core import Field  # noqa

from ._version import get_versions

__version__ = get_versions()["version"]
del get_versions
