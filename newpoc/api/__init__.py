#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import re
import sys
import json
import base64
import random
import argparse
import textwrap
import importlib
from queue import Queue
from pathlib import Path
from urllib.parse import quote
from collections import OrderedDict
from urllib3 import encode_multipart_formdata
from urllib.parse import urljoin as parse_urljoin


from newpoc.core.output import Output
from newpoc.core.poc import PocBase
from newpoc.core.hookrequests import requests, urljoin
from newpoc.utils.dicter import Dicter

