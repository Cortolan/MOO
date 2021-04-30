FILE = "rss_links.txt"

input_data = open(FILE, 'r')
check_line = input_data.readline()
check_line = check_line.rstrip()

lines = []

while check_line:
    found = False
    for line in lines:
        if line == check_line:
            found = True
            break
    
    if found == False:        
        lines.append(check_line)
    
    check_line = input_data.readline()
    check_line = check_line.rstrip()
input_data.close()

output_data = open(FILE, 'w')
for line in lines:
    output_data.write(line + "\n")
  