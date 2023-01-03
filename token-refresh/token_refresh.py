from pathlib import Path
from os.path import expanduser
import os
import requests
import configparser
import json
import yaml

config_file = "config.yaml"

def token_refresh():
    aws_path = "/.aws"
    # get the token refresh config
    token_config = yaml.safe_load(Path(config_file).read_text())
    api_endpoint = "https://portal.sdc.dot.gov/{0}_users/{1}".format(
        token_config["data_provider_slug"], token_config["api_resource"]
    )
    # Requests credentials from token generator api
    response = requests.post(
        api_endpoint, data=json.dumps({}), headers={"Accept": "application/json", "x-api-key": token_config["api_key"]}
    )
    credentials = response.json()

    # Update ~/.aws/credentials file
    home = expanduser("~")
    os.makedirs(home + aws_path, exist_ok=True)
    con_parser = configparser.RawConfigParser()
    credentials_file = home + f"{aws_path}/credentials"
    con_parser.read(credentials_file)

    if not con_parser.has_section(token_config["data_provider_slug"]):
        con_parser.add_section(token_config["data_provider_slug"])

    con_parser.set(
        token_config["data_provider_slug"],
        "aws_access_key_id",
        credentials["AccessKeyId"],
    )
    con_parser.set(
        token_config["data_provider_slug"],
        "aws_secret_access_key",
        credentials["SecretAccessKey"],
    )
    con_parser.set(
        token_config["data_provider_slug"],
        "aws_session_token",
        credentials["SessionToken"],
    )

    with open(credentials_file, "w+") as credentialsfile:
        con_parser.write(credentialsfile)

    # Update ~/.aws/config file
    cred_parser = configparser.RawConfigParser()
    config_file = home + f"{aws_path}/config"
    cred_parser.read(config_file)

    if not cred_parser.has_section("profile " + token_config["data_provider_slug"]):
        cred_parser.add_section("profile " + token_config["data_provider_slug"])

    cred_parser.set("profile " + token_config["data_provider_slug"], "output", "json")
    cred_parser.set("profile " + token_config["data_provider_slug"], "region", "us-east-1")

    with open(config_file, "w+") as configfile:
        cred_parser.write(configfile)

    print("\n\n----------------------------------------------------------------")
    print("Note: your AWS credentials will expire at {0}.".format(credentials["Expiration"]))
    print("----------------------------------------------------------------\n\n")
