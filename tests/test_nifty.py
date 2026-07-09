from market.nifty import NiftyService

service = NiftyService()

df = service.load()

print(df.tail())
print(df.shape)