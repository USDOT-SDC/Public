from token_refresh import token_refresh
import functions as func


config_file = "config.yaml"
src_path = "test-files/"
dst_prefix = "test-prefix/"


for src_file in func.get_src_files(src_path):
    src = func.get_src(src_path=src_file["path"], src_filename=src_file["filename"])
    dst = func.get_dst(src_path=src_file["path"], src_filename=src_file["filename"], dst_prefix=dst_prefix)
    token_refresh(config_file=config_file)
    print("Uploading: " + src)
    print("       To: " + dst)
    func.cp_to_s3(src, dst, config_file=config_file)
    print("     Done: " + src_file["filename"] + "\n")
