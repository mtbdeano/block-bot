# block-bot
A small discord bot that allows you to check on a minecraft server running on Google cloud, and start and stop it as neccessary.

`DISCORD_TOKEN` is your ... wait for it ... discord token

`MINECRAFT_URI` is an environment variable that is either `hostname:port` or a json blog with this structure:

```json
[
    {
        "server": "somehost.somewhere.net",
        "port": 12345,
        "name": "somehost"
    },
    {
        "server": "8.7.6.4",
        "port": 25565,
        "name": "googles minecraft hub"
    }
]
```
