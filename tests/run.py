#!/usr/bin/env python
import os
import sys


if __name__ == "__main__":
    sys.path.append(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    os.environ.setdefault("APP_ENV", "test")
    from tests.management.manager import TestManager
    TestManager().run()
