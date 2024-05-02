#　構成
main.pyが総元締めのコードで、data_loader.py、map_creator.py、ui.pyはそこから呼び出して使っているだけの子供たち
なんとなくコードが長くなったのでファイルを分けているだけ

# 必要なパッケージ
requirements.txt　にすべて記載した。
オフライン端末のWinPython環境でインストールするには、WinPythonのフォルダにあるWinPython Terminal.exeを立ち上げて、以下の感じでインストール作業をすればよいと思われる。

1.オンライン端末
```c
pip download --d ./packages -r requirements.txt
tar cfvz archive.tar.gz ./packages
```
これでたぶん、packagesフォルダにパッケージがダウンロードされる


2.オフライン端末
```c
tar xfvz archive.tar.gz
pip install --no-index --find-links=./packages shap
```
これでインストール完了

