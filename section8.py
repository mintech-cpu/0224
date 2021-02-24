#!/usr/bin/env python
# coding: utf-8

# # 【第8回】複数ページからの情報取得をマスターしよう！
# 
# 今回の講義では、複数ページの情報取得をおこなっていきたいと思います。
# 
# 前回の第7回目では、SUUMOのホームページで1ページ目の情報をすべて取得しました。
# 
# 
# https://suumo.jp/chintai/tokyo/sc_shinjuku/
# 
# <br>
# 
# 今回は、その続きということになります。
# 
# 複数ページに対してスクレイピングできるようになると、Webページ全体から情報取得できるようになります。
# 
# <br>
# 
# さらに、この動画まで見ていくと、複数ページから情報取得するときの注意点まで分かるようになります。
# 
# 「スクレイピングの基本スキルはしっかり身についている」といえるレベルになれますので、一緒に頑張っていきましょう！
# 
# <br>
# 
# *※動画の感想を、僕のTwitterにメンションしてツイートしていただけると嬉しいです（ ;  ; ）！*
# 
# Twitter : [@hayatasuuu](https://twitter.com/hayatasuuu)

# # ライブラリのインポート
# 
# 今回使うライブラリをインポートしていきます。
# 
# 今までは`Requests`と`BeautifulSoup`しかインポートしていませんでしたが、今回は新しく`time`から`sleep`をインポートしたいと思います。

# In[1]:


# ライブラリのインポート
from time import sleep
from bs4 import BeautifulSoup
import requests


# `sleep()`は名前からも想像できるかもしれませんが、Pythonの実行を()の中に書いた秒数だけ休止できます。
# 
# 例えば、`sleep(1)`のように書いてあったら「1秒間だけPythonの実行を休止する」という意味になります。
# 
# 「これをどこで使うのか」に関しては、後ほどのコード作成で見ていきましょう！

# # 1ページ取得するコードを確認
# 
# 複数ページに対してスクレイピングするには、今まで作成しておいた1ページ目のコードが基になります。
# 
# なので今一度、1ページ目を取得したときに使ったプログラムを確認していきましょう。
# 
# <br>
# 
# 全体の流れは、以下のようになっています。
# 
# 1. アクセスするURLを設定する
# 2. `Requests`を使って1で設定したURLにアクセスする
# 3. 取得したHTMLを`BeautifulSoup`で解析する
# 4. すべての物件情報を取得する(20件)
# 5. 各物件情報から「物件の詳細」と「各部屋情報」を取得する
# 6. それぞれを解析する
# 7. 解析した結果を辞書に格納する

# In[17]:


# 1. アクセスするURLを設定する
url = 'https://suumo.jp/chintai/tokyo/sc_shinjuku/?page={}'

target_url = url.format(3)

print(target_url)


# In[3]:


# 2. `Requests`を使って1で設定したURLにアクセスする
r = requests.get(target_url)

# 3. 取得したHTMLを`BeautifulSoup`で解析する
soup = BeautifulSoup(r.text)


# In[4]:


d_list = []

# 4. すべての物件情報を取得する(20件)
contents = soup.find_all('div', class_='cassetteitem')


# 5. 各物件情報から「物件の詳細」と「各部屋情報」を取得する
for content in contents:
    # 6. それぞれを解析する
    detail = content.find('div', class_='cassetteitem_content')
    table = content.find('table', class_='cassetteitem_other')
    
    title = detail.find('div', class_='cassetteitem_content-title').text
    address = detail.find('li', class_='cassetteitem_detail-col1').text
    access = detail.find('li', class_='cassetteitem_detail-col2').text
    age = detail.find('li', class_='cassetteitem_detail-col3').text

    tr_tags = table.find_all('tr', class_='js-cassette_link')
    

    for tr_tag in tr_tags:        
        
        floor, price, first_fee, capacity = tr_tag.find_all('td')[2:6]
        
        fee, management_fee = price.find_all('li')
        deposit, gratuity = first_fee.find_all('li')
        madori, menseki = capacity.find_all('li')


        # 7. 解析した結果を辞書に格納する
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
        
        d_list.append(d)


# In[5]:


from pprint import pprint


# この流れを確認すると、複数ページから情報抽出するためには「1. アクセスするURLを設定する」で書いておいた以下の部分：
# 
# ```
# url = 'https://suumo.jp/chintai/tokyo/sc_shinjuku/?page={}'
# 
# target_url = url.format(1)
# ```
# 
# を変更するだけで良いことが分かります。
# 
# <br>
# 
# 今回は、最初にベースになるURLを設定し、その後`format`を使ってアクセスするページを指定する形にしておきました。
# 
# なので追加でforループを使って、`format()`のカッコの中身を変えることで、アクセスしたいURLを変更すればコードの編集は完了します。

# In[7]:


pprint(d_list[0])
pprint(d_list[1])


# # 複数ページから情報取得する
# 
# というわけで、元になる変数`url`から、アクセスするURL(=`target_url`)を設定する間に、forループを使ってあげましょう。
# 
# まずはループと関係ない部分だけ書いておきたいと思います。

# In[8]:


# 変数urlにSUUMOホームページのURLを格納する
url = 'https://suumo.jp/chintai/tokyo/sc_shinjuku/?page={}'

