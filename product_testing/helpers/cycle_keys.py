import requests
import dropbox
import os
from dotenv import load_dotenv

load_dotenv()

### FILE REMAINS UNLINKED - USE ONLY WHEN TOKEN EXPIRED
### NAVIGATE TO https://developers.facebook.com/tools/explorer/ AND GENERATE NEW SHORT-LIVED TOKEN
### NAVIGATE TO https://www.dropbox.com/developers/apps/info/68t93etp9ej005e AND GENERATE NEW SHORT-LIVED TOKEN


def get_long_meta_token(app_id, app_secret, short_lived_token):
    """
    Uses requests library to submit a Meta short-access token in exchange for a long-lived one
    (couple hours expiry) -> (60 days expiry)
    """
    url = "https://graph.facebook.com/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": app_id,
        "client_secret": app_secret,
        "fb_exchange_token": short_lived_token,
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json().get("access_token", "No token found in response")
    else:
        return f"Error: {response.status_code} - {response.text}"


def get_long_dropbox_token(app_key, app_secret, refresh_token):
    """
    Uses requests library to submit a Dropbox short-access token in exchange for a long-lived one
    (couple hours expiry) -> (60 days expiry)
    """
    try:
        dbx = dropbox.Dropbox(
            oauth2_access_token=refresh_token, app_key=app_key, app_secret=app_secret
        )

        # Making a test API call to trigger token refresh
        dbx.users_get_current_account()
        new_access_token = dbx._oauth2_access_token
        return new_access_token

    except Exception as e:
        print("Error occurred: ", e)
        return None


if __name__ == "__main__":
    # Meta key cycling
    # print(
    #     "Meta token: ",
    #     get_long_meta_token(
    #         os.getenv("META_APP_ID"),
    #         os.getenv("META_APP_SECRET"),
    #         os.getenv("META_SHORT_TOKEN"),
    #     ),
    # )

    # Dropbox key cycling
    print(
        "DBX token: ",
        get_long_dropbox_token(
            os.getenv("DROPBOX_KEY"),
            os.getenv("DROPBOX_SECRET"),
            os.getenv("DROPBOX_SHORT_TOKEN"),
        ),
    )
