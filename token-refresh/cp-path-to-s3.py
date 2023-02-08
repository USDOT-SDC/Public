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
            src_files.append({"path": Path(dirpath), "filename": filename})
    return src_files


def get_src(src_path, src_filename):
    return os.path.join(src_path, src_filename)


def get_dst(src_path, src_filename, dst_prefix):
    src_prefix = Path(*src_file["path"].parts[1:]).as_posix()
    if src_prefix == ".":
        return dst_prefix + src_filename
    else:
        return dst_prefix + src_prefix + "/" + src_filename


def get_dropzone(config_file):
    return "prod.sdc.dot.gov.data-lake.drop-zone." + get_data_provider_slug(config_file)


def get_data_provider_slug(config_file):
    return yaml.safe_load(Path(config_file).read_text())["data_provider_slug"]


def cp_to_s3(filename, key, config_file=config_file):
    # set the default profile
    boto3.setup_default_session(profile_name=get_data_provider_slug(config_file))
    # Set the desired multipart threshold value (4GB)
    GB = 1024**3
    config = TransferConfig(multipart_threshold=GB * 4)
    # Perform the transfer
    s3 = boto3.client("s3")
    s3.upload_file(
        Filename=filename,
        Bucket=get_dropzone(config_file),
        Key=key,
        Config=config,
    )


src_path = f"test-files/"
dst_prefix = f"test-prefix/"
for src_file in get_src_files(src_path):
    src = get_src(src_path=src_file["path"], src_filename=src_file["filename"])
    dst = get_dst(src_path=src_file["path"], src_filename=src_file["filename"], dst_prefix=dst_prefix)
    token_refresh()
    print("Uploading: " + src)
    print("       To: " + dst)
    cp_to_s3(src, dst)
    print("     Done: " + src_file["filename"] + "\n")
