import cli
from aws_sso_menu import show_menu
from retrieve_aws_sso_token import retrieve_aws_sso_token


def main(args):
    aws_sso_token = retrieve_aws_sso_token(args)

    if args.output_file:
        with open(args.output_file, 'w') as f:
            f.write(aws_sso_token)
            print(f"Wrote the AWS SSO token to {args.output_file}")

    show_menu(aws_sso_token, args.region)


if __name__ == "__main__":
    main(cli.parser.parse_args())
