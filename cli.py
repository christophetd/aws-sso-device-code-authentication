import argparse

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument(
    "-u", "--sso-start-url",
    dest='start_url',
    help='AWS SSO start URL. Example: https://mycompany.awssapps.com/start',
    required=True
)

parser.add_argument(
    "-r", "--sso-region",
    dest='region',
    help='AWS region in which AWS SSO is configured (e.g. us-east-1)',
    required=True
)

parser.add_argument(
    "-i", "--sso-token-file",
    dest='sso_token_file',
    help='File to read the AWS SSO token from. If provided, no device code URL is generated'
)
parser.add_argument(
    "-o",
    dest='output_file',
    help='File to write the retrieved AWS SSO token'
)
