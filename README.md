
# PEP440 Versioning Helper

The `pep440` Python package provides utilities to help manage versioning of projects based on the [PEP 440](https://peps.python.org/pep-0440/) versioning scheme.

## Features

- Parses and validates versions based on PEP 440.
- Determines the next version based on the current version and desired release type.

## Installation

To install `pep440`, simply use [Poetry](https://python-poetry.org/):

```bash
poetry add pep440
```

Alternatively, you can install it from PyPI using `pip`:

```bash
pip install pep440
```

## Usage

Here's a simple usage example:

```python
from pep440 import get_next_pep440_version

current_version = "0.1.0.dev1"
release_type = "a"
next_version = get_next_pep440_version(current_version, release_type)
print(next_version)  # Expected: 0.1.0a1
```

## Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pep440.git
```

2. Navigate to the project directory and install dependencies:
```bash
cd pep440
poetry install
```

3. Run tests (after you've added them):
```bash
poetry run pytest
```

## Contribution

Contributions are welcome! Please submit pull requests or open issues to discuss potential changes or additions.

## License

[MIT](https://choosealicense.com/licenses/mit/)
