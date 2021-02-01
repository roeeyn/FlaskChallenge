from src.users import get_paginated_users
import pytest


@pytest.mark.parametrize(
    "test_rows,test_page",
    [
        # we have 150 fixed users in the test db
        (25, 1),  # Common execution
        (25, 5),  # Common execution
        (200, 1),  # More rows than db elements, 1st page
        (200, 5),  # More rows than db elements, n page
        (-1, 1),  # Negative rows
        (0, 1),  # Zero row
        (25, -1),  # Negative page
        (25, 0),  # Zero page
    ],
)
def test_users(test_rows, test_page):
    users_in_db = 150  # making a count with each query would degrade performance
    users, rows, page = get_paginated_users(test_rows, test_page)

    # Check length of the result
    if test_rows > users_in_db:
        if page == 1:
            assert len(users) == users_in_db
        else:
            assert len(users) == 0
    else:
        assert len(users) == min(rows, users_in_db)

    # Check page
    assert page == test_page if test_page > 0 else 1

    # Check rows
    assert rows == test_rows if test_rows > 0 else 1

    # Check id integrity
    if len(users) > 0:
        # We check the first and last id to see if they are
        # correct according to the sequence from 1 to users_in_db
        first_user_id = users[0]["id"] - 1
        last_user_id = users[-1]["id"]

        assert first_user_id == (page - 1) * rows
        assert last_user_id == ((page - 1) * rows) + min(users_in_db, rows)
