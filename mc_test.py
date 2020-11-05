"""

"""
import json
from pathlib import Path
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
HOME_DIR = Path(__file__).resolve().parent

def get_config():
    config_file = HOME_DIR.joinpath('data/config.json')
    with open(config_file) as f:
        return json.load(f)

def main():


    try:
        client = MailchimpMarketing.Client()
        client.set_config({
            "api_key": "YOUR_API_KEY",
            "server": "us9"
        })
        response = client.ping.get()
        print(response)
    except ApiClientError as error:
        print(error)


if __name__ == '__main__':
    config = get_config()
    print(config)
