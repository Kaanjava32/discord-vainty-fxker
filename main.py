import requests
import time

def check_vanity(token, guild_id, vanity_url, webhook_url):
    headers = {
        "authorization": token,
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    }

    while True:
        try:
            if not vanity_url:
                print("> Vanity URL is empty, waiting for a new URL...")
            else:
                response = requests.get(f"https://discord.com/api/v9/invites/{vanity_url}?with_counts=true&with_expiration=true", headers=headers)
                if response.status_code == 404:
                    print(f"> Changing Vanity URL: {vanity_url}")
                    change_vanity(token, guild_id, vanity_url, webhook_url)
                else:
                    print(f"> Vanity URL still active: {vanity_url}")
            time.sleep(0.2)
        except requests.exceptions.RequestException:
            print("> Rate limited :(")
            time.sleep(5)

def change_vanity(token, guild_id, vanity_url, webhook_url):
    headers = {
        "authorization": token,
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    }
    payload = { "code": vanity_url }

    response = requests.patch(f"https://discord.com/api/v10/guilds/{guild_id}/vanity-url", headers=headers, json=payload)
    if response.status_code == 200:
        print(f"> URL changed: {vanity_url}")
        data = {
            "content": f"@everyone discord.gg/{vanity_url} yours now!",
            "username": "Ayhu",
            "avatar_url": "https://i.imgur.com/oKzncfw.png"
        }
        requests.post(webhook_url, json=data)
        exit()
    else:
        print(f"> Vanity URL could not be changed, error code: {response.status_code}")

def main():
    token = input("> Your Account Token: ")
    guild_id = input("> Your Server ID: ")
    webhook_url = input("> Discord webhook URL: ")
    vanity_url = input("> Vanity URL: ")

    check_vanity(token, guild_id, vanity_url, webhook_url)

if __name__ == "__main__":
    main()
