import pytest

from src.pep440 import get_next_pep440_version

# Test cases to validate transitions based on the current version and next desired stage.
# Tuple format: (current_version, desired_next_stage, expected_output)
test_cases = [
    # From dev releases
    ("0.0.1.dev1", "dev", "0.0.1.dev2"),
    ("0.0.1.dev1", "a", "0.0.1.a1"),
    ("0.0.1.dev1", "b", "0.0.1.b1"),
    ("0.0.1.dev1", "rc", "0.0.1.rc1"),
    ("0.0.1.dev1", "final", "0.0.1"),
    ("0.0.1.dev1", "post", "0.0.2.post1"),
    # From alpha, beta, rc releases
    ("0.0.1.a1", "a", "0.0.1.a2"),
    ("0.0.1.a1", "b", "0.0.1.b1"),
    ("0.0.1.b1", "b", "0.0.1.b2"),
    ("0.0.1.b1", "rc", "0.0.1.rc1"),
    ("0.0.1.rc1", "rc", "0.0.1.rc2"),
    ("0.0.1.a1", "final", "0.0.1"),
    ("0.0.1.a1", "dev", "0.0.2.dev1"),
    ("0.0.1.a1", "post", "0.0.2.post1"),
    # From final versions
    ("0.0.1", "dev", "0.0.2.dev1"),
    ("0.0.1", "a", "0.0.2.a1"),
    ("0.0.1", "b", "0.0.2.b1"),
    ("0.0.1", "rc", "0.0.2.rc1"),
    ("0.0.1", "post", "0.0.2.post1"),
    # From post releases
    ("0.0.1.post1", "post", "0.0.1.post2"),
    ("0.0.1.post1", "dev", "0.0.2.dev1"),
    ("0.0.1.post1", "a", "0.0.2.a1"),
    ("0.0.1.post1", "b", "0.0.2.b1"),
    ("0.0.1.post1", "rc", "0.0.2.rc1"),
    ("0.0.1.post1", "final", "0.0.2"),
]

extended_test_cases = [
    ("1.0.0", "a", "1.0.1.a1"),
    ("1.0.0", "b", "1.0.1.b1"),
    ("1.0.0", "rc", "1.0.1.rc1"),
    ("1.0.0", "post", "1.0.1.post1"),
    ("1.0.0", "dev", "1.0.1.dev1"),
    ("1.0.0+local", "a", "1.0.1.a1"),
    ("2!1.0.0", "a", "2!1.0.1.a1"),
    ("1.0.10", "a", "1.0.11.a1"),
    ("1.0.0", "post", "1.0.1.post1"),
    ("2", "a", "2.0.1.a1"),
    ("0.0.1.a1", "dev", "0.0.2.dev1"),
]

test_cases.extend(extended_test_cases)


@pytest.mark.parametrize("current, next_stage, expected", test_cases)
def test_valid_transitions(current, next_stage, expected):
    assert get_next_pep440_version(current, next_stage) == expected


# Test cases for invalid inputs or transitions
invalid_cases = [
    ("0.0.1", "z"),  # 'z' is not a valid release type
    ("0.0.1.1", "a"),  # Improperly formatted version string
    ("0.0.1..a1", "final"),  # Double dots in version string
    ("a.b.c", "final"),  # Non-numeric version segments
    ("0.0.1.devA", "a"),  # Non-numeric dev version
    ("", "final"),  # Empty version string
]


@pytest.mark.parametrize("current, next_stage", invalid_cases)
def test_invalid_transitions(current, next_stage):
    with pytest.raises(ValueError):
        get_next_pep440_version(current, next_stage)
