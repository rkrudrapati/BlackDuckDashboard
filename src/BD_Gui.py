# import tkinter as tk
#
# root = tk.Tk()
# root.geometry("400x300")
# root.title("Project Details")
#
# # Project Name Label and Entry Field
# project_name_label = tk.Label(root, text="Project Name:")
# project_name_label.pack()
# project_name_entry = tk.Entry(root)
# project_name_entry.pack()
#
# # Version Name Label and Entry Field
# version_name_label = tk.Label(root, text="Version Name:")
# version_name_label.pack()
# version_name_entry = tk.Entry(root)
# version_name_entry.pack()
#
# # Business Name Label and Entry Field
# business_name_label = tk.Label(root, text="Business Name:")
# business_name_label.pack()
# business_name_entry = tk.Entry(root)
# business_name_entry.pack()
#
# # Business Group Label and Entry Field
# business_group_label = tk.Label(root, text="Business Group:")
# business_group_label.pack()
# business_group_entry = tk.Entry(root)
# business_group_entry.pack()
#
# # Project Owner Label and Entry Field
# project_owner_label = tk.Label(root, text="Project Owner:")
# project_owner_label.pack()
# project_owner_entry = tk.Entry(root)
# project_owner_entry.pack()
#
# # Comments Label and Entry Field
# comments_label = tk.Label(root, text="Comments:")
# comments_label.pack()
# comments_entry = tk.Entry(root)
# comments_entry.pack()
#
# root.mainloop()

import tkinter as tk

root = tk.Tk()
root.geometry("400x400")
root.title("Project Details")


# Function to be called when the submit button is clicked
def submit():
    project_name = project_name_entry.get()
    version_name = version_name_entry.get()
    business_name = business_name_entry.get()
    business_group = business_group_entry.get()
    project_owner = project_owner_entry.get()
    comments = comments_entry.get()

    # Clear the text field
    text_field.delete("1.0", tk.END)

    # Print the values to the text field
    text_field.insert(tk.END, "Project Name: " + project_name + "\n")
    text_field.insert(tk.END, "Version Name: " + version_name + "\n")
    text_field.insert(tk.END, "Business Name: " + business_name + "\n")
    text_field.insert(tk.END, "Business Group: " + business_group + "\n")
    text_field.insert(tk.END, "Project Owner: " + project_owner + "\n")
    text_field.insert(tk.END, "Comments: " + comments)


# Project Name Label and Entry Field
project_name_label = tk.Label(root, text="Project Name:")
project_name_label.pack()
project_name_entry = tk.Entry(root)
project_name_entry.pack()

# Version Name Label and Entry Field
version_name_label = tk.Label(root, text="Version Name:")
version_name_label.pack()
version_name_entry = tk.Entry(root)
version_name_entry.pack()

# Business Name Label and Entry Field
business_name_label = tk.Label(root, text="Business Name:")
business_name_label.pack()
business_name_entry = tk.Entry(root)
business_name_entry.pack()

# Business Group Label and Entry Field
business_group_label = tk.Label(root, text="Business Group:")
business_group_label.pack()
business_group_entry = tk.Entry(root)
business_group_entry.pack()

# Project Owner Label and Entry Field
project_owner_label = tk.Label(root, text="Project Owner:")
project_owner_label.pack()
project_owner_entry = tk.Entry(root)
project_owner_entry.pack()

# Comments Label and Entry Field
comments_label = tk.Label(root, text="Comments:")
comments_label.pack()
comments_entry = tk.Entry(root)
comments_entry.pack()

# Submit Button
submit_button = tk.Button(root, text="Submit", command=submit)
submit_button.pack()

# Text Field
text_field = tk.Text(root)
text_field.pack()

root.mainloop()
