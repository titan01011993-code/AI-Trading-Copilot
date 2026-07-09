from app.settings import settings

print("=" * 50)
print("Angel One Configuration Test")
print("=" * 50)

print("API Key Loaded       :", bool(settings.ANGEL_API_KEY))
print("Client ID Loaded     :", bool(settings.ANGEL_CLIENT_ID))
print("Password Loaded      :", bool(settings.ANGEL_PASSWORD))
print("TOTP Secret Loaded   :", bool(settings.ANGEL_TOTP_SECRET))