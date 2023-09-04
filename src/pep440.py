# Path: scripts/pep440.py
# Author: Azat Bilge (azataiot)

"""
pep440.py
~~~~~~~~~~~

This module provides utility functions to handle PEP 440 compliant version strings.
The main functionality revolves around transitioning from one version to the next
based on specified release types.

Usage:
    from pep440 import get_next_pep440_version

    new_version = get_next_pep440_version("0.0.1.dev1", "a")
    print(new_version)  # Outputs: 0.0.1.a1
"""

import re

# Regex pattern that describes the structure of PEP 440 compliant version strings.
# It's used to parse the current version string to determine its components.
_version_pattern = r"""
            v?
            (?:
                (?:(?P<epoch>[0-9]+)!)?                           # epoch
                (?P<release>[0-9]+(?:\.[0-9]+)*)                  # release segment
                (?P<pre>                                          # pre-release
                    [-_\.]?
                    (?P<pre_l>(a|b|c|rc|alpha|beta|pre|preview))
                    [-_\.]?
                    (?P<pre_n>[0-9]+)?
                )?
                (?P<post>                                         # post release
                    (?:-(?P<post_n1>[0-9]+))
                    |
                    (?:
                        [-_\.]?
                        (?P<post_l>post|rev|r)
                        [-_\.]?
                        (?P<post_n2>[0-9]+)?
                    )
                )?
                (?P<dev>                                          # dev release
                    [-_\.]?
                    (?P<dev_l>dev)
                    [-_\.]?
                    (?P<dev_n>[0-9]+)?
                )?
            )
            (?:\+(?P<local>[a-z0-9]+(?:[-_\.][a-z0-9]+)*))?       # local version
        """

# Precompiled regex pattern for efficiency in repeated parsing.
_regex = re.compile(
    r"^\s*" + _version_pattern + r"\s*$",
    re.VERBOSE | re.IGNORECASE,
)

VALID_RELEASE_TYPES = {"a", "b", "rc", "final", "dev", "post"}


def get_next_pep440_version(current_version: str, release_type: str) -> str:
    """
    Calculate the next version string based on the current version and desired release type.

    Args:
        current_version (str): The current version string, e.g., "0.0.1.dev1"
        release_type (str): The desired release type to transition to, e.g., "a", "b", "rc", "final", etc.

    Returns:
        str: The next version string based on the transition logic.

    Raises:
        ValueError: If the current version format is invalid or an invalid transition is attempted.
    """

    if release_type not in VALID_RELEASE_TYPES:
        raise ValueError(f"Invalid release type: {release_type}")

    # Parse the current version
    match = _regex.match(current_version)
    if not match:
        raise ValueError(f"Invalid current version format for {current_version}")

    components = match.groupdict()
    release_segments = components["release"].split(".")

    # Check for improperly formatted version string
    if (
        any(not segment.isdigit() for segment in release_segments)
        or len(release_segments) > 3
    ):
        raise ValueError(f"Invalid release segment format for {current_version}")

    while len(release_segments) < 3:
        release_segments.append("0")

    major, minor, *remaining = map(int, release_segments)
    patch = remaining[0] if remaining else 0
    epoch = components["epoch"]

    pre_l = components["pre_l"]
    pre_n = components["pre_n"]
    post_l = components["post_l"]
    post_n = components["post_n1"] or components["post_n2"]
    dev_l = components["dev_l"]
    dev_n = components["dev_n"]

    # Epoch prefix
    epoch_prefix = f"{epoch}!" if epoch else ""

    # From dev
    if dev_l:
        if release_type == "dev":
            return f"{epoch_prefix}{major}.{minor}.{patch}.dev{int(dev_n) + 1}"
        elif release_type in ["a", "b", "rc"]:
            return f"{epoch_prefix}{major}.{minor}.{patch}.{release_type}1"
        elif release_type == "final":
            return f"{epoch_prefix}{major}.{minor}.{patch}"
        elif release_type == "post":
            return f"{epoch_prefix}{major}.{minor}.{patch + 1}.post1"

    # From alpha, beta, rc
    elif pre_l:
        if release_type in ["a", "b", "rc"]:
            if release_type == pre_l:
                return f"{epoch_prefix}{major}.{minor}.{patch}.{release_type}{int(pre_n) + 1}"  # noqa: E501
            else:
                return f"{epoch_prefix}{major}.{minor}.{patch}.{release_type}1"
        elif release_type == "final":
            return f"{epoch_prefix}{major}.{minor}.{patch}"
        elif release_type == "dev":
            return f"{epoch_prefix}{major}.{minor}.{patch + 1}.dev1"
        elif release_type == "post":
            return f"{epoch_prefix}{major}.{minor}.{patch + 1}.post1"

    # From final version
    elif not pre_l and not post_l and not dev_l:
        if release_type == "a":
            return f"{epoch_prefix}{major}.{minor}.{patch + 1}.a1"
        elif release_type == "dev":
            return f"{epoch_prefix}{major}.{minor}.{patch + 1}.dev1"
        elif release_type == "post":
            return f"{epoch_prefix}{major}.{minor}.{patch + 1}.post1"
        elif release_type in ["b", "rc"]:
            return f"{epoch_prefix}{major}.{minor}.{patch + 1}.{release_type}1"

    # From post-release
    elif post_l:
        if release_type == "post":
            return f"{epoch_prefix}{major}.{minor}.{patch}.post{int(post_n) + 1}"
        elif release_type == "final":
            return f"{epoch_prefix}{major}.{minor}.{patch + 1}"
        elif release_type in ["dev", "a", "b", "rc"]:
            return f"{epoch_prefix}{major}.{minor}.{patch + 1}.{release_type}1"

    raise ValueError(f"Invalid transition from {current_version} to {release_type}")
