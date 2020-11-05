"""

"""
import json
from pathlib import Path

import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

HOME_DIR = Path(__file__).resolve().parent


def get_config():
    config_file = Path.home().joinpath('Documents/_rc/mc_config.json')
    with open(config_file) as f:
        return json.load(f)


def main():
    config = get_config()
    try:
        client = MailchimpMarketing.Client()
        client.set_config({
            "api_key": config['key'],
            "server": config['server']
        })
        response = client.ping.get()
        print(response)
    except ApiClientError as error:
        print(error)


def save_environ():
    import os
    environ = {k: v for k, v in os.environ.item()}
    with open('junk.json', 'w', encoding='utf-8') as f:
        json.dump(environ, f)


if __name__ == '__main__':
    main()
