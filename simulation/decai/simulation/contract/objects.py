# Objects for all smart contracts.
# 所有智能合约的对象
from dataclasses import dataclass, field
from typing import Optional

from injector import singleton

Address = str
""" An address that can receive funds and participate in training models. """
""" 一个可以接收资金和参与训练模型的地址 """


@dataclass
class Msg:
    """
    A message sent to a smart contract.

    :param sender: The sender's address.
    :param value: Amount sent with the message.
    """
    """
    发送智能合约的消息
    
    :param sender: 发送者的地址
    :param value: 随着消息发送的金额
    """
    sender: Address
    # Need to use float since the numbers might be large. They should still actually be integers.
    # 需要使用float， 因为数值可能很大。它们实际上仍然是整型。
    value: float


class RejectException(Exception):
    """
    The smart contract rejected the transaction.
    """
    """
    智能合约拒绝了交易
    """
    pass


class SmartContract(object):
    """
    A fake smart contract.
    """
    """
    一个假的智能合约
    """

    def __init__(self):
        self.address: Address = f'{type(self).__name__}-{id(self)}'
        """ The address of this contract. """

        self.owner: Optional[Address] = None
        """ The owner of this contract. """


@singleton
@dataclass
class TimeMock(object):
    """
    Helps fake the current time (in seconds).
    Ideally the value returned is an integer (like `now` in Solidity) but this is not guaranteed.
    Normally in an Ethereum smart contract `now` can be called.
    To speed up simulations, use this class to get the current time.
    """
    """
    帮助仿造当前时间（秒）
    理想上，值返回的是一个整型，但这是不受保证的
    在以太坊，通常智能合约的 now 可以被回调
    为加速模拟，使用类获取当前时间
    """

    _time: float = field(default=0, init=False)

    def __call__(self, *args, **kwargs):
        """ Get the currently set time (in seconds). """
        return self._time

    def add_time(self, amount):
        """ Add `amount` (in seconds) to the current time. """
        self._time += amount

    def set_time(self, time_value):
        """ Set the time to return when `time()` is called. """
        self._time = time_value

    def time(self):
        """ Get the currently set time (in seconds). """
        return self._time
