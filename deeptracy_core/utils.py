import os
import uuid

import requests


def make_uuid() -> str:
    return uuid.uuid4().hex
