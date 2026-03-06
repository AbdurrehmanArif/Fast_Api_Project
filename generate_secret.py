# Script to generate a secure SECRET_KEY for your .env
import secrets
print("Your secure SECRET_KEY:")
print(secrets.token_hex(32))
