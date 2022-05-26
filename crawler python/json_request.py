import sys
from urllib.request import Request, urlopen
from datetime import *
import json

# error log 출력
def json_request_error(e):
