# -*- coding:utf-8 -*-
# python updateListOfTheSpecifiedFilePattern.py

"""
    1. motivation
        I would like to perform file management 
        for the specified file type(pattern) 
        under the specified path(directory).

        For example,
          1) Even if the extension  .py can be listed with the tree command,
             It is difficult to grasp what type of time stamp is the latest
             among the execution process which is the history showing the progress
             reflecting the process of evolution of various models of skeleton. 
          2) Handling of tree commands.
             on each OS such as windows / linux is not unified 
          3) I would like to use any OS-independent wrappers. 
       [動機
　　　　　指定したパス（ディレクトリ）下の
　　　　　指定したファイルタイプ（パターン）を対象としたファイル管理を行いたい。

　　　　　例えば、
　　　　　　１）　拡張子 .pyがtreeコマンドで一覧が取れても、
　　　　　　　　　スケルトンの多様なモデルの進化の過程を反映した経過を示す歴史である実行過程、
　　　　　　　　　そのうちタイプスタンプが最新のものがどれかを把握するのが困難であった。
　　　　　　２）　tree commandに対するwindows/linuxなどOSでの取り扱いが統一されていない。
　　　　　　３）　OSに依存しないラッパーがあれば使用したい。]

    2. updateListOfTheSpecifiedFilePattern.py
       [指定したパターンの更新一覧 py]

    3. Prerequisites for using
       [使う上での前提条件]

      1) python 3 If possible install v 3 6 or later 
         However, considering when python 2 is already installed. 
         [python3 出来れば　v3 6以降をインストール。
         　但し、python2がインストール済みの場合の考慮すること]

          https://www python org/downloads/release/python-366/ is no problem

      2) Since clipboard operation is used, after installing python 3,
         execute the following command to acquire external library.
         [クリップボード操作を使うのでpython3インストール後、
          外部ライブラリ取得のため、下記コマンドを行う]

          >pip install pyperclip

      3) How to use,
          (1) describe the specified path, directory pattern, and file pattern 
              in one line with a space.
              (use any editor, 
               and the pattern is a regular expression (re) of python 3).
                Ex -top F:\96_kvm_docs 
                   -dirpattern (?!.*(python3|hold)) 
                   -filepattern (?<=.)(py|html)$
                   -dirlist no
                   -abspath yes

-toppath f:\96_kvm_docs -dirpattern (?!.*(python3|hold)) -filepattern (?<=.)(py|html)$ -dirlist no -abspath yes

          (2) select and clip the described information.
          (3) execute >python updateListOfTheSpecifiedFilePattern.py.
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
     2018/10/04 12:50 (JST,UTC+9h)  v1.0.0 by ShozoNamikawa

"""

import os
import re
import datetime

import pyperclip

class ClipBoard():
    """
    read the text content of the current clipboard,
    or paste the new text contents and update the contents
    [現在のクリップボードのテキスト内容を読む、ないし新たなテキスト内容を貼り付け内容を更新する]
    """

    def get(self):
        """
        Contents of current clipboard\
        [現在クリップボードの内容]
        """
        return (str(pyperclip.paste()))

    def set(self, past_text):
        """
        Rewrite the clipboard to this content
        [この内容に、クリップボードを書き換える]
        """
        pyperclip.copy(past_text)
        return(past_text)

