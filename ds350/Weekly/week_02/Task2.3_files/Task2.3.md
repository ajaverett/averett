---
title: "Task 2.3"
author: "Aj Averett"
date: "April 26, 2022"
output: 
 html_document:
  keep_md: TRUE
  toc: true
  toc_float: true
  code_folding: show
---

# Setup


```r
#install.packages("gapminder") #uncomment and run once. 
library(gapminder)
library(tidyverse)
```

```
## -- Attaching packages --------------------------------------- tidyverse 1.3.1 --
```

```
## v ggplot2 3.3.5     v purrr   0.3.4
## v tibble  3.1.6     v dplyr   1.0.8
## v tidyr   1.2.0     v stringr 1.4.0
## v readr   2.1.2     v forcats 0.5.1
```

```
## -- Conflicts ------------------------------------------ tidyverse_conflicts() --
## x dplyr::filter() masks stats::filter()
## x dplyr::lag()    masks stats::lag()
```
# The Gapminder Data

After watching Hans Rosling’s original TED talk, some insights include - My agreement in that public data should be made accessible and easy to use
- Data from virtually any domain can be made understandable through the expanse of human boredom and curiosity.

## Pick a quantitative variable and create a chart that summarizes the distribution.



```r
temp <- gapminder[gapminder$country == 'United States',]

gapminder[gapminder$country == 'United States',] %>%
  ggplot(aes(x=year, y=lifeExp)) +
    geom_line() +
    theme_classic()
```

![](Task2.3_files/figure-html/unnamed-chunk-2-1.png)<!-- -->


## Pick a qualitative variable and create a chart that summarizes the distribution.



```r
gapminder[gapminder$year == 2007,] %>% 
  ggplot(aes(x = continent, fill = continent)) +
  geom_bar()
```

![](Task2.3_files/figure-html/unnamed-chunk-3-1.png)<!-- -->

## Pick two variables and create a chart that summarizes the bivariate distribution (the relationship between the two).



```r
gapminder %>% 
  ggplot(aes(x = lifeExp, y = gdpPercap, color = continent)) + 
    geom_point() + 
  theme_classic()
```

![](Task2.3_files/figure-html/unnamed-chunk-4-1.png)<!-- -->

## Try using color, shape, alpha, facets, etc., to visualize the relationships among 3 or more variables.



```r
gapminder[gapminder$year == 2007,] %>%
  ggplot(aes(x = reorder(continent,lifeExp), y = lifeExp, fill = continent)) +
    geom_boxplot() +
    theme_classic()
```

![](Task2.3_files/figure-html/unnamed-chunk-5-1.png)<!-- -->

## Use the rest of your preparation time for this task to repeat the above on various variables.



```r
gapminder[gapminder$year == 2007,] %>%
  ggplot(aes(x=gdpPercap, group=continent, fill=continent)) +
    geom_density(adjust=1.5, alpha=.3) +
    theme_classic()
```

![](Task2.3_files/figure-html/unnamed-chunk-6-1.png)<!-- -->




  
