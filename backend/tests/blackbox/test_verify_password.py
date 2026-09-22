from __future__ import annotations

import pytest

from participium.core.security import verify_password

@pytest.mark.parametrize(
    "plain_password, hashed_password, expected_result",
    [
        ("correct_pwd", "correct_hash", True),
        ("wrong_pwd", "correct_hash", False),
        ("", "correct_hash", False),
        ("correct_pwd", "not-an-hash", False),
        ("correct_pwd", "", False),
    ]
)

def test_verify_password(plain_password, hashed_password, expected_result):
    assert verify_password(plain_password, hashed_password) == expected_result