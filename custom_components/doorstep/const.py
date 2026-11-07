"""Constants for the doorstep integration."""

from datetime import timedelta

DOMAIN = "doorstep"

# doorstep reads its records from local disk on every request, so asking
# often is cheap. Its own carrier polling runs on a much longer interval.
UPDATE_INTERVAL = timedelta(minutes=5)
