#! /usr/bin/env python
import x
import base64
import argparse
from urllib import quote

vjudgex = x.X()
vjudgex.login('footoredo', '123456')

parser = argparse.ArgumentParser(description='A interactive command line tool for submitting & judging code in vjudge.')
parser.add_argument("--oj", nargs = '?', help = "Name of OJ.")
parser.add_argument("--prob", nargs = '?', help = "Name of problem.")
parser.add_argument("--lang", nargs = '?', help = "Languages in which you want to submit your code.")
parser.add_argument("--code", nargs = '?', help = "Filename which you want to submit.")
#parser.print_help()
args = parser.parse_args()

if (args.oj == None):
    args.oj = raw_input("OJ: ")
vjudgex.setoj(args.oj)
if (args.prob == None):
    args.prob = raw_input("probNum: ")
vjudgex.setprob(args.prob)
if (args.lang == None):
    args.lang = vjudgex.input_language()
vjudgex.setlang(args.lang)
if (args.code == None):
    args.code = raw_input("code file: ")

code = open(args.code, 'r').read()
#print code
#print quote(code)
#print base64.b64encode(quote(code))
vjudgex.submit(code)
