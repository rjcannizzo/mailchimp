"""
explore this: https://mailchimp.com/developer/api/transactional/exports/export-activity-history/
"""
import json
from pathlib import Path
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from utilities import write_to_json_file, get_config_file, get_json_from_file

HOME_DIR = Path(__file__).resolve().parent


def ping():
    config = get_config_file()
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


def parser():
    file_to_parse = HOME_DIR.joinpath('data/campaign_recipients_example.json')
    with open(file_to_parse) as f:
        jo = json.load(f)
    # print(jo['results'][0]['campaign']['report_summary'])
    print(jo['sent_to'][0]['last_open'])
    print(jo['sent_to'][0]['status'])
    print(jo['sent_to'][0]['email_address'])
    print(jo['sent_to'][0]['email_id'])


def get_campaigns(configs, list_id="761df5fbb3"):
    """
    Return a json object of campaign info.
    :param configs: Mailchimp config info
    :param list_id: id of list to query; defaults to 'current' list
    :return: json object
    """
    try:
        client = MailchimpMarketing.Client()
        client.set_config({
            "api_key": configs['key'],
            "server": configs['server']
        })

        response = client.campaigns.list(list_id=list_id)
        return response
    except ApiClientError as error:
        print("Error: {}".format(error.text))


def save_query_results(out_file_name):
    configs = get_config_file()
    # result = get_campaigns(configs)
    # out_file = HOME_DIR.joinpath('data/results').joinpath(out_file_name)
    # write_to_json_file(out_file, result)


if __name__ == '__main__':
    config_info = get_config_file()
    save_query_results()