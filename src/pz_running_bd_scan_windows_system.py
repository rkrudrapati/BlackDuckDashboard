from os import system

my_input = """
C:\Program Files
C:\Program Files (x86)
C:\Python27
"""


my_input = my_input.split('\n')
my_token = ""
project_name = ""
version_name = ""

command = '''powershell "[Net.ServicePointManager]::SecurityProtocol = 'tls12'; irm https://detect.synopsys.com/detect.ps1?$(Get-Random) | iex; detect" \
            --blackduck.url=https://blackduckweb.philips.com --blackduck.api.token={0} --detect.project.name={2} --detect.project.version.name={3} \
            --blackduck.trust.cert=true --detect.source.path="{1}" --detect.detector.search.exclusion.paths=/tst/ --detect.bom.aggregate.name={3}_aggregate_bom'''
for item in my_input:
    if item != "" :
        updated_command = command.format(my_token, item, project_name, version_name)
        print(updated_command)
        system(updated_command)
