from __future__ import annotations

import argparse
from pathlib import Path

from ._version import version as __version__
from .vendor import vendorize

__all__ = ["main"]


def __dir__() -> list[str]:
    return __all__


def main() -> None:
    """
    Entry point.
    """
    parser = argparse.ArgumentParser(description="CMake F2Py module helper")
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    subparser = parser.add_subparsers(required=True)
    vendor_parser = subparser.add_parser("vendor", help="Vendor CMake helpers")
    vendor_parser.add_argument(
        "target", type=Path, help="Directory to vendor the CMake helpers"
    )
    args = parser.parse_args()
    vendorize(args.target)


if __name__ == "__main__":
    main()
