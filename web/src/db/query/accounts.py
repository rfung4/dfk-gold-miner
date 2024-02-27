from web.src.db.ORM.dfk_orm import Account
from web.src.db.db import dfk_session_creator
from web.src.encrypt.encrypt import encrypt_string


def get_accounts() -> [Account]:
    with dfk_session_creator() as session:
        return session.query(Account).all()


def set_account_data(public_address: str, private_key: str) -> None:
    with dfk_session_creator() as session:
        encrypted_private_key = encrypt_string(private_key)
        account = Account(private_key=encrypted_private_key, public_address=public_address)
        session.add(account)
        session.commit()


def get_account_from_address(public_address: str) -> Account:
    with dfk_session_creator() as session:
        return session.query(Account).filter(Account.public_address == public_address).first()



