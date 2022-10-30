#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import re
import argparse
import textwrap
import importlib
from pathlib import Path
from queue import Queue
from newpoc.core.output import Output
from newpoc.core.poc import PocBase
from newpoc.core.hookrequests import requests, urljoin
from newpoc.utils.dicter import Dicter