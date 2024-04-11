from facebook_business.adobjects.business import Business
from facebook_business.api import FacebookAdsApi
from facebook_business.exceptions import FacebookRequestError
from rich.console import Console


def generate_pixel(
    app_id, app_secret, access_token, business_id, ad_account_ids, pid, store_name
):
    """
    Receives keys, business id and ad-account ids to instantiate Meta Ads API.
    Receives project code (PID) and store name {store_name} to create Ad Pixel with nomenclature
    Enables AAM and links ad accounts.
    returns pixel_name and pixel_code as variables.
    """
    # Initialize Meta Ads API
    console = Console()
    console.print("Connecting to Meta Advertising API...", style="bold cyan")
    FacebookAdsApi.init(app_id, app_secret, access_token)
    console.print("Successfully connected to Meta Advertising API.", style="bold cyan")
    console.print(f"Generating Pixel ({pid} {store_name})...", style="bold cyan")

    try:
        business = Business(business_id)

        # create meta pixel
        pixel = business.create_ads_pixel(
            fields=["name", "code"], params={"name": f"{pid} {store_name}"}
        )

        # retrieve the name and code
        pixel_name = pixel.get("name")
        pixel_code = pixel.get("code")

        # enable automatic advanced matching
        pixel.api_update(params={"enable_automatic_matching": True})
        pixel.api_update(
            params={
                "automatic_matching_fields": ["em", "ph", "ge", "db", "ln", "fn"],
                "enable_auto_assign_to_accounts": True,
            }
        )
        console.print("Automatic Advanced Matching Enabled.", style="bold cyan")

        # add the ad accounts
        for account in ad_account_ids:
            pixel.create_shared_account(
                params={"account_id": account, "business": business_id},
            )
            console.print(
                f"Pixel successfully linked to Ad Account: {account}.",
                style="bold cyan",
            )

        console.print(
            f"Pixel generation complete. Returning Pixel name ({pixel_name}) and code.",
            style="bold cyan",
        )
        return pixel_name, pixel_code

    except FacebookRequestError as e:
        print(f"Error: {e}")
