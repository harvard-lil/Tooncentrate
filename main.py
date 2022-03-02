from Tooncentrate import Tooncentrate

import sys
from getopt import getopt, GetoptError
# See readme

def main():
    try:
        opts, args = getopt(sys.argv[1:], "h", ["help", "--info"] + [f"{name}=" for name in Tooncentrate.ARG_DESCRIPTIONS])
    except GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    output = None
    verbose = False
    kwargs = {}
    for o, a in opts:
        argname = o.lstrip('-')
        if o in ("-h", "--help", "--info"):
            usage()
            sys.exit()
        elif argname in Tooncentrate.ARG_DESCRIPTIONS:
            if Tooncentrate.ARG_DESCRIPTIONS[argname][0] == bool:
                if a.endwith("rue") and (a.startswith("T") or a.startswith("t")):
                    kwargs[argname] = True
                elif a.endwith("alse") and (a.startswith("F") or a.startswith("f")):
                    kwargs[argname] = False
                else:
                    print(f"{argname} must be a boolean")
            elif Tooncentrate.ARG_DESCRIPTIONS[argname][0] == int:
                if a.isnumeric():
                    try:
                        kwargs[argname] = int(a)
                    except ValueError:
                        print(f"{argname} must be an integer")
                else:
                    print(f"{argname} must be an integer")
            elif argname == 'volume':
                if a in Tooncentrate.VOL:
                    kwargs[argname] = a
                else:
                    print(f"Volume value must any of these: {Tooncentrate.VOL}... ignoring and using default {Tooncentrate.ARG_DESCRIPTIONS[argname][2]}")
            else:
                print(f"Specifying {argname} on the CLI isn't yet implemented... ignoring and using default {Tooncentrate.ARG_DESCRIPTIONS[argname][0]}.\n (feel free to implement it.)")
        else:
            assert False, "unhandled option"
    timer = Tooncentrate(**kwargs)
    timer.start()

def usage():
    print(f"""
Usage: python3 main.py [options]
Options:

  -h, --help, --info: Print this help message""")
    for name in Tooncentrate.ARG_DESCRIPTIONS:
        print(f"\n  --{name}:\n    ", Tooncentrate.ARG_DESCRIPTIONS[name][1], str(Tooncentrate.ARG_DESCRIPTIONS[name][0]), f"default: {str(Tooncentrate.ARG_DESCRIPTIONS[name][2])}")

if __name__ == '__main__':
    main()