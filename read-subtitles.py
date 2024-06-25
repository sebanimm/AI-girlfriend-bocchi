import re

filtered_script = ""
pattern = r"(?<=（ひとり）)[^（|♪]*"

for i in range(1, 13):
    with open(f"txt-files/E{i:02}.txt", "r", encoding="utf-8") as file:
        text = file.read()
        matches = re.findall(pattern, text)

        for match in matches:
            filtered_script += match

    filtered_script += "\n"


with open("script.txt", "w", encoding="utf-8") as file:
    file.write(filtered_script)
