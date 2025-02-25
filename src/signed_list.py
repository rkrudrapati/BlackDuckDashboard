import json
EICAR = "$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!"
# EICAR = "X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"

# file_name = r"C:\Acquisitions\00000376-A6LDx113542\00000376-A6LDx113542-uploadTracker.json"
file_name = r"C:\Acquisitions\00000367-A6LDx113542\00000367-A6LDx113542-uploadTracker.json"
search_text = "true"

# creating a variable and storing the text
# that we want to add
replace_text = "false"

# Opening our text file in read only
# mode using the open() function
with open(file_name, 'r') as file:
    # Reading the content of the file
    # using the read() function and storing
    # them in a new variable
    data = json.load(file)
    for items in data['Files']:
        items['Uploaded'] = items['Uploaded'].replace("true", "false")
    # Searching and replacing the text
    # using the replace() function
    data = data.replace(search_text, replace_text)

# Opening our text file in write only
# mode to write the replaced content
with open(file_name, 'w') as file:
    # Writing the replaced data in our
    # text file
    json.dump(data, file_name)

# Printing Text replaced
print("Text replaced")