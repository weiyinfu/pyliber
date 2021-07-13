import io
import sys
from types import FunctionType


class StdinStdout:
    def __init__(self, stdin=None, stdout=None):
        self.stdin = stdin
        self.stdout = stdout
        self.stdin_ = None
        self.stdout_ = None

    def __enter__(self):
        if self.stdin:
            self.stdin_ = sys.stdin
            sys.stdin = self.stdin
        if self.stdout:
            self.stdout_ = sys.stdout
            sys.stdout = self.stdout

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.stdin:
            sys.stdin = self.stdin_
        if self.stdout:
            sys.stdout = self.stdout_


def get_content(f: FunctionType) -> str:
    x = io.StringIO()
    with StdinStdout(stdout=x):
        f()
    return x.getvalue()
