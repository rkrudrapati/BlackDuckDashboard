#
# file_name = "2023-01-20.log"
# dir_name = "blackduck-bomengine"
# logs_dir = r"C:\Users\code1\Desktop\_temp\_delete\tajenkins_log_anly\standard"
# dir_tag = "app-log"
#
# search_param = "b520df32-4413-41be-b6f8-5c2f8c65ac30"
#
# distination_path = r"C:\Users\code1\Desktop\_temp\_delete\tajenkins_log_anly\forensic"
#
# full_path = f"{logs_dir}/{dir_name}/{dir_tag}/{file_name}"
# print(full_path)
# with open(full_path, 'r') as bdlogs:
#     for lines in bdlogs.readlines():
#         if search_param in lines:
#             print(lines.strip())

import os

target = r"C:\Users\code1\Desktop\_temp\_delete\tajenkins_log_anly\standard"
search_param = "b520df32-4413-41be-b6f8-5c2f8c65ac30"
# C:\Users\code1\Desktop\_temp\_delete\tajenkins_log_anly\standard\
for root, dirs, files in os.walk(target):
    for file in files:
        if ".log" in file and ("-18" in file or "-19" in file or "-20" in file):
            new_file = True
            with open(os.path.join(root, file), "r") as bd_logs:
                if new_file:
                    current_path = os.path.join(root, file)
                    temp = current_path.split("standard")
                    dest_file_path = temp[1][1:].replace("\\", "_")
                    updated_file_path = temp[0] + "forensic\\" + dest_file_path
                    new_file = False
                for line in bd_logs:
                    if search_param in line:
                        with open(updated_file_path, 'a') as new_line:
                            new_line.writelines(line)
                            new_line.close()
                            # print(new_line)

