# HANDOFF.md — Claude Codeへの引き継ぎ指示書

## このプロジェクトは何か

「Rules Without Rulers / 支配者なきルール」という日本語Bitcoinコンセプト・アルバム（全10曲、Suno生成予定）の**先行シングル特設サイト**を構築する。

詳細なアルバム背景は `PROJECT.md` を参照。**まずそちらを必ず読んでから本ドキュメントに戻ること。**

このサイト自体は**シングル「Rules Without Rulers」（アルバム02トラッ「Rules Without Rulers / 支配者なきルール」を先行リリースしたもの）**の単独ランディングページ。アルバム本体サイトは別途構築予定（このプロジェクトとは別ディレクトリで管理する想定）。

## 引き継ぎ時点の状況

- シングルサイトのデザイン仕様はClaude（Claude.ai）との対話で確定済み
- このパッケージには動作する**HTMLプロトタイプ**が含まれている → `prototype/index.html`
- レコード画像は背景透過処理済みのWebPに変換済み → `prototype/record_circle.webp`
- オリジナルのレコード画像（白背景PNG）も同梱 → `assets/record_original.png`

## 作ってほしいもの

`prototype/index.html` のデザイン・体験を**Astroベースの本番実装**に移植する。プロトタイプは1ファイルHTML+JSでベタ書きされているので、これをコンポーネント分割してメンテナブルなコードベースにする。

### 確定している仕様（プロトタイプから読み取れる）

- 真っ黒背景（#050505）、微細なフィルムグレイン
- ページ中央に円形に切り抜かれたレコード画像が浮かぶ
- レコード盤上のオレンジBitcoinロゴが**そのままPLAYボタン**になる（透明ボタンを重ねる）
- クリックで:
  - レコードが回転（CSS animation、1.5秒/周）
  - トーンアームが外側から針を盤面に降ろす（cubic-bezierイージング）
  - カウンターが秒数を刻む
- 上部に「— A LEAD SINGLE —」キッカー、「王 不 在」「Rules Without Rulers」
- 下部にAndreas引用、ライナーノート、ナビ、フッター
- フォント: Inter（英）、Shippori Mincho（和）、JetBrains Mono（メタ）
- アクセントカラー: Bitcoinオレンジ（#f7931a、レコードラベルの色と一致）

### まだ決まってないこと（実装中に詰めるか、Hiroに確認する）

- **音源ファイル**: Sunoで生成した音源（mp3）が確定したら `<audio>` タグでつなぐ。現状プロトタイプはダミーのカウンター（0:00→3:42でループ）だけ動いている。実装時は本物の音源と同期させる構造に切り替える
- **歌詞ページ**: `/lyrics` のサブページ。歌詞は `02_RulesWithoutRullers.md` として別途渡される予定（Hiroに依頼）
- **アルバム全体ページへのリンク先**: 今は `#` のダミー。アルバム本体サイトのURL確定後に差し替え
- **OGP画像、faviconなど**: 後工程
- **ドメイン**: 最終的に `katakoto.org/single/rules-without-rulers/` 配下か、サブドメインかは未定

### ユーザー（Hiro）が判断したい残りの設計ポイント

実装を始める前にHiroに以下を確認してもいい（または最初は現状維持で実装し、後で微調整する）:

1. レコードの最大サイズ（現状560px）
2. トーンアームの角度・存在感（現状-22度→-2度のスイング）
3. PLAYボタンの常時表示/ホバー表示（現状ホバー時のみ▶白アイコン）
4. 回転速度（現状1.5秒/周＝33⅓ RPM、シネマ的にもっとゆっくりにする選択肢あり）
5. タイトル位置（現状レコードの上）

## 技術スタック

### 採用: Astro

理由:

- 静的サイトで軽い・速い・SEOに強い
- 将来のアルバム本体サイトと同じスタックで揃えられる
- Markdownで歌詞・解説が書ける（10曲分のページを増やすときに有利）
- コンポーネント単位の再利用ができる
- 必要な部分だけJSをハイドレートできる（このサイトはレコードプレイヤー部分のみインタラクティブ）

### 推奨構成

```
src/
├── pages/
│   ├── index.astro          ← トップ（このページ）
│   └── lyrics.astro         ← 歌詞ページ（後工程）
├── components/
│   ├── RecordPlayer.astro   ← レコード+トーンアーム+PLAYボタンの中核
│   ├── Hero.astro           ← タイトル、キッカー、メタストリップ
│   ├── Quote.astro          ← Andreas引用ブロック
│   ├── LinerNote.astro      ← ライナーノート
│   ├── Nav.astro
│   └── Footer.astro
├── layouts/
│   └── BaseLayout.astro     ← フォント読み込み、メタタグ、グレイン
├── styles/
│   └── global.css           ← CSS変数、ベースリセット
└── assets/
    └── record_circle.webp
```

レコードプレイヤーの中身（再生ロジック、トーンアームの動き、回転）はバニラJSで `<script>` タグに書く形でOK。Reactなどのフレームワークを入れる必要はない。

### CSSの方針

プロトタイプの `:root` 変数とほぼ同じ構成を `global.css` に移す。新規にTailwindなどを入れる必要はない（プロジェクトの規模的にオーバーキル）。コンポーネントスコープのスタイルはAstroの `<style>` タグで書く。

