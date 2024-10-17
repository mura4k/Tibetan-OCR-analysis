

text = input()
result = []
shad = '/'
igo = '@'
prev = text[0]
for i in range(1, len(text)):
    if text[i] == ' ':
        result.append(prev)
        prev = ''
    elif text[i] == shad:
        if prev[-1] == shad or prev == '':
            prev += shad
        else:
            result.append(prev)
            prev = shad
    elif text[i] == igo:
        if prev[-1] == igo or prev == '':
            prev += igo
        else:
            result.append(prev)
            prev = igo
    else:
        if prev == '':
            prev = text[i]
        elif prev[-1] == shad or prev[-1] == igo:
            result.append(prev)
            prev = text[i]
        else:
            prev += text[i]
result.append(prev)
print()
print(result)