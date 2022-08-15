import os
import sys
from typing import Optional
from injector import Injector

# For `bokeh serve`.
# Bokeh is a Python library for creating interactive visualizations for modern web browsers.
# It helps you build beautiful graphics, ranging from simple plots to complex dashboards with streaming datasets.
# With Bokeh, you can create JavaScript-powered visualizations without writing any JavaScript yourself.
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from decai.simulation.contract.classification.perceptron import PerceptronModule
from decai.simulation.contract.collab_trainer import DefaultCollaborativeTrainerModule
from decai.simulation.contract.incentive.stakeable import StakeableImModule
from decai.simulation.data.imdb_data_loader import ImdbDataModule
from decai.simulation.logging_module import LoggingModule
from decai.simulation.simulate import Agent, Simulator

num_words = 1000
# 可选类型，等价于 Union[X, None]
train_size: Optional[int] = None
if train_size is None:
    init_train_data_portion = 0.08
else:
    init_train_data_portion = 100 / train_size


def main():
    # Set up the agents that will act in the simulation.
    # 设置将在模拟起作用的代理
    agents = [
        # Good
        Agent(address="Good",
              start_balance=10_000,
              mean_deposit=50,  # 平均保证金
              stdev_deposit=10,  # 标准保证金
              mean_update_wait_s=10 * 60,
              prob_mistake=0.0001,
              ),
        # Malicious: A determined agent with the goal of disrupting others.
        Agent(address="Bad",
              start_balance=10_000,
              mean_deposit=100,
              stdev_deposit=3,
              mean_update_wait_s=1 * 60 * 60,
              good=False,
              ),
        # One that just calls the model and pays to use the model.
        Agent(address="Caller",
              start_balance=30_000,
              mean_deposit=0,
              stdev_deposit=0,
              mean_update_wait_s=2 * 60 * 60,
              calls_model=True,
              pay_to_call=50
              ),
    ]
    # No caller (assume free to call).
    agents = agents[:-1]

    # Set up the data, model, and incentive mechanism.
    inj = Injector([
        DefaultCollaborativeTrainerModule,
        ImdbDataModule(num_words=num_words),
        LoggingModule,
        PerceptronModule,
        StakeableImModule,
    ])
    s = inj.get(Simulator)

    # Accuracy on hidden test set after training with all training data:
    baseline_accuracies = {
        100: 0.6210,
        200: 0.6173,
        1000: 0.7945,
        10000: 0.84692,
        20000: 0.8484,
    }

    # Start the simulation.
    s.simulate(agents,
               baseline_accuracy=baseline_accuracies[num_words],
               init_train_data_portion=init_train_data_portion,
               train_size=train_size,
               )


# Run with `bokeh serve PATH`.
# if __name__.startswith('bk_script_'):
if __name__ == '__main__':
    main()
