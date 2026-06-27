#!/usr/bin/env python3
"""Generate vibe_manual_translations.json with all 399 Distinction VI translations."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "distinction_manual" / "vibe_source.json"
OUT = Path(__file__).with_name("vibe_manual_translations.json")

# fmt: off
T: dict[int, dict] = {
1: {"nativeDefinition": "The distinctive atmosphere or feeling of a place, person, or situation.", "japaneseMeaning": "雰囲気、バイブス", "etymology": "vibration（振動）の短縮形で、人や場所から感じ取れる独特の空気感を表すスラング。", "examples": {"B": "あのレストランは雰囲気が最高だし、料理もすごく美味しい。", "C": "マットは本当にいい人だよ。彼のポジティブな雰囲気が好きなんだ。", "D": "気まぐれな性格"}},
2: {"nativeDefinition": "To make brief contact with someone to discuss or update them on something.", "japaneseMeaning": "（人と）連絡を取る、様子を確認する", "etymology": "野球のベースに触れるイメージから、短く連絡を取ることを表すビジネス英語。", "examples": {"B": "マークです。来週のミーティングについて、一度連絡を取りたくて電話しました。", "C": "アイデアが形になってきたので、来週あなたに連絡を取ります。", "D": "誰かに連絡する"}},
3: {"nativeDefinition": "Slang for something excellent, impressive, or exciting.", "japaneseMeaning": "最高だ、めちゃくちゃいい（スラング）", "etymology": "fire（火）から、燃えるほど素晴らしいという意味で使われる現代スラング。", "examples": {"B": "この景色は最高だ。街を見渡していると世界の頂点にいる気分になる。", "C": "この曲は最高だよ。即興で作ったなんて信じられない。", "D": "すごい"}},
4: {"nativeDefinition": "To be fully understood or realized, especially after a delay.", "japaneseMeaning": "（理解・実感が）じわじわと身に染みる、腑に落ちる", "etymology": "sink（沈む）＋ in（中へ）で、情報が心の中に沈み込んで理解されるイメージ。", "examples": {"B": "優勝したこと、まだ実感がわかない。", "C": "念願の仕事に就けたことが、ようやく実感としてわいてきた。", "D": "完全に理解される"}},
5: {"nativeDefinition": "There is no limit to what someone can achieve.", "japaneseMeaning": "限界はない、可能性は無限大", "etymology": "空が限界という比喩で、どこまでも上を目指せることを表す。", "examples": {"B": "彼の天性の才能なら、可能性は無限大だ。", "C": "人生で何をしたい？俳優？起業？可能性は無限大だよ。", "D": "制限はない"}},
6: {"nativeDefinition": "To be very willing and eager to do something.", "japaneseMeaning": "喜んで〜する、大歓迎で〜する", "etymology": "happy（喜んで）を more than（それ以上に）で強調し、非常に快く引き受けることを表す。", "examples": {"B": "喜んでお手伝いしますよ。", "C": "ゆっくりしていいですよ。喜んで待ちます。", "D": "とても進んで〜する"}},
7: {"nativeDefinition": "Something boring, tedious, or annoying.", "japaneseMeaning": "面倒なこと、退屈なこと", "etymology": "drag（引きずる）から、時間が長く感じられる退屈なことを比喩的に表す。", "examples": {"B": "朝にスーツとネクタイを着るのは本当に面倒だ。特に急いでいるときは。", "C": "彼女がインスタで私のフォロー相手を一つ一つチェックしているのを見た。本当に面倒だ。", "D": "新しい意味"}},
8: {"nativeDefinition": "A day that is significant, eventful, or demanding.", "japaneseMeaning": "大事な日、充実した一日", "etymology": "big（大きい）＋ day（日）で、重要な出来事のある日を表す。", "examples": {"B": "今夜はゆっくりしたい。今日は充実した一日だったから。", "C": "今日は大事な日だ。遠くに住む親友にやっと会える。", "D": "とても大変な日。とても重要な日。"}},
9: {"nativeDefinition": "More than what is needed or sufficient.", "japaneseMeaning": "十分すぎるほど、余裕で", "etymology": "enough（十分）を more than（それ以上）で強調し、必要以上にあることを表す。", "examples": {"B": "彼女は「2時間無視されたら、それだけで私にとって何でもない証拠だ」と言った。ちょっと大げさだと思う。", "C": "今日はもう十分やったので、そろそろ帰ります。", "D": "十分以上"}},
10: {"nativeDefinition": "To resist or confront something or someone unfair or abusive.", "japaneseMeaning": "（不当な扱いに）立ち向かう、抵抗する", "etymology": "stand up（立ち上がる）で、不正に対して毅然と立ち向かうイメージ。", "examples": {"B": "理由もなく上司に怒鳴られたときは立ち向かうべきだと思うけど、決定権を握っている相手だから難しい。", "C": "前向きでいることが、ネガティブに立ち向かう最善の方法だ。", "D": "不当な虐待的扱いを受け入れない"}},
11: {"nativeDefinition": "A person who visits a place frequently; a habitual customer.", "japaneseMeaning": "常連客、常連", "etymology": "regular（規則的な）から、定期的に訪れる人を指す。", "examples": {"B": "カフェの店主がもう私の名前を覚えてくれた。ついに常連になった。", "C": "あまり頻繁には行かないけど、行くたびに彼女がいる。きっと常連なんだろう。", "D": "常連の訪問者や顧客"}},
12: {"nativeDefinition": "To cause someone to feel disgusted or repulsed.", "japaneseMeaning": "（人を）気持ち悪がらせる、ゾッとさせる", "etymology": "gross（気持ち悪い）の使役形で、強い嫌悪感を与えることを表す。", "examples": {"B": "私の強迫観念がつらい。何人もと握手しなきゃいけないとき、ちょっと気持ち悪くなる。", "C": "ゴキブリほど気持ち悪いものはない。", "D": "誰かについて話し合う"}},
13: {"nativeDefinition": "To owe someone a favor because they helped you.", "japaneseMeaning": "（人に）借りができる、恩がある", "etymology": "owe（借りている）＋ one（一つ）で、一つ恩義があることを表すカジュアルな表現。", "examples": {"B": "昨夜の行方について嘘をついてあげられるよ。でもお前も一つ借りができるぞ。", "C": "ランチを取ってきてくれてありがとう。借りができるよ。", "D": "誰かに感謝している"}},
14: {"nativeDefinition": "Unnecessary and inappropriate; not justified.", "japaneseMeaning": "必要のない、行き過ぎた", "etymology": "uncalled for は「呼ばれていない」、つまり必要もないことを表す。", "examples": {"B": "サムは時々うざいけど、みんなの前で彼を酷く扱うのは行き過ぎだと思う。", "C": "あの否定的なツイートは本当に必要のないものだった。最後の一押しでフォローを外した。", "D": "不必要な"}},
15: {"nativeDefinition": "To pay for something as a gift or special treat for someone.", "japaneseMeaning": "（人に）〜をごちそうする、おごる", "etymology": "treat（もてなす）で、食事や贈り物をおごることを表す。", "examples": {"B": "今夜ディナーをおごってもいい？最近すごく助けてくれたから、何かお返ししたいんだ。", "C": "後でウイスキーをごちそうしよう。今週は大変だったから。", "D": "贈り物や報酬として何かを与える"}},
16: {"nativeDefinition": "I completely agree with what you just said.", "japaneseMeaning": "その通り、まさにそう", "etymology": "「もう一度言ってもいいよ」という形から、強い同意を表す表現になった。", "examples": {"B": "「彼は生まれながらの金持ちだね」「その通り。一日も働いたことがないって本人が言ってたよ。」", "C": "「便りがないのは良い知らせ？」「まさにそう。リズからのメッセージのたびに、何かひどいことが起きたみたいなんだ。」", "D": "完全に同意する"}},
17: {"nativeDefinition": "That is disappointing or unfortunate.", "japaneseMeaning": "残念だね、それは惜しい", "etymology": "shame（残念なこと）を that is で受け、残念な状況を表す。", "examples": {"B": "え、もう売り切れ？残念だね。ヤフオクでメルカリをすぐ確認してみる。", "C": "Netflixがお気に入りの番組を打ち切った。残念だね。", "D": "がっかりする"}},
18: {"nativeDefinition": "To support and protect someone.", "japaneseMeaning": "（人の）味方でいる、バックアップする", "etymology": "have one's back（背中を預ける）で、困ったときに支えてくれることを表す。", "examples": {"B": "心配しないで。何が起きても、いつも味方だから。", "C": "マークはいつも味方してくれる。いつ電話しても出てくれる。", "D": "誰かを支援する"}},
19: {"nativeDefinition": "Very selective or hard to please, especially about small details.", "japaneseMeaning": "（食べ物などに）うるさい、好みが厳しい", "etymology": "pick（選ぶ）から、細かいところまでこだわって選ぶ人を表す。", "examples": {"B": "彼女はすごくうるさいから、コーヒーをどこで飲むかは彼女に決めてもらう。僕ならコンビニでいいんだけど。", "C": "彼はインテリアデザイナーだから、家具にはかなりうるさい。", "D": "こだわりのある"}},
20: {"nativeDefinition": "To have no idea or knowledge about something.", "japaneseMeaning": "まったくわからない、見当もつかない", "etymology": "clue（手がかり）がない、つまり全く見当がつかないことを表す。", "examples": {"B": "このラスボスをどうやって倒すかまったくわからない。弱点があるはずなのに、見つけられない。", "C": "クラスの男子全員がiPhoneを使う理由がまったくわからない。Androidの方がずっといいと思う。", "D": "見当もつかない"}},
21: {"nativeDefinition": "To give a particular impression to others.", "japaneseMeaning": "（そういう）印象を与える", "etymology": "come across（出会う・伝わる）で、相手に与える印象を表す。", "examples": {"B": "フレッド、私が怒ってると思ったの？そんなつもりじゃなかったんだ。ただ疲れてただけ。", "C": "直接会ったらすごく意地悪だった。Twitter上ではそんな印象を与えなかったのに。", "D": "その印象を与える"}},
22: {"nativeDefinition": "Coming very soon; imminent.", "japaneseMeaning": "もうすぐ、間近に", "etymology": "角（corner）の向こうにすぐある、という比喩で間近を表す。", "examples": {"B": "また早起きの生活に戻して新学期に備える。もうすぐだ。", "C": "誕生日がもうすぐだなんて信じられない。もう1年経ったの？", "D": "もうすぐ来る"}},
23: {"nativeDefinition": "To disappoint someone by failing to meet expectations.", "japaneseMeaning": "（人を）がっかりさせる、裏切る", "etymology": "let down（下に落とす）で、期待を裏切ることを表す。", "examples": {"B": "体調が優れないので今日のワークショップはキャンセルする。みんなをがっかりさせたくなかったけど、安全が第一だ。", "C": "今月だけで5回目のディナーキャンセルだ。正直ちょっとがっかりしてる。", "D": "誰かを失望させる"}},
24: {"nativeDefinition": "The most important or essential point.", "japaneseMeaning": "要するに、結論として", "etymology": "会計の bottom line（最終利益）から、最も重要な点を表すようになった。", "examples": {"B": "要するに、来年の計画を具体化するには何としても資金を調達する必要がある。", "C": "理由はあったと思うけど、結論として一番必要なときに見捨てられた。", "D": "重要なポイント"}},
25: {"nativeDefinition": "To think about something too much or too anxiously.", "japaneseMeaning": "（ことを）考えすぎる、深く考え込む", "etymology": "over（過度に）＋ think（考える）で、必要以上に考え込むことを表す。", "examples": {"B": "考えすぎないで、人生を楽しんで。誰にでも浮き沈みはある。", "C": "私は考えすぎる癖があるから、これからは気楽にいこうと思う。", "D": "何かについて考えすぎる"}},
26: {"nativeDefinition": "To have meaningful activities and interests outside of work.", "japaneseMeaning": "プライベートがある、自分の生活がある", "etymology": "have a life（人生がある）で、仕事以外に充実した生活があることを表す。", "examples": {"B": "いつもオフィスにいる。プライベートがないんじゃないか。", "C": "呼ばれたからってすぐ飛んでいけないよ。自分の生活もあるんだから。", "D": "人生に意味のあることをする"}},
27: {"nativeDefinition": "Someone is already handling or working on it.", "japaneseMeaning": "（誰かが）対応中だ、任せて", "etymology": "on it（それに取り組んでいる）で、すでに対応していることを表す。", "examples": {"B": "調査は心配しないで。僕がやってる。", "C": "プレゼンのスライドの仕上げは心配しないで。もう対応してる。", "D": "誰かがそれに取り組んでいる"}},
28: {"nativeDefinition": "A lazy person who spends a lot of time sitting and watching TV.", "japaneseMeaning": "ソファーに寝転がるだけの人、ぐうたら", "etymology": "couch（ソファー）＋ potato（じゃがいも）で、動かずに座りっぱなしの人を表す。", "examples": {"B": "今日はぐうたらしたいのに、友達がずっと遊ぼうってうるさい。", "C": "子どもが一日にテレビを見られる時間にはルールがある。ぐうたらになるのは嫌だから。", "D": "怠惰な人"}},
29: {"nativeDefinition": "To amaze or astonish someone greatly.", "japaneseMeaning": "（人を）驚かせる、度肝を抜く", "etymology": "blow one's mind（心を吹き飛ばす）で、強烈な驚きを与えることを表す。", "examples": {"B": "父がサプライズプレゼントをくれた。完全に不意打ちで度肝を抜かれた。", "C": "プレステ1を手に入れたときのグラフィックは当時度肝を抜かれた。すごかった！", "D": "誰かの基準"}},
30: {"nativeDefinition": "Occasionally; from time to time.", "japaneseMeaning": "たまに、時々", "etymology": "now and then（今とそれから）で、時折という意味。", "examples": {"B": "英語を3年勉強してるけど、まだたまに単語をググる。", "C": "娘がたまに好きな食べ物を届けに来てくれる。", "D": "時々"}},
31: {"nativeDefinition": "To take care of and watch over someone.", "japaneseMeaning": "（人の）面倒を見る、気にかける", "etymology": "look out（見張る）＋ for（〜のために）で、誰かのことを気にかけることを表す。", "examples": {"B": "雑談が苦手で冷たく見えるけど、実はいつも周りの人のことを気にかけている。", "C": "ブライアンの面倒を見てくれる？新人だからまだ指導が必要なんだ。", "D": "誰かの世話をする"}},
32: {"nativeDefinition": "Disregard that; ignore what was just said.", "japaneseMeaning": "それは忘れて、やっぱりなし", "etymology": "forget about（〜について忘れる）で、直前の発言を取り消す表現。", "examples": {"B": "あの数字を直してくれる？やっぱりなし。バッチリ合ってる。", "C": "今夜飲み物を買ってくるって言ったっけ？やっぱりなし。家にたくさんある。", "D": "それを無視する"}},
33: {"nativeDefinition": "To upset, disturb, or make someone nervous.", "japaneseMeaning": "（人を）動揺させる、ひどく不安にさせる", "etymology": "rattle（ガタガタ鳴らす）で、心を揺さぶって動揺させることを表す。", "examples": {"B": "あの映画で一日中動揺しっぱなしだった。ホラー映画はもう二度と見ない。", "C": "向こうの相手チームの応援団のことは気にしないで。試合前に動揺させようとしてるだけだ。", "D": "戦士のように誰かを動揺させる"}},
34: {"nativeDefinition": "An overly enthusiastic female fan of a celebrity.", "japaneseMeaning": "熱狂的な女性ファン、ファンガール", "etymology": "fan（ファン）＋ girl（女の子）の造語で、熱狂的な女性ファンを指す。", "examples": {"B": "女優が他の女優に熱狂するのを見るの、すごく可愛い。", "C": "このYouTuberの売りはよくわからないけど、ファンガールがたくさんいるみたい。", "D": "過度に熱狂的なファン"}},
35: {"nativeDefinition": "I don't know either; we are equally uncertain.", "japaneseMeaning": "私にもわからない、お互い様", "etymology": "your guess is as good as mine で、相手の推測も自分と同じくらい当てになる、つまりわからないことを表す。", "examples": {"B": "次のボーナスがいくらかは言えない。私にもわからない。", "C": "明日雪が降るといいけど、私にもわからない。", "D": "私もよくわからない"}},
36: {"nativeDefinition": "To remain in a place; stay nearby.", "japaneseMeaning": "（その場に）留まる、そばにいる", "etymology": "stick（くっつく）＋ around（周りに）で、近くに留まることを表す。", "examples": {"B": "いつまでもここにいるわけじゃないから、聞きたいことがあるなら早めにして。", "C": "彼が朝3時までそばにいるのは驚かない。本物のパーティーアニマルだから。", "D": "残る"}},
37: {"nativeDefinition": "The choice of words used in speech or writing.", "japaneseMeaning": "言い回し、表現の仕方", "etymology": "word（言葉）＋ ing で、使われる言葉の選び方を表す。", "examples": {"B": "この手紙に使うべき決まった言い回しはある？法的文書だから、適当に書きたくない。", "C": "このメールの言い回しがいいね。チーム全員に転送してくれる？", "D": "表現"}},
38: {"nativeDefinition": "At the current point in a process or situation.", "japaneseMeaning": "現時点では、この段階では", "etymology": "stage（段階）で、今の時点での状況を表す。", "examples": {"B": "現時点ではロンドンに永住するつもりはない。数年後に気が変わるかもしれないけど。", "C": "現時点ではランチの場所は決まってない。後で考えよう。", "D": "この時点で"}},
39: {"nativeDefinition": "To pass time while waiting for something.", "japaneseMeaning": "時間をつぶす", "etymology": "kill（殺す）＋ time（時間）で、待ち時間を何かで過ごすことを表す。", "examples": {"B": "誰かからメッセージが来てほしい。時間をつぶしたいんだ。", "C": "空港で20時間も時間をつぶさなきゃいけない。耐えられるといいけど。", "D": "待っている間に何かに忙しくする"}},
40: {"nativeDefinition": "Something overpriced; a swindle.", "japaneseMeaning": "ぼったくり、法外な値段", "etymology": "rip off（引き裂く）から、不当に高い値段で搾取することを表す。", "examples": {"B": "あの古いiPodに50万円も払ったなんて信じられない。ぼったくられたよ。", "C": "コーヒー1杯に15ドル？ぼったくりだよ！出費を抑えた方がいい。積み重なれば大きいんだから。", "D": "社交する"}},
}
# PLACEHOLDER_BATCH2
# fmt: on


def main() -> None:
    with open(SOURCE, encoding="utf-8") as f:
        source = json.load(f)

    missing = [w["number"] for w in source if w["number"] not in T]
    if missing:
        print(f"WARNING: {len(missing)} translations still missing: {missing[:10]}...")

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({str(k): v for k, v in sorted(T.items())}, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Wrote {len(T)} entries to {OUT}")


if __name__ == "__main__":
    main()
