def print_formated_yarn_pkg(myList):
    local_pkgs_list = []
    for items in myList:
        items = items.replace('"', '').replace(":", '').replace('^','').replace(',','').replace('>=','').replace('<3','').strip()
        temp = items.split('@')
        for each in temp:
            if each != '':
                local_pkgs_list.append(each)
    # print(local_pkgs_list)
    for i in range(0, local_pkgs_list.__len__(), 2):
            print('{},{}'.format(local_pkgs_list[i],local_pkgs_list[i+1]))


with open(r'C:\Scan_Code\vue-dev\yarn.lock', 'r') as yarn_pkg:
    pkg_name = False
    for lines in yarn_pkg:
        string_utf = lines.encode(encoding='UTF-8')
        if pkg_name == True:
            print_formated_yarn_pkg(lines.split())
            pkg_name = False
        if string_utf == "\n".encode(encoding='UTF-8'):
            # print(previous_line.split())
            pkg_name = True

        # print(string_utf)