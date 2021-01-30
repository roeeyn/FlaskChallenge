import requests
import sqlite3
from sqlite3 import Error, Connection
from typing import Union


def create_connection(db_file: str) -> Union[Connection, None]:
    """create a database connection to a SQLite database
    :param db_file: The name of the DB file
    :return: The connection to the DB
    """

    try:
        return sqlite3.connect(db_file)

    except Error as e:
        print(e)


def create_table(conn: Connection, create_table_sql: str) -> None:
    """create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)

    except Error as e:
        print(e)


def get_github_users(total=150) -> list[dict[str, str]]:
    """get github users from the GitHub API
    :param total: number of users we want in our DB
    :return: The list of GitHub users fetched from the API
    """
    headers = {"Accept": "application/vnd.github.v3+json"}
    remainder = total
    last_user_id = 0
    users = []

    while remainder > 0:
        max_elements = 100  # max elements per page in the API is 100
        print("Remaining:", remainder)
        if remainder >= max_elements:
            response = requests.get(
                f"https://api.github.com/users?per_page={max_elements}&since={last_user_id}",
                headers=headers,
            )
            parsed_response = response.json()
            users += parsed_response
            last_user_id = parsed_response[-1]["id"]
            remainder -= max_elements

        else:
            response = requests.get(
                f"https://api.github.com/users?per_page={remainder}&since={last_user_id}",
                headers=headers,
            )
            users += response.json()
            remainder -= remainder  # This will always be zero, but it's clear that we're updating the remainder
            print("Finished fetching users from API")

    return users


def parse_github_user(github_user: dict[str, str]) -> dict[str, str]:
    """parse API user
    Rename the keys so it would be easier for the db to insert the registry
    :param github_user: the original API user that was fetched
    :return: The parsed GitHub user
    """

    return {
        "username": github_user["login"],
        "id": github_user["id"],
        "img_url": github_user["avatar_url"],
        "type": github_user["type"],
        "profile_url": github_user["html_url"],
    }


def insert_github_user(conn: Connection, github_user: dict[str, str]) -> None:
    user_tuple = (
        github_user["id"],
        github_user["username"],
        github_user["img_url"],
        github_user["type"],
        github_user["profile_url"],
    )

    sql_statement = """ INSERT INTO github_users(id, username, img_url, type, profile_url)
              VALUES(?,?,?,?,?) """

    cur = conn.cursor()
    cur.execute(sql_statement, user_tuple)
    conn.commit()


def main(total=150):
    database = "github_users.db"

    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS github_users (
                                        id integer PRIMARY KEY,
                                        username text NOT NULL,
                                        img_url text NOT NULL,
                                        type text NOT NULL,
                                        profile_url text NOT NULL
                                    ); """

    # create a database connection
    conn = create_connection(database)

    if conn is None:
        print("An error occured while connecting to the DB")
        return

    with conn:
        # create github users table
        create_table(conn, sql_create_projects_table)

        raw_users = get_github_users(total)
        parsed_users = [parse_github_user(user) for user in raw_users]

        for user in parsed_users:
            insert_github_user(conn, user)

        print("Finished adding users to DB")


if __name__ == "__main__":
    main()
