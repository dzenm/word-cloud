#encoding="utf-8"

from wordcloud import WordCloud

f=open(u'word.txt','r').read()
wordcloud=WordCloud(background_color="yellow",width=1000,height=800,margin=2).generate(f)

import matplotlib.pyplot as plt

plt.imshow(wordcloud)
plt.axis("off")
plt.show()

wordcloud.to_file("word_result.png")