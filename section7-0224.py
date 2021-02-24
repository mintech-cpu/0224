#!/usr/bin/env python
# coding: utf-8

# # 【第7回】不動産ページから情報取得する②
# 
# 前回の第6回目では、SUUMOのホームページから、物件情報だけ取得しました。
# 
# 
# 今回は、物件情報だけでなく、各部屋の情報まで取得していきたいと思います。
# 
# *※前回と同様に、少し複雑になってきます。なので、何回も動画を見て復習していただけると良いかなと思います！*
# 
# 
# <br>
# 
# なお、前回使ったソースコードは、そのまま使っていきたいので、以下に残してあります。
# 
# これらを実行してから、今回の内容に入っていきましょう！
# 
# *※動画の感想を、僕のTwitterにメンションしてツイートしていただけると嬉しいです（ ;  ; ）！*
# 
# Twitter : [@hayatasuuu](https://twitter.com/hayatasuuu)

# # まずは小さく情報取得してみる
# 
# スクレイピングで情報取得するとき、forループを使って繰り返し処理をすることが多いです。
# 
# でもまずは、forループを使わないでデータを取ってみましょう！
# 
# - 小さく情報取得してみる
# - 大丈夫そうだったらforループする
# 
# この手順で進めていこうと思います。

# ## ライブラリのインポート
# 
# まずは、ライブラリのインポートからやっていきます。
# 
# とは言っても、いつもとやることは変わりません。`Requests`と`BeautifulSoup`をインポートしていきましょう。

# In[1]:


from bs4 import BeautifulSoup
import requests


# ## RequestsでURLにアクセスしてHTMLを解析する
# 
# 次に`Requests`を使ってURLにアクセスし、HTMLを取得して解析していきます。
# 
# URLは`https://suumo.jp/chintai/tokyo/sc_shinjuku/`ですが、今回は以下のように書いておきたいと思います。

# In[2]:


# 変数urlにSUUMOホームページのURLを格納する
url = 'https://suumo.jp/chintai/tokyo/sc_shinjuku/?page={}'

# アクセスするためのURLをtarget_urlに格納する
target_url = url.format(1)

# print()してtarget_urlを確認する
print(target_url)


# このように、`?page={]`を付けて、あとから`format`を使ってURLを作成しました。
# 
# 最初から`url = 'https://suumo.jp/chintai/tokyo/sc_shinjuku/?page=1'`のように書かない理由は、2ページ目以降にアクセスするとき、forループを使っていくためです。
# 
# <br>
# 
# 
# というのも、2ページ目のURLは`https://suumo.jp/chintai/tokyo/sc_shinjuku/?page=2`になっています。
# 
# それ以降のページに関しても`?page=3`のように、数字が変更されるだけです。
# 
# <br>
# 
# 数字だけ変更すれば使い回しできるってわけですね。
# 
# 今回はまだforループを使わないでデータを取っていきますので、この`target_url`にアクセスしていきましょう。

# In[3]:


# target_urlへのアクセス結果を、変数rに格納
r = requests.get(target_url)

# 取得結果を解析してsoupに格納
soup = BeautifulSoup(r.text)


# この部分はいつもどおりですね。
# 
# あとは`soup`に対して`find()`や`find_all()`を使って情報を取得するだけです！

# ## soupから情報を抽出する
# 
# まずは、各賃貸情報がどのような形で格納されているか確認しましょう。
# 
# Webページで「検証」を開くと、HTMLの構造を閲覧できます。
# 
# <br>
# 
# HTMLを確認すると、それぞれの賃貸情報は`div`タグの`cassetteitem`に格納されていることが分かります。
# 
# まずは各賃貸情報をすべて取得して、その後でそれぞれのブロックから情報を抽出するようにしましょう。
# 
# すべてのタグ情報をクラス付きで指定する方法は、前回やった`find_all(タグ名, class_='')`ですね！

# In[4]:


# cassetteクラスを持ったdivタグをすべて取得して、変数contentsに格納
contents = soup.find_all('div', class_='cassetteitem')


# これで、`cassette`を持つすべての`div`タグを取得できました。
# 
# SUUMOのページでは、デフォルトで1ページあたり20件の賃貸情報が掲載されているようです。
# 
# `find_all()`で取得した結果は、Pythonリスト形式になっているので、`len()`を使えば中身の要素数を確認できます。

# In[5]:


# 変数contentsの中身を確認する
len(contents)


# ちゃんと賃貸情報のブロックを取得できていますね。
# 
# いまはforループを使わないでコード作成したいので、変数`content`の中に最初の要素を格納しておきましょう。

