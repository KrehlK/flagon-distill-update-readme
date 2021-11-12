# Segment Testing
import json
import pandas as pd
import segment

def getUUID(log, uid):
    return str(log['sessionID']) + str(log['clientTime']) + str(log["logType"]) + str(uid)

if __name__ == '__main__':
    jsonFile = "./sampleLogs2Session.json"

    with open(jsonFile) as json_file:
        rawData = json.load(json_file)

    data = {}
    i = 0
    for log in rawData:
        data[getUUID(log, i)] = log
        i += 1
    
    # Convert clientTime to Date/Time object
    for uid in data:
        log = data[uid]
        clientTime = log['clientTime']
        new_dateTime = pd.to_datetime(clientTime, unit='ms', origin='unix')
        log['clientTime'] = (new_dateTime - pd.Timestamp('1970-01-01')) // pd.Timedelta('1ms')
    
    # Sort
    sorted_data = sorted(data.items(), key = lambda kv: kv[1]['clientTime'])
    sorted_dict = dict(sorted_data)

    # Create Test Segment Tuples
    start_end_vals = []
    start_end_vals.append((sorted_data[1][1]['clientTime'], sorted_data[50][1]['clientTime']))
    start_end_vals.append((sorted_data[25][1]['clientTime'], sorted_data[50][1]['clientTime']))
    start_end_vals.append((sorted_data[50][1]['clientTime'], sorted_data[75][1]['clientTime']))

    segment_names = ["segment1", "segment2", "segment3"]

    # Call create segment
    result = segment.Segment.create_segment(sorted_dict, segment_names, start_end_vals)

    for segment in result:
        print(result[segment].segment_name)
        print(result[segment].num_logs)
        print()