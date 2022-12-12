from brownie import Lottery, accounts, config, network
from web3 import Web3
from scripts.helpful_scripts import get_account, get_contract, fund_link
import time


def deploy_lottery():
    account = get_account()

    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["key_hash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("deployed lottery")
    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    start_tx = lottery.startLottery({"from": account})
    start_tx.wait(1)
    print("lottery started")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    entrance_fee = lottery.getEntranceFee({"from": account}) + 1000000000
    enter = lottery.enter({"from": account, "value": entrance_fee})
    enter.wait(1)
    print("entry success")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    fund = fund_link(lottery.address)
    fund.wait(1)
    final_tx = lottery.endLottery({"from": account})
    final_tx.wait(1)
    time.sleep(120)
    print(f"lottery ended and the winner is {lottery.Winner()}")


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
