import os

print(*[filename.split(".")[0] for filename in os.listdir("./opinions")], sep="\n") #*zamienia liste elementow na niezalezne elementy


