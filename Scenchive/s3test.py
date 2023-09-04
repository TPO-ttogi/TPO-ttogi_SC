import boto3

def s3_connection():
    try:
        s3 = boto3.client(
            service_name = "****",
            region_name = "****",
            aws_access_key_id = "****",
            aws_secret_access_key = "****",
        )
    except Exception as e:
        print(e)
    else:
        print("s3 bucket connected!")
        return s3

s3 = s3_connection()
