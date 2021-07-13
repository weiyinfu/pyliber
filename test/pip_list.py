from pip._internal.cli import main as pip_main
import io
import sys

x = sys.stdout
y = io.StringIO()
sys.stdout = y
a = pip_main.main(["list"])
sys.stdout = x
print(y.getvalue())
