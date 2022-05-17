file_input = input("Enter full file name: ")

try:
    file = open(file_input)
except:
    print("Too bad,", file_input, "doesn't exist. :(")
    quit() # basically completely exit from program and do not run any code from here on

count = 0

for ln in file:
    if ln.startswith('From'):
        count += 1
    print(ln)

print("There were", count, "email recipients in", file_input)

file.close()