# investor_advisor
This project mimics the functionality of [investing.com](investing.com)'s technical indicators. It calculates the value of each indicator and interprets whether the indicator is in a "buy" or "sell" state. If all indicators are in a "buy" state, and the `trend.txt` file (which tracks the latest **strong** trend) is in a "sell" state - the program will write "buy" to the `trend.txt` file and use a discord webhook to send a message indicating that the trend has changed. The same is true in the opposite case.
## Dependencies
* [Docker](https://docs.docker.com/engine/install/)
* cron
## Usage
1. Rename `myBot.py.example` to `myBot.py`
2. Create a discord webhook and assign it to the url variable
If you want to run the program manually, Enter the following command:\
`docker compose up -d`\
To schedule it, run the `schedule.sh` script with the following command:\
`chmod +x schedule.sh && ./schedule.sh`
## Missing
Technical indicators not implimented:
* Bull/Bear Power(13)
* ADX(14)
* Highs/Lows(14)