# In[6]:


# 変数contentにcontentsの最初の要素を格納する
content = contents[0]


# あとは、最初のブロックに入っている賃貸情報から、自分が欲しい情報を取得していくだけです。
# 
# このページからは色々な情報を抽出できますが、今回は以下の項目を取得したいと思います。
# 
# - 物件情報
#   - 物件名
#   - 住所
#   - アクセス
#   - 築年数
# - 部屋情報
#   - 物件の階数
#   - 物件の賃料/管理費
#   - 物件の敷金・礼金
#   - 物件の間取り・面積

# ### 物件情報と部屋情報が入ったブロックを取得する
# 
# 賃貸情報のブロックを確認すると、「物件・建物の情報」と「各部屋の情報」で格納されているタグが、別になっていることが分かります。
# 
# あとで詳細情報を取り出しやすいように、それぞれの情報を変数に格納しておきましょう。

# In[7]:


# 物件・建物情報を変数detailに格納する
detail = content.find('div', class_='cassetteitem_content')

# 各部屋の情報を変数tableに格納する
table = content.find('table', class_='cassetteitem_other')


# こうしておくと、毎回`find()`以降を書かずに済みます。

# ### 物件情報を抽出する
# 
# ということで、まずは物件情報を取得していきましょう。
# 
# 物件情報で取得できるのは、以下の部分です。
# 
# - 物件名
# - 住所
# - アクセス
# - 築年数
# 
# これらの情報を取得するには、SUUMOのホームページで「検証」をクリックして、どこのタグに格納されているのか確認する必要があります。
# 
# <br>
# 
# どのタグに格納されているのか確認できたら、取得結果を変数に格納してあげましょう。

# In[8]:


# 変数titleに、物件名を格納する
title = detail.find('div', class_='cassetteitem_content-title').text

# 変数addressに住所を格納する
address = detail.find('li', class_='cassetteitem_detail-col1').text

# 変数accessにアクセス情報を格納する
access = detail.find('li', class_='cassetteitem_detail-col2').text

# 変数ageに築年数を格納する
age = detail.find('li', class_='cassetteitem_detail-col3').text


# 取得結果を格納できたら、実際に中身を見てみましょう。

# In[9]:


# 各変数の取得結果を確認
title, address, access, age


# しっかりと中身を取得できていますね！
# 
# *※途中で改行記号(`\n`)などが入っていますが、それらは無視して大丈夫です。*
# 

# ### 部屋情報を抽出する
# 
# 次は各部屋の情報を取得していきましょう。
# 
# 変数`table`に格納しておいたHTMLの解析結果から、以下の情報を取得していきたいと思います。
# 
# - 物件の階数
# - 物件の賃料/管理費
# - 物件の敷金・礼金
# - 物件の間取り・面積
# 
# 各部屋の情報は`<table>`タグに囲まれているので、`<tr>`を見てあげると1つの部屋情報になっているはずです。
# 
# *※`<tr>`はtable rowの省略で、`<table>`タグの行(横一列)のことです。SUUMOのページを見ると、1つ1つの部屋情報は、横1列に並んでいるかと思います。*
# 
# なので、テーブルから部屋情報を抽出するときは、複数の`<tr>`タグを見てあげる必要があります。
# 
# <br>
# 
# 複数の`<tr>`タグを抽出するには...。そうです、`find_all()`を使って取得していきます。
# 
# さらに習得した結果はリストになっていますので、今回は最初の1つ(=インデックス番号0)だけ取得してみましょう。

# In[10]:


# 変数tableからすべてのtrタグを取得して、変数tr_tagsに格納
tr_tags = table.find_all('tr', class_='js-cassette_link')

# tr_targsの中から最初の1つだけtr_tagに格納
tr_tag = tr_tags[0]


# これで、複数の部屋情報から、1つの部屋情報だけ取得できました。
# 
# あとは、変数`tr_tag`から以下4つの情報を取得するだけです。
# 
# - 物件の階数
# - 物件の賃料/管理費
# - 物件の敷金・礼金
# - 物件の間取り・面積

# <hr>
# 
# ▼▽▼▽▼▽▼▽第7回目▼▽▼▽▼▽▼▽
# 
# <hr>

# ### 演習
# 
# 変数`tr_tag`から、以下の情報を取得してみましょう。
# 
# - 物件の階数
# - 物件の賃料/管理費
# - 物件の敷金・礼金
# - 物件の間取り・面積
# 
# *※参考程度に、僕の方で作成してある答えは、1行で書けるコードになっています！*

