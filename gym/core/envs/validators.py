import numpy as np
class Validator():

    """
        The validator class is to represent the validator in the PoS Ethereum Blockchain.

        Parameters:
            self. strategy : The strategy of the validator, 0 for honest, 1 for malicious
            self. status : The status of the validator, 0 for propose, 1 for vote
            self. current_balance : The current balance of the validator
    """

    def __init__(self, strategy, status, current_balance, proportion, total_active_balance) -> None:
        self.strategy = strategy 
        self.status = status
        self.current_balance = current_balance
        self.proportion = proportion
        self.total_active_balance = total_active_balance

    def get_strategy(self) -> int:
        return self.strategy
    
    def get_status(self) -> int:
        return self.status
    
    def get_current_balance(self) -> float:
        self.current_balance = self.current_balance + self.duty_weight() * self.base_reward() * self.proportion
        return self.current_balance
        
    def get_base_reward(self) -> float:
        base_reward = self.get_effective_balance() / (4 * np.sqrt(self.total_active_balance))
        return base_reward
    
    def get_effective_balance(self) -> float:
        
        return 0
    
    def duty_weight(self) -> float:
        if self.strategy == 0 and self.status == 0:
            return 1/8
        elif self.strategy == 0 and self.status == 1:
            return 7/8
        elif self.strategy == 1 and self.status == 0:
            return 0
        elif self.strategy == 1 and self.status == 1:
            return 7/8
        else:
            return 0

