import pandas as pd
import numpy as np
import random
import time
import re
from datetime import timedelta
import pysrt 
import datetime


def srt2df(srt_path):
    caps = pysrt.open(srt_path)
    starts = []
    texts = [] 
    for c in caps:
        texts.append(c.text)
        t = c.start.to_time()
        starts.append((t.hour * 60 + t.minute) * 60 + t.second )

    df = pd.DataFrame()
    df['chat'] =texts
    df = df['chat'].str.split(':',n=1,expand=True).rename({0:'username',1:'message'},axis=1)

    df['start_time'] = [c.start.to_time() for c in caps]
    df['username'] = df['username'].str.lower() 
    df = df[~df['username'].str.contains('bot')]
    df['message'] = df['message'].str.strip()
    df = df[~df['message'].str.startswith('!')]
    df = df.drop(['username'],axis=1)
  
    return df