# Flask Demo Project

This is my solution to the following scenario.

## Initial Instructions

Using the [API of GitHub](https://docs.github.com/en/free-pro-team@latest/rest/reference) do the following tasks:

- Create a script called `[seed.py](http://seed.py)` that populates a SQLite database. By default it should search for the first 150 users from GitHub but the script should accept a param called `total` to customize the number of users.
- The fields required for this users are:
    - username
    - id
    - image url
    - type
    - link to his GitHub profile

Once you have created the script and has a complete db create a Flask application that has:

- A view to show the info of all the users of the database in a table. Profile avatar should be visible and clicking the username should send me to the GitHub profile. Pagination is needed and by default it should be of size 25. Make sure that the page is responsive even with a large amount of data (use any optimization) *Optional but desired*: arguments to change pagination size and ordering

Create an script to run your server and a `README.md` file where you explain your decisions and architecture.

**Unit tests for all the code is needed.**

After completion of the tasks create a public repository and put all the code there. Be sure to not include compiled files and the db.

**Optional**

- Add an endpoint where you return a JSON with the information stored in the database. The user will be able to use query params to filter the results. At least there should be for username and id but for type, pagination size, order by and GitHub profile is a plus. Example:

`<your_endpoint>/profiles?username=test1&pagination=20&order_by=id`

- Deploy your app to a Heroku server or any other free option and include the link in the email
- Include as many optimizations as you can (e.g cache)

*Note: Things like code style, documentation, architecture are really important. Develop this app assuming production quality code*

## My Solution

### Seeding

> Using the [API of GitHub](https://docs.github.com/en/free-pro-team@latest/rest/reference) do the following tasks:
>
> - Create a script called `[seed.py](http://seed.py)` that populates a SQLite database. By default it should search for the first 150 users from GitHub but the script should accept a param called `total` to customize the number of users.
> - The fields required for this users are:
>    - username
>    - id
>    - image url
>    - type
>    - link to his GitHub profile

#### Libraries

I created the required script named `seed.py` with its own requirements file, called `seed_requirements.txt`. In this seeding file I tried to use as least libraries as possible to avoid installing no needed stuff.

To install the required libraries just execute:

```bash
pip install -r seed_requirements.txt
```

#### Process

##### 1. Create Connection

Inside the function `create_connection` I create a useful connection to the DB, which will be used later for inserting the data.

##### 2. Get GitHub Users

Using the GitHub API, I fetch GitHub users with the function `get_github_users` by calculating the pagination and remainder, because the API has a maximum of 100 per page, so if we need more than that I do several requests and then just collect all the data in a single list.

***Caveats***: I know that if we fetch A LOT of users all the memory would be consumed by the users list, so in that case we would need to be processing the users as they arrive (maybe asynchronously with a queue), but for the simplicity of the exercise, I left it as this.

##### 3. Save GitHub Users

With the list created in the previous step, I iterate and for each element, parse it (rename keys and delete the unused ones) and do a insertion to the DB.
At the end I will have my DB file with all the fetched users 😊
