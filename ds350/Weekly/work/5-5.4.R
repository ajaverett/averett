library(tidyverse)
library(stringi)
library(lubridate)
sentences[1]
stri_stats_latex(sentences[1])

count_words <- function(x){stri_stats_latex(x)["Words"]}
count_chars_word <- function(x){stri_stats_latex(x)["CharsWord"]}
count_chars_white <- function(x){stri_stats_latex(x)["CharsWhite"]}
count_len <- function(x){str_length(x)}

chp <- read_csv("https://byuistats.github.io/M335/data/chipotle_reduced.csv")

test_string <- chp$popularity_by_day[chp$placekey == "zzw-222@5vg-nwf-mp9"]

weekday_clean = function(str){
  str <- str_split(str,',') 
  day <- str |> unlist()
  df <- data.frame(day)
  df|> 
    separate(day,c("a","Day","Value","d")) |> 
    select(c(Day,Value)) |> 
    arrange(desc(Value))
}

aggregate_df <- function(df){
  df |>
    pull(popularity_by_day)|> 
    list() |>  
    flatten() |> 
    weekday_clean() |> 
    na.omit() |>
    group_by(Day) |> 
    mutate(Value = as.numeric(Value)) |> 
    summarize(total_visits = sum(Value),
              avg_visits = mean(Value)) |> 
    arrange(desc(total_visits))
}

t.key <- "22c-222@5z5-3rs-hwk"
t.key2 <- "zzw-223@5r8-fqv-xkf"

day_popularity <- function(key, df){
  df |> 
    filter(placekey == key) |> 
    pull(popularity_by_day) |> 
    weekday_clean() |> 
    slice(which.max(Value)) %>%
    .[1] |> as.character()
    
}

day_popularity(t.key2, chp)

key <- t.key2
chp |> 
    filter(placekey == key) |> 
    pull(popularity_by_day) |> 
    weekday_clean() |> 
    slice(which.max(Value)) %>%
    .[1] |> as.character()




