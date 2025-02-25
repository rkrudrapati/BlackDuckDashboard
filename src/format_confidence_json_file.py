# "C:\Users\code1\Downloads\sample.json"
import json
from icecream import ic

ic.disable()
filename = input(r'''enter the path to sample.json file. 
Eg: C:\Users\Downloads\sample.json
Enter here: ''')
filename = filename.strip('"')

header = 'Component Name,Version,Match Type,Confidence'
op = open(r'C:\Users\code1\Desktop\Work\Lumea_FP\formattedjson.csv', 'w', encoding='UTF8')
op.writelines(header+"\n")
report = ""
with open(filename, 'r') as json_input:
    convert_to_json = (json.loads(json_input.read()))
    for items in convert_to_json:
        # print(items)
        report = ""
        if 'declaredComponentPath' in items:
            temp = items['declaredComponentPath']
            value = temp.split('/')[-1]
            value = value.replace(':', ',')
            report = report + value
            for matches in items['matches']:
                report = report + ',' + matches['matchType']
                report = report + ',' + str(matches['matchConfidencePercentage'])
            ic(report)
            op.writelines(report+"\n")
        elif 'uri' in items:
            report = items['uri'].split('/')[-1]
            for matches in items['matches']:
                report = report + ',,' + matches['matchType']
                report = report + ',' + str(matches['matchConfidencePercentage'])
            ic(report)
            op.writelines(report+"\n")
        else:
            print("missed items: \n" %items)
op.close()
print(r"Output file can be found here: C:\Users\code1\Desktop\Work\Lumea_FP")