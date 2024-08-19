from pathlib import Path
from os.path import expanduser
from datetime import datetime
import sys
from typing import Any
import requests
import configparser
import json
import yaml


def token_refresh(config_file: str) -> None:
    """Generates a new token refresh token

    Args:
        config_file (str): the config file to be used
    """
    # get the token refresh config
    base_path: Path = Path(__file__).parents[0]
    config_file_path: Path = base_path / config_file
    config: Any = yaml.safe_load(config_file_path.read_text())
    api_endpoint: str = config.get("api_endpoint", "https://api.sample.com/v1/token")
    region_name: str = config.get("aws_config", None).get("region_name", "us-east-1")

    print_in_box(
        [
            "".ljust(80),
            f"{config.get("profile_name", None)} profile:",
            "Requesting new access keys and session token from...",
            f"{api_endpoint.split("?")[0]}",
            f"?{api_endpoint.split("?")[1]}",
            "",
        ],
        has_bottom=False,
        line="double",
    )

    # Requests credentials from api
    response: requests.Response = requests.post(
        api_endpoint,
        data=json.dumps({}),
        headers={
            "Accept": "application/json",
            "x-api-key": config["api_key"],
        },
    )
    credentials: Any = response.json()
    if credentials.get("message"):
        sys.exit(f"The API responded with '{credentials.get("message")}'")

    print_in_box(
        [
            "".ljust(80),
            f'AccessKeyId: {credentials["AccessKeyId"]}',
            "",
        ],
        has_top=False,
        has_bottom=False,
        line="double",
    )

    # Update ~/.aws/credentials file
    home_path = Path(expanduser("~"))
    aws_path: Path = home_path / ".aws"
    aws_path.mkdir(parents=True, exist_ok=True)
    credentials_parser = configparser.RawConfigParser()
    credentials_file: Path = aws_path / "credentials"
    credentials_parser.read(credentials_file)

    if not credentials_parser.has_section(config["profile_name"]):
        credentials_parser.add_section(config["profile_name"])

    credentials_parser.set(
        config["profile_name"],
        "aws_access_key_id",
        credentials["AccessKeyId"],
    )
    credentials_parser.set(
        config["profile_name"],
        "aws_secret_access_key",
        credentials["SecretAccessKey"],
    )
    credentials_parser.set(
        config["profile_name"],
        "aws_session_token",
        credentials["SessionToken"],
    )

    with open(credentials_file, "w+") as f:
        credentials_parser.write(f)

    # Update ~/.aws/config file
    config_parser = configparser.RawConfigParser()
    config_file: Path = aws_path / "config"
    config_parser.read(config_file)

    if not config_parser.has_section("profile " + config["profile_name"]):
        config_parser.add_section("profile " + config["profile_name"])

    config_parser.set("profile " + config["profile_name"], "output", "json")
    config_parser.set("profile " + config["profile_name"], "region", region_name)

    with open(config_file, "w+") as f:
        config_parser.write(f)

    print_in_box(
        [
            "".ljust(80),
            f"Note: your AWS credentials will expire at {credentials['Expiration']}".ljust(80),
            "",
        ],
        has_top=False,
        line="double",
    )

def print_in_box(strings: list[str], line: str = "single", has_top: bool = True, has_bottom: bool = True) -> None:
    max_len = 0
    for string in strings:
        str_len: int = len(string) + 1
        if str_len > max_len:
            max_len: int = str_len
    box_draw_chars: dict[str, dict[str, str]] = {
        "single": {
            "se": "┘",
            "ne": "┐",
            "nw": "┌",
            "sw": "└",
            "h": "─",
            "v": "│",
        },
        "double": {
            "se": "╝",
            "ne": "╗",
            "nw": "╔",
            "sw": "╚",
            "h": "═",
            "v": "║",
        },
    }
    se: str | None = box_draw_chars.get(line).get("se")
    ne: str | None = box_draw_chars.get(line).get("ne")
    nw: str | None = box_draw_chars.get(line).get("nw")
    sw: str | None = box_draw_chars.get(line).get("sw")
    h: str | None = box_draw_chars.get(line).get("h")
    v: str | None = box_draw_chars.get(line).get("v")
    h_line: Any = (h * max_len) + h
    if has_top:
        print(f"\n {nw}{h_line}{ne}")
    for string in strings:
        print(f" {v} {string.ljust(max_len)}{v}")
    if has_bottom:
        print(f" {sw}{h_line}{se}\n")
