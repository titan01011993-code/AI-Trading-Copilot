from market.historical import HistoricalService

history = HistoricalService()

daily = history.load("NIFTY")

hourly = history.load("NIFTY", "1H")

m15 = history.load("NIFTY", "15m")

m5 = history.load("NIFTY", "5m")

print("Daily :", len(daily))
print("1H    :", len(hourly))
print("15m   :", len(m15))
print("5m    :", len(m5))

print("\nDaily")
print(daily.tail())

print("\n1H")
print(hourly.tail())

print("\n15m")
print(m15.tail())

print("\n5m")
print(m5.tail())