from os import walk, path
import icecream as ic

i = 0
with open('C:\BlackDuck Dashboard\output.csv','w', encoding='cp1252') as my_output_data:
    for root, dirs, files in walk(r'C:\BlackDuck Dashboard\vuln'):
        for name in files:
            file_path = path.abspath(path.join(root, name))
            with open(file_path, 'r') as my_input_data:
                temp_input = my_input_data.readlines()
                for each_line in temp_input:
                    print(each_line.strip())
                    my_output_data.writelines(each_line)
                    i += 1
            my_input_data.close()
my_output_data.close()
print(i)