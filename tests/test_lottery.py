from brownie import Lottery, accounts, config, network, exceptions
from web3 import Web3
from scripts.deploy import deploy_lottery, enter_lottery, end_lottery, start_lottery
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS, fund_link
import pytest, time


def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # assign
    # account = get_account()
    lottery = deploy_lottery()
    # act
    contract_entrance_fee = lottery.getEntranceFee()
    entry_fee = Web3.toWei(0.025, "ether")
    # Assert
    assert contract_entrance_fee >= entry_fee


def test_cant_enter_unless_started():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Assign
    lottery = deploy_lottery()
    # Act/Assert
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": get_account(), "value": lottery.getEntranceFee()})


def test_can_start_and_enter_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Assign
    lottery = deploy_lottery()
    account = get_account()
    # Act
    lottery.startLottery({"from": account})

    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    # Assert
    assert lottery.players(0) == account


def test_can_end_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    # Assign
    lottery = deploy_lottery()
    account = get_account()
    # Act
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    fund_link(lottery)
    lottery.endLottery({"from":account})
    # Assert
    assert lottery.lottery_state() == 2

