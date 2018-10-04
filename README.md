# python3-cli-updateListOfTheSpecifiedPattern

    1. motivation
        I would like to perform file management 
        for the specified file type(pattern) 
        under the specified path(directory) 

        For example,
          1) Even if the extension  .py can be listed with the tree command,
             It is difficult to grasp what type of time stamp is the latest
             among the execution process which is the history showing the progress
             reflecting the process of evolution of various models of skeleton 
          2) Handling of tree commands 
             on each OS such as windows / linux is not unified 
          3) I would like to use any OS-independent wrappers 
       [動機
　　　　　指定したパス（ディレクトリ）下の指定したファイルタイプ（パターン）を対象としたファイル管理を行いたい。　例えば、

　　　　　　１）　拡張子 .pyがtreeコマンドで一覧が取れても、スケルトンの多様なモデルの進化の過程を反映した経過を示す歴史である実行過程がある。そのうちタイプスタンプが最新のものがどれかを把握するのが困難であった。
　　　　　　２）　tree commandに対するwindows/linuxなどOSでの取り扱いが統一されていない。
　　　　　　３）　OSに依存しないラッパーがあれば使用したい。]

    2. updateListOfTheSpecifiedFilePattern.py
       [指定したパターンの更新一覧 py]

    3. Prerequisites for using
       [使う上での前提条件]

      1) python 3 If possible install v 3 6 or later 
         However, considering when python 2 is already installed 
         [python3 出来れば　v3 6以降をインストール。但し、python2がインストール済みの場合の考慮すること]

          https://www python org/downloads/release/python-366/ is no problem

      2) Since clipboard operation is used, after installing python 3,
         execute the following command to acquire external library
         [クリップボード操作を使うのでpython3インストール後、外部ライブラリ取得のため、下記コマンドを行う。]

          >pip install pyperclip

      3) How to use,
          (1) describe the specified path, directory pattern, and file pattern 
              in one line with a space.
              (use any editor, 
               and the pattern is a regular expression (re) of python 3)
                Ex -top F:\96_kvm_docs 
                   -dirpattern (?!.*(python3|hold)) 
                   -filepattern (?<=.)(py|html)$
                   -dirlist no
                   -abspath yes

-toppath f:\96_kvm_docs -dirpattern (?!.*(python3|hold)) -filepattern (?<=.)(py|html)$ -dirlist no -abspath yes

          (2) select and clip the described information
          (3) execute >python updateListOfTheSpecifiedFilePattern.py
          (4) since the tree structure has been copied to the clipboard, paste it to spreadsheet.
        [
          使用方法は、
          　（１）　指定パス、ディレクトリパターン、ファイルパターンを空白をおいて一行に記述する。
           　　　　（任意のエディターを使用、　またパターンはpython3の正規表現（re）とする）
           
           　　　　例　-toppath F:\96_kvm_docs
                   　　-dirpattern (?!.*(python3|hold))
                       -filepattern (?<=.)(py|html)$
                       -dirlist no
                       -abspath yes

-toppath f:\96_kvm_docs -dirpattern (?!.*(python3|hold)) -filepattern (?<=.)(py|html)$ -dirlist no -abspath yes

          （２）　記述した情報を選択しクリップする。
　　　　　　（３）　実行する。　>python updateListOfTheSpecifiedFilePattern.py
　　　　　　（４）　tree構造がクリップボードにコピーされているので、表計算ソフトに貼り付ける。
        ]

 History
     2018/10/04 12:50 (JST,UTC+9h)  v1 0 0 by ShozoNamikawa
