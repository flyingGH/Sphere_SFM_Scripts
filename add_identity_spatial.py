import os

def modify_and_save_file(input_filename, output_filename):
    append_string = "1.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 1.0"

    if not os.path.exists(input_filename):
        print(f"Error: The file {input_filename} does not exist.")
        return

    try:
        with open(input_filename, 'r') as file:
            lines = file.readlines()

        output_content = "#F=N X Y Z R\n"

        for line in lines:
            if line.strip() and not line.startswith("#") and not line.startswith("E"):  
                parts = line.split()
                formatted_line = ' '.join(parts) + " " + append_string
                output_content += formatted_line + "\n"

        print(output_content)

        with open(output_filename, 'w') as file:
            file.write(output_content)

        print(f"Data has been successfully written to {output_filename}")

    except Exception as e:
        print(f"An error occurred: {e}")

input_file = 'geo.txt'
output_file = 'POS.txt'
modify_and_save_file(input_file, output_file)