# #### 答え合わせ
# 
# それでは`<tr>`から、各部屋の情報を取得していきましょう。
# 
# まずはSUUMOのホームページで、以下の4つがどのタグに格納されているのか、確認する必要があります。
# 
# https://suumo.jp/chintai/tokyo/sc_shinjuku/
# 
# `<tr>`の中身を確認してみると、どうやら9つの`<td>`タグで構成されていることが分かります。
# 
# このうち、今回取得したい情報は、3番目から6番目の`<td>`タグに格納されていますね。
# 
# - 物件の階数 : 3番目
# - 物件の賃料/管理費 : 4番目
# - 物件の敷金・礼金 : 5番目
# - 物件の間取り・面積 : 6番目
# 
# `find_all()`で取得した結果は、Pythonのリスト形式になっていたことを思い出すと、すべての`<td>`タグを取得したあとに、スライスを使ってあげれば1行で欲しい情報を取得できます。

# In[15]:


# 変数floor, price, first_fee, capacityに4つの情報を格納する
floor, price, first_fee, capacity = tr_tag.find_all('td')[2:6]


# 少し難しいかもしれませんが、ここでやっていることは以下のようになります。
# 
# ```
# l = [1, 2, 3, 4, 5]
# a, b = l[2:4]
# print(a, b) # --> 3, 4
# ```
# 
# このように複数の変数を左側に準備しておくと、該当する場所に各数字(今回だと3と4)を格納してくれます。
# 
# <br>
# 
# 実際に、部屋情報もそれぞれの変数に格納できているか確認してみましょう。

# In[16]:


# floor, price, first_fee, capacityの中身を確認する
floor, price, first_fee, capacity


# 出力を見てみると、目的としていた情報を取得できていますね。
# 
# <br>
# 
# さらに、部屋の階数(`floor`)以外の部分は、さらに2つの`<li>`タグに格納されていることが分かります。
# 
# なぜかというと、それぞれの変数には以下の項目が格納されているからです。
# 
# - price : 「賃料」と「管理費」
# - first_fee : 「敷金」と「礼金」
# - capacity : 「間取り」と「専有面積」
# 
# これらの複数入っている要素をバラバラにしたいので、さらに`find_all()`を使って情報の抽出をおこなっていきましょう。

# In[22]:


# 変数feeとmanagement_feeに、賃料と管理費を格納する
fee, management_fee = price.find_all('li')

# 変数depositとgratuityに、敷金と礼金を格納する
deposit, gratuity = first_fee.find_all('li')
 
# 変数madoriとmensekiに、間取りと面積を格納する
madori, menseki= capacity.find_all('li')


# それぞれの変数に分割できたら、中身を確認しておきます。

# In[20]:


# 変数feeとmanagement_feeを確認する
print(fee)
print(management_fee)
print('*******************')

# 変数depositとgratuityを確認する
print(deposit)
print(gratuity)
print('*******************')

# 変数madoriとmensekiを確認する
print(madori)
print(menseki)


# このように、しっかりと目的の情報を取得できていますね。

# ### 取得した情報を辞書に格納する
# 
# それでは、これまで取得した以下の項目を、辞書を使って保存しておきましょう。
# 
# - title : 物件の名前
# - address : 住所
# - access : アクセス
# - age : 築年数
# - floor : 部屋の階数
# - fee : 部屋の賃料
# - management_fee : 管理費
# - deposit : 敷金
# - gratuity : 礼金
# - madori : 間取り
# - menseki : 専有面積
# 
# *※「なぜ辞書を使うのか」は、あとでデータを扱いやすくするためです。*
# 
# なお、辞書に格納するときは、タグ情報を外して中身のテキストだけ取得するようにしましょう。
# 
# `title`、`address`、`access`、`age`はテキスト情報だけになっていたので、残りは`.text`をつけて格納してあげます。

# In[23]:


# 変数dに、これまで取得した11項目を格納する
d = {
    'title': title,
    'address': address,
    'access': access,
    'age': age,
    'floor': floor.text,
    'fee': fee.text,
    'management_fee': management_fee.text,
    'deposit': deposit.text,
    'gratuity': gratuity.text,
    'madori': madori.text,
    'menseki': menseki.text
}


# 辞書を使って情報を格納できたら、中身を確認してみましょう。

# In[24]:


# 変数dの中身を確認する
d


