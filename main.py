import arrow
import yfinance as yf
import os

os.system("clear")

def get_stock_data(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    hist = stock.history(start=start_date, end=end_date)
    if hist.empty:
        return []

    data = []
    for date, row in hist.iterrows():
        try:
            open_price = row['Open']
            close_price = row['Close']
            data.append((date, open_price, close_price))
        except IndexError:
            continue
    return data
    
def days_between_dates(start_date, end_date):
    start = arrow.get(start_date)
    end = arrow.get(end_date)
    return (end - start).days

# print("Open", get_stock_data('AAPL', arrow.Arrow(2000,1,1), at_open=True))
# print("Close", get_stock_data('AAPL', arrow.Arrow(2021,1,1), at_open=False))

START_MONEY = 1000
SHARES = 0
STOCK = "MSFT"
START_DATE = arrow.Arrow(2000,1,1)
MONEY = START_MONEY

stock_data = get_stock_data(STOCK, START_DATE, arrow.now())
for date, open_price, close_price in stock_data:
    if open_price is None or close_price is None:
        continue
    dist = open_price-close_price
    if dist < 0:
        SHARES -= (dist)/close_price if SHARES >= (dist)/close_price else 0
        MONEY += (dist) if SHARES >= (dist)/close_price else 0
    elif dist > 0:
        SHARES += (dist)/close_price if MONEY >= dist else 0
        MONEY -= (dist) if MONEY >= dist else 0
    else:
        pass
    print(-days_between_dates(date, START_DATE), MONEY, SHARES, SHARES*close_price + MONEY) if days_between_dates(date, START_DATE) % 30 == 0 else None

# start_date = "2021-01-01"
# end_date = "2021-12-31"
# print(f"Days between {start_date} and {end_date}: {days_between_dates(start_date, end_date)}")

