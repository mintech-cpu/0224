#!/usr/bin/env python
# coding: utf-8

# # 【第9回】スクレイピング結果をCSVに保存しよう！
# 
# 
# 今回の講義では、スクレイピング結果をCSVに保存する方法を習得していきたいと思います。
# 
# 前回の講義でSUUMOのホームページを使い、複数ページから情報取得する方法を学びました。
# 
# <br>
# 
# ただ、その取得結果を保存する方法は、まだ学習していませんでした。
# 
# そもそもスクレイピングをする目的は、だいたい以下になります。
# 
# - 手作業でおこなうと面倒なデータ取得をプログラムで自動化する
# - コピペするときのヒューマンエラーをなくす
# - 取得したデータを分析する
# 
# 上記のような目的があることを考えると、やはりスクレイピング結果は保存しておけることが重要です。
# 
# <br>
# 
# というわけで、スクレイピング結果をCSVに保存する方法を学んでいきましょう。
# 
# この動画まで見ていただくと「スクレイピングにおける一連の流れをしっかりと習得できている」と言えます！
# 
# 一緒に頑張っていきましょう！
# 
# <br>
# 
# *※動画の感想を、僕のTwitterにメンションしてツイートしていただけると嬉しいです（ ;  ; ）！*
# 
# Twitter : [@hayatasuuu](https://twitter.com/hayatasuuu)

# # ライブラリのインポート
# 
# 今回は、前回の講義で紹介した3つのライブラリに追加して、`Pandas`を使っていきたいと思います。

# In[5]:


# ライブラリのインポート
from time import sleep
from bs4 import BeautifulSoup
from pprint import pprint

import pandas as pd
import requests


# `Pandas`はデータを扱いやすくするライブラリで、データサイエンスの場面で非常によく使われています。
# 
# *※というか、データサイエンスで1番使うライブラリが`Pandas`です。サッカーでいうとリフティングみたいなイメージですかね。地味だけど、非常に重要なライブラリです！*
# 
# <br>
# 
# 今回の動画では、CSVを作成するときに`Pandas`を使っていきます。
# 
# 本来はもっと色々なことができますが、それだけで1つの講義シリーズを作成できてしまうので、今回は使う部分だけ紹介していきますね！

# # 複数ページから情報取得する
# 
# まずはCSVに保存するために、前回と同様にデータを取得していきましょう。
# 
# 以前に作成したコードを使って、今回は1ページ目と2ページ目だけスクレイピングしていきたいと思います。
# 
# <br>
# 
# 今回は取得結果の保存が目的なので、以下のコードは実行するだけで良いですね！

# In[6]:


# 変数urlにSUUMOホームページのURLを格納する
url = 'https://suumo.jp/chintai/tokyo/sc_shinjuku/?page={}'

# 変数d_listに空のリストを作成する
d_list = []

# アクセスするためのURLをtarget_urlに格納する
for i in range(1, 3):
    print('d_listの大きさ：', len(d_list))
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


# これでスクレイピングが完了しました。
# 
# 今回取得したデータは「リストの中に辞書を入れる」という形にしていたので、スライスを使うことで、中身に入っているデータをいくつか確認できますね。

# In[7]:


# d_listの2番目まで中身を確認してみる
pprint(d_list[0])
pprint(d_list[1])


# というわけで、このリストを使ってCSVを作成していきましょう！

# # 取得したデータを保存する
# 
# スクレイピングで取ってきたデータを保存するには、以下のステップが必要になります。
# 
# - 取得したデータを表形式にする
# - 表形式の取得結果をCSVに出力する
# 
# 今までスクレイピング結果を`[{辞書1}, {辞書2}, ..., {辞書N}]`のように、少し面倒な形式で変数に格納していました。
# 
# このような書き方をしていたのは、実は「**取得したデータの表変換をカンタンにする**」のが目的でした。
# 
# <br>
# 
# なので、取得したデータの保存はスムーズにやっていけます！

