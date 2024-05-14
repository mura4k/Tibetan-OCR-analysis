import re

with open("transliteration TCCG-001_471_500.txt", "r") as f:
    text = f.read()
text = re.split(r"\nPage \d\d\d\d\n\n", text)
for i in range(471, 501):
    filename = "0" + str(i) + ".txt"
    with open(filename, "w") as f:
        f.write(text[i - 471])