# 変数d_listに空のリストを作成する
d_list = []


# あとはループを使って、複数ページから情報を取得していきましょう。
# 
# 今回は、最初の3ページから情報を取得していきたいと思いますので、`for i in range(1, 4)`のように書いてあげればOKですね！
# 
# <br>
# 
# 試しに、URLの変更部分だけ確認しておきましょう。

# In[10]:


# 1〜3をループする
for i in range(1, 4):
    # 変数target_urlに、アクセス先のURLを格納する
    target_url = url.format(i)
    # print()してtarget_urlを確認する
    print(target_url)


# このような出力結果になりました。
# 
# それぞれのURLを確認してみると、しっかりSUUMOのページにアクセスできるかと思います。
# 
# <br>
# 
# それでは下準備ができましたので、あとは今まで使っていたコードを、`target_url`の下に貼り付けてあげましょう。
# 
# コピペが完了したら、あとは実行すればOK...と言いたいところですが、実はまだやるべきことがあります。
# 
# それは、すでにインポートしておいた`sleep()`の利用です。`sleep(1)`のように書くことで「1秒間だけPythonの実行を休止する」という処理ができました。
# 
# <br>
# 
# そして、これが複数ページに対してスクレイピングするときの注意点になるのですが、**それぞれのリクエスト間に、数秒のsleep()を挟んであげる**必要があります。
# 
# なぜ`sleep()`を使ってPythonの動作を少し止めるのか。それは、第1回目の講義でもお伝えしたように、相手のサーバーに負荷をかけないためです。
# 
# <br>
# 
# というのも、Pythonでプログラムを実行すると、ほぼ一瞬で処理が完了してしまいます。
# 
# 試しに1〜10を出力するプログラムを実行してみましょう。

# In[11]:


get_ipython().run_cell_magic('time', '', '# 1〜10を出力するコードを、時間計測とともに出力する\nl = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\nprint(l)')


# `%%time`をつけて時間も測定して実行すると、Wall timeで〇〇µsと表示されるはずです。
# 
# 「µs = 100万分の1秒」なので、非常に高速な処理をおこなっていることが分かりますね。
# 
# <br>
# 
# この高速な処理をWebサイトに対しておこなってしまうと...、明らかに相手のサーバーに負荷をかけてしまいます。
# 
# なので、一回ごとのリクエスト後に、`sleep()`を挟んであげることで、相手のサーバーに負荷をかけないようにしてスクレイピングしていく必要があります。
# 
# <br>
# 
# リクエスト後に`sleep()`を挟まないと「サイトが攻撃されている」と思われかねないので注意しておきましょう。
# 
# それでは、以上の点も踏まえて、コードの作成をしていきます。

# In[13]:


from time import sleep
from bs4 import BeautifulSoup
import requests


# In[14]:


# 変数urlにSUUMOホームページのURLを格納する
url = 'https://suumo.jp/chintai/tokyo/sc_shinjuku/?page={}'

# 変数d_listに空のリストを作成する
d_list = []


# In[15]:


# アクセスするためのURLをtarget_urlに格納する
for i in range(1, 4):
    print('d_listの内容量：', len(d_list))
    target_url = url.format(i)

    # print()してtarget_urlを確認する
    print(target_url)

    # target_urlへのアクセス結果を、変数rに格納
    r = requests.get(target_url)
    
    sleep(1)

    # 取得結果を解析してsoupに格納
    soup = BeautifulSoup(r.text)
    
    # すべての物件情報(20件)を取得する
    contents = soup.find_all('div', class_='cassetteitem')

    # 各物件情報をforループで取得する
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


# 作成したコードを実行すると、上記のような実行結果になるかと思います。
# 
# 今回は3ページ目まで取得するコードを書いているので、1番最後の要素は3ページ目の最後の物件情報になっているはずです。
# 
# <br>
# 
# というわけで、`d_list`の最後の要素を確認したのち、SUUMOのホームページに掲載されている3ページ目の最後の物件情報をチェックしてみましょう。

# In[16]:


# d_listに格納されている最後のインデックスを確認する
d_list[-1]


# *※ちなみに、最後のインデックスに該当する要素を指定するときは、`d_list[-1]`のように書くのがベストです。`d_list[len(d_list)]`のような書き方はあまり良くないので、これを機に直していきましょう!!*
# 
# 取得したリストと3ページ目に入っている最後の要素を確認してみると、ちゃんとスクレイピングできていることが分かりますね。
# 
# <br>
# 
# これで複数ページから情報取得できるようになりました！
# 
# ここまで勉強したことを使えば、すでにスクレイピングの基礎知識はしっかり身に付いています(^ ^)！
# 
# <br>
# 
# あとは、スクレイピングで取得した結果をCSVファイルなど、いつでも確認できるようにしておくと良いですよね。
# 
# なので、次回の講義ではスクレイピングで取得した結果を、CSVに保存する方法を紹介していきます。
# 
# <br>
# 
# いままで`[{辞書1}, {辞書2}, ..., {辞書N}]`のような形で、スクレイピングした結果を保管しておいた意義が、ようやく分かるようになります。
# 
# `Requests`と`BeautifulSoup`編も残りわずかなので、最後まで頑張っていきましょう(｀・ω・´)！

# In[ ]:




