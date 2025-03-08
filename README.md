# UserTools

## Features

- 一般ユーザーがメッセージをピン留めできるようにする
- 管理者ユーザーが Whois を使えるようにする

## Usage

- Linux 及び Windows 上での動作を想定しています．
- [`UserTools.py`](./UserTools.py) を配置しているリポジトリ内に `.env` ファイルを用意し，環境変数を設定してください．
- 設定後 `python UserTools.py` で起動できます．

## Environment Variables

| Name                | Description                                           | デフォルト値            |
| ------------------- | ----------------------------------------------------- | ----------------------- |
| `DISCORD_TOKEN` | Discord Bot のトークン                                | ---                     |
| `GUILD_ID` | 監視対象ギルドのID                                | ---                     |
| `PERMISSION_ROLE` | 管理者のロールID                                | ---                     |
| `LOG_CHANNEL_ID` | ログ用のチャンネルID                                | ---                     |