class IsArgs():
    """
    Check consistency of arguments describing specified path, file pattern, etc.
    [指定パス、ディレクトリパターン、ファイルパターン等を記述された引数の整合性を調べる。]
    """

    def __init__(self):
        """
        define the name of the arguments
        [引数の名称を定義する]
        """
        # leading argument
        self.indicator = '-'

        # take to confirmation means
        self.path = 'path'
        self.re = 're'
        self.yes_no = 'yes_no'

        # name of argument
        self.top_p = 'toppath'
        self.dir_re = 'dirpattern'
        self.fil_re = 'filepattern'
        self.dir_l = 'dirlist'
        self.abs_p = 'abspath'

        # value of argument
        self.yes = 'yes'
        self.no = 'no'

        # define arguments type
        self.args_def = {
                self.top_p : self.path,
                self.dir_re : self.re,
                self.fil_re : self.re,
                self.dir_l : self.yes_no,
                self.abs_p : self.yes_no,
            }

    def isArgs(self, args):
        """
        parse arguments describing specified path, directory pattern, file pattern.
           ex.  -toppath F:\96_kvm_docs
                -dirpattern (?!.*(python3|hold))
                -filepattern (?<=.)py$
                -dirlist no
                -fullpath yes

-toppath f:\96_kvm_docs -dirpattern (?!.*(python3|hold)) -filepattern (?<=.)(py|html)$ -dirlist no -abspath yes

        [指定パス、ディレクトリパター、ファイルパターンを記述した引数を解釈]
        """
        self.args = args
        self.args_list = self.args.split()

        # make dict of arguments
        self.args_dict = {}
        k = ''
        v = ''
        for arg in self.args_list:
            if arg.startswith(self.indicator):
                k = str(arg[1:]).lstrip(self.indicator)
                v = ""
            else:
                if k:
                    v = arg
                    self.args_dict[k] = v
                    k = ""
                else:
                    print('not specifid -{}'.format(arg))
                    return(False)

        # Check the clipboard contents.
        # sufficient argument?
        for k in self.args_def:
            if self.args_dict.get(k):
                if self.args_def[k] == self.yes_no:
                    if self.args_dict[k] == self.yes or self.args_dict[k] == self.no:
                        pass
                    else:
                        print('not yes or no -{}'.format(k))
                        return (False)
                pass
            else:
                print('not specifid -{}'.format(k))
                return(False)

        # this path exist?
        if self.args_def[self.top_p] == self.path:
            # make it an os dependent separator
            self.args_dict[self.top_p].replace('\\', os.sep)
            if os.path.isdir(self.args_dict[self.top_p]):
                pass
            else:
                print("top path specification may be illegal.")
                return(False)
        return(True)

class ParseTree():
    """
    parse specified tree structure
    [tree構造を解析する]
    """
    # parse specified tree structure
    def list_files(self, is_args):
        # prepare output list(add os.linesep)
        self.lists = ''
        head_column = '\t'.join([str('time stamp'), str('level'), ' ', str('path/file')])
        self.lists = self.lists + head_column + os.linesep
        # print(head_column)
        self.top_p = is_args.args_dict[is_args.top_p]
        self.dir_re = is_args.args_dict[is_args.dir_re]
        self.fil_re = is_args.args_dict[is_args.fil_re]
        self.dir_l = is_args.args_dict[is_args.dir_l]
        self.abs_p = is_args.args_dict[is_args.abs_p]
        self.path = ''
        self.full_path = ''
        self.header = ''
        for toppath, dirs, files in os.walk(self.top_p):
            level = toppath.replace(self.top_p, '').count(os.sep)
            # process directory
            if re.search(self.dir_re, toppath):
                if self.dir_l == is_args.yes:
                    timestamp = datetime.datetime.fromtimestamp(os.stat(toppath).st_mtime)
                    if self.abs_p == is_args.yes:
                        self.path = toppath
                    else:
                        self.header, self.path = os.path.split(toppath)
                    top_column = '\t'.join([str(timestamp), str(level), 'd', str(self.path)])
                    self.lists = self.lists + top_column + os.linesep
                    # print(top_column)

                # process files of the same hierarchy
                subindent = level + 1
                for f in files:
                    if re.search(self.fil_re, f):
                        self.full_path = os.path.join(toppath, f)
                        timestamp = datetime.datetime.fromtimestamp(os.stat(self.full_path).st_mtime)
                        if self.abs_p == is_args.yes:
                            self.path = self.full_path
                        else:
                            self.path = f
                        file_column = '\t'.join([str(timestamp), str(subindent), 'f', str(self.path)])
                        self.lists = self.lists + file_column + os.linesep
                        # print(file_column)
        return(self.lists)

if __name__ == '__main__':

    # read clipping content at startup
    clip_board = ClipBoard()
    clip_args = clip_board.get()
    # confirm
    print(clip_args)

    # determine argument
    is_args  = IsArgs()
    if is_args.isArgs(clip_args):
        # parse and list tree structure
        parse_tree = ParseTree()
        clip_board.set(parse_tree.list_files(is_args))
