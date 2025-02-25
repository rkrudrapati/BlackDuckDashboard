import csv

recepie_name = ""
package_Name = ""
package_Version = ""
license = ""
summary = ""


csv_file = r"C:\Users\code1\Desktop\_Work\SBOM\Phase2\Lars\OSS_in_CSV.csv"
# csv_file = r"C:\Users\code1\Desktop\_Work\SBOM\Phase2\Eleva\DXR_Eleva_OperatingSystem-AWS-2X_1607.0.5_2020-05-29_115513\components_2020-05-29_115513.csv"
with open(csv_file,mode="r") as details:
    for items in csv.reader(details):
        project_Name = "IntelliVue"
        # project_Name = "IntelliVue"
        recepie_name = items[0]
        if not 'Unknown' in recepie_name:
            package_Name = items[1]
            package_Version = items[2]
            license = items[3]
            spdx_id = "SPDXRef-"+ package_Name.replace(" ", "-")
            PackageComment = "<text>PURL is pkg:supplier/{}/{}@{}</text>".format(recepie_name, package_Name.replace(" ", "-"), package_Version)
            # summary = items[4]
            # SPDXRef-INFUSION CONTAINS SPDXRef-Windows-Embedded-Standard-7-SP1
            Relationship = "SPDXRef-{} CONTAINS {}".format(project_Name, spdx_id)

            temp1 = """        PackageName: {0}
            SPDXID: {1}
            PackageComment: {2}
            PackageVersion: {3}
            PackageSupplier: {4}
            Relationship: {5}
            PackageDownloadLocation: NOASSERTION
            FilesAnalyzed: false
            PackageLicenseConcluded: NOASSERTION
            PackageLicenseDeclared: {6}
            PackageCopyrightText: NOASSERTION
            
            """.format(package_Name, spdx_id, PackageComment, package_Version, recepie_name, Relationship, license)
            print(temp1)