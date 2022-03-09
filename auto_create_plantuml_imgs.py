import os, shutil

source_dir = "plantuml/uml-relations"

command = f"java -jar D:/Downloads/plantuml.jar {source_dir}/*.plantuml"
print( "executing: " + command)

res = os.system(command)
print( "returned: ", res)

target_dir = "img/uml-relations"
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

for file in os.listdir(source_dir):
    if ".png" in file:
        print(file)
        shutil.move(source_dir + "/" + file, target_dir)
