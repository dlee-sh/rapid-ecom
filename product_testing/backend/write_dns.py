import CloudFlare
from rich.console import Console


def write_dns(CLOUDFLARE_EMAIL, CLOUDFLARE_API_KEY, domain_name):
    """
    Receives CloudFlare Email and CloudFlare API Key to connect to CloudFlare API
    Receives domain name (without http or trailing characters) to search for Zone ID
    Publishes mailserver and storefront DNS settings
    CNAME records are "DNS ONLY"
    """
    console = Console()
    console.print("Connecting to CloudFlare API...", style="bold cyan")

    # Initialize cloudflare API
    cf = CloudFlare.CloudFlare(email=CLOUDFLARE_EMAIL, key=CLOUDFLARE_API_KEY)
    console.print("Successfully connected to CloudFlare API.", style="bold cyan")

    # retrieve the zone id
    console.print("Attempting to link to zone id...", style="bold cyan")
    zones = cf.zones.get(params={"name": domain_name})
    for zone in zones:
        if zone["name"] == domain_name:
            zone_id = zone["id"]
            console.print(
                "Domain linked successfully, writing DNS settings...", style="bold cyan"
            )

    # DNS record template
    dns_records = [
        {"name": "@", "type": "A", "content": "23.227.38.65", "ttl": 3600},
        {
            "name": "@",
            "type": "MX",
            "content": "in1-smtp.messagingengine.com.",
            "ttl": 3600,
            "priority": 10,
        },
        {
            "name": "@",
            "type": "MX",
            "content": "in2-smtp.messagingengine.com.",
            "ttl": 3600,
            "priority": 20,
        },
        {
            "name": "@",
            "type": "TXT",
            "content": "v=spf1 include:spf.messagingengine.com ?all",
            "ttl": 3600,
        },
        {
            "name": "fm1._domainkey",
            "type": "CNAME",
            "content": f"fm1.{domain_name}.dkim.fmhosted.com.",
        },
        {
            "name": "fm2._domainkey",
            "type": "CNAME",
            "content": f"fm2.{domain_name}.dkim.fmhosted.com.",
        },
        {
            "name": "fm3._domainkey",
            "type": "CNAME",
            "content": f"fm3.{domain_name}.dkim.fmhosted.com.",
        },
        {"name": "www", "type": "CNAME", "content": "shops.myshopify.com", "ttl": 3600},
    ]

    for dns_record in dns_records:
        r = cf.zones.dns_records.post(zone_id, data=dns_record)

    console.print("DNS Settings written successfully", style="bold cyan")
    return