# ## 取得したデータを表形式にする
# 
# まずはCSVに保存するために、取得した結果を表形式にしたいと思います。
# 
# そのためには、新しくインポートした`Pandas`を使って、**スクレイピング結果が入っているリストをデータフレームに変換**してあげます。
# 
# <br>
# 
# 一般的に、Python上で一からデータフレームを作成するのは難しいのですが、リスト内に辞書を入れておくことで、簡単に表形式に変換できます。
# 
# 実際に変数`d_list`を使って、データフレームの作成をやっていきましょう。

# In[8]:


# 変数d_listを使って、データフレームを作成する
df = pd.DataFrame(d_list)


# この一行だけで、リスト形式で格納していたデータを表形式に変換できました。
# 
# 実際に中身を確認していきましょう。
# 
# <br>
# 
# データフレームの中身を確認するとき、`df.head()`と書くことで先頭の5行を確認できます。

# In[9]:


# データフレームの先頭5行を確認する
df.head()


# このように、スクレイピングで取得した結果が、表形式になっていますね。
# 
# 表の大きさを確認するときは、`df.shape`を使ってあげます。

# In[11]:


# dfの大きさを確認する
df.shape


# そうすると、2つの数字がカッコに入った状態で取得できました。
# 
# これは(行数, 列数)を表していて、要するに(縦の数, 横の数)ということになります。
# 
# <br>
# 
# 今回でいうと、(取得した部屋の数, 取得した項目の数)ですね。
# 
# <br>
# 
# また、取得した物件数は1ページにつき20件なので、合計で40件になっているはずです。それも合わせて確認しておきましょう。
# 
# 物件名を重複無しで取得して、その大きさを取得するには以下のように書きます。

# In[13]:


# 物件名の重複を削除して、その大きさを確認する
len(df.title.unique())


# そうすると"40"と表示されましたので、「今回取得した物件数は40件だった」ということが分かります。

# ## 表形式の取得結果をCSVに出力する
# 
# スクレイピングで取得した結果を表形式にできたので、あとはCSVに出力するだけです。
# 
# データフレームをCSVに出力するには、以下のように`df.to_csv()`を使ってあげます。

# In[14]:


# to_csv()を使って、データフレームをCSV出力する
df.to_csv('suumo.csv', index=None, encoding='utf-8-sig')


# これで、カッコの中に書いたファイル名でCSVを作成できました。
# 
# CSVを作成するときは、他にも2つの引数を設定しています。それぞれの意味は、以下のとおりです。
# 
# - index=None : インデックス部分をつけない
# - encoding="utf-8-sig" : 文字コードを指定(→Excelで開いたときの文字化け対策です)
# 
# 基本的にCSV出力するときは、このような設定にしておくと良いと思います。
# 
# *※時間があったら、それぞれの引数を設定しないCSVも出力してみると面白いと思います！*
# 
# <br>
# 
# 少し余談ですが、会社の分析環境がLinux、使っているPCはWindowsが多いので、この文字化け問題は、わりとあるあるです！笑
# 
# *※Linuxとかよく分からない場合は、分析している場所がタイで、実際にCSVを読みたい人は日本人と考えていただけると良いかと。日本人がタイ語を解読するのは難しいですよね！*
# 
# この動画の第1回目で紹介したように「副業でスクレイピングをやってみたい」と思っているなら、文字コードは`utf-8-sig`にしてあげるのが優しいと思います！

