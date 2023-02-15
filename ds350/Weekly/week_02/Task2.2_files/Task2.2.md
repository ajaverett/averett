---
title: "Task 2.02 - Fix this chart"
author: "Aj Averett"
date: "April 26, 2022"
output: 
 html_document:
  keep_md: TRUE
  toc: true
  toc_float: true
  code_folding: hide
---



## Loading in data

The code below loads in the RCW or "Research & Creative Works" data. Since the University administrators track student participation in the RCW conference to help them prepare for future semesters every semester, we can use graphical summaries to see the trends of attendance over time. The head function is used to preview the first few rows of data.


```r
library(readr)
library(ggplot2)

rcw <- read_csv("https://byuistats.github.io/M335/data/rcw.csv", 
            col_types = cols(Semester_Date = col_date(format = "%m/%d/%y"), 
                             Semester = col_factor(levels = c("Winter", "Spring", "Fall"))))
head(rcw)
```

```
## # A tibble: 6 x 5
##    Year Semester Semester_Date Count Department
##   <dbl> <fct>    <date>        <dbl> <chr>     
## 1  2016 Spring   2016-04-01        7 Chem      
## 2  2016 Fall     2016-09-01       10 Chem      
## 3  2017 Winter   2017-01-01       21 Chem      
## 4  2017 Spring   2017-04-01        8 Chem      
## 5  2017 Fall     2017-09-01       12 Chem      
## 6  2018 Winter   2018-01-01       16 Chem
```

The code below creates a box plot of all three years recorded. From this box plot, we can see the average change of the shape of data over the three years.


```r
ggplot(data = rcw, aes(x=as.factor(Year), y=Count)) +
  geom_boxplot(fill="slateblue", alpha=0.2) + 
    xlab("Year") +
  theme_classic()
```

![](Task2.2_files/figure-html/unnamed-chunk-2-1.png)<!-- -->
<br>

As seen above, the trend between 2016-2018 seems to be slowly going up. 
