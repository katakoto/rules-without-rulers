# PROJECT.md — Bitcoin Concept Album「Rules Without Rulers / 支配者のいないルール」

## プロジェクト概要

Andreas M. Antonopoulosのスピーチ語録を核に据えた、日本語Bitcoinコンセプト・アルバムの制作プロジェクト。各曲がAndreasの「一節」から始まり、その思想を日本語の歌詞・リズム・空気感で展開する。翻訳プロジェクト「The Internet of Money（日本語版）」の延長線上にある、「文字での受容」に対する「音での受容」の試み。

最終形：Sunoで全曲生成 → 配信プラットフォーム（Spotify / Apple Music等）でリリース + 自前サーバー（katakoto.org）に本籍地となる特設サイトを構築。

このリポジトリは、その**先行シングル**「Rules Without Rulers」（=アルバム02トラック「支配者のいないルール」の英題リリース）の特設ページを管理する。アルバム本体サイトは別リポジトリ予定。

---

## 制作の基本方針

### 1. 1曲1コンセプト
各曲は Andreas の「一節」を核にする。複数の思想を一曲に詰め込まない。スピーチ由来の熱量とリズムを、日本語の音楽として再構成する。

### 2. 翻訳プロジェクトとの用語統一

訳語は必ず以下に従うこと（歌詞として崩す場合も、核のコンセプトは保持）：

| 英語 | 日本語 | 備考 |
|---|---|---|
| trustless | 信頼不要 | 「信頼できない」と誤解させない |
| permissionless | 許可不要 / 誰でも参加できる | |
| decentralized | 分散型 | |
| censorship-resistant | 検閲耐性 | |
| sovereignty | 主権 / 金融主権 | |
| self-custody | 自己管理 / 自己保管 | |
| store of value | 価値の保存手段 | |
| sound money | 健全な通貨 | |
| Internet of Money | お金のインターネット | |
| not your keys, not your coins | 鍵を持たなければ、コインもあなたのものではない | 慣用的表現 |
| Rules Without Rulers | 支配者のいないルール | アルバムの核 |

### 3. ジャンルで感情を翻訳

思想の質感に合わせてジャンルを選ぶ：

- 怒り・告発 → Hardcore Hip-Hop / Punk
- 観察・諦観 → 路地裏Boom Bap / ゆらゆら帝国系アンダーグラウンドロック
- 希望・肯定 → Indie Rock / Synthpop
- 包摂・祈り → Folk / Acoustic
- 未来・永続性 → Ambient / Post-Rock

### 4. 初心者が入口

Bitcoin知識ゼロでも聴ける歌詞を目指す。専門用語は文脈で意味が伝わるように配置する。ただしBitcoinerが聴いても「わかってる」と感じる深度は必ず担保する。

### 5. 日本語ラップの美学を尊重

抽象論で終わらせず、身体性・具体性に着地させる（「路地裏で煙草吹かして考える」「夜中3時ノードの音だけが鳴ってる」「じいちゃんが言ってた」など）。韻は意味の衝突で踏む。

---

## 既存トラックの記録

### 01. 注ぎ込め

- Andreas語録：「我々の労働力、創造性、情熱それら全てを"この場にとどまれ！"と促すこのクソみたいなぶっ壊れたシステムから引き出して、Bitcoinエコシステム、このオープンな金融の未来へと注ぎ込むのだ」
- ジャンル：Japanese Underground Rock（ゆらゆら帝国 style）
- BPM：108
- 状態：歌詞完成、Suno生成待ち

### 02. 王不在 ← このリポジトリの主役

- Andreas語録：「今日に至るまで我々は支配者なしにルールを持つことができなかった。機関による監視・ガイダンス・階層・説明責任といったものなしに、我々はルールを持ちえなかったのだ。Bitcoinは世界に"支配者のいないルール"をもたらす」
- ジャンル：Japanese Underground Hip-Hop（路地裏 / 舐達麻系）
- BPM：86
- 状態：歌詞完成、Suno生成待ち
- **英題リリース「Rules Without Rulers」として先行シングル化**

---

## アルバム収録予定曲（仮）

