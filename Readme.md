# GetNotifyEarly

Tired of digging through different leagues to find out what's on tonight?

Every morning, your phone just tells you.

## How it works

A script wakes up on GitHub's servers, asks what's being played today across
the Premier League, La Liga, Serie A, Bundesliga, Ligue 1, and the Champions
League, and sends it to your phone.

One notification. Tap it, see the full list, grouped by league, in your
timezone.

That's it.

## Setup

```bash
pip install -r requirements.txt
```

Two environment variables:

```
FOOTBALL_DATA_KEY   # free key from football-data.org
NTFY_TOPIC          # subscribe to it in the ntfy app
```

```bash
python fixtures.py
```

## Built with

football-data.org for fixtures · ntfy.sh for push notifications · GitHub
Actions for scheduling.