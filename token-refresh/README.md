# User Guide
This User Guide contains essential information for you to make use of this example script. The script  addresses a common use case, uploading data to the data lake drop zone. It can also serve as a starting point for other use cases. This guide includes a description of the script functions and step-by-step instructions for setting up a system to use the script.

_This guide is written for primarily for Windows, but you should find it helpful for other systems._

## Prerequisites
If you haven't already, download and install the following:
- [Python 3](https://www.python.org/downloads/release/python-3913/)  
  _Any 3.x version should work. We use 3.9.13; the latest runtime available for AWS Lambda._
  - :arrow_forward: [How to Install Python 3.9 on Windows 10](https://www.youtube.com/watch?v=kIBPxiuBm1M)
- [AWS Command Line Interface](https://aws.amazon.com/cli/)
  - :arrow_forward: [How to Install AWS CLI on Windows](https://www.youtube.com/watch?v=Gy-jlF3uMLc)
- [Git](https://git-scm.com/download/win)  
  _optional, but recommended_
  - :arrow_forward: [How to Install Git on Windows 10](https://www.youtube.com/watch?v=cJTXh7g-uCM)


## Clone The Repo
1. Open a Command Prompt and navigate to the parent directory of where you would like to put this repo. For example `C:\Users\user-name\some-dir`
2. Type `git clone git@github.com:USDOT-SDC/Public.git` and press Enter
   1. __Note:__ If you do not have Git installed, you can download the [zip file](https://github.com/USDOT-SDC/Public/archive/refs/heads/main.zip) of the repo and unzip it into `Public`
3. You should see something like this
    ```
    Cloning into 'Public'...
    remote: Enumerating objects: 52, done.
    remote: Counting objects: 100% (52/52), done.
    remote: Compressing objects: 100% (39/39), done.
    remote: Total 52 (delta 23), reused 35 (delta 12), pack-reused 0
    Receiving objects: 100% (52/52), 24.12 KiB | 130.00 KiB/s, done.
    Resolving deltas: 100% (23/23), done.
   ```
## Create The Virtual Environment & Install Requirements
1. Type `cd Public\token-refresh` and press Enter
2. Type `python -m venv .venv --prompt token-refresh` and press Enter
3. Type `.venv\Scripts\activate` and press Enter
4. Your prompt should change to `(token-refresh) C:\Users\user-name\some-dir\Public\token-refresh>`
5.  Type `pip install -r requirements.txt` and press Enter
6. You should see something like this
    ```
    Collecting PyYAML~=6.0
    Using cached PyYAML-6.0-cp39-cp39-win_amd64.whl (151 kB)
    Collecting requests~=2.28.1
    Using cached requests-2.28.1-py3-none-any.whl (62 kB)
    Collecting certifi~=2022.12.7
    Using cached certifi-2022.12.7-py3-none-any.whl (155 kB)
    Collecting charset-normalizer~=2.1.1
    Using cached charset_normalizer-2.1.1-py3-none-any.whl (39 kB)
    Collecting idna~=3.4
    Using cached idna-3.4-py3-none-any.whl (61 kB)
    Collecting urllib3~=1.26.13
    Using cached urllib3-1.26.13-py2.py3-none-any.whl (140 kB)
    Collecting boto3~=1.26
    Downloading boto3-1.26.43-py3-none-any.whl (132 kB)
        ---------------------------------------- 132.7/132.7 KB 489.7 kB/s eta 0:00:00
    Collecting botocore<1.30.0,>=1.29.43
    Downloading botocore-1.29.43-py3-none-any.whl (10.3 MB)
        ---------------------------------------- 10.3/10.3 MB 8.6 MB/s eta 0:00:00
    Collecting jmespath<2.0.0,>=0.7.1
    Using cached jmespath-1.0.1-py3-none-any.whl (20 kB)
    Collecting s3transfer<0.7.0,>=0.6.0
    Using cached s3transfer-0.6.0-py3-none-any.whl (79 kB)
    Collecting python-dateutil<3.0.0,>=2.1
    Using cached python_dateutil-2.8.2-py2.py3-none-any.whl (247 kB)
    Collecting six>=1.5
    Using cached six-1.16.0-py2.py3-none-any.whl (11 kB)
    Installing collected packages: urllib3, six, PyYAML, jmespath, idna, charset-normalizer, certifi, requests, python-dateutil, botocore, s3transfer, boto3
    Successfully installed PyYAML-6.0 boto3-1.26.43 botocore-1.29.43 certifi-2022.12.7 charset-normalizer-2.1.1 idna-3.4 jmespath-1.0.1 python-dateutil-2.8.2 requests-2.28.1 s3transfer-0.6.0 six-1.16.0 urllib3-1.26.13
   ```
## Update The Configuration
1.  Type `cp config.sample.yaml config.yaml` and press Enter
2.  Update the `config.yaml` file with the information provided by the SDC Enablement team.
## Upload Files To The Data Lake Drop Zone
1.  At this point you have to option to test the script as is using the test files, or you may edit some of the variables in `cp-path-to-s3.py` file to start uploading data
    1.  `src_path` is the local path to the files you want to upload. The `get_src_files()` function is recursive and will get a list of all files, including sub-directories, in the path
    2.  `dst_prefix` is a prefix that is added to the path of files during upload  
    For example:
    `dst_prefix = "project04"` or `dst_prefix = "sub-group_42"`
2.  Type `python cp-path-to-s3.py` and press Enter
3.  You should see something like this
    ```
    ----------------------------------------------------------------
    Note: your AWS credentials will expire at 2023-01-04 23:55:15+00:00.
    ----------------------------------------------------------------

    Uploading:test-files\01-10mb.test to:test-prefix/test-files/01-10mb.test...
    Uploading:test-files\01-10mb.test to:test-prefix/test-files/01-10mb.test...Done

    ----------------------------------------------------------------
    Note: your AWS credentials will expire at 2023-01-04 23:58:41+00:00.
    ----------------------------------------------------------------

    Uploading:test-files\sub-files\08-10mb.test to:test-prefix/test-files/sub-files/08-10mb.test...
    Uploading:test-files\sub-files\08-10mb.test to:test-prefix/test-files/sub-files/08-10mb.test...Done
    ```
    _This will repeat for all files in the `src_path`_