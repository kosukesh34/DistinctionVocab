# fmt: off
"""Hand-crafted Japanese translations for Distinction V (sbslike). Entries 1-65."""

TRANSLATIONS_PART1: dict[int, dict] = {
1: {
    "nativeDefinition": "Used to report what someone said or thought, often in casual storytelling.",
    "japaneseMeaning": "〜って言ってた／〜って感じ",
    "etymology": "likeが口語で「こう言った／こう思った」のニュアンスを担う。引用や内心の言葉をそのまま伝える話し言葉の型。",
    "examples": {
        "B": "グレッグが仕事のあと行くイベントに僕を誘ってくれたんだ。飲み物がタダらしいから、二回も聞かなくていいよって感じ。",
        "C": "兄妹がナスの切り方でかなり熱く議論してて、僕はただ早く切ってくれって感じだった。ナス一本なのに。",
        "D": "誰かが言った",
    },
},
2: {
    "nativeDefinition": "Used to clarify or soften a statement by giving the real reason.",
    "japaneseMeaning": "ただ〜なだけ、というのは",
    "etymology": "just thatで「本当のところはただ〜だ」と言い訳や補足をする口語表現。",
    "examples": {
        "B": "普段は卓球なんてしないんだ。ただ、しばらく雨が降り続くから、今は野球をやりたくないだけなんだ。",
        "C": "飛行機が怖いわけじゃないんだ。ただ、電車の方がずっと快適だからそっちを選ぶだけ。",
        "D": "しかし",
    },
},
3: {
    "nativeDefinition": "Used to deny a misunderstanding before giving the actual reason.",
    "japaneseMeaning": "〜というわけではない、〜から嫌いなわけじゃない",
    "etymology": "not thatで「そういう意味ではない」と誤解を否定し、本当の理由を続ける型。",
    "examples": {
        "B": "勉強が嫌いなわけじゃない。ただ試験勉強が好きじゃないだけ。",
        "C": "コーヒーを飲まないわけじゃない。ただ昼食後はなるべく避けてるだけ。",
        "D": "そう言うのは正確じゃない",
    },
},
4: {
    "nativeDefinition": "Used to say that something is not true or not as extreme as suggested.",
    "japaneseMeaning": "〜というわけじゃない、そんなことない",
    "etymology": "not likeで「そういう状況ではない／そこまでではない」と事実や程度を否定する。",
    "examples": {
        "B": "なんで彼女はいつも僕に時間を聞いてくるの？僕の方がスマホを見るのが上手いわけじゃないのに。",
        "C": "僕がエクストリームスポーツが大好きだって人に言うのはやめて。スカイダイビングは一度だけ。毎週末クレイジーなことしてるわけじゃない。",
        "D": "そういうことではない",
    },
},
5: {
    "nativeDefinition": "Used to reframe or correct how something should be described.",
    "japaneseMeaning": "というより〜だ、むしろ〜に近い",
    "etymology": "more likeで「正確にはこっちに近い」と言い換え・修正する口語表現。",
    "examples": {
        "B": "元カノと別れたというより、時間が経つうちに自然と離れていった感じ。",
        "C": "彼のアイデアを盗んだわけじゃない。というより借りて、自分なりにアレンジしただけ。",
        "D": "むしろそう言える",
    },
},
6: {
    "nativeDefinition": "Used to comment on how surprising or noteworthy something is.",
    "japaneseMeaning": "〜って（本当に）形容詞だね",
    "etymology": "it's + 形容詞 + howで「〜というのがどれだけ形容詞か」を強調する感嘆の型。",
    "examples": {
        "B": "夜にコーヒー飲むとすごく眠くなるの、ちょっと変だよね。",
        "C": "匂いでこんなに記憶が蘇るって、面白くない？",
        "D": "形容詞だ",
    },
},
7: {
    "nativeDefinition": "Used to give a reason while expressing a feeling about the situation.",
    "japaneseMeaning": "〜だから（本当に）形容詞だ",
    "etymology": "it's + 形容詞 + becauseで「その理由があるからこそ、こう感じる」と理由と感情を結びつける。",
    "examples": {
        "B": "昨夜ずっと暗号資産の仕組みを調べてたんだけど、いくら読んでも理解できなくて本当にイライラする。",
        "C": "ウィルはタクシーに乗れないから帰らないって言うけど、いつも高い服着てるのに変だよね。",
        "D": "形容詞は何だ",
    },
},
8: {
    "nativeDefinition": "Used to express appreciation for a particular quality or aspect.",
    "japaneseMeaning": "〜なところが好き／素敵",
    "etymology": "like/love howで「こういう点が好き」と特定の良さを挙げる表現。",
    "examples": {
        "B": "同僚が突然上司の物まねをするの、好きなんだよね。",
        "C": "もちろん初めて会った時のこと覚えてるよ。すぐ打ち解けたのが本当に良かった。",
        "D": "好きだ、大好きだ",
    },
},
9: {
    "nativeDefinition": "Used to explain the method or way something is done or achieved.",
    "japaneseMeaning": "こうやって〜する、そういう風に育った",
    "etymology": "this/that's howで「こういうやり方で」「そういう経緯で」と方法・過程を説明する。",
    "examples": {
        "B": "目標を立てて、努力して、達成して、それを繰り返す。自信はそうやって築いていくものだ。",
        "C": "僕はいつも後ろの人のためにドアを開けてあげる。そういう風に育てられたから。",
        "D": "そういう方法だ",
    },
},
10: {
    "nativeDefinition": "Used to introduce something you are about to talk about.",
    "japaneseMeaning": "こういう〜、あの〜",
    "etymology": "this/these + 名詞で「こういう話をこれからする」と聞き手の注意を引く口語の導入。",
    "examples": {
        "B": "真夜中に裏庭を何かが走り回ってたんだ。リスだったみたいだけど、確認しないと安心できなくて。",
        "C": "ねえ、昨日Tinderでめちゃくちゃ可愛い子を見つけたんだ。僕には釣り合わない感じだったけど、勇気出してLikeしたらマッチした。",
        "D": "これから話すこと",
    },
},
11: {
    "nativeDefinition": "Used to make a suggestion in a friendly way.",
    "japaneseMeaning": "〜はどう？、〜しませんか",
    "etymology": "how aboutで「こうするのはどう？」と提案・勧誘するカジュアルな表現。",
    "examples": {
        "B": "会議の時間を節約するために、資料は事前に送るのはどう？",
        "C": "あと1ヶ月くらい待って、このマーケ施策の結果を見てみるのはどう？今変更するのは早いと思う。",
        "D": "提案する",
    },
},
12: {
    "nativeDefinition": "Used as an exclamation to emphasize how adjective something is.",
    "japaneseMeaning": "〜って（どれだけ）形容詞なんだ",
    "etymology": "how + 形容詞 + isで「どれだけ〜か」を強調する感嘆文。疑問形だが驚きや称賛のニュアンス。",
    "examples": {
        "B": "首相が握手しようとしてる人にフィストバンプしてる写真見た？めちゃくちゃおかしくない？",
        "C": "オーストラリア英語でピーマンをcapsicumって言うんだって。可愛くない？ラテン語みたい。",
        "D": "とても形容詞だ",
    },
},
13: {
    "nativeDefinition": "Used to compare something to another thing it resembles.",
    "japaneseMeaning": "まるで〜のようだ、〜みたいなもの",
    "etymology": "it's like + 名詞/動名詞で「AはBに似ている」と比喩・類似を示す。",
    "examples": {
        "B": "やっとスケボーに慣れてきた。陸上でサーフィンしてるみたい。",
        "C": "Disney+を見たことがあるなら、大人向けのDisneyランドみたいなものだよ。",
        "D": "〜に似ている",
    },
},
14: {
    "nativeDefinition": "Used to say something seems or feels as if a certain situation is true.",
    "japaneseMeaning": "まるで〜みたいだ、〜しているようだ",
    "etymology": "it's like + 節で「まるでこういう状況のようだ」と推測・印象を述べる。",
    "examples": {
        "B": "ステイシーは僕が話しかけたい時だけいつも超忙しそうで、まるでわざと避けてるみたい。",
        "C": "先週買った株が全部急騰してる。まるで未来が見えてるみたいだね。",
        "D": "まるで〜のようだ",
    },
},
15: {
    "nativeDefinition": "Used to describe something as somewhat similar to something else.",
    "japaneseMeaning": "ちょっと〜みたいな感じ",
    "etymology": "kind of likeで「完全には同じじゃないけど、なんとなく〜に似てる」と柔らかく比較する。",
    "examples": {
        "B": "コンブチャ飲んだことある？僕は先週初めて試したんだけど、甘いお茶みたいな感じで、思ってたよりマシだった。",
        "C": "基本文法もわからずに語学を勉強するのは良くない。ルールを知らずにスポーツするみたいなものだ。",
        "D": "〜と言える",
    },
},
16: {
    "nativeDefinition": "Used to say something feels somewhat as if a situation were true.",
    "japaneseMeaning": "なんとなく〜みたいな感じ",
    "etymology": "kind of like + 節で「完全ではないが、なんとなくまるで〜のようだ」と印象を述べる。",
    "examples": {
        "B": "お酒を飲むと、なんとなく本当の自分が出てくる感じがする。",
        "C": "ディズニーランド行ったことないの？あの attraction も建物もすごく綺麗で、別次元にいるみたいな感じだよ。",
        "D": "まるで〜のようだ",
    },
},
17: {
    "nativeDefinition": "Used to compare something as being very close to something else.",
    "japaneseMeaning": "ほとんど〜も同然、まるで〜のようなもの",
    "etymology": "almost likeで「ほぼ〜と同じくらい」と強い類似を示す。",
    "examples": {
        "B": "このアルバムで一曲だけ好きなのを選ぶの、ほとんど好きな子を一つ選べって言うのと同じくらい難しい。全部良いんだ。",
        "C": "F1の車を運転するの楽しい？めちゃくちゃ楽しいよ。地上でスカイダイビングしてるみたい。",
        "D": "ほぼ〜だ",
    },
},
18: {
    "nativeDefinition": "Used to say something feels almost as if a situation were true.",
    "japaneseMeaning": "まるで〜も同然、ほとんど〜のよう",
    "etymology": "almost like + 節で「ほとんどまるで〜のようだ」と強い感覚・印象を伝える。",
    "examples": {
        "B": "今ベッドでホットドッグとナッツ食べてるんだけど、死なずに天国に行ってるみたい。",
        "C": "この靴すごく履き心地いい。まるで何も履いてないみたい。",
        "D": "ほとんど〜のように感じる",
    },
},
19: {
    "nativeDefinition": "Used to give an example or say something is done in a similar way.",
    "japaneseMeaning": "〜のように、〜みたいに",
    "etymology": "likeは比較・例示・引用のマーカーとして「〜のように」「例えば」と機能する。",
    "examples": {
        "B": "彼の言うことを鵜呑みにしちゃダメだよ。いつもみたいに大げさに言ってるだけだから。",
        "C": "ロナウドみたいにボールを蹴ろうとしてるんだけど、全然あの速さには届かない。",
        "D": "〜のように",
    },
},
20: {
    "nativeDefinition": "Used to express a subjective impression or sense that something is true.",
    "japaneseMeaning": "〜のような気がする",
    "etymology": "feels likeで「そう感じる／そんな気がする」と主観的な印象を述べる。",
    "examples": {
        "B": "Netflixで見るもの、もう全部見ちゃった気がする。他に時間つぶすものがない。",
        "C": "最近スティーブはなんとなく手を抜いてる気がする。以前はもっと情熱的だったのに。",
        "D": "そう思う",
    },
},
21: {
    "nativeDefinition": "Used to identify a type of thing that fits a certain category.",
    "japaneseMeaning": "まさにそういうこと、そういうタイプのもの",
    "etymology": "the kind/sort of thingで「まさにそういう類のこと」と典型例を示す。",
    "examples": {
        "B": "昔の生徒から今日合格したって連絡が来た。まさにこういうことが僕を本当に嬉しくする。",
        "C": "わあ、この地球の歴史のドキュメンタリー面白い。まさに僕がワクワクするタイプのものだ。",
        "D": "そういうタイプのこと",
    },
},
22: {
    "nativeDefinition": "Used to describe something vaguely as a certain type of thing.",
    "japaneseMeaning": "〜みたいなもの、〜っぽいもの",
    "etymology": "a + 名詞 + kind/sort of thingで「なんとなく〜っぽいもの」と曖昧に分類する。",
    "examples": {
        "B": "リスとクマの中間みたいな感じ。他にどう言えばいいかわからない。",
        "C": "この新しいスマホは折りたたみ式っぽいんだけど、タッチスクリーンもある。",
        "D": "〜みたいなもの",
    },
},
23: {
    "nativeDefinition": "Used to refer to a trend, activity, or concept in a casual way.",
    "japaneseMeaning": "〜というもの、〜ブーム",
    "etymology": "sth + thingで「その〜というもの／現象」をカジュアルに指す。やや距離を置いた言い方。",
    "examples": {
        "B": "このファストファッションってのは環境に良くないから、質のいい服を買うようにしてる。",
        "C": "今夜Uber Eatsってのを試してみる。楽しみ。",
        "D": "よく知らないもの",
    },
},
24: {
    "nativeDefinition": "Used to express uncertainty or a tentative conclusion.",
    "japaneseMeaning": "〜かな、〜だと思う（たぶん）",
    "etymology": "I guessは文末に付けて「たぶんそう／なんとなくそう思う」と控えめに言う。",
    "examples": {
        "B": "最近忙しすぎて仕事以外何もできてない。忙しい時に代わりにやってくれる右腕が必要かな。",
        "C": "意識が現実を作ると思うから、ある見方をすれば僕たちの世界はほとんどVRみたいなものかな。",
        "D": "たぶん",
    },
},
25: {
    "nativeDefinition": "Used to express a personal opinion, often as an afterthought.",
    "japaneseMeaning": "〜だと思う",
    "etymology": "I thinkを文末や文中に置き、自分の考え・推測を柔らかく示す。",
    "examples": {
        "B": "このプロジェクトは順調だと思う。だから今夜は少し早めに帰るつもり。",
        "C": "今夜すごく楽しみ。映画もきっと面白いと思う。",
        "D": "私の意見では",
    },
},
26: {
    "nativeDefinition": "Used to insert a personal opinion in the middle of a sentence.",
    "japaneseMeaning": "〜だと思うけど（文の途中で）",
    "etymology": "I thinkを文中に挟み、意見を差し込む口語の挿入表現。",
    "examples": {
        "B": "君の英語、ちょっとヨーロッパ訛りがあると思うんだけど、どこで英語習ったの？",
        "C": "はっきり言うと、昨日の彼のプレゼンは今までで一番ひどかったと思う。形だけで誰にも響いてなかった。",
        "D": "ただの意見",
    },
},
27: {
    "nativeDefinition": "Used to describe a background action happening at the same time.",
    "japaneseMeaning": "〜しながら、〜している最中に",
    "etymology": "文末のdoingで主動作の背景で別の行為が同時進行していることを示す。",
    "examples": {
        "B": "昨夜電車を待ちながら、その日に起きたことをぼんやり考えてたら、新商品のアイデアがひらめいた。",
        "C": "晴れた週末は、特に目的地もなく歩き回るのが好き。",
        "D": "〜しながら",
    },
},
28: {
    "nativeDefinition": "Used as a subject to describe someone's typical behavior (often with criticism).",
    "japaneseMeaning": "〜するのは（いつも）〜だ",
    "etymology": "sb/sth + doingを主語にして「〜すること自体が〜だ」と行為を評価・批判する型。",
    "examples": {
        "B": "彼女の言うことを深読みしすぎるのは僕にとって普通。彼女の言葉はいつも曖昧でよくわからないから。",
        "C": "うちの犬があんな吠え方するのはちょっと変だね。すごくお腹空いてるんだと思う。",
        "D": "〜しているという事実",
    },
},
29: {
    "nativeDefinition": "Used as a subject to comment on someone or something doing an action.",
    "japaneseMeaning": "〜している〜（は）",
    "etymology": "sb/sth + doingを主語にして、目の前の行為についてコメントする口語表現。",
    "examples": {
        "B": "あの猫が自分の尻尾を追いかけ回してるの、本当に面白い。犬だけだと思ってた。",
        "C": "32個のビッグマックを一気に食べる男の動画を見た。狂ってる。",
        "D": "〜している人",
    },
},
30: {
    "nativeDefinition": "Used to point out a photo or video showing someone doing something.",
    "japaneseMeaning": "これが〜しているところ",
    "etymology": "this is + sb doingで写真や動画の場面を「これが〜してるところ」と紹介する。",
    "examples": {
        "B": "これが去年の誕生日パーティーで友達と楽しんでる僕。いい写真でしょ？",
        "C": "ほら、これがうちの犬が床に落としたアイスクリーム食べてるところ。可愛くない？",
        "D": "〜している場面",
    },
},
31: {
    "nativeDefinition": "Used to contrast one action with a stronger judgment about another.",
    "japaneseMeaning": "〜するのは〜だけど、〜するのは別",
    "etymology": "A doing, that's B で「Aはまだいいが、Bは違う」と二つの行為を対比して評価する。",
    "examples": {
        "B": "このラーメン屋がスープにホイップクリーム入れるのはキモい。誰が注文するの？",
        "C": "妹が一緒にジングルベルを弾きたがるのはいいけど、人生見つけろって言われるのはキツい。",
        "D": "〜するのは形容詞だ",
    },
},
32: {
    "nativeDefinition": "Used to say that a hypothetical situation would be a certain way.",
    "japaneseMeaning": "〜したら〜だろうに、〜すれば〜なのに",
    "etymology": "A doing, that'd be B で仮定の状況がどうなるかを述べる。願望や想像を含む。",
    "examples": {
        "B": "アパートの隣にスタバができたら最高なのに。僕はほぼ毎日そこで勉強してるから。",
        "C": "ニューオーリンズに何があるかよくわからないけど、君と数日行ったらすごく楽しそう。",
        "D": "〜だろう",
    },
},
33: {
    "nativeDefinition": "Used when someone makes or keeps you doing something.",
    "japaneseMeaning": "（人に）〜させられる、〜させられる",
    "etymology": "have + 人 + doingで「（何度も／しばらく）〜させられる」継続・反復の使役。",
    "examples": {
        "B": "子供の頃は読書が好きだったのに、親は勉強させた。小説家になるなんて思ってなかっただろうね。",
        "C": "上司に振り回されてる。仕事を断るたびに、誰も興味ない細かい話を延々とされる。",
        "D": "人に〜させる",
    },
},
34: {
    "nativeDefinition": "Used when something causes you to start or keep doing something.",
    "japaneseMeaning": "〜させられる、〜してしまう",
    "etymology": "get + 人 + doingで「（何かがきっかけで）〜し始める／〜させられる」状態変化の使役。",
    "examples": {
        "B": "ジブリ映画ばかり見てて、なんであの料理はこんなにおいしそうに見えるのか考えさせられてる。",
        "C": "暑さのせいで毎朝すごく早く目が覚めるから、仕事に着く頃にはもう疲れてる。今夜は早く寝る。",
        "D": "人に〜させる",
    },
},
35: {
    "nativeDefinition": "Used to express having the opportunity or permission to do something.",
    "japaneseMeaning": "〜できる、〜する機会がある",
    "etymology": "get to doは「〜する機会・許可を得る」という好ましい機会のニュアンスを持つ。",
    "examples": {
        "B": "バーで働くのが好きなのは、好きな飲み物を無料で飲めるから。毎日が天国だよ。",
        "C": "昨日は人生最高の日だった。舞台のキャストの一人と話せたんだ。夢が叶った。",
        "D": "〜する機会がある",
    },
},
36: {
    "nativeDefinition": "Used to urge starting an action, often energetically.",
    "japaneseMeaning": "さあ〜しよう、〜し始めよう",
    "etymology": "get + doingは「さあ〜し始めよう」と行動を促す口語。get going, get cookingなど。",
    "examples": {
        "B": "ダニエル、昨夜すごくぎこちなかった。みんなが政治の話をしてるのに、僕はニュース読まないけどなんとか乗り切った。",
        "C": "その通り、遅刻するから急ごう。気が利くね。",
        "D": "始める",
    },
},
37: {
    "nativeDefinition": "Used to say someone will inevitably need to do something.",
    "japaneseMeaning": "〜しなければならなくなる、〜する羽目になる",
    "etymology": "be going to have to doで「いずれ／必然的に〜しなければならない」と将来の義務を述べる。",
    "examples": {
        "B": "日本で医療が無料だったらいいけど、誰かが払わなきゃいけないでしょ？現実的じゃないよ。",
        "C": "フランス語の勉強はどう？僕もそろそろスペイン語を復習しなきゃ。使わないと忘れるよね。",
        "D": "おそらく〜しなければならない",
    },
},
38: {
    "nativeDefinition": "Used to say someone will need to do something in the future.",
    "japaneseMeaning": "〜する必要があるだろう、〜しなきゃ",
    "etymology": "be going to need to doで「（近い将来）〜する必要が出てくる」と必要性を予告する。",
    "examples": {
        "B": "ネイティブが使うフレーズを早く覚えたいなら、Distinctionみたいな良い教材が必要になるよ。",
        "C": "いずれアメリカに移住したいから、そろそろ運転を覚える必要がある。",
        "D": "おそらく必要だ",
    },
},
39: {
    "nativeDefinition": "Used to say someone will need something in the future.",
    "japaneseMeaning": "〜が必要になる、〜を要する",
    "etymology": "be going to need + 名詞で「（これから）〜が必要になる」と物や援助の必要性を述べる。",
    "examples": {
        "B": "週末に投稿したいなら、明日の朝までにこの動画の初稿が必要になる。",
        "C": "忙しいのはわかるけど、この件は君の助けが必要なんだ。",
        "D": "おそらく何かが必要",
    },
},
40: {
    "nativeDefinition": "Used to describe a planned ongoing action in the near future.",
    "japaneseMeaning": "〜することになる、〜する予定だ",
    "etymology": "be going to be doingで「（近い将来）ずっと／しばらく〜していることになる」と継続動作の予定を述べる。",
    "examples": {
        "B": "火曜日に試験があるから、午後ずっと図書館で勉強することになる。",
        "C": "今日の動画では、最高のスイカジュースの作り方について話していく予定だ。",
        "D": "〜する予定だ",
    },
},
41: {
    "nativeDefinition": "Used in casual speech to suggest going somewhere to do something.",
    "japaneseMeaning": "〜に行こう、〜しに行く",
    "etymology": "go + 動詞原形は口語で「〜しに行こう」と誘う・提案するカジュアルな構文。",
    "examples": {
        "B": "ランチ食べに行かない？いい店知ってるよ。",
        "C": "お気持ちはわかりますが、僕には権限がなくて。店長に話しに行ってみますね。",
        "D": "行って〜する",
    },
},
42: {
    "nativeDefinition": "Used to invite someone to come and do something.",
    "japaneseMeaning": "〜しに来て、〜してみて",
    "etymology": "come + 動詞原形で「来て〜して」と誘う口語表現。come visit, come join usなど。",
    "examples": {
        "B": "サンフランシスコに新店をオープンしたから、ぜひ遊びに来て。",
        "C": "彼女に会いに来てくれたらいいのに。今すごく忙しいから無理なんだけど。",
        "D": "来て〜しなさい",
    },
},
43: {
    "nativeDefinition": "Used when something refuses to work or someone refuses to allow something.",
    "japaneseMeaning": "どうしても〜しない、〜させてくれない",
    "etymology": "won't/wouldn't doで「どうしても〜しない／させてくれない」と強い拒否・不調を表す。",
    "examples": {
        "B": "アプリが開かないんだ。何度もインストールし直したけどダメ。",
        "C": "高校の時、親は9時過ぎまで外出させてくれなかった。過保護だったと思う？",
        "D": "しない、しなかった",
    },
},
44: {
    "nativeDefinition": "Used to reveal an unexpected fact after learning or discovering something.",
    "japaneseMeaning": "〜だとわかった、実は〜だった",
    "etymology": "turns out thatで「調べたら／後からわかったら、実は〜だった」と意外な結果を報告する。",
    "examples": {
        "B": "猫がアヒルと踊ってる動画にすごく感動したんだけど、全部フェイクだったんだ。",
        "C": "Twitterでステーキの焼き方で口論してた相手、シェフだったんだ。最初から間違ってるのわかってたのに。",
        "D": "驚くべきことに",
    },
},
45: {
    "nativeDefinition": "Used when you realize you are doing something, often unintentionally.",
    "japaneseMeaning": "（気づいたら）〜している、思わず〜してしまう",
    "etymology": "find oneself doingで「気づいたら〜していた／いつも〜してしまう」と無意識の行動を述べる。",
    "examples": {
        "B": "最近なんとなく何もせずダラダラしてる自分に気づいた。早く抜け出さないと。",
        "C": "ここ数ヶ月、気づいたらマネージャーの役を引き受けてた。自分でも誇らしい。",
        "D": "どういうわけか〜している",
    },
},
46: {
    "nativeDefinition": "Used to introduce a hypothetical scenario for discussion.",
    "japaneseMeaning": "仮に〜だとしたら、例えば〜なら",
    "etymology": "let's sayで「仮に〜だとしよう」と仮定の場面を設定して議論を進める。",
    "examples": {
        "B": "仮に先週の金曜にスピードデーティングに行ったとして、本当に運命の人に出会えたと思う？無理でしょ。だから行かないんだ。",
        "C": "仮に奥さんが家計を支えて、今ほど働かなくていいとしたら、幸せ？",
        "D": "仮定しよう",
    },
},
47: {
    "nativeDefinition": "Used to make a strong suggestion or recommendation.",
    "japaneseMeaning": "〜すべきだ、〜しよう",
    "etymology": "I sayで「私はこう言う／こうすべきだ」と強めの提案・意見を述べる。",
    "examples": {
        "B": "リズが彼女になるかどうか決めるのに時間かけすぎ。保険みたいに扱ってる気がするから、そろそろはっきりさせた方がいいと思う。",
        "C": "長いエッセイで説明するより図を描こう。一枚の絵は千の言葉に値するから。",
        "D": "〜すべきだと思う",
    },
},
48: {
    "nativeDefinition": "Used to give a personal estimate or opinion.",
    "japaneseMeaning": "〜だと思う、〜だろうね",
    "etymology": "I'd sayで「私ならこう言う／こう見積もる」と個人的な評価・推定を述べる。",
    "examples": {
        "B": "洗濯はまとめてやった方が、毎日少しずつやるよりずっと効率的だと思う。",
        "C": "経済学者は未来を予測できるかのように振る舞うけど、科学というより芸術に近いと思う。",
        "D": "私の見解では",
    },
},
49: {
    "nativeDefinition": "Used to describe what people would say upon seeing or experiencing something.",
    "japaneseMeaning": "〜と言うだろう、〜って言うはず",
    "etymology": "and sayで「見たら／食べたらこう言うだろう」と他者の反応を予想する。",
    "examples": {
        "B": "孫たちが今のスマホを見て、こんなのすごいと思ってたの？って言うだろうね。",
        "C": "きゅうりに蜂蜜、面白い組み合わせだよ。食べたらメロンみたいだって言うはず。",
        "D": "そして言うだろう",
    },
},
50: {
    "nativeDefinition": "Used to describe what people would think upon seeing or considering something.",
    "japaneseMeaning": "〜と思うだろう、〜って思うはず",
    "etymology": "and thinkで「見たらこう思うだろう」と他者の内心の反応を予想する。",
    "examples": {
        "B": "半分しか剃ってない頭を見たら、わざとやったの？ってほとんどの人は思うだろうね。",
        "C": "森を歩いてる時、木々が話せたら何を教えてくれるんだろうって、たまに立ち止まって考える。",
        "D": "そして思うだろう",
    },
},
51: {
    "nativeDefinition": "Used to predict what someone would do in a hypothetical situation.",
    "japaneseMeaning": "〜するだろう、〜してくれないだろう",
    "etymology": "sb would doで「（その状況なら）こうするだろう」と仮定の場面での行動を予測する。",
    "examples": {
        "B": "新しい車買いたいんだけど、妻は許してくれないだろうね。先月勝手に時計買った時すごく怒られたから。",
        "C": "引っ越しの家具運び手伝ってくれない？200ドルは払うよ。",
        "D": "〜するだろうと思う",
    },
},
52: {
    "nativeDefinition": "Used to describe typical or expected behavior of someone or something.",
    "japaneseMeaning": "〜するものだ、普通は〜する",
    "etymology": "sb/sth would doで一般的傾向・典型例として「普通はこうする」と述べる。",
    "examples": {
        "B": "アメリカ人はcenterのtを発音しないけど、イギリス人は普通発音する。",
        "C": "ローカライズって商品を現地のニーズに合わせることだよ。例えばスタバの日本版みたいに、桜フラペやほうじ茶ラテがある。",
        "D": "〜すると思う",
    },
},
53: {
    "nativeDefinition": "Used to give advice or a recommendation.",
    "japaneseMeaning": "〜することをお勧めする、〜した方がいい",
    "etymology": "I'd suggest/recommend thatで「〜することを勧める」と助言・推薦を述べる。",
    "examples": {
        "B": "授業中はメモを取ることをお勧めする。スライドは学生サイトにアップされないから。",
        "C": "週末はしっかり寝た方がいいよ。すごく疲れて見える。",
        "D": "提案する、勧める",
    },
},
54: {
    "nativeDefinition": "Used to describe past habitual actions.",
    "japaneseMeaning": "よく〜していた、いつも〜したものだ",
    "etymology": "would doは過去の習慣・反復を表す。「いつも〜していた」「よく〜したものだ」。",
    "examples": {
        "B": "この番組懐かしい。放課後に何時間もテレビの前に座って見てたのを思い出す。",
        "C": "大学時代は大変だった。ほとんど毎日、授業前にレストランで働いて、夜はバーやクラブで働いてた。",
        "D": "以前よく〜した",
    },
},
55: {
    "nativeDefinition": "Used to say what you would do in someone's situation.",
    "japaneseMeaning": "私なら〜する、〜した方がいい",
    "etymology": "I'd doで「私ならこうする／こうすべき」と自分ならの行動を助言する。",
    "examples": {
        "B": "ランチの予約は早めに取った方がいいよ。あの店すごく混むから。",
        "C": "昇進したのに給料上がらないの？絶対交渉した方がいいよ。同じ給料で仕事増えるなんてありえない。",
        "D": "すべきだ",
    },
},
56: {
    "nativeDefinition": "Used to say what someone would have done in a past hypothetical situation.",
    "japaneseMeaning": "〜しただろうに、〜していたはず",
    "etymology": "would've doneは過去の仮定「（もし〜だったら）こうしていただろうに」と後悔や想像を述べる。",
    "examples": {
        "B": "10代の時にYouTubeがあれば、めちゃくちゃ稼げたのに。",
        "C": "NBAの試合つまらないなんて。チケットくれれば僕はめちゃくちゃ楽しんだのに。",
        "D": "しただろう",
    },
},
57: {
    "nativeDefinition": "Used to infer what someone probably did or experienced in the past.",
    "japaneseMeaning": "〜していただろう、〜したはずだ",
    "etymology": "would've doneは過去の推定「（その状況なら）きっと〜していた」と経験を推測する。",
    "examples": {
        "B": "祖父母が子供の頃は、この古いレコードプレーヤーで音楽を聴いてたんだろうね。",
        "C": "この壺は古代エジプト人が食料や水を保存するのに使っていたはずだ。",
        "D": "おそらくした",
    },
},
58: {
    "nativeDefinition": "Used to express surprise that something is not as expected.",
    "japaneseMeaning": "〜だと思っていたのに、〜のはずなのに",
    "etymology": "I would've thought thatで「普通はこうだと思うのに（実際は違った）」と予想とのズレを述べる。",
    "examples": {
        "B": "すごく楽しそうだね。クラブで踊るの嫌いだと思ってたのに。",
        "C": "自分で食事代払ったの？上司とランチなら会社持ちだと思ってた。",
        "D": "そうだと思っていたが違った",
    },
},
59: {
    "nativeDefinition": "Used to express a reasonable assumption or expectation.",
    "japaneseMeaning": "〜だと思う、〜のはずだ",
    "etymology": "I'd think thatで「普通はこうだと思う」と妥当な推測を述べる。",
    "examples": {
        "B": "10月のオーストラリア行きの便はそんなに高くないと思う。あの時期はどこ行くにもセールが多いから。",
        "C": "何歳だと思う？難しい質問だね。20代前半くらいかな。",
        "D": "想像する",
    },
},
60: {
    "nativeDefinition": "Used when something is surprisingly not as one would expect.",
    "japaneseMeaning": "〜だと思うけど（実際は違う）、〜のはずなのに",
    "etymology": "you'd think thatで「普通そう思うよね（なのに違う）」と常識とのギャップを指摘する。",
    "examples": {
        "B": "日本ってすごく技術が進んでると思うでしょ。でも先日、クレジットカード作るのに身分証のコピーを印刷して貼って郵送しろって言われたんだ。",
        "C": "この青いロボットキャラ、ラクーンかと思うでしょ。実は猫なんだ。",
        "D": "そう思うのも無理はない",
    },
},
61: {
    "nativeDefinition": "Used to say something might or is able to happen.",
    "japaneseMeaning": "〜するかもしれない、〜できる",
    "etymology": "could doは可能性・能力を表す。「〜かもしれない」「〜できる」。",
    "examples": {
        "B": "彼女の誕生日プレゼントは早めに注文した。届くのに最大6週間かかるって言われたから。",
        "C": "上司は昇進を後押ししてくれるかもしれないけど、本当にそうするかはわからない。",
        "D": "〜するかもしれない",
    },
},
62: {
    "nativeDefinition": "Used to discuss future possibilities or ability.",
    "japaneseMeaning": "〜できるかもしれない、〜する可能性がある",
    "etymology": "could doは将来の可能性について「〜できる／〜するかもしれない」と述べる。",
    "examples": {
        "B": "いつかAIがほとんどの仕事を代替するかもしれないけど、まだ成熟してないと思う。",
        "C": "イーロン・マスクは10年以内に人類が火星に着陸できると言ってる。現実的だと思う？",
        "D": "〜できるかもしれない",
    },
},
63: {
    "nativeDefinition": "Used to mention something as a possible option.",
    "japaneseMeaning": "〜してもいい、〜するのもあり",
    "etymology": "could doは選択肢として「〜するのもあり」と可能性を示す。go for ramen, could walkなど。",
    "examples": {
        "B": "今日スマホ落として画面割っちゃった。新しいの買ってもいいけど、新しい機種が好きじゃないから修理したい。",
        "C": "自転車じゃなくて歩いて行ってもいいよ。そんなに遠くないし。",
        "D": "選択肢だ",
    },
},
64: {
    "nativeDefinition": "Used to suggest a possible explanation for something.",
    "japaneseMeaning": "〜かもしれない、〜の可能性がある",
    "etymology": "it could/might/may be thatで「もしかしたら〜ということかもしれない」と原因・理由の可能性を述べる。",
    "examples": {
        "B": "ウェインが自然にフィットしてるのかもしれないけど、運動をかなり頻繁にしてる可能性の方が高い。ノーペイン・ノーゲインだから。",
        "C": "子供が学校を嫌がる理由はたくさんある。いじめられてるのかもしれない。勉強についていけてないのかもしれない。複合的な要因かもしれない。",
        "D": "たぶん",
    },
},
65: {
    "nativeDefinition": "Used to say there is no strong reason not to do something.",
    "japaneseMeaning": "〜した方がいい、〜してもいいんじゃない",
    "etymology": "might as well doで「どうせ〜した方がマシ」「やるしかない」と消極的だが合理的な選択を述べる。",
    "examples": {
        "B": "もう提出しちゃおう。締切は明日だし、この段階でできることは限られてるから。",
        "C": "その情報は読者を混乱させるかもしれないから、記事からは省いちゃった方がいいよ。",
        "D": "〜した方がいいかもしれない",
    },
},
}
