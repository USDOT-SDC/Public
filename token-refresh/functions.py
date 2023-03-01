import boto3
from botocore.config import Config
from botocore.exceptions import ClientError, ParamValidationError
from pathlib import Path
import os
import os.path
import yaml
import base64
import hashlib


aws_config = Config(
    region_name="us-east-1",
    signature_version="v4",
    retries={"max_attempts": 10, "mode": "standard"},
)


def get_src_files(src_path):
    src_files = []
    for dirpath, dirnames, filenames in os.walk(Path(src_path)):
        for filename in filenames:
            src_files.append({"path": Path(dirpath), "filename": filename})
    return src_files


def get_src(src_path, src_filename):
    return os.path.join(src_path, src_filename)


def get_dst(src_path, src_filename, dst_prefix):
    src_prefix = Path(*src_path.parts[1:]).as_posix()
    if src_prefix == ".":
        return dst_prefix + src_filename
    else:
        return dst_prefix + src_prefix + "/" + src_filename


def get_dropzone(config_file):
    return "prod.sdc.dot.gov.data-lake.drop-zone." + get_data_provider_slug(config_file)


def get_data_provider_slug(config_file):
    return yaml.safe_load(Path(config_file).read_text())["data_provider_slug"]


def get_md5(data):
    md5 = hashlib.md5()
    md5.update(data)
    md5_digest = md5.digest()
    return base64.b64encode(md5_digest).decode("utf-8")


def read_in_chunks(file_object, chunk_size=15 * 1024**2):
    # chunk_size: 15MiB, AWS default
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def cp_to_s3(filename, key, config_file):
    try:
        # set the default profile
        boto3.setup_default_session(profile_name=get_data_provider_slug(config_file))
        # s3 client
        s3 = boto3.client("s3", config=aws_config)
        # create the multipart upload
        mpu_crt = s3.create_multipart_upload(Bucket=get_dropzone(config_file), Key=key)
        # collect info on all the parts
        multipart_upload = {"Parts": []}
        # open the file
        with open(filename, "rb") as f:
            part_number = 1
            # read file in chunks
            for chunk in read_in_chunks(f):
                # upload this chunk
                print(f"                Uploading Part: {str(part_number)}...")
                mpu_part = s3.upload_part(
                    Body=chunk,
                    Bucket=mpu_crt["Bucket"],
                    ContentMD5=get_md5(chunk),
                    Key=mpu_crt["Key"],
                    PartNumber=part_number,
                    UploadId=mpu_crt["UploadId"],
                )
                # collect info on this chunk
                multipart_upload["Parts"].append(
                    {
                        "ETag": mpu_part["ETag"],
                        "PartNumber": part_number,
                    }
                )
                print(f"                Uploading Part: {str(part_number)}...complete")
                # increment to next chunk
                part_number += 1
        # complete this mpu
        mpu_cmplt = s3.complete_multipart_upload(
            Bucket=mpu_crt["Bucket"],
            Key=mpu_crt["Key"],
            UploadId=mpu_crt["UploadId"],
            MultipartUpload=multipart_upload,
        )
        return mpu_cmplt

    except ClientError as error:
        mpu_abrt = s3.abort_multipart_upload(
            Bucket=mpu_crt["Bucket"],
            Key=mpu_crt["Key"],
            UploadId=mpu_crt["UploadId"],
        )
        print(error)
        raise error

    except ParamValidationError as error:
        mpu_abrt = s3.abort_multipart_upload(
            Bucket=mpu_crt["Bucket"],
            Key=mpu_crt["Key"],
            UploadId=mpu_crt["UploadId"],
        )
        print(error)
        raise ValueError("The parameters you provided are incorrect: {}".format(error))

