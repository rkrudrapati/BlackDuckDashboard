import csv
output=["PACKAGE NAME",
        "PACKAGE VERSION",
        "CVE",
        "CVE STATUS",
        "CVE SUMMARY",
        "CVSS v2 BASE SCORE",
        "CVSS v3 BASE SCORE",
        "VECTOR",
        "MORE INFORMATION"
        ]
# output = []
my_dictionary = {}
# with open(file=r"C:\Users\code1\Desktop\_Work\Yacto\test.txt", mode='a') as writer:
with open(file=r"C:\Users\code1\Desktop\_Work\Yacto\test.csv", mode='w', newline='', encoding="utf8") as csvfile:
    fieldnames = output
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    with open(file=r"C:\Users\code1\Desktop\_Work\Yacto\core-image-minimal-qemuarm-20200507192641.rootfs.cve", mode="r", encoding="utf8") as cve_data:
        for lines in cve_data.readlines():
            if lines != "\n":
                lines = lines.replace("\n", "")
                key = lines[:lines.index(":")]
                value = lines[lines.index(":")+1:]
                value = (value.strip())
                my_dictionary.update({key:value})
            else:
                writer.writerow(my_dictionary)
                my_dictionary = {}