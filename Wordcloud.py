
def cloud():

    from wordcloud import WordCloud, STOPWORDS
    import matplotlib.pyplot as plt
    import wikipedia
    from PIL import Image
    import numpy as np

    term="Bitcoin"

    def find_term():
        title=wikipedia.search(term)[0]
        page=wikipedia.page(title)
        return page.content

    def cloud(text):
        junk=set(STOPWORDS)
        mask=np.array(Image.open('mask9.png'))
        cloud=WordCloud(background_color='black',mask=mask,stopwords=junk).generate(text)
        plt.imshow(cloud)
        plt.axis('off')
        plt.savefig('cloud.png',bbox_inches='tight')
        plt.show()

    cloud(find_term())

