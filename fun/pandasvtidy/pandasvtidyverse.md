---
title: "Pandas vs tidyverse"
output:
  rmdformats::readthedown:
    keep_md: true
---




# Creating a dataframe

**tidyverse**
```r
df <- data.frame(
      col_one = c('A','B','C','D'),
      col_two = c(1,2,3,4)
)
```

**pandas**
```python
df = pd.DataFrame(
      {'col_one': ['A', 'B', 'C','D'],
       'col_two': [1, 2, 3, 4]}
)
```

# Inspecting a dataframe

**tidyverse**
```r
df %>% colnames
df %>% dim
df %>% nrow
df %>% ncol
df %>% head(n)
df %>% tail(n)
df %>% summary
```

**pandas**
```python
df.columns
df.shape
df.shape[0]
df.shape[1]
df.head(n)
df.tails(n)
df.describe()
```


# Cleaning a dataframe

**tidyverse**
```r
df %>% janitor::clean_names()
```

**pandas**
```python
from skimpy import clean_columns
clean_columns(df)
```

# Import

**tidyverse**
```r
df <- read_csv('data.csv')
df <- read_csv('data.csv', col_names = F)
```

**pandas**
```python
df = pd.read_csv('data.csv')
df = pd.read_csv('data.csv', header=None)
```
# Count

**tidyverse**
```r
df %>% count(col_one)
df %>% count(col_one, sort = T)
df$col_one %>% janitor::tabyl()
""
NA
```

**pandas**
```python
from skimpy import clean_columns
df['col_one'].value_counts()
df['col_one'].value_counts(ascending = False)
df['col_one'].value_counts(dropna=False)
df['col_one'].value_counts(normalize=True)
df['col_one'].value_counts(bin = n)
```
# Calculate

**tidyverse**
```r
df$col_one %>% mean
df$col_one %>% median
df$col_one %>% sd
df$col_one %>% min
df$col_one %>% max
```

**pandas**
```python
df['col_one'].mean()
df['col_one'].median()
df['col_one'].std()
df['col_one'].min()
df['col_one'].max()
```
# Select

**tidyverse**
```r
df %>% select(col_one)
df %>% select(col_one,col_two)
df %>%select(matches("[pt]al"))
df %>% select(starts_with("col"))
""
df %>% select(ends_with("two"))
""
df %>% select(contains("col"))
""
```

**pandas**
```python
df.filter(items=['col_one'])
df.filter(items=['col_one','col_two'])
df.filter(regex='[pt]al')
df.loc[:,df.columns.str.startswith("col")]
df.filter(regex='^col')
df.loc[:,df.columns.str.endswith("two")]
df.filter(regex='two$')
df.loc[:,df.columns.str.contains("col")]
df.filter(like='col')
```
# Drop

**tidyverse**
```r
df %>% select(!col_one)
df %>% select(!c(col_one,col_two))
```

**pandas**
```python
df.drop(columns=['col_one'])
df.drop(columns=['col_one','col_two'])
```

# Rename

**tidyverse**
```r
df %>% rename(col_1 = column_one)
df %>% rename(col_1 = column_one, 
                              col_2 = column_two
)
```

**pandas**
```python
df.rename(columns={"column_one": "col_1"})
df.rename(columns={"column_one": "col_1", 
                                       "column_two": "col_2"}
)
```

# Change Datatype

**tidyverse**
```r
df %>% mutate(Race = as.character(Race), Age = as.numeric(Age))
```

**pandas**
```python
df.astype({"Race":'category', "Age":'int64'})
```

# Locate

**tidyverse**
```r
df[,]
df[1,]
df[c(1,6),]
df[c(1:6),]
df[,'col_one']
df[,c('col_one','col_three')]
NA
df[,c(1,3)]
df[,c('1:3')]
```

**pandas**
```python
df.loc[:,:]
df.loc[1,:] 
df.loc[[1,6],:] 
df.loc[[1:6],:] 
df.loc[:,['col_one']]
df.loc[:,['col_one','col_three']] 
df.loc[:,'col_one':'col_three'] 
df.iloc[:,[1,3]]
df.iloc[:,1:3]
```
# Query

**tidyverse**
```r
df %>% filter(col_one >= 100)
df %>% filter(col_one != "Blue")
df %>% filter(col_one %in% c('A','B'))
df %>% filter(!(Race == "White" & Gender == "Male"))
```

