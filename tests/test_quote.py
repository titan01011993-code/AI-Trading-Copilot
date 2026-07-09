from market.quotes import QuoteService

quote = QuoteService()

response = quote.get_quote("RELIANCE")

print(response)