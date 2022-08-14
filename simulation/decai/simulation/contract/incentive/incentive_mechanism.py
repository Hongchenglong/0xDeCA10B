from abc import ABC, abstractmethod

import math

from decai.simulation.contract.data.data_handler import StoredData
from decai.simulation.contract.objects import Address, SmartContract


class IncentiveMechanism(ABC, SmartContract):
    """
    Defines incentives for others to contribute "good" quality data.
    """
    """
    定义为其他人贡献good质量数据的激励
    """

    def __init__(self, refund_time_s=math.inf, any_address_claim_wait_time_s=math.inf):
        super().__init__()
        self.refund_time_s = refund_time_s
        """
        Amount of time to wait to get a refund back.
        Once this amount of time has passed, the entire deposit can be reclaimed.
        Also once this amount of time has passed, the deposit (in full or in part) can be taken by others.
        Default to not allowing refunds.
        """

        self.any_address_claim_wait_time_s = any_address_claim_wait_time_s
        """
        Amount of time after which anyone can take someone's entire remaining deposit.
        The purpose of this is to help ensure that value does not get "stuck" in a contract.
        This must be greater than the required amount of time to wait for attempting a refund.
        Contracts may want to enforce that this is much greater than the amount of time to wait for attempting a refund
        to give even more time to get the deposit back and not let others take too much.
        """

    @abstractmethod
    def distribute_payment_for_prediction(self, sender: str, value: float):
        """
        Share `value` with those that submit data.

        :param sender: The address of the one calling prediction.
        :param value: The amount sent with the request to call prediction.
        """
        """
        与共享数据的人分享value
        
        :param sender: 调用预测的人的地址
        :param value: 调用预测的请求的发送数量
        """
        pass

    @abstractmethod
    def handle_add_data(self, contributor_address: Address, msg_value: float, data, classification) \
            -> (float, bool):
        """
        Determine if the request to add data is acceptable.

        :param contributor_address: The address of the one attempting to add data
        :param msg_value: The value sent with the initial transaction to add data.
        :param data: A single sample of training data for the model.
        :param classification: The label for `data`.
        :return: tuple
            The cost required to add new data.
            `True` if the model should be updated, `False` otherwise.
        """
        """
        决定添加数据的请求是否是可接受的
        
        :param contributor_address: 尝试添加数据的人的地址
        :param msg_value: 和初始交易一起发送去添加数据的值
        :param data: 模型的一个训练样本
        :param classification: 数据的标签
        :return: tuple
            The cost required to add new data.
            添加新数据需要的花费
            `True` if the model should be updated, `False` otherwise.
            如果模型上传返回True
        """
        pass

    @abstractmethod
    def handle_refund(self, submitter: str, stored_data: StoredData,
                      claimable_amount: float, claimed_by_submitter: bool,
                      prediction) -> float:
        """
        Notify that a refund is being attempted.

        :param submitter: The address of the one attempting a refund.
        :param stored_data: The data for which a refund is being attempted.
        :param claimable_amount: The amount that can be claimed for the refund.
        :param claimed_by_submitter: True if the data has already been claimed by `submitter`, otherwise false.
        :param prediction: The current prediction of the model for data
            or a callable with no parameters to lazily get the prediction of the model on the data.
        :return: The amount to refund to `submitter`.
        """
        """
        通知正在尝试退还
        
        :param submitter: 尝试退还的人的地址
        :param stored_data: 正在尝试退款的数据
        :param claimable_amount: 这次退款可以申请的数量
        :param claimed_by_submitter: 如果提交者已经声明了数据返回true
        :param prediction: The current prediction of the model for data
            or a callable with no parameters to lazily get the prediction of the model on the data.
            
            目前模型预测 或 无参回调懒加载去预测模型
        :return: The amount to refund to `submitter`.
        """
        pass

    @abstractmethod
    def handle_report(self, reporter: str, stored_data: StoredData, claimed_by_reporter: bool, prediction) \
            -> float:
        """
        Notify that data is being reported as bad or old.

        :param reporter: The address of the one reporting about the data.
        :param stored_data: The data being reported.
        :param claimed_by_reporter: True if the data has already been claimed by `reporter`, otherwise false.
        :param prediction: The current prediction of the model for data
            or a callable with no parameters to lazily get the prediction of the model on the data.
        :return: The amount to reward to `reporter`.
        """
        """
        通知 数据被报告为是坏的还是旧的

        :param reporter: 报告数据的地址
        :param stored_data: 被报告的数据
        :param claimed_by_reporter: True if the data has already been claimed by `reporter`, otherwise false.
        :param prediction: The current prediction of the model for data
            or a callable with no parameters to lazily get the prediction of the model on the data.
        :return: 奖励给报告者的数量
        """
        pass
