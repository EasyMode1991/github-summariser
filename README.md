This takes a github URL and records data about it, I originally wrote this
to keep track of what is going on in the repositories of various cryptocurrency
projects as i felt that an important factor in the success of any open source project
is the activity on it's github repositories.

for more info on how to use this please refer to github's documentation
<a href="https://developer.github.com/v3/">here</a>

There are also some features in the summariser that don't use the API,
but instead uses BeautifulSoup to find some numbers from the page and
put them into a dict.


How to use -

1. Clone the repo
1. install the requirements (pip intall -r requirements.txt)
1. enter your access token (which you can get
  <a href = "https://developer.github.com/v3/#authentication">here</a>)
1. You can see an example use in src/example.py
