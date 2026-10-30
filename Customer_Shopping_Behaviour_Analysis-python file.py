#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd

df = pd.read_csv("D:\project\customer_shopping_behavior.csv")


# In[4]:


df.head()


# In[5]:


df.info()


# In[6]:


df.describe()


# In[8]:


df.describe(include='all')


# In[9]:


df.isnull().sum()


# In[12]:


df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))


# In[13]:


df.isnull().sum()


# In[22]:


df.columns = [
    col.replace('_', '').replace(' ', '_').lower().strip('_')
    for col in df.columns
]

print(df.columns.tolist())


# In[23]:


df.columns = [
    col.replace('_', ' ').strip().lower().replace(' ', '_')
    for col in df.columns
]

df = df.rename(columns={'purchase_amount_usd': 'purchase_amount'})

print(df.columns.tolist())


# In[24]:


import re

df.columns = [
    re.sub(r'(?<=[a-z])(?=[A-Z])', '_', col)
    for col in df.columns
]


# In[25]:


df.columns = [
    'Customer ID', 'Age', 'Gender', 'Item Purchased',
    'Category', 'Purchase Amount (USD)', 'Location',
    'Size', 'Color', 'Season', 'Review Rating',
    'Subscription Status', 'Shipping Type',
    'Discount Applied', 'Promo Code Used',
    'Previous Purchases', 'Payment Method',
    'Frequency of Purchases'
]

df.columns = (
    df.columns.str.lower()
    .str.strip()
    .str.replace(r'[^a-z0-9]+', '_', regex=True)
    .str.strip('_')
)

df = df.rename(columns={'purchase_amount_usd': 'purchase_amount'})

print(df.columns.tolist())


# In[26]:


#create a column age_group
labels = ['Young Adult','Adult','Middle-aged','Senior']
df['age_group'] = pd.qcut(df['age'], q=4, labels = labels)


# In[27]:


df[['age','age_group']].head(10)


# In[30]:


# create column purchase_frequency_days

frequency_mapping = {
    'Fortnightly': 14,
    'Weekly': 7,
    'Monthly': 30,
    'Quarterly': 90,
    'Bi-Weekly': 14,
    'Annually': 365,
    'Every 3 Months': 90
}

df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)


# In[31]:


df[['purchase_frequency_days','frequency_of_purchases']].head(10)


# In[32]:


df[['discount_applied','promo_code_used']].head(10)


# In[33]:


(df['discount_applied'] == df['promo_code_used']).all()


# In[34]:


df = df.drop('promo_code_used', axis=1)


# In[35]:


df.columns


# In[36]:


pip install pyodbc pandas sqlalchemy


# In[48]:


get_ipython().run_line_magic('pip', 'install sqlalchemy pymysql')


# In[49]:


from sqlalchemy import create_engine
from urllib.parse import quote_plus

mysql_user = "jupyter_user"
mysql_password = quote_plus("Choose_A_Strong_Password_123!")

engine = create_engine(
    f"mysql+pymysql://{mysql_user}:{mysql_password}"
    "@localhost:3306/customer_behaviour"
)


# In[50]:


import pandas as pd

pd.read_sql("SELECT DATABASE()", engine)


# In[51]:


df.to_sql(
    name="shopping_trends",
    con=engine,
    if_exists="fail",
    index=False
)


# In[52]:


pd.read_sql(
    "SELECT * FROM shopping_trends LIMIT 5",
    engine
)


# In[ ]:




