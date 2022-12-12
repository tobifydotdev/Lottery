from brownie import (
    network,
    config,
    accounts,
    MockV3Aggregator,
    Contract,
    VRFCoordinatorMock,
    LinkToken,
)

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork-dev"]
contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link": LinkToken,
}
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

DECIMALS = 8
STARTING_PRICE = 200000000000


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    return accounts.load("tobiade")


def get_contract(contract_name):
    """This function will grab contrcat addresses from the brownei config if defined, else, it will delpoy a mock version of that contract and return that mock contract

    Args:
        contract_name (string)

    Returns:
        brownie.network.contract.projectContract: The most recebtly deployed version of this contract
        MockV3Aggregator[-1]

    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def deploy_mocks(decimals=DECIMALS, initial_value=STARTING_PRICE):
    account = get_account()
    MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token, {"from": account})
    print("deployed")


def fund_link(contract_address, account=None, amount=100000000000000000, link=None):
    account = account if account is not None else get_account()
    link = link if link is not None else get_contract("link")
    tx = link.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("contract funded")
    return tx
