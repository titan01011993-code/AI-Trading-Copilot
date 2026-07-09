from app.settings import settings

print("Client ID:", settings.DHAN_CLIENT_ID)
print("Token Length:", len(settings.DHAN_ACCESS_TOKEN))
print("First 5:", settings.DHAN_ACCESS_TOKEN[:5])
print("Last 5:", settings.DHAN_ACCESS_TOKEN[-5:])