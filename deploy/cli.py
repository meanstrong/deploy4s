#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import traceback

from deploy import Deploy


def main():
    bundle = None
    for arg in sys.argv:
        if arg.startswith("--bundle="):
            bundle = arg.split("=", 1)[1]

    if bundle is None:
        print_help()
        sys.exit(1)
    try:
        deploy = Deploy()
        deploy.deploy(bundle)
    except Exception as err:
        traceback.print_exc()
        sys.exit(1)

def print_help():
    msg = '''
    Usage: deploy --bundle=example.zip
    Options:
        --bundle    The deploy archive file path, it can be local file path or
                    internet path.
    '''
    print(msg)


if __name__ == "__main__":
    main()