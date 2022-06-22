# import finnhub
from celery import Celery
from sqlalchemy import text
from app.db import engine
from app.settings import settings
from binance import Client


# configure the Binance client and Celery to use the Redis broker defined in the application settings
client = Client(api_key=settings.api_key, api_secret=settings.api_secret)
celery_app = Celery(broker=settings.celery_broker)


# worker is started from the root of the project, command line:
# python -m celery --app app.worker.celery_app worker --beat -l info -c 1

# Create a periodic task for each symbol defined in the settings.
# This registers a new periodic per symbol after Celery is connected to the broker
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    Setup a periodic task for every symbol defined in the settings.
    """
    for symbol in settings.symbols:
        sender.add_periodic_task(settings.frequency, fetch.s(symbol))


@celery_app.task
def fetch(symbol: str):
    """
    Fetch the stock info for a given symbol from Binance and load it into QuestDB.
    """

    quote = client.get_klines(symbol=symbol, interval=client.KLINE_INTERVAL_1MINUTE, limit=1)


    # https://docs.binance.us/?python#get-candlestick-data
    # quote =
    # [
    #   [
    #     1499040000000,      // Open time
    #     "0.00386200",       // Open
    #     "0.00386200",       // High
    #     "0.00386200",       // Low
    #     "0.00386200",       // Close
    #     "0.47000000",  // Volume
    #     1499644799999,      // Close time
    #     "0.00181514",    // Quote asset volume
    #     1,                // Number of trades
    #     "0.47000000",    // Taker buy base asset volume
    #     "0.00181514",      // Taker buy quote asset volume
    #     "0" // Ignore.
    #   ]
    # ]

    query = f"""
    INSERT INTO quotes(stock_symbol, current_price, high_price, low_price, open_price, num_trades, tradets, ts)
    VALUES(
        '{symbol}',
        {quote[0][4]},
        {quote[0][2]},
        {quote[0][3]},
        {quote[0][1]},
        {quote[0][8]},
        {quote[0][6]} * 1000,
        systimestamp()
    );
    """

    with engine.connect() as conn:
        conn.execute(text(query))