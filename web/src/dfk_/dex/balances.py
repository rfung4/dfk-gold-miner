from dfktools.dex import erc20


def get_item(item: str) -> tuple:
    return next(filter(lambda a: a[1] == item, erc20.ITEMS))


def _get_item_count(account_address: str, item_name: str):
    rune_item = get_item(item_name)
    return erc20.balance_of(address=account_address,
                            token_address=rune_item[0], rpc_address='https://harmony-0-rpc.gateway.pokt.network')


def get_rune_count(account_address: str):
    return _get_item_count(account_address, 'DFKSHVAS')


def get_jewel_count(account_address: str):
    raw_val = _get_item_count(account_address, 'JEWEL') / 10**18
    return "{:.2f}".format(raw_val)


