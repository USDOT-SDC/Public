from token_refresh import token_refresh
import boto3
from boto3.s3.transfer import TransferConfig
from pathlib import Path
import os
import os.path
import yaml


config_file = "config.yaml"


def get_src_files(src_path):
    src_files = []
    for dirpath, dirnames, filenames in os.walk(Path(src_path)):
        for filename in filenames:
            src_files.append({"path": Path(dirpath.removeprefix(src_path)), "filename": filename})
    return src_files


def cp_to_s3(filename, key, config_file=config_file):
    # get the date provider slug
    data_provider_slug = yaml.safe_load(Path(config_file).read_text())["data_provider_slug"]
    # set the default profile
    boto3.setup_default_session(profile_name=data_provider_slug)
    # Set the desired multipart threshold value (4GB)
    GB = 1024**3
    config = TransferConfig(multipart_threshold=GB * 4)
    # Perform the transfer
    s3 = boto3.client("s3")
    s3.upload_file(
        Filename=filename,
        Bucket="prod.sdc.dot.gov.data-lake.drop-zone." + data_provider_slug,
        Key=key,
        Config=config,
    )


src_path = f"test-files"
dst_prefix = f"test-prefix/"
for src_file in get_src_files(src_path):
    src = os.path.join(src_file["path"], src_file["filename"])
    src_prefix = Path(*src_file["path"].parts[1:]).as_posix()
    dst = dst_prefix + src_prefix + "/" + src_file["filename"]
    token_refresh()
    print("Uploading:" + src + " to:" + dst + "...")
    cp_to_s3(src, dst)
    print("Uploading:" + src + " to:" + dst + "...Done")
