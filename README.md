# Usage AI - Tech Interview

Hey!

We've listed four challenges. Get as far as you can in 1.5 hours. No worries if you don't finish.

Feel free to use Google, Stack Overflow, or whatever else you like. We only ask that you not ask friends for help!

We'll be looking at how much progress you make, as well your style of coding. We'll pay especially close attention to code quality in Challenge 4.

We won't be evaluating your submission programmatically. If you find the instructions unclear, go with your gut! If you get stuck, shoot us a message. We're here to help!

## Getting started

Use Python 3.7+.

Install the dependencies in requirements.txt:

```
pip install -r requirements.txt
```

Run the Streamlit app:

```
streamlit run dashboard.py
```

Streamlit will tell you where to find your live app, likely at `localhost:8501`. You can open this address in your browser. You should see an error on the webpage. We'll fix this in Challenge 2.

## Submitting

Make a pull request from your forked repo to [sean-hackett/usageai-tech-interview](https://github.com/sean-hackett/usageai-tech-interview). Please resolve any merge conflicts in your own branch should any arise.

## Challenges

First, we'll build an application analyze holidays. We'll use the Hello, Salut! API to welcome users to the app. We'll use the Nager.Date API to find info about public holidays from around the world.

Next, we'll build an application to which users will can log-in and view their own personal data.

We'll use Streamlit to render our applications and handle interactivity. You can see the Streamlit documentation [here](https://docs.streamlit.io/en/stable/api.html). Streamlit has a menu of interactive components, like dropdown menus and buttons, and data visualization tools, like line and bar charts.

Be sure to update the `requirements.txt` throughout the interview, as appropriate.

Good luck!

#### Challenge 1

Let's give this application some flair.

Every time the app loads, show a new salutation.

Randomly generate an IP address. Use the Hello, Salut! API to find the salutation corresponding with that IP address's geographic location. Show that salutation at the top of the dashboard, replacing the text 'Have fun!'

You can find documentation for the Hello, Salut! API [here](https://fourtonfish.com/project/hellosalut-api/).

#### Challenge 2

We already got started by making a request to the Nager.Date API's `AvailableCountries` endpoint.

Notice that the `load_country_codes` function does not return a list of country codes. Fix the `load_country_codes` function so that it returns the list of country codes provided by the Nager.Date API.

You can find documentation for the Nager.Date API [here](https://date.nager.at/swagger/index.html).

#### Challenge 3

Holiday time! When the user selects a country code from the dropdown, display a line chart showing the number of holidays in that country, by year, for the last decade.

Use a Numpy array to store the number of holidays per year.

#### Challenge 4

Enough salutations and holidays. Let's create a new Streamlit app.

Create `person_dashboard.py`.

Use the RandomUser API, available [here](https://randomuser.me/).

Use "usageai" as the seed when interacting with the RandomUser API.

Download the first 100 users from the API. Do not store the user's plaintext password. Store the user's hashed password, with the hashing algorithm of your choosing, and the user's salt.

Add a log-in form to the dashboard. If the user enters the correct email and password to the log-in form, show the corresponding user's first name, last name, and date of birth.

Be sure to store the user data in an object-oriented fashion. You can ignore any key/value fields provided by the RandomUser API which are not of use to this challenge.

Use Streamlit's caching to improve your app's performance.

If you make it this far, try improving the cache so that the cache persists across runs of the Streamlit app. Do not use the `persist` argument on the `st.cache` function. Roll your own solution. Hint, hint - write to disk.

## Questions?

Email sean@usage.ai.

## Solution

Completed all four parts of the challenge.
Tested successfully.

Added mongodb backend to save the users on disk, so API call performed only once.
Cached the API call so successive calls are much faster.

execute "docker-compose -f compose.yaml up -d" to bring up the entire stack and access the app at "http://localhost:8501/" and see the db records at "http://localhost:8081/"

#NOTE: Replace "localhost" by VM IP "192.168.99.100" if using docker on a VM.
