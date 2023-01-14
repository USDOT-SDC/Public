from token_refresh import token_refresh
import boto3
from boto3.s3.transfer import TransferConfig
from pathlib import Path
import os
import os.path
import yaml


def get_src_files(src_path):
    src_path = Path(src_path)
    src_files = []
    for dirpath, dirnames, filenames in os.walk(src_path):
        for filename in filenames:
            src_files.append({"dirpath": dirpath, "filename": filename})
    return src_files


def cp_to_s3(filename, key):
    # get the date provider slug
    data_provider_slug = yaml.safe_load(Path("config.yaml").read_text())["data_provider_slug"]
    # set the default profile
    boto3.setup_default_session(profile_name=data_provider_slug)
    # Set the desired multipart threshold value (1GB)
    GB = 1024**3
    config = TransferConfig(multipart_threshold=1 * GB)
    # Perform the transfer
    s3 = boto3.client("s3")
    s3.upload_file(
        Filename=filename,
        Bucket="prod.sdc.dot.gov.data-lake.drop-zone." + data_provider_slug,
        Key=key,
        Config=config,
    )

src_path = "test-files"
dst_prefix = "test-prefix"
for src_file in get_src_files(src_path):
    src = os.path.join(src_file["dirpath"], src_file["filename"])
    src_prefix = src_file["dirpath"].removeprefix(src_path).replace("\\", "/")
    print(src_prefix)
    dst = dst_prefix + src_prefix + "/" + src_file["filename"]
    token_refresh()
    print("Uploading:" + src + " to:" + dst + "...")
    cp_to_s3(src, dst)
    print("Uploading:" + src + " to:" + dst + "...Done")
