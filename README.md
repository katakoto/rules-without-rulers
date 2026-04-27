# Rules Without Rulers — Single Site Handoff Package

このフォルダは、シングル「Rules Without Rulers / 王不在」特設サイトの**Claude Codeへの引き継ぎパッケージ**です。

## 中身

- **HANDOFF.md** — Claude Codeへの作業指示書（最初に読ませる）
- **PROJECT.md** — アルバム全体のコンセプト・用語集・収録曲リスト
- **prototype/** — 動作確認済みの試作HTML
  - `index.html` — ブラウザで開けば実際に動く
  - `record_circle.webp` — 背景透過済みのレコード画像
- **assets/** — オリジナル素材
  - `record_original.png` — 元のレコード画像（白背景PNG）

## 使い方（Hiro向け）

### 1. このフォルダをWindowsの作業ディレクトリに移動

例:

```
C:\Users\Hiro\projects\katakoto\rules-without-rulers\
```

### 2. WSL（Ubuntu）からアクセスできるか確認

PowerShellで:

```powershell
wsl --version
```

入っていなければ管理者権限のPowerShellで:

```powershell
wsl --install
```

→ 再起動 → Ubuntuセットアップ完了まで待つ。

### 3. WSL内のターミナルでこのフォルダに入る

WSLを起動して:

```bash
# WindowsのCドライブ配下にあるなら:
cd /mnt/c/Users/Hiro/projects/katakoto/rules-without-rulers
ls
```

`HANDOFF.md`、`PROJECT.md`、`prototype/`、`assets/` が見えればOK。

### 4. Claude Codeを起動

まだインストールしていなければ:

```bash
npm install -g @anthropic-ai/claude-code
```

そしてこのフォルダで:

```bash
claude
```

### 5. 最初のプロンプト

Claude Codeが起動したら、こう打つだけ:

```
HANDOFF.md と PROJECT.md を読んで、プロジェクトの状況を把握してから、
Astroで本実装を始める準備をしてください。
```

これでClaude Codeが状況把握 → セットアップ手順を案内 → 実装開始という流れになります。

## プロトタイプの動作確認

`prototype/index.html` をダブルクリックでブラウザで開けば、レコード盤上のオレンジBitcoinロゴをクリックすることで:

- レコードが回転する
- トーンアームが盤面に降りる
- カウンターが秒数を刻む

この動作・デザインを、Astroベースの本番実装に移植するのがClaude Codeの仕事です。
