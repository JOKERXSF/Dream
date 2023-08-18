import jieba
from matplotlib import pylab as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np
from pymysql import connect
import json


def get_img(field, targetImgSrc, resImgSrc):
    con = connect(host="localhost", user="root", password="123456", database="dreaminfo", port=3306, charset="utf8")
    cursor = con.cursor()
    sql = f"select  {field} from jobinfo"
    cursor.execute(sql)
    data = cursor.fetchall()
    text = ''
    for i in data:
        text += i[0]
        # if i[0] != '无':
        #     companyTagsArr = json.loads(i[0])[0].split('，')
        #     for j in companyTagsArr:
        #         text += j
    cursor.close()
    con.close()
    data_cut = jieba.cut(text, cut_all=False)
    stop_words = []
    with open('./Dreamapp/stopwords.txt', 'r', encoding='utf8') as rf:
        for line in rf:
            if len(line) > 0:
                stop_words.append(line.strip())
    data_result = [x for x in data_cut if x not in stop_words]
    string = ' '.join(data_result)

    img = Image.open(targetImgSrc)
    img_arr = np.array(img)
    wc = WordCloud(
        background_color='white',
        mask=img_arr,
        font_path='STHUPO.TTF'
    )
    wc.generate_from_text(string)

    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')

    plt.savefig(resImgSrc, dpi=800)


#get_img('companyTags', '../Dream-master/static/3.png', '../Dream-master/static/companyTags_cloud2.png')
get_img('title', '../Dream-master/static/1.png', '../Dream-master/static/companyTags_cloud.png')
