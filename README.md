# eth-el
## Replicable code for "Redesign Incentives in Proof-of-Stake Ethereum: An Interdisciplinary Approach of Reinforcement Learning and Mechanism Design"

## How to run the code
- Clone the repository to your local directory
- Install or upgrade pip: https://pip.pypa.io/en/stable/installation/

```
pip install --upgrade pip
```

- Run the code to install required packages
```
pip install -r requirements.txt
```
## Explanation of the files
- requirements.txt including all the installed packages is generated using the following code: 
  
```
pip freeze > requirements.txt
```
- the "gym" folder includes the Reinforcement Learning (RL) environment
- the "model" folder includes the RL algorithms
- the "tmp" folder stores the best RL algorithm
- the "results" folder stores the output data from trained RL
- the "analysis.ipynb" represents the virtualizations
- the "figures" folder saves the output figures from "analysis.ipynb"
- the "makefile" defines the short-cut of pytest command
