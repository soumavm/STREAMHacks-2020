# STREAMHacks-2020

A Google API key is required for the Python server.
To add an API key, write a file named `.env` in the same directory as the `server.py` file with the following line:

```APIKEY={KEY}```

Replace `{KEY}` with your API key.

Online web app with a python server used to promote environmentally feasible modes of transportation.
Features include - A bootstrap frontend with underlying JS elements (such as point counters, quests, and leaderboards)
                 - A python server which automatically updates a global leaderboard
                 - A google firebase backend which syncs personal points to unique user accounts
                 - A google maps API & distance calculator which determines time required to walk, bike when prompted with a location (ex. park)
