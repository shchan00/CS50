import cs50

text = cs50.get_string("Text: ")
letters = 0
words = 1
sentences = 0
for i in range(len(text)):
    if (text[i].isalpha()):
        letters += 1
    elif (text[i] == " "):
        words += 1
    elif (text[i] in [".", "!", "?"]):
        sentences += 1
index = round(0.0588 * letters / words * 100 - 0.296 * sentences / words * 100 - 15.8)
if (index < 1):
    print("Before Grade 1")
elif (index > 16):
    print("Grade 16+")
else:
    print(f"Grade {index}")
