#! /usr/bin/env python
import x
import base64
import argparse
import config
import sys
from urllib import quote

parser = argparse.ArgumentParser(description='A interactive command line tool for submitting & judging code in vjudge.')
parser.add_argument("--oj", nargs = '?', help = "Name of OJ.")
parser.add_argument("--prob", nargs = '?', help = "Name of problem.")
parser.add_argument("--lang", nargs = '?', help = "Languages in which you want to submit your code.")
parser.add_argument("--code", nargs = '?', help = "Filename which you want to submit.")
parser.add_argument("--clear", action = 'store_true', help = "Clear configure file.")
#parser.print_help()
args = parser.parse_args()
if args.clear:
    config.clear()
    sys.exit()

vjudgex = x.X()
vjudgex.login('footoredo', '123456')
default = config.load_obj()

if (args.oj == None):
    if default["oj"] != None:
        print "[d = %s]" % default["oj"],
    resp = raw_input("OJ: ")
    if resp != '':
        args.oj = resp
    else:
        args.oj = default["oj"]
vjudgex.setoj(args.oj)
if (args.prob == None):
    if args.oj in default["prob"]:
        print "[d = %s]" % default["prob"][args.oj],
    resp = raw_input("Problem: ")
    if resp != '':
        args.prob = resp
    else:
        args.prob = default["prob"][args.oj]
vjudgex.setprob(args.prob)
if (args.lang == None):
#    print default["lang"]
    args.lang = vjudgex.input_language(default["lang"][args.oj] if args.oj in default["lang"] else None)
vjudgex.setlang(args.lang)
if (args.code == None):
    if default["code"] != None:
        print "[d = %s]" % default["code"],
    resp = raw_input("Code file: ")
    if resp != '':
        args.code = resp
    else:
        args.code = default["code"]
config.save_obj(args, default)

code = open(args.code, 'r').read()
#print code
#print quote(code)
#print base64.b64encode(quote(code))
vjudgex.submit(code)
