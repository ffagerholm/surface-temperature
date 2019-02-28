"""
Script for uploading data to AWS S3.
Usage:
    python .\src\upload_data.py <file path> <bucket name> <bucket directory> 

Where:
<file path>: Path to the local file.
<bucket name>: Name of the S3 bucket.
<bucket directory>:  Name of the directory in the bucket.

Example:
    python .\src\upload_data.py ".\data\NASA_GISS_LOTI_long_format.csv" "tempdev-data" "data" 
"""
import sys
import os
import boto3
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


def upload_data(file_path, bucket_name, directory):
    _, file_name = os.path.split(file_path)
    bucket_path = '/'.join([directory, file_name])

    print("Uploading file to S3")
    s3 = boto3.resource('s3')

    with open(file_path, 'rb') as infile:
        s3.Bucket(bucket_name).put_object(
            Key=bucket_path, Body=infile)

    print("Done.")

def main():
    if len(sys.argv) == 4:
        file_path = sys.argv[1]
        bucket_name = sys.argv[2]
        directory = sys.argv[3]

        upload_data(file_path, bucket_name, directory)
    else:
        raise RuntimeError('Not enough commandline arguments.')    
    
if __name__ == "__main__":
    main()