# # まとめと余談
# 
# というわけで、これでスクレイピング結果の保存もできるようになりました。
# 
# 第9回目までスクレイピングについて紹介してきましたが、いかがだったでしょうか？
# 
# <br>
# 
# ここまで学んでくださった皆さんであれば、あとは自分の好きなWebサイトで、スクレイピングできるようになっているはずです。
# 
# ここまでで一旦の区切りになりますが、スクレイピング入門は後半戦も続いていきます。
# 
# <br>
# 
# 後半戦では、JavaScriptが使われているサイトで、`Selenium`を使ってスクレイピングしていく方法を紹介していきます。
# 
# 具体的には「好きな女優の画像を自動で保存する」方法を紹介します。
# 
# *※ちなみに、僕が好きな女優は岡本玲と小芝風花です！*
# 
# <br>
# 
# `Selenium`を学ぶと、ブラウザの自動操作ができるようになるので、スクレイピング以外にも色々なことができるようになります。
# 
# <br>
# 
# もっとPythonやスクレイピングを学んでみたい人は、一緒に頑張っていきましょう！
# 
# 

# ## (余談)余計な文字を削除する方法
# 
# こちらは動画内で解説しませんが「ぜひしておくと良いかな？」といった知識になります。
# 
# 今回取得したデータには、以下のように「余計な文字」が含まれていました。
# 
# - \r
# - \n
# - \t
# 
# これらは、シンプルに必要ない文字になります。
# 
# 特に、`\t`タブで空白をあける記号ですが、これはCSVをタブ区切りにしたとき、バグを発生させる原因になります。
# 
# *※CSVはカンマ区切りがスタンダードですが、タブでも区切ることができます。*
# 
# なので、これらの文字は削除してしまいましょう。
# 
# <br>
# 
# これには正規表現を使ってあげると良く、Pythonで正規表現を扱うには`re`(Regular Expressions)をインポートする必要があります。

# In[ ]:


# reをインポートする
import re


# 作成しておいた`df`に対して、`re.sub()`を使ってあげると、文字列の削除ができます。
# 
# *※正確には、文字の置換をするメソッドです。*
# 
# <br>
# 
# まずは実際に`\n`を削除するコードを見てみましょう。

# In[ ]:


df2 = df.applymap(lambda x: re.sub('\n', ' ', x))
df2.head()


# 取得してあるデータフレームから`\n`を削除するには、このように書きます。
# 
# かなり難しいですね...！
# 
# - 正規表現`re`の取り扱い
# - ラムダ式の取り扱い
# - `Pandas`の取り扱い
# 
# これらが分からないと、完全に意味不明になるはずです。なので今の段階では、「ああ、こうやって書くんだな〜」くらいの感覚で大丈夫です。
# 
# 一応、やっていることは、以下のようになっています。
# 
# - df.applymap() : データフレーム全体に対して、カッコ内の関数を適応する
# - lambda x: re.sub('\n', ' ', x)) : 引数で渡された`x`に対して、`\n`を半角スペースに置換する
# 
# まとめると、データフレーム全体に「`\n`を半角スペースに置換する」という処理を当てているということになります。
# 
# <br>
# 
# 追加で`\r`と`\t`も削除したい場合には、以下のように書けばOKですね！

# In[ ]:


df3 = df2.applymap(lambda x: re.sub('\r', ' ', x))
df3.applymap(lambda x: re.sub('\t', ' ', x))


# これで余計な記号がなくなり、キレイなデータになりました。
# 
# 余談の知識でしたが、実践の場ではよく使うのでおさえておいて損はないですね。
# 
# <br>
# 
# 「なんだか難しいけど、こうやってデータを扱えるようになっていきたいな〜」と思ったら、データサイエンスを勉強していくのが良いです。
# 
# 特に、Pythonを使ってデータを自由自在に扱っていくなら、`Pandas`を勉強すると良いですよ！
# 
# *※もし需要があったら、僕の得意分野なので、動画で紹介していきたいと思います!!*
# 
# <br>
# 
# Pythonは勉強することが盛りだくさんです。焦らず、コツコツと頑張っていきましょう！
# 
# もし良かったら、スクレイピング入門の後半戦も一緒に勉強していけると嬉しいです(｀・ω・´)！

# In[ ]:




