import os
from dotenv import load_dotenv

print("--- DIAGNOSTIC START ---")
print(f"Current working directory: {os.getcwd()}")
env_path = os.path.join(os.getcwd(), ".env")
print(f"Checking for .env at: {env_path}")

if os.path.exists(env_path):
    print("✅ .env file found.")
    # Read raw content to check format (safely)
    with open(env_path, "r") as f:
        content = f.read()
        if "GOOGLE_API_KEY" in content:
            print("✅ 'GOOGLE_API_KEY' string found in .env file.")
        else:
            print("❌ 'GOOGLE_API_KEY' NOT found in .env file.")
else:
    print("❌ .env file NOT found.")

print("Loading .env...")
load_dotenv()

key = os.environ.get("GOOGLE_API_KEY")
if key:
    print(f"✅ GOOGLE_API_KEY loaded into environment. Length: {len(key)}")
    print(f"Key starts with: {key[:4]}...")
else:
    print("❌ GOOGLE_API_KEY is None in os.environ.")

print("--- DIAGNOSTIC END ---")
