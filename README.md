# telegram-bot-hyperliquid
Very basic `Telegram` bot to retrieve information from [Hyperliquid](https://hyperliquid.xyz/).

After you obtained your bot key, you can configure it by simply editting the Makefile with your
config options:
| Config            | Description                                                         |
|-------------------|---------------------------------------------------------------------|
| `BOT_TOKEN`       | Your bot API key, provided by `telegram`                            |
| `HL_DEFAULT_VAULT`| The default `Hyperliquid` vault address to retrieve information for |

## Usage
Script provides the following Make targets:
| Target      | Description                             |
|-------------|-----------------------------------------|
| `bootstrap` | Create the environment and get all deps |
| `clean`     | Remove build artifacts                  |
| `deploy`    | Start the bot using the configuration   |

### Environment setup
The following OS dependencies are required:
|   Dependency   |
|----------------|
| git            |
| make           |
| python         |
| python-venv    |

Before first usage, you have to grab all the required python libraries:
```
% make bootstrap
```
### Execution
Since we are using a `python` virtual environment, we have to source
it before starting the bot:
```
% . {FULL_PATH_REPO}/venv/bin/activate
```
After that, you can modify the configuration and start the bot:
```
% make deploy
```
After the bot is up and running, you can verify it's working by
sending it a prompt like `/hl vault`. The bot should respond with
information for your default vault.
