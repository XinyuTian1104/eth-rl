def duty_weight(strategy, status):
    if strategy == 0 and status == 0:
        return 1/8
    elif strategy == 0 and status == 1:
        return 7/8
    elif strategy == 1 and status == 0:
        return 0
    elif strategy == 1 and status == 1:
        return 7/8
    else:
        return 0
    
def base_reward(validator_action, strategy, status):
    if validator_action == 1:
        return self.alpha
    elif validator_action == 0 and strategy == 1:
        return self.beta
    elif validator_action == 0 and strategy == 0 and status == 1:
        return self.gamma
    elif validator_action == 0 and strategy == 0 and status == 0:
        return self.delta
    else:
        return 0
    
def reward(validator_action, strategy, status):
    if validator_action == 1:
        return self.alpha
    elif validator_action == 0 and strategy == 1:
        return self.beta
    elif validator_action == 0 and strategy == 0 and status == 1:
        return self.gamma
    elif validator_action == 0 and strategy == 0 and status == 0:
        return self.delta
    else:
        return 0
    
def penalty(self, validator_action, strategy, status):
    if validator_action == 1:
        return self.alpha
    elif validator_action == 0 and strategy == 1:
        return self.beta
    elif validator_action == 0 and strategy == 0 and status == 1:
        return self.gamma
    elif validator_action == 0 and strategy == 0 and status == 0:
        return self.delta
    else:
        return 0

