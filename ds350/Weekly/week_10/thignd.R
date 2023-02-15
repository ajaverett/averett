# 5.2 Task: Chipotle Promo - Part 1
# You got your dream job working as a data analyst for one of your favorite restaurants, Chipotle. Chipotle is planning to run a large 1 or 2 day promotion. They would like the promotion to take place when the restaurant is busiest. They have gathered restaurant level data that you can use to answer the question, "What is the busiest day in the restaurant?"
# 
# We will answer this question over the course of a couple of tasks. In this task, we'll focus on creating some functions that we'll iterate over in a later task.
# 
# Before exploring the Chipotle data, let's walk through the process of creating new functions in a different context we've seen before. We previous explored the stri_stats_latex() function from the stringi package. Run the code below to load the needed libraries and remind yourself what stri_stats_latex() does.
# 
library(tidyverse)
library(stringi)
sentences[1]
stri_stats_latex(sentences[1])
# Rather than get a list of facts about a string, we can create our own functions to extract exactly the pieces of information we want, such as the word count or number of white space characters. Below we create functions to individually count 4 specific things.
# 
count_words <- function(x){stri_stats_latex(x)["Words"]}
count_chars_word <- function(x){stri_stats_latex(x)["CharsWord"]}
count_chars_white <- function(x){stri_stats_latex(x)["CharsWhite"]}
count_len <- function(x){str_length(x)}

sentences[1]
count_words(sentences[1])
count_chars_word(sentences[1])
count_chars_white(sentences[1])
count_len(sentences[1])
# We can count all 4 items above and return the information in a nice tibble (tidy table), by writing other functions, as shown below.
# 
count_stats_wide <- function(x){
  tibble(
    words = count_words(x),
    chars_word = count_chars_word(x),
    chars_white = count_chars_white(x),
    len = count_len(x)
  )
}
count_stats_long <- function(x){
  tibble(
    name = c("words","chars_word","chars_white","len"),
    value = c(count_words(x),
              count_chars_word(x),
              count_chars_white(x),
              count_len(x))
  )
}
# 
sentences[1]
count_stats_wide(sentences[1])
count_stats_long(sentences[1])
# Run all the code above, and come with any questions you have about parts of the code. We're now ready to tackle the Chipotle data.
# 
# Read in the restaurant level data from 

temp <- read_csv('https://byuistats.github.io/M335/data/chipotle_reduced.csv')
# 
chp <- read_csv("https://byuistats.github.io/M335/data/chipotle_reduced.csv")
# This data dictionary can help answer questions you may have about the data.
# The data contains a column popularity_by_day. This column contains a lot of information we need to extract from a string. As an example, for the restaurant with placekey equal to "zzw-222@5vg-nwf-mp9", we can obtain a test_string below.
# 
"{\"Monday\":94,\"Tuesday\":76,\"Wednesday\":89,\"Thursday\":106,\"Friday\":130,\"Saturday\":128,\"Sunday\":58}"
# 
# #This code uses base R to extract the string.
 test_string <- chp$popularity_by_day[chp$placekey == "zzw-222@5vg-nwf-mp9"]
# 
# #This code uses dplyr to extract the string
 test_string <- chp %>% 
   filter(placekey == "zzw-222@5vg-nwf-mp9") %>%
   pull(popularity_by_day)
# 
# test_string
# Your task is to create 2 functions to help us obtain meaningful data from these strings.
# 
# The first function should take as input a string from the popularity_by_day column, such as test_string above, and return a tibble that contains the name of each day of the week in one column, and the number of visits at that store in the other column.
# 
# The second function should have the same input as the previous function (so a long string from the popularity_by_day column), and return the most popular day of the week, in terms of visists (or a comma separated string if there are ties).
# 
# Verify that your functions are working.
# 
# For the test_string above (with placekey "zzw-222@5vg-nwf-mp9"), your first function should return a table similar to the one below, while the second function should return "Friday".
# # Monday       94
# # Tuesday      76
# # Wednesday    89
# # Thursday    106
# # Friday      130
# # Saturday    128
# # Sunday       58
# For the popularity_by_day string corresponding to placekey "22c-222@5z5-3rs-hwk", your first function should return a table similar to the one below, while the second function should return "Saturday".
# # Monday       18
# # Tuesday      16
# # Wednesday    14
# # Thursday     27
# # Friday       26
# # Saturday     36
# # Sunday       20
# For the popularity_by_day string corresponding to placekey "zzw-223@5r8-fqv-xkf", your first function should return a table similar to the one below, while the second function should return "Wednesday, Saturday".
# # Monday       0
# # Tuesday      0
# # Wednesday    1
# # Thursday     0
# # Friday       0
# # Saturday     1
# # Sunday       0
 
temp <- chp$popularity_by_day[2]

temp2 <- str_split(temp, ",") |> unlist()
  
temp3 <- str_extract(temp2, "[\\d]+")
temp4 <- str_extract(temp2, "[:alpha:]+")

data.frame(temp4, temp3)

c(1,"2") 
chp |> View() 
  mutate()



