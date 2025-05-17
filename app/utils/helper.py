def strip_account_number(account_number):
    """
    Strips the account number of any non-numeric characters.
    """
    return "".join(filter(str.isdigit, account_number))