**pandas**
```python
df.query("col_one >= 100")
df.query("col_one != 'Blue'")
df.query("col_one in ['A', 'B']")
df.query("not (Race == 'White' and Gender == 'Male')")
```
# Sort

**tidyverse**
```r
df %>% arrange('col_one')
df %>% arrange(col_one %>% desc())
```

**pandas**
```python
df.sort_values('col_one')
df.sort_values('col_one', ascending=False)
```
# Replace

**tidyverse**
```r
df %>% mutate(across(everything(), ~replace(., . ==  2 , "foo")))
df %>% mutate(across(c(col_one,col_two), ~replace(., . ==  2 , "foo")))
df %>% mutate(col_one = ifelse(col_one == 2, "foo", col_one))
```

**pandas**
```python
df.replace(2,"foo")
df[['col_one','col_two']].replace(2,"foo")
df['col_one'].replace(2,"foo")
```
# Drop NA

**tidyverse**
```r
df %>% drop_na
df %>% drop_na(c("col_one", "col_two"))
NA
```

**pandas**
```python
df.dropna()
df.dropna(subset=['col_one', 'col_two'])
df.dropna(thresh=n)
```
# Fill NA

**tidyverse**
```r
df %>% replace(is.na(.), x)
df %>% mutate(col_one = ifelse(is.na(col_one),x,col_one))
NA
df %>% mutate(col_one= ifelse(is.na(col_one), mean(df$col_one, na.rm = T), col_one))
```

**pandas**
```python
df.fillna(x)
df['col_one'].fillna(x)
df['col_one'].fillna(method = 'ffill')
df['col_two'].fillna(df['col_two'].mean())
```
# Group & Summarize

**tidyverse**
```r
df %>% group_by(Race) %>% count()
df %>% group_by(Race) %>% summarize(new_col = median(Income))
df %>% group_by(Race, Sex) %>%
     summarize(
       new_col1 = median(Income),
       new_col2 = n(),
       new_col3 = mean(age)
)
```

**pandas**
```python
df.groupby('Race', as_index=False).count()
df.groupby('Race', as_index=False)['Income'].median()
(df.groupby(['Race', 'Sex'], as_index=False)
   .agg(
      new_col1=pd.NamedAgg(column = 'Income', aggfunc = np.median),
      new_col1=pd.NamedAgg(column = 'Age', aggfunc = np.mean)
))

```
# Pivot Longer

**tidyverse**
```r
df %>% 
  pivot_longer(
     cols = Belgium:`United Kingdom`,
     names_to = "Country",
     values_to = "Fatalities"
)
```

**pandas**
```python
(df
  .melt(
    id_vars=['iyear'],
    var_name='Country', 
    value_name='Fatalities')
)
```
# Pivot Wider

**tidyverse**
```r
df %>% pivot_wider(
      names_from = state, 
      values_from = number
)
```

**pandas**
```python
df.pivot_table(index=['year','name','sex'],
      columns='state',
      values='number'
)
```
# Bind

**tidyverse**
```r
df1 %>% bind_rows(df2)
df1 %>% bind_cols(df2)
```

**pandas**
```python
df1.append(df2)
pd.concat([df1,df2], axis=1)
```
# Inner Join

**tidyverse**
```r
df1 %>% inner_join(
      df2, by = c(col_one = "first_col")
)
```

**pandas**
```python
pd.merge(df1, df2, 
     left_on='col_one', right_on='first_col'
)
```
# Left Join

**tidyverse**
```r
df1 %>% left_join(df2, 
      by = c(col_one = "first_col")
)
```

**pandas**
```python
pd.merge(df1, df2, how = 'left',
     left_on='col_one', right_on='first_col'
)
```
# Mutate

**tidyverse**
```r
df %>% mutate(
      twomore = x + 2,
      twoless    = x - 2
)
```

**pandas**
```python
df.assign(
  twomore = lambda df: df.x + 2,
  twoless    = lambda df: df.x - 2
)
```
# Distinct

**tidyverse**
```r
df %>% distinct(col_one, .keep_all = T)
df %>% distinct()
```

**pandas**
```python
df.drop_duplicates(subset = ["col_one"])
df.drop_duplicates()
```