| # | タイトル | Andreas語録 | ジャンル | 状態 |
|---|---|---|---|---|
| 01 | 注ぎ込め | Pour it into the open financial future | Underground Rock | 完成 |
| 02 | 王不在 (Rules Without Rulers) | Rules without rulers | Underground Hip-Hop | 完成 |
| 03 | Not Your Keys | Not your keys, not your coins | Hardcore Hip-Hop | 未 |
| 04 | Don't Trust, Verify | Don't trust, verify | Dub / Electronic | 未 |
| 05 | お金のインターネット | Bitcoin is the internet of money | Synthpop | 未 |
| 06 | 銀行なき者たちへ | Bitcoin banks the unbanked | Folk | 未 |
| 07 | 十四歳のハッカーたちへ | Somewhere out there is a 14-year-old... | Emo Rock | 未 |
| 08 | 許可なんて要らない | You don't have to ask permission | Punk | 未 |
| 09 | 独裁者のいない通貨 | Money without a dictator | Industrial | 未 |
| 10 | 地平線の向こう | We are building a future we will never see | Ambient / Post-Rock | 未 |

---

## このシングルサイトのデザインコンセプト

### 採用方向: 黒地・主役レコード（方向X）

複数の方向性を比較検討した結果、以下の方向に決定。

- **画面の主役はレコードそのもの**——背景は引く
- 80年代和シティポップの感性は「色」「タイポ」「余白」だけで効かせる——絵で説明しない
- 真っ黒な背景（#050505）に、回転するレコードがどんと中央
- レコード盤上のオレンジBitcoinロゴをそのままPLAYボタンとして機能させる
- トーンアームが外側から針を盤面に降ろすアニメーション
- タイトル・引用は最小限のタイポグラフィでレコードの上下に配置

### 検討して却下した方向

- **路地裏ネオン**: 02王不在の音とは合うが、シティポップの「都市夜景」表現と過剰に重ねるとノイズが多すぎた
- **80年代シティポップのジャケット風シーン**（ホテルのバー、グラスとソファ）: 一度試作したが、レコード本体の存在感を喧嘩して殺してしまった
- **モノクロ・タイポグラフィ重視**: 知的だが音楽的高揚感が弱い
- **カセットテープ・ジン文化**: アルバム本体サイトには採用予定（このシングルサイトとは別フォーマット）

### このサイトとアルバム本体サイトの関係性

- **シングル特設サイト**（このリポジトリ）= レコード世界（一点豪華・回転する物体）
- **アルバム本体サイト**（別途構築）= カセット世界（DIY・ジン・全10曲）

媒体を変えることで、シングルの特別感が立つ。「レコード盤としての先行シングル → 全10曲のミックステープ」という対比。

---

## やらないこと

- 安易な英語カタカナ語の多用（ただしBitcoin用語は例外）
- 教科書的な説明調の歌詞・コピー
- 政治的偏向の直接表現（思想は提示するが、特定政党批判などはしない）
- AI生成曲であることを恥じる姿勢（むしろAndreasの思想とAIの民主化を結びつける視点）
- 著作権上グレーな既存楽曲の模倣

---

## リリース戦略

- 配信先：Spotify / Apple Music / YouTube Music / その他
- X（Twitter）で曲ごとに先行公開
- アルバムジャケット、曲解説記事も制作物として視野に
- Lightning tips: tips@katakoto.org 併設
- **本籍地は自前サーバー**：「This album lives on a server I own」を打ち出す。Spotify/AppleMusicは配信窓口にすぎない、作品の本拠地は自分のドメイン

---

## 作者コンテキスト

- **Hiro**: Williams Lake, BC在住。Bitcoin Maximalist、cypherpunk philosophy
- **パートナー Saki**: フリーランスの漫画エッセイ作家（ジャケットアート協力の可能性あり、アルバム本体サイト関連）
- **lostinbitcoin.jp** の寄稿者
- **翻訳プロジェクト「The Internet of Money 日本語版」**進行中（用語集はこのドキュメントの上記表に集約）

---

## このリポジトリのスコープ

このリポジトリで管理するのは:

- ✅ シングル「Rules Without Rulers」の単独特設ページ
- ✅ 02王不在の歌詞ページ
- ✅ Andreas引用、ライナーノート
- ✅ シングル音源の埋め込み（Suno生成完了後）

このリポジトリで管理しないもの（別途）:

- ❌ アルバム本体サイト（10曲全体 + ジャケットアート + 全歌詞）
- ❌ lostinbitcoin.jp（独立したブログ）
- ❌ 翻訳プロジェクト関連
