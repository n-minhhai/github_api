import sys
import requests
import json
from datetime import datetime, timedelta

# convert to date time string format
def remove_chars(string):
    string = string.replace('T', ' ')
    string = string.replace('Z', '')
    string = string[:19]
    return string

# update the histogram of the time intervals between a merged pull request creation and the corresponding approved review
def update_histogram(bins, time):
    if time < timedelta(hours=1):
        bins[0] += 1
        result = 'Less than 1 hour'
    elif time > timedelta(hours=1) and time < timedelta(days=1):
        bins[1] += 1
        result = 'Between 1 hour and 1 day'
    else:
        bins[2] += 1
        result = 'More than 1 day'
    return bins, result

# github token for increased API requests
######################################################### PLEASE ADD USERNAME AND TOKEN
username = ''
token = ''
#########################################################

# state='closed' to filter out open pull requests that haven't been merged yet
# sort='created' to retrieve the most recent pull requests
payload = dict(
    state='closed',
    sort='created',
    direction='desc',
    per_page=100
)

# check if we are testing with mock API or performing requests on GITHUB
if len(sys.argv) < 3:
    mock = True
    url = 'https://6096a1f8116f3f00174b3625.mockapi.io/pulls'
else:
    mock = False
    # Retrieve pull requests of a given GitHub organisation and repository
    owner = sys.argv[1]
    repo = sys.argv[2]
    url = 'https://api.github.com/repos/{}/{}/pulls'.format(owner, repo)

# check for third optional argument for N
if len(sys.argv) == 4:
    n = int(sys.argv[3])
else:
    n = 10

count = 0 # number of merged pull requests with approved review retrieved
approved_IDs = [] # list of merged pull request IDs with approved reviews
histogram = [0, 0, 0] # final result to be returned

############################## UNCOMMENT TO USE GITHUB TOKEN
PR = requests.get(url=url, params=payload, auth=(username, token))
#PR = requests.get(url=url, params=payload)
if PR.status_code != 200:
    print('API Call Failed.')
    exit()

# iterate through closed pull requests and search for approved reviews
for pull_request in PR.json():

    ID = pull_request['number']

    if mock:
        reviews = requests.get(url=url + '/{}/reviews'.format(ID)) # retrieve reviews
    else:
        ############################################ UNCOMMENT TO USE GITHUB TOKEN
        reviews = requests.get(url=url + '/{}/reviews'.format(ID), params=payload, auth=(username, token))
        #reviews = requests.get(url=url + '/{}/reviews'.format(ID)) # retrieve reviews

    if (reviews.status_code != 200):
        continue
    
    # search for approved review
    for i in range(len(reviews.json())):
        if reviews.json()[i]['state'] == 'APPROVED':
            approved_IDs.append(ID)
    
            time_created_str = remove_chars(pull_request['created_at']) # remove unnecessary characters from timestamp
            time_created = datetime.strptime(time_created_str, '%Y-%m-%d %H:%M:%S') # convert to datetime format
            
            time_approved_received_str = remove_chars(reviews.json()[i]['submitted_at']) # remove unnecessary characters from timestamp
            time_approved_received = datetime.strptime(time_approved_received_str, '%Y-%m-%d %H:%M:%S') # convert to datetime format

            time_interval = time_approved_received - time_created
            histogram, result = update_histogram(histogram, time_interval) # update histogram count

            if mock:
                print('Merged Pull Request with Approved Review: (ID) {}, Time difference: {}'.format(ID, result))
            count += 1
            break
    # Stop when 10 merged pull requests with approved reviews were retrieved
    if count == n:
        break

json_histogram = json.dumps({'Less than 1 hour':histogram[0], 'Between 1 hour and 1 day':histogram[1], 'More than 1 day':histogram[2]}, indent=4)
print(json_histogram)

if mock:
    assert(PR.json()[0]['number'] == '4') # check that we only consider CLOSED pull requests 
    assert(approved_IDs[0] == '7') # check that we only consider approved reviews
    assert(histogram == [4,6,0])
