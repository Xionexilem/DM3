n = 6
with open('cipher17.txt', encoding='utf_8') as file:
    text = file.readline()
text += ' ' * (n - len(text) % n)
decoded_text = ''
for i in range(0, len(text), n):
    string = text[i:i+n]
    new_string = string[0:3] + string[5] + string[3:5]
    decoded_text += new_string
print(decoded_text)
