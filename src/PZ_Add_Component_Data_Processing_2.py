with open("data.txt", 'r') as my_data:
    line_count = 0
    names = []
    duplicates = []
    for lines in my_data:
        if line_count == 2:
            names.append(lines)
            line_count = 0
        else:
            line_count += 1
            # if line_count == 3:
            #     line_count = 0
    for each_link in names:
        print(each_link.strip())
    #
    # for each_name in names:
    #     if names.count(each_name) > 1:
    #         duplicates.append(each_name)
    # for items in duplicates:
    #     print(items.strip())