import json
with open('input', 'r', encoding='UTF-8') as file_input:
    # print(file_input)
    json_input = json.load(file_input)
    list_input = []
    for each_item in json_input["items"]:
        # print(f"License Name: {each_item['name']}")
        # print(f"Link: {each_item['_meta']['href']}")
        list_input.append([each_item['name'], each_item['_meta']['href']])
    # for items in list_input:
    #     print(items)
print(list_input)
