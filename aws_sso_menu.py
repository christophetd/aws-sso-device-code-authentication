import boto3

from simple_term_menu import TerminalMenu


def retrieve_aws_accounts(sso_client, aws_sso_token):
    aws_accounts_response = sso_client.list_accounts(
        accessToken=aws_sso_token,
        maxResults=100
    )
    if len(aws_accounts_response.get('accountList', [])) == 0:
        raise RuntimeError('Unable to retrieve AWS SSO account list\n')
    return  aws_accounts_response.get('accountList')


def retrieve_roles_in_account(sso_client, aws_sso_token, account):
    account_id = account.get('accountId')
    roles_response = sso_client.list_account_roles(accessToken=aws_sso_token, accountId=account_id)
    if len(roles_response.get('roleList', [])) == 0:
        raise RuntimeError(f'Unable to retrieve roles in account {account_id}\n')

    return [role.get('roleName') for role in roles_response.get('roleList')]


def retrieve_credentials(sso_client, aws_sso_token, account_id, role_name):
    sts_creds = sso_client.get_role_credentials(
        accessToken=aws_sso_token,
        roleName=role_name,
        accountId=account_id
    )
    if 'roleCredentials' not in sts_creds:
        raise RuntimeError('Unable to retrieve STS credentials')
    credentials = sts_creds.get('roleCredentials')
    if 'accessKeyId' not in credentials:
        raise RuntimeError('Unable to retrieve STS credentials')

    return credentials.get('accessKeyId'), credentials.get('secretAccessKey'), credentials.get('sessionToken')


def print_credentials(credentials, account, role_name):
    print(f"Here are your temporary STS credentials for the '{role_name}' role in the AWS account '{account.get('accountName')}' ({account.get('accountId')})")
    print()
    print(f"export AWS_ACCESS_KEY_ID={credentials[0]}")
    print(f"export AWS_SECRET_ACCESS_KEY={credentials[1]}")
    print(f"export AWS_SESSION_TOKEN={credentials[2]}")


def show_menu(aws_sso_token, region):
    sso_client = boto3.client('sso', region_name=region)
    aws_accounts_list = retrieve_aws_accounts(sso_client, aws_sso_token)
    human_readable_accounts_list = [f"{account['accountName']} ({account['accountId']})" for account in
                                    aws_accounts_list]
    back_to_main_menu = True
    while back_to_main_menu:
        selected_account_index = TerminalMenu(human_readable_accounts_list).show()
        if selected_account_index is None:
            print('Bye')
            exit(0)
        selected_account = aws_accounts_list[selected_account_index]
        roles_in_account = retrieve_roles_in_account(sso_client, aws_sso_token, selected_account)
        roles_in_account.append("(back to accounts list)")
        selected_role_index = TerminalMenu(roles_in_account).show()
        if selected_role_index is None:
            print('Bye')
            exit(0)
        if selected_role_index < len(roles_in_account) - 1:
            selected_role = roles_in_account[selected_role_index]
            back_to_main_menu = False
            selected_role = roles_in_account[selected_role_index]
            credentials = retrieve_credentials(
                sso_client,
                aws_sso_token,
                selected_account.get('accountId'),
                selected_role
            )
            print_credentials(credentials, selected_account, selected_role)
