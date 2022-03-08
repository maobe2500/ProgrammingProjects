from wordcloud import WordCloud

with open("AUSTEN.txt") as f:
    whole_text = f.read()

def clean_text(txt):
    txt.strip()
    new_text = ""
    for letter in txt:
        if (letter.isalpha()):
            new_text += letter
    return new_text

def get_frequencies(clened_text):
    frequencies = {}
    txt = clened_text.split(" ")
    for word in txt:
        frequencies[word] = txt.count(word)
    return frequencies
    


t = clean_text(whole_text)
frequencies = get_frequencies(t)

cloud = wordcloud.WordCloud()
cloud.generate_from_frequencies(frequencies)
cloud.to_file("myfile.jpg")
