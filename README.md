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

Tasks:
- [x] Create the seeding script
- [x] Consume the GitHub API
- [x] Customize number of saved users

#### Libraries

I created the required script named `seed.py` with its own requirements file, called `seed_requirements.txt`. In this seeding file I tried to use as least libraries as possible to avoid installing no needed stuff.

To install the required libraries just execute:

```bash
pip install -r seed_requirements.txt
```

#### Process

For this process you can customize the number of users inside the script. It is the parameter of the `main` function.

##### 1. Create Connection

Inside the function `create_connection` I create a useful connection to the DB, which will be used later for inserting the data.

##### 2. Get GitHub Users

Using the GitHub API, I fetch GitHub users with the function `get_github_users` by calculating the pagination and remainder, because the API has a maximum of 100 per page, so if we need more than that I do several requests and then just collect all the data in a single list.

***Caveats***: I know that if we fetch A LOT of users all the memory would be consumed by the users list, so in that case we would need to be processing the users as they arrive (maybe asynchronously with a queue), but for the simplicity of the exercise, I left it as this. Also, I didn't create any unit testing for the seeding script as it exists only for the purpose for the example and probably would not exist in a real world project. For that I would use some other approach such as migrations.

##### 3. Save GitHub Users

With the list created in the previous step, I iterate and for each element, parse it (rename keys and delete the unused ones) and do a insertion to the DB.
At the end I will have my DB file with all the fetched users 😊

### View

> Once you have created the script and has a complete db create a Flask application that has:
>
>- A view to show the info of all the users of the database in a table. Profile avatar should be visible and clicking the username should send me to the GitHub profile. Pagination is needed and by default it should be of size 25. Make sure that the page is responsive even with a large amount of data (use any optimization) *Optional but desired*: arguments to change pagination size and ordering

Tasks:
- [x] View that shows the info of the DB users.
- [x] Pagination for the users with a fixed size of 25
- [x] Customizable page and row size (via URL params)
- [x] Visible profile avatar
- [x] Clicking username takes you to the profile
- [ ] Infinite scrolling for managing LARGE amount of data

I created the view as simple as possible just using some Jinja templates and vanilla JS and CSS. The pagination works with just two buttons, but if you modify the URL you can get a more specific result with any page number or row size.

***Caveats***: The view can be improved with a better UX for the page number and the row size (at the moment it only works if you change manually the URL params), but for the simplicity of the exercise I didn't invest too much time in that. Also, I know the page may be unresponsive with A LOT of info, but implementing manually an infinite scroll approach (the better for very large amounts of data in my opinion) would take a lot of time and it wouldn't match with the simplicity of the exercise. For this view part I didn't create any unit test because in my experience, the unit testing of views does not guarantee much to the developers, it is tedious because of the abundant screen sizes and browser versions, and changes a lot because the view (frontend) is one of the software pieces that changes more because of business constant evolving demands (such as new colors, new look and feel, etc)

### Server

Tasks:

- [x] Flask server
- [x] Unit testing for the important stuff
- [ ] Cache
- [x] Documentation
- [x] Repo in GitHub
- [x] Deploy to Heroku

My flask server only creates a connection to the DB and fetch the users based on the page and the row size.
As it is a common function, it serves well for the view and for the API, the only difference is that one returns a rendered template and the other one returns a JSON.

> Create an script to run your server and a `README.md` file where you explain your decisions and architecture.

To run the script locally you can run:

```bash
# Install dependencies
pip install -r requirements

# Run the server (it will use local env)
flask run
```

or if you prefer, you can build and use the Docker image

```bash
docker build -t flask-challenge .
docker run --rm -p 5000:5000 -e PORT=5000 flask-challenge
```

> Unit tests for all the code is needed

In the case of the server, I consider that the only function that is word testing is the one that fetch the users from the DB with the pagination approach. This is because is the function that use the API and the view.

In the case of the routes itself I believe that testing them will be like testing flask itself, because we don't do anything complex enough to be tested, just call the shared function.

For the unit testing itself I used `pytest` and its hooks. With this each time the tests run, a mock DB will be created and at the end of the tests it will be destroyed. It is important that **before running the tests we need to set `ENV` to `test`** (or something different than `local` or `prod`). If we do not do this, we will be testing with the seeded DB.

For running the tests we need to execute:

```bash
# Make sure we won't be using seeded DB
export ENV=test
pytest
```

> After completion of the tasks create a public repository and put all the code there. Be sure to not include compiled files and the db.

You are seeing it 😆 

> Optional
>
> - Add an endpoint where you return a JSON with the information stored in the database. The user will be able to use query params to filter the results. At least there should be for username and id but for type, pagination size, order by and GitHub profile is a plus. Example:
> 
> `<your_endpoint>/profiles?username=test1&pagination=20&order_by=id`

I achieved this by creating the route `/api/profiles?rows=25&page=4`, which will return the same info, but in JSON format. The only params you can modify are rows and page.

> - Deploy your app to a Heroku server or any other free option and include the link in the email
👉🏼 https://roeeyn-flask-tutorial.herokuapp.com/profiles

> - Include as many optimizations as you can (e.g cache)
For the simplicity of the exercise, I did not include a external cache as it would need an extra server, or even cluster (Redis is the best in my opinion). This would optimize for sure the response time as our system is *read heavy* and zero writing. I did not consider using internal cache such as memoizing as I feel it as "cheating" as the DB will never change (it's seeded with the GitHub API) and in that case it would be better to just initialize a dict from a file instead of using the DB itself but that would break the exercise.
