import re
import os
from tkinter import Tk, Label, Entry, Button, filedialog

def extract_logical_part():
    def browse_input_file():
        filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if filepath:
            input_file_entry.delete(0, 'end')
            input_file_entry.insert('end', filepath)

    def browse_output_file():
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if filepath:
            output_file_entry.delete(0, 'end')
            output_file_entry.insert('end', filepath)

    def process_files():
        input_file = input_file_entry.get()
        output_file = output_file_entry.get()

        if input_file and output_file:
            with open(input_file, 'r') as file:
                content = file.read()

                content = re.sub(r'#include\s*<.*?>', '', content)
                content = remove_comments(content)

                logical_part = []

                lines = content.strip().split('\n')

                for line in lines:
                    line = process_line(line)
                    if line is not None:
                        logical_part.append(line)

                if logical_part:
                    if logical_part[0] == "{":
                        logical_part.pop(0)
                    if logical_part[-1] == "}":
                        logical_part.pop()

                    logical_part.insert(0, "----------Logical Part Starts----------")
                    logical_part.append("----------Logical Part Ends----------")

                if logical_part:
                    if os.path.isfile(output_file):
                        with open(output_file, 'w') as outfile:
                            outfile.write('\n'.join(logical_part))
                    else:
                        with open(output_file, 'w') as outfile:
                            outfile.write('\n'.join(logical_part))
                    result_label.config(text='Logical part extracted and stored in:\n' + output_file)
                else:
                    result_label.config(text='No logical part found in the input file.')
        else:
            result_label.config(text='Please provide input and output file paths.')

    def remove_comments(content):
        content = re.sub(r'//.*', '', content)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        return content.strip()

    def process_line(line):
        line = line.strip()

        if line is None or line == "":
            return None
        

        if re.match(r'\b(int|double|void|string|char|float|return)\b', line) and '=' not in line:
            line = None

        if line is not None:
            
            format_specifiers = re.findall(r'%[a-zA-Z]', line)
            variables = re.findall(r'(?<=",)\s*([^,]+)', line)
            for i in range(min(len(format_specifiers), len(variables))):
                line = line.replace(format_specifiers[i],variables[i])
            line = re.sub(r',\s*[^,]+', '', line)
            
            # Replacing '\n' and '\t'
            line = line.replace("\n", ' ').replace('\t', ' ')
                
            if "scanf" in line:
                line = "INPUT------>" + line.replace('\n', '\t').replace('\\n', '\t')
                line = re.sub(r'scanf\s*\((.*?)\)', r'scanf \1', line)
                line = re.sub(r'scanf\s*([^,]*),\s*', r'scanf \1', line)
                line = re.sub(r'(scanf|"|%d|%f|&|;)', '', line)
            if "printf" in line:
                line = "OUTPUT------>" + line.replace('\n', '\t')
                line = re.sub(r'printf\s*\((.*?)\)', r'printf \1', line)
                line = re.sub(r'(printf|%s|&|;|")', '', line)
                line = re.sub(r'(printf|%[a-zA-Z]|&|;|\n)', '', line)
                
            if line == "return 0;" or line == "exit(0);":
                line = None

            if line is not None:
                line = line.replace('&&', 'AND')
                line = line.replace('||', 'OR')

            if line is not None and line.endswith(';'):
                line = line[:-1]
                

        return line

    root = Tk()
    root.title("Extract Logical Part")
    root.geometry("400x280")
    root.configure(bg="#F5F5F5")  # Set background color

    # Input File
    input_file_label = Label(root, text="Input File:", bg="#F5F5F5", fg="#333333", font=("Arial", 12))
    input_file_label.pack()
    input_file_entry = Entry(root, width=30)
    input_file_entry.pack(pady=5)

    browse_input_button = Button(root, text="Browse", command=browse_input_file, bg="#007BFF", fg="white")
    browse_input_button.pack(pady=5)

    # Output File
    output_file_label = Label(root, text="Output File:", bg="#F5F5F5", fg="#333333", font=("Arial", 12))
    output_file_label.pack()
    output_file_entry = Entry(root, width=30)
    output_file_entry.pack(pady=5)
    
    browse_output_button = Button(root, text="Browse", command=browse_output_file, bg="#007BFF", fg="white")
    browse_output_button.pack(pady=5)

    # Process Button
    process_button = Button(root, text="Process", command=process_files, bg="#28A745", fg="white", font=("Arial", 12))
    process_button.pack(pady=10)

    # Result Label
    result_label = Label(root, text="", bg="#F5F5F5", fg="#333333", font=("Arial", 12))
    result_label.pack()

    root.mainloop()

extract_logical_part()
