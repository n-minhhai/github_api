# Dependancies
- import requests
- import json
- from datetime import datetime, timedelta

# How to Run

Run script.py with 2 arguments corresponding to {owner, repository}, with a third optional argument to determine the N number of pull requests

Example:
Without third argument, with N=10 by default<br />
> python script.py scikit-learn scikit-learn

With third argument, where N=15<br />
> python script.py scikit-learn scikit-learn 15

Example result with N=15:<br />
{
    "Less than 1 hour": 7,
    "Between 1 hour and 1 day": 6,
    "More than 1 day": 2
}


# Test

Run script.py with no arguments to use a mock API created using mockapi.io. This is to ensure the data remains static.<br />
First 3 data entries with IDs 1,2,3 are expected to be filtered out since they do not have CLOSED state (similar to merged pull requests)<br />
Data entries with IDs 4,5,6 are expected to be filtered out since they do not have APPROVED state (similar to merged pull requests with approved reviews)

Example: 
> python script.py

Example result: <br />
Merged Pull Request with Approved Review: (ID) 7, Time difference: Less than 1 hour<br />
Merged Pull Request with Approved Review: (ID) 8, Time difference: Between 1 hour and 1 day<br />
Merged Pull Request with Approved Review: (ID) 9, Time difference: Less than 1 hour<br />
Merged Pull Request with Approved Review: (ID) 10, Time difference: Between 1 hour and 1 day<br />
Merged Pull Request with Approved Review: (ID) 11, Time difference: Less than 1 hour<br />
Merged Pull Request with Approved Review: (ID) 12, Time difference: Between 1 hour and 1 day<br />
Merged Pull Request with Approved Review: (ID) 13, Time difference: Between 1 hour and 1 day<br />
Merged Pull Request with Approved Review: (ID) 14, Time difference: Between 1 hour and 1 day<br />
Merged Pull Request with Approved Review: (ID) 15, Time difference: Less than 1 hour<br />
Merged Pull Request with Approved Review: (ID) 16, Time difference: Between 1 hour and 1 day<br />
{
    "Less than 1 hour": 4,
    "Between 1 hour and 1 day": 6,
    "More than 1 day": 0
}
