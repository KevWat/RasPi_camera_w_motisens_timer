#!python3.7
# config: UTF-8
import requests
################################
# Upload on Slack
################################
#Upload Captured File
def slack_upload(filename):
    # Read Slack's token, channels
    # Mpved dir path due to support webApp_ctrl
    f = open('../../../config_slk.txt', 'r')
    data_lines = f.readlines() # Line0 = token, Line1 = channels
    f.close()
    
    # delete \n
    for i in range(len(data_lines)):
        data_lines[i] = data_lines[i].rstrip('\n')
        
    url = "https://slack.com/api/files.upload"
    data = {
        "token": data_lines[0],
        #"channels": "cats3",
        "channels": data_lines[1],
        "title": "Today's Picture"
        }
    files = {'file': open(filename, 'rb')}
    requests.post(url, data=data, files=files)
    print("Done: File Upload")
################################
'''
# test
slack_upload('test.jpg')
'''