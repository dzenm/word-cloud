#!/usr/bin/env python

from wordcloud import (WordCloud, get_single_color_func)
import matplotlib.pyplot as plt


class SimpleGroupedColorFunc(object):
    def __init__(self, color_to_words, default_color):
        self.word_to_color = {word: color
                              for (color, words) in color_to_words.items()
                              for word in words}
        self.default_color = default_color
    def __call__(self, word, **kwargs):
        return self.word_to_color.get(word, self.default_color)

class GroupedColorFunc(object):
    def __init__(self, color_to_words, default_color):
        self.color_func_to_words = [
            (get_single_color_func(color), set(words))
            for (color, words) in color_to_words.items()]
        self.default_color_func = get_single_color_func(default_color)
    def get_color_func(self, word):
        try:
            color_func = next(
                color_func for (color_func, words) in self.color_func_to_words
                if word in words)
        except StopIteration:
            color_func = self.default_color_func
        return color_func
    def __call__(self, word, **kwargs):
        return self.get_color_func(word)(word, **kwargs)

text = """The Zen of Python, by Tim Peters
Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!"""

# Since the text is small collocations are turned off and text is lower-cased
wc = WordCloud(collocations=False).generate(text.lower())

# 自定义所有单词的颜色
color_to_words = {
    # # words below will be colored with a green single color function
    # '#00ff00': ['beautiful', 'explicit', 'simple', 'sparse',
    #             'readability', 'rules', 'practicality',
    #             'explicitly', 'one', 'now', 'easy', 'obvious', 'better'],
    # # will be colored with a red single color function
    # 'red': ['ugly', 'implicit', 'complex', 'complicated', 'nested',
    #         'dense', 'special', 'errors', 'silently', 'ambiguity',
    #         'guess', 'hard'],
}

default_color = 'grey'
grouped_color_func = GroupedColorFunc(color_to_words, default_color)

# 如果你也可以将color_func的参数设置为图片,详细的说明请看 下一部分
wc.recolor(color_func=grouped_color_func)

plt.figure()
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.show()
wc.to_file("diy_font_color_result.png")