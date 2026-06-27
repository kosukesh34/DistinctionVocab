#!/usr/bin/env python3
"""Generate all vibe manual translation batch files and vibe.json."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "distinction_manual" / "vibe_source.json"
OUT = ROOT / "data" / "distinction_manual" / "vibe.json"
SCRIPTS = Path(__file__).resolve().parent


def e(num, nd, jm, et, b, c, d):
    return num, {
        "nativeDefinition": nd,
        "japaneseMeaning": jm,
        "etymology": et,
        "examples": {"B": b, "C": c, "D": d},
    }


# fmt: off
# (number, nativeDefinition, japaneseMeaning, etymology, B, C, D)
RAW = [
e(1,"The distinctive atmosphere or feeling of a place, person, or situation.","雰囲気、バイブス","vibration（振動）の短縮形で、人や場所から感じ取れる独特の空気感を表すスラング。","あのレストランは雰囲気が最高だし、料理もすごく美味しい。","マットは本当にいい人だよ。彼のポジティブな雰囲気が好きなんだ。","気まぐれな性格"),
e(2,"To make brief contact with someone to discuss or update them on something.","（人と）連絡を取る、様子を確認する","野球のベースに触れるイメージから、短く連絡を取ることを表すビジネス英語。","マークです。来週のミーティングについて、一度連絡を取りたくて電話しました。","アイデアが形になってきたので、来週あなたに連絡を取ります。","誰かに連絡する"),
e(3,"Slang for something excellent, impressive, or exciting.","最高だ、めちゃくちゃいい（スラング）","fire（火）から、燃えるほど素晴らしいという意味で使われる現代スラング。","この景色は最高だ。街を見渡していると世界の頂点にいる気分になる。","この曲は最高だよ。即興で作ったなんて信じられない。","すごい"),
e(4,"To be fully understood or realized, especially after a delay.","（理解・実感が）じわじわと身に染みる、腑に落ちる","sink（沈む）＋ in（中へ）で、情報が心の中に沈み込んで理解されるイメージ。","優勝したこと、まだ実感がわかない。","念願の仕事に就けたことが、ようやく実感としてわいてきた。","完全に理解される"),
e(5,"There is no limit to what someone can achieve.","限界はない、可能性は無限大","空が限界という比喩で、どこまでも上を目指せることを表す。","彼の天性の才能なら、可能性は無限大だ。","人生で何をしたい？俳優？起業？可能性は無限大だよ。","制限はない"),
e(6,"To be very willing and eager to do something.","喜んで〜する、大歓迎で〜する","happy（喜んで）を more than（それ以上に）で強調し、非常に快く引き受けることを表す。","喜んでお手伝いしますよ。","ゆっくりしていいですよ。喜んで待ちます。","とても進んで〜する"),
e(7,"Something boring, tedious, or annoying.","面倒なこと、退屈なこと","drag（引きずる）から、時間が長く感じられる退屈なことを比喩的に表す。","朝にスーツとネクタイを着るのは本当に面倒だ。特に急いでいるときは。","彼女がインスタで私のフォロー相手を一つ一つチェックしているのを見た。本当に面倒だ。","新しい意味"),
e(8,"A day that is significant, eventful, or demanding.","大事な日、充実した一日","big（大きい）＋ day（日）で、重要な出来事のある日を表す。","今夜はゆっくりしたい。今日は充実した一日だったから。","今日は大事な日だ。遠くに住む親友にやっと会える。","とても大変な日。とても重要な日。"),
e(9,"More than what is needed or sufficient.","十分すぎるほど、余裕で","enough（十分）を more than（それ以上）で強調し、必要以上にあることを表す。","彼女は「2時間無視されたら、それだけで私にとって何でもない証拠だ」と言った。ちょっと大げさだと思う。","今日はもう十分やったので、そろそろ帰ります。","十分以上"),
e(10,"To resist or confront something or someone unfair or abusive.","（不当な扱いに）立ち向かう、抵抗する","stand up（立ち上がる）で、不正に対して毅然と立ち向かうイメージ。","理由もなく上司に怒鳴られたときは立ち向かうべきだと思うけど、決定権を握っている相手だから難しい。","前向きでいることが、ネガティブに立ち向かう最善の方法だ。","不当な虐待的扱いを受け入れない"),
]
# fmt: on
# PLACEHOLDER_MORE
