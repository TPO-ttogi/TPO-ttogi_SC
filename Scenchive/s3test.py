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

# filename = "4bc49d4eb97c5f22c5e3a425cdba76e6.jpg"
filename = "brand/" + "character_new01.gif"
bucket_name = "scenchive"

def check_s3_object_exists(bucket_name, object_key):
    try:
        s3.head_object(Bucket=bucket_name, Key=object_key)
        return True
    except Exception as e:
        return False

if check_s3_object_exists(bucket_name, filename):
    print("https://scenchive.s3.ap-northeast-2.amazonaws.com/" + filename)
else:
    print(f"The object '{filename}' does not exist in the bucket '{bucket_name}'.")
