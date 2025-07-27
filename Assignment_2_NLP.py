#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd

df = pd.read_csv('parsed_date_inputs_only.csv')
df.head()


# In[5]:


import re
from datetime import datetime

# Month mapping
MONTHS = {
    'jan': '01', 'january': '01',
    'feb': '02', 'february': '02',
    'mar': '03', 'march': '03',
    'apr': '04', 'april': '04',
    'may': '05',
    'jun': '06', 'june': '06',
    'jul': '07', 'july': '07',
    'aug': '08', 'august': '08',
    'sep': '09', 'september': '09',
    'oct': '10', 'october': '10',
    'nov': '11', 'november': '11',
    'dec': '12', 'december': '12',
}

# All formats, with optional 'of' and allowing dot separators
DATE_PATTERNS = [
    r'(?P<day>\d{1,2})(?:st|nd|rd|th)?(?:\s+of)?\s+(?P<month>[A-Za-z]+)[, ]+\s*(?P<year>\d{2,4})',
    r'(?P<month>[A-Za-z]+)\s+(?P<day>\d{1,2})(?:st|nd|rd|th)?[,]?\s+(?P<year>\d{2,4})',
    r'(?P<year>\d{2,4})[-/.](?P<month>\d{1,2})[-/.](?P<day>\d{1,2})',
    r'(?P<day>\d{1,2})[-/.](?P<month>\d{1,2})[-/.](?P<year>\d{2,4})',
    r'(?P<month>\d{1,2})[-/.](?P<day>\d{1,2})[-/.](?P<year>\d{2,4})',  # US format fallback
]

compiled = [re.compile(p, re.IGNORECASE) for p in DATE_PATTERNS]

def normalize_date_str(day, month, year):
    d = int(day)
    y = int(year)
    if y < 100:  # Fix 2-digit years
        y += 2000 if y < 50 else 1900
    if month.isdigit():
        m = int(month)
    else:
        m = int(MONTHS.get(month.lower()[:3], 0))
    if m > 12:  # Invalid month (e.g., due to wrong US format match)
        raise ValueError("Invalid month")
    return f"{d:02d}/{m:02d}/{y:04d}"

def extract_date(text):
    for pattern in compiled:
        m = pattern.search(text)
        if m:
            gd = m.groupdict()
            try:
                # Try regular format
                return normalize_date_str(gd['day'], gd['month'], gd['year'])
            except:
                try:
                    # Try flipping MM/DD/YYYY if first try fails
                    return normalize_date_str(gd['month'], gd['day'], gd['year'])
                except:
                    continue
    return None



# In[6]:


# Apply the function to the 'Input' column
df['Parsed Date'] = df['Input'].apply(extract_date)

# Display first few results
df.head()


# In[7]:


from IPython.display import display

display(df)  # Shows the entire DataFrame in a scrollable format



# In[ ]:




