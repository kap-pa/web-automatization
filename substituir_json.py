f = open("C:\\Users\Arnau\Desktop\pass.txt", "r")
new_json = []
for i in f.readlines():
    new_json.append(i.strip())
print(new_json)