# Python Test

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

### Optional

- Add an endpoint where you return a JSON with the information stored in the database. The user will be able to use query params to filter the results. At least there should be for username and id but for type, pagination size, order by and GitHub profile is a plus. Example:

`<your_endpoint>/profiles?username=test1&pagination=20&order_by=id`

- Deploy your app to a Heroku server or any other free option and include the link in the email
- Include as many optimizations as you can (e.g cache)

*Note: Things like code style, documentation, architecture are really important. Develop this app assuming production quality code*
