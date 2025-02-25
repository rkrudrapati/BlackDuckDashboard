import os
import json


def print_formated_packages(data):
    for each_pkg in data:
        print('{},{}'.format(each_pkg, str(data[each_pkg]).replace("^","")))
        # line_to_list = each_pkg.strip().split(':')
        # pkg_name = line_to_list[0].split('"')[1]
        # pkg_version = line_to_list[1].split('"')[1].replace("^","")
        # # print(line_to_list)
        # print("{},{}".format(pkg_name, pkg_version))


def readjsondata(paths):
    with open(paths, 'r') as tempname:
        json_reader = json.load(tempname)
    tempname.close()
    for items in json_reader:
        if 'devDependencies' == items:
            print_formated_packages(json_reader['devDependencies'])
        if 'dependencies' == items:
            print_formated_packages(json_reader['dependencies'])
# paths = r'C:\Scan_Code\vue-dev\package.json'
# readjsondata(paths)


paths_list = []
pkg_mgr_list = ['package-lock.json', 'package.json']#, 'yarn.lock']
for root, dir, files in os.walk(r"C:\Scan_Code\vue-dev"):
    if "node_modules" in dir:
        continue
    for each_item in pkg_mgr_list:
        if each_item in files:
            paths_list.append(os.path.join(root, each_item))
for paths in paths_list:
    #print(paths+',')
    readjsondata(paths)
