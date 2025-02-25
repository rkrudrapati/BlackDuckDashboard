with open(r"C:\temp\BDBA_ISO_VM_Analysis\yum_list_installed_more", 'r') as input_data:
    for lines in input_data:
        variable_list = lines.split()
        version = variable_list[1].split("-")
        print(variable_list[0]+"_"+version[0])


