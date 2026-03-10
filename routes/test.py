import os

path = "./files/javafx"
files = []
print(os.listdir(path))
for file in os.listdir(path):
    files.append(file)

print(files)
