# IPStack_client

A python command line client for IPStack's IP geolocation
API. Returns a json object with latitude and longitude.

Requires a (free from IPStack.com) API key.

Security isn't excellent (the free API is http!) but this
makes it easier for the user to do a sensible thing and
store the API key in a file with restrictive permissions.

With this script the API key doesn't appear in the process
environment or arguments (which can be visible to other
users on the machine).

The key may appear in stderr if an exception is raised.
