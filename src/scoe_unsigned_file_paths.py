#
# fle_path = r"C:\Users\code1\Desktop\_Work\SCoE\2478_Clinical_Insights_Manager-1.1\other\CIM_ThickClient_Checks\signCheck_output.txt"
#
# with open(file=fle_path) as lv_input:
#     previous_line = ""
#     for lines in lv_input:
#         read_line = lines.strip()
#         if "Unsigned" in read_line:
#             print(previous_line[:-1])
#         previous_line = read_line


items = [
"C:\Program Files\Philips\CIM\Main\Product\DWrite.dll                         ",
r"C:\Program Files\Philips\CIM\Main\Product\ncrypt.DLL                         ",
r"C:\Program Files\Philips\CIM\Main\Product\NTASN1.dll                         ",
"C:\Program Files\Philips\CIM\Main\Product\cscapi.dll                         ",
r"C:\Program Files\Philips\CIM\Main\Product\rasman.dll                         ",
"C:\Program Files\Philips\CIM\Main\Product\lsm.dll                            ",
"C:\Program Files\Philips\CIM\Main\Product\HvHostSvc.dll                      ",
"C:\Program Files\Philips\CIM\Main\Product\AzRoles.dll                        ",
"C:\Program Files\Philips\CIM\Main\Product\cscsvc.dll                         ",
"C:\Program Files\Philips\CIM\Main\Product\cscsvc.dll                         ",
"C:\Program Files\Philips\CIM\Main\Product\cscsvc.dll                         ",
r"C:\Program Files\Philips\CIM\Main\Product\tssdjet.dll                        ",
r"C:\Program Files\Philips\CIM\Main\Product\tssdjet.dll                        ",
"C:\Program Files\Philips\CIM\Main\Product\wmp.dll                            ",
"C:\Program Files\Philips\CIM\Main\Product\wmp.dll                            ",
r"C:\Program Files\Philips\CIM\Main\Product\rdpcorets.dll                      ",
r"C:\Program Files\Philips\CIM\Main\Product\rdpcorets.dll                      ",
r"C:\Program Files\Philips\CIM\Main\Product\rdpcorets.dll                      ",
r"C:\Program Files\Philips\CIM\Main\Product\rdpcorets.dll                      ",
r"C:\Program Files\Philips\CIM\Main\Product\NetLogon.dll                       ",
r"C:\Program Files\Philips\CIM\Main\Product\NetLogon.dll	                      ",
"C:\Program Files\Philips\CIM\Main\Product\WsmRes.dll	                      ",
"C:\Program Files\Philips\CIM\Main\Product\WsmRes.dll	                      ",
"C:\Program Files\Philips\CIM\Main\Product\edputil.dll	                      ",
"C:\Program Files\Philips\CIM\Main\Product\CLDAPI.dll	                      ",
"C:\Program Files\Philips\CIM\Main\Product\FLTLIB.DLL	                      ",
"C:\Program Files\Philips\CIM\Main\Product\CRYPTBASE.dll	                  ",
"C:\Program Files\Philips\CIM\Main\Product\winnlsres.dll	                  ",
"C:\Program Files\Philips\CIM\Main\Product\Philips.Platform.XmlSerializers.dll",
r"C:\Program Files\Philips\CIM\Main\Product\ncrypt.DLL                         ",
r"C:\Program Files\Philips\CIM\Main\Product\NTASN1.dll                         ",
"C:\Program Files\Philips\CIM\Main\Product\msvcp110_win.dll                   ",
"C:\Program Files\Philips\CIM\Main\Product\MsftEdit.dll                       ",
"C:\Program Files\Philips\CIM\Main\Product\edputil.dll                        ",
"C:\Program Files\Philips\CIM\Main\Product\imageres.dll                       ",
"C:\Program Files\Philips\CIM\Main\Product\samcli.dll                         ",
"C:\Program Files\Philips\CIM\Main\Product\SAMLIB.dll                         ",
r"C:\Program Files\Philips\CIM\Main\Product\netutils.dll                       ",
"C:\Program Files\Philips\CIM\Main\Product\CLDAPI.dll                         ",
"C:\Program Files\Philips\CIM\Main\Product\FLTLIB.DLL                         ",
"C:\Program Files\Philips\CIM\Main\Product\LINKINFO.dll                       ",
"C:\Program Files\Philips\CIM\Main\Product\cscapi.dll                         ",
"C:\Program Files\Philips\CIM\Main\Product\srvcli.dll                         ",
"C:\Program Files\Philips\CIM\Main\Product\MsftEdit.dll                       ",
"C:\Program Files\Philips\CIM\Main\Product\imageres.dll                       ",
"C:\Program Files\Philips\CIM\Main\Product\log4net.dll                        ",
"C:\Program Files\Philips\CIM\Main\Product\Crypt32.dll                        ",
r"C:\Program Files\Philips\CIM\Main\Product\NTASN1.dll                         ",
]

new_list = []
for each_items in items:
    each_items = each_items.strip()
    new_list.append(each_items)

input_list = list(set(new_list))

# importing os module
import os

# importing shutil module
import shutil

source = "C:\Temp\cim\hello-world-x86_SCoE.dll"

# Destination path
for items in input_list:
    name = items.split("\\")[-1]
    destination = f"C:\\Temp\\cim\\{name}"
    # print(destination)
    dest = shutil.copyfile(source, destination)

# Copy the content of
# source to destination
