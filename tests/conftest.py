import os
import pytest
from factories.UserFactory import UserFactory
from src.db import session


@pytest.hookimpl
def pytest_sessionstart():
    mock_users = 150  # Fixing the DB to 150 mock users
    users = UserFactory.build_batch(mock_users)
    for user in users:
        session.add(user)
        print(user)

    session.commit()
    print("Test DB initialized")


@pytest.hookimpl
def pytest_sessionfinish():
    # As we're using sqlite, for this very specific example
    # it's easier to drop all the DB at the end of the tests
    test_file = "github_users_test.db"

    if os.path.exists(test_file):
        os.remove(test_file)
        print("\nDeleted Test DB")
