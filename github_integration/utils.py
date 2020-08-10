from github_integration import encryption_type


def encrypt_personal_token(personal_token: str) -> str:
    return encryption_type.encrypt(
        personal_token.encode('utf-8')
    ).decode('utf-8', 'ignore')


def decode_personal_token(personal_token: str) -> str:
    return encryption_type.decrypt(
        personal_token.encode('utf-8')
    ).decode('utf-8', 'ignore')
