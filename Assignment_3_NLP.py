#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

df = pd.read_csv("pronoun_testcases.csv")

print(df.head())



# In[4]:


import pandas as pd
import re

# Load CSV
df = pd.read_csv("pronoun_testcases.csv")

# Define function
def swap_gender_pronouns(text, target):
    text = re.sub(r'([.,!?])', r' \1 ', text)
    words = text.split()
    swapped = []

    for i, word in enumerate(words):
        lw = word.lower()
        next_word = words[i + 1].lower() if i + 1 < len(words) else ""

        if target == "female":
            if lw == 'he':
                replacement = 'she'
            elif lw == 'him':
                replacement = 'her'
            elif lw == 'his':
                replacement = 'her'
            elif lw == 'himself':
                replacement = 'herself'
            else:
                replacement = word

        elif target == "male":
            if lw == 'she':
                replacement = 'he'
            elif lw == 'herself':
                replacement = 'himself'
            elif lw == 'her':
                # Determine if 'her' is possessive (followed by a noun)
                if next_word.isalpha() and next_word not in [
                    'is', 'was', 'has', 'have', 'can', 'will',
                    'would', 'should', 'could', 'had', 'did', 'does'
                ]:
                    replacement = 'his'
                else:
                    replacement = 'him'
            elif lw == 'hers':
                replacement = 'his'
            else:
                replacement = word
        else:
            replacement = word

        # Capitalize if needed
        if word.istitle():
            replacement = replacement.capitalize()

        swapped.append(replacement)

    result = ' '.join(swapped)
    result = re.sub(r'\s+([.,!?])', r'\1', result)
    return result

# Apply to DataFrame
df["predicted_output"] = df.apply(
    lambda row: swap_gender_pronouns(row["input_text"], row["target_gender"]),
    axis=1
)

# Preview
print(df[["input_text", "target_gender", "predicted_output"]].head())

# Optionally save
df.to_csv("pronoun_testcases_with_predictions.csv", index=False)


# In[5]:


display()


# In[6]:


pd.set_option("display.max_rows", None)  # Show all rows
print(df[["input_text", "target_gender", "expected_output", "predicted_output"]])


# In[7]:


import pandas as pd
import re

# Load your dataset
df = pd.read_csv("pronoun_testcases.csv")  # Use full path if needed

def swap_gender_pronouns(text, target):
    text = re.sub(r'([.,!?])', r' \1 ', text)  # space punctuation for split
    words = text.split()
    swapped = []

    for i, word in enumerate(words):
        lw = word.lower()
        next_word = words[i + 1].lower() if i + 1 < len(words) else ""

        # Swap to female
        if target == "female":
            if lw == "he":
                replacement = "she"
            elif lw == "him":
                replacement = "her"
            elif lw == "his":
                replacement = "her"
            elif lw == "himself":
                replacement = "herself"
            elif lw == "his":
                replacement = "her"
            else:
                replacement = word

        # Swap to male
        elif target == "male":
            if lw == "she":
                replacement = "he"
            elif lw == "herself":
                replacement = "himself"
            elif lw == "her":
                # Context check: possessive or object?
                if next_word.isalpha() and next_word not in [
                    'is', 'was', 'has', 'have', 'can', 'will',
                    'would', 'should', 'could', 'had', 'did', 'does'
                ]:
                    replacement = "his"
                else:
                    replacement = "him"
            elif lw == "hers":
                replacement = "his"
            else:
                replacement = word
        else:
            replacement = word

        # Maintain case
        if word.istitle():
            replacement = replacement.capitalize()

        swapped.append(replacement)

    # Clean spacing around punctuation
    result = ' '.join(swapped)
    result = re.sub(r'\s+([.,!?])', r'\1', result)
    return result

# Apply to all rows
df["predicted_output"] = df.apply(
    lambda row: swap_gender_pronouns(row["input_text"], row["target_gender"]),
    axis=1
)

# Show all rows
pd.set_option("display.max_rows", None)
print(df[["input_text", "target_gender", "expected_output", "predicted_output"]])


# In[ ]:




