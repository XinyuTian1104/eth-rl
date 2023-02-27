class Validator():

    """
        The validator class is to represent the validator in the PoS Ethereum Blockchain.

        Parameters:
            self. strategy : The strategy of the validator, 0 for honest, 1 for malicious
            self. status : The status of the validator, 0 for propose, 1 for vote
            self. current_balance : The current balance of the validator
    """

    def __init__(self, strategy, status, current_balance) -> None:
        self.strategy = strategy # The strategy of the validator
        self.status = status
        # self.current_balance = current_balance

    def get_strategy(self) -> int:
        return self.strategy
    
    def get_status(self) -> int:
        return self.status
    
    def get_current_balance(self) -> float:
        self.current_balance = self.current_balance + self.reward() - self.penalty()
        
        return self.current_balance
        
    def balance_update(self) -> float:
        balance_update = self.duty_weight() * self.base_reward()
        return self.current_balance + self.reward() - self.penalty()

    def base_reward(self) -> float:
        baseReward = self.get_effective_balance() * self.duty_weight()
        return 0
    
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