### 音源の取り扱い

実装時はおそらく次のような構造になる:

```html
<audio id="track" src="/audio/rules-without-rulers.mp3" preload="metadata"></audio>
```

PLAYボタンは `audio.play()` / `audio.pause()` を呼び、`timeupdate` イベントでカウンターを更新、`ended` でリセット。**現状のダミーカウンターはこの実装に置き換える**。音源ファイルが届くまではプロトタイプ通りのダミーで動かしておいて構わない。

## デプロイの方針

最終的には**Hiroの自前サーバー（katakoto.org）にデプロイ**する。これはこのアルバムの「中央集権プラットフォームに依存しない」思想と整合する。

ただし開発中は **Cloudflare Pages** でプレビューURL を発行して、Hiroが進捗を確認しやすくする。Cloudflare Pagesは無料、Astroの静的ビルドと相性◎、Gitリポジトリと連携してプッシュするだけで自動デプロイされる。

### 推奨フロー

1. ローカルで `npm run dev` で開発
2. GitHubにpush → Cloudflare Pagesで自動プレビュー
3. デザイン確定後、`npm run build` でビルド
4. ビルド成果物（`dist/` フォルダ）を自前サーバーへrsync / scp / FTPでアップロード

`README.md` に上記手順を記録すること。

## Windows環境のセットアップ手順

ユーザー（Hiro）はWindowsユーザー。Claude Codeの動作はWSL（Windows Subsystem for Linux）経由が公式推奨。以下の手順を確認・補助してほしい。

### 前提: WSLとNode.jsが入っているか確認

```bash
wsl --version       # PowerShellで実行 → WSLが入っているか
node --version      # WSL内のターミナルで → Node.js 18+ が望ましい
npm --version
```

入っていない場合の対応:

- **WSL未インストール**: PowerShellを管理者権限で開いて `wsl --install` を実行 → 再起動 → Ubuntuが立ち上がる
- **Node.js未インストール**: WSL（Ubuntu）内で以下を実行:
  ```bash
  curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
  sudo apt-get install -y nodejs
  ```

### Astroプロジェクトの初期化

```bash
cd ~/projects/katakoto      # 作業フォルダに移動
npm create astro@latest rules-without-rulers
# → "Empty"テンプレートを選択（依頼者に最大の自由度）
# → TypeScriptは Yes（推奨）
# → 依存関係インストール: Yes
# → git init: Yes

cd rules-without-rulers
npm run dev
# → http://localhost:4321 でプレビューが立ち上がる
```

### このパッケージの取り込み

引き継ぎ時に渡されたファイル群を以下に配置:

- `prototype/record_circle.webp` → `src/assets/record_circle.webp`
- `prototype/index.html` → 参照用に `prototype/` ディレクトリごとプロジェクト内に保管（Astro実装の参照元として）
- `assets/record_original.png` → `prototype/assets/` に保管（バックアップ）
- `PROJECT.md`, `HANDOFF.md` → プロジェクトルートに保管

## チェックリスト（Claude Codeへの作業指示）

実装時、以下の順で進めてほしい:

- [ ] `PROJECT.md` を読み、アルバム全体の文脈を把握
- [ ] `prototype/index.html` をブラウザで開いて、目標とする動作を確認
- [ ] Hiroに「Windows + WSLの環境は整っているか」確認（必要なら上記セットアップを案内）
- [ ] Astroプロジェクトを初期化（上記コマンド参照）
- [ ] プロトタイプのHTML/CSS/JSをAstroコンポーネントに分解（上記推奨構成を参照）
- [ ] `npm run dev` でローカルプレビューが正しく動くことを確認
- [ ] Gitリポジトリにinitial commit
- [ ] HiroにGitHubリポジトリ作成を依頼 → push
- [ ] Cloudflare Pagesでプレビュー環境セットアップを案内
- [ ] 残っている設計判断（上記5項目）をHiroに確認、必要なら微調整
- [ ] 音源ファイルが揃ったら `<audio>` タグ実装に切り替え
- [ ] 歌詞ページ `/lyrics` を実装（歌詞MDが渡された後）

## やらないこと

- React / Next.js / Vue などのSPAフレームワーク導入（Astroの素のままで十分）
- Tailwind CSS の導入（規模的に不要、CSS変数で十分）
- バックエンド・データベース（このサイトは完全静的）
- アナリティクス（プライバシー重視、Bitcoinの精神と整合させる）
- SNSログイン・ユーザー登録機能
- 広告・トラッカー・サードパーティスクリプト

## ユーザーとのコミュニケーション

- ユーザー（Hiro）の母語は日本語。コミュニケーションは日本語で
- 専門用語の訳語は `PROJECT.md` の用語集を厳守（trustless = 信頼不要、permissionless = 許可不要、など）

## 質問・判断に迷ったら

実装中に「これでいいのか？」と迷うことがあれば、以下の優先順で対処:

1. **プロトタイプの動作を確認**（`prototype/index.html` がground truth）
2. **`PROJECT.md` のコンセプトと照合**（思想的な一貫性）
3. **Hiroに直接確認**（軽い質問はその都度、重い意思決定は選択肢を提示して判断を仰ぐ）

迷ったら勝手に進めず、聞いてほしい。