# 中身を確認すると、「1ページ目」の「最初の物件」の「最初の部屋」を取得できているはずです。
# 
# あとは、今まで`contents[0]`のように書いておいた部分でforループを使ってあげれば、すべての情報を取得できるようになります。

# # 1ページ目からすべての情報を取得する
# 
# 今回のプログラム作成では、以下の手順を踏んでいました。
# 
# - 小さく情報取得してみる
# - 大丈夫そうだったらforループする
# 
# このうち、小さく情報取得してみる部分が完了したので、forループを使って総仕上げしていきたいと思います！
# 
# <br>
# 
# 基本的には、今まで書いていたコードをコピペしていき、仮決めで`contents[0]`のようにしていた部分でforループを使っていくだけです。
# 
# ただし！forループを使っていきますので、それぞれの部屋情報を格納できるように、変数`d_list`という名前でリストを準備しておきましょう。
# 
# <br>
# 
# アクセスはすでに完了しているので、`soup`から情報取得する部分から書いていけば良いと思います。

# In[26]:


# 変数d_listに空のリストを作成する
d_list = []

# すべての物件情報(20件)を取得する
contents = soup.find_all('div', class_='cassetteitem')


# 各物件情報をforループで取得する
# content = contents[0]
for content in contents:
    
    # 物件情報と部屋情報を取得しておく
    detail = content.find('div', class_='cassetteitem_content')
    table = content.find('table', class_='cassetteitem_other')
    
    # 物件情報から必要な情報を取得する
    title = detail.find('div', class_='cassetteitem_content-title').text
    address = detail.find('li', class_='cassetteitem_detail-col1').text
    access = detail.find('li', class_='cassetteitem_detail-col2').text
    age = detail.find('li', class_='cassetteitem_detail-col3').text
    
    # 部屋情報のブロックから、各部屋情報を取得する
    tr_tags = table.find_all('tr', class_='js-cassette_link')
    
    # 各部屋情報をforループで取得する
    #tr_tag = tr_tags[0]
    for tr_tag in tr_tags:
        
        # 部屋情報の行から、欲しい情報を取得する
        floor, price, first_fee, capacity = tr_tag.find_all('td')[2:6]
        # さらに細かい情報を取得する
        fee, management_fee = price.find_all('li')
        deposit, gratuity = first_fee.find_all('li')
        madori, menseki = capacity.find_all('li')

        # 取得したすべての情報を辞書に格納する
        d = {
            'title': title,
            'address': address,
            'access': access,
            'age': age,
            'floor': floor.text,
            'fee': fee.text,
            'management_fee': management_fee.text,
            'deposit': deposit.text,
            'gratuity': gratuity.text,
            'madori': madori.text,
            'menseki': menseki.text
        }
        
        # 取得した辞書をd_listに格納する
        d_list.append(d)
        


# これで、1ページ目のすべての物件情報を取得するコードを作成できました。
# 
# 変数`d_list`のインデックス0やインデックス1を見てみると、最初の物件に入っている2つの部屋情報を取得できているかと思います。
# 
# <br>
# 
# なお、普通に`print()`を使うと、辞書が見辛い形になってしまいます。
# 
# こういった場合に、体裁を綺麗にしたまま表示できる`pprint`を使ってあげると便利です。

# In[ ]:





# In[27]:


# d_listに入っているインデックスの0番目と1番目を確認する


# In[30]:


# pprintをインポートする
from pprint import pprint


# In[31]:


pprint(d_list[0])
pprint(d_list[1])


# 出力結果を見てみると、しっかりと情報抽出できていますね！
# 
# これで、1ページ目に入っているすべての物件情報を取得できました。
# 
# ここまで学習したことを使っていくと、JavaScriptが使われていないWebページであれば、自由自在に情報抽出できるようになっているはずです。
# 
# <br>
# 
# あとは、現状1ページ目しか取得していなかった部分を、複数ページで取得できるようにできると良いですね！
# 
# ということで、次回は1ページ目だけではなく、複数ページも取得できるようにしたいと思います。
# 
# <br>
# 
# 複数ページを取得するときは、1つ注意点がありますので、次回の動画もしっかり見ていただけると嬉しいです。
# 
# また、少しずつ難しくなっていると思いますので、動画を見返しつつ復習していただけると良いかなと思います。
# 
# *※動画をみるのが面倒だったら、配布しているNotebookで復習するのもオススメです！*
# 
# <br>
# 
# 無料動画とはいえど、ちゃんと役に立つスキルを学べるようにしていきますので、一緒に頑張っていきましょう(｀・ω・´)！

# In[ ]:




