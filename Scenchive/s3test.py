import boto3

def s3_connection():
    try:
        s3 = boto3.client(
            service_name = "s3",
            region_name = "ap-northeast-2",
            aws_access_key_id = "AKIAWTXFO4EJSQNOR4GW",
            aws_secret_access_key = "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",
        )
    except Exception as e:
        print(e)
    else:
        print("s3 bucket connected!")
        return s3

s3 = s3_connection()
