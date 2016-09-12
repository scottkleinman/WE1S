## Setup

### Requirements
1. Python 2.7 and up, but not Python 3.
2. The corresponding `pip`. To install `pip`, follow the instructions [here](https://pip.pypa.io/en/stable/installing/).


### Dependencies
Dependencies required by this application are listed in `requirements.txt`. To install dependencies, run 

```bash
pip install -r requirements.txt
```


### Configurations
1. Create an instance configuration file `instance/config.py` based on the template file at `instance/config.py.temp`. 
Configurations in this file should be instance-dependent, and thus the file is ignored in Git. 
2. `config.py` is another configuration file for rest of the configurations. Adjust them if needed.

## Run
1. Make sure that 