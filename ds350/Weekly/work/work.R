library(tidyverse)
library(stringi)

lds <- rio::import("http://scriptures.nephi.org/downloads/lds-scriptures.csv.zip")

rds <- rio::import("https://byuistats.github.io/M335/data/BoM_SaviorNames.rds")

jesuspat <- rds |> 
  pull(name) |> 
  str_c(collapse = "|")

get_text <- function(book){
  text <- lds |> 
      filter(book_lds_url == book) |> 
      pull(scripture_text) |> 
      unlist() |> 
      str_c(collapse = " ")
  text
}

break_jesus <- function(phrase,pattern){
  count_words <- function(x){stri_stats_latex(x)["Words"]}
  temp <- str_split(phrase, pattern) |> unlist()
  data.frame(temp)|>
    rowwise() |> 
    mutate(word_count = count_words(temp))
}

gswc <- function(book){
break_jesus(get_text(book),jesuspat) |> 
    mutate(book = book)
}
 
gswc("jacob")

bom_books <- lds |> 
  filter(volume_lds_url == "bm") %>%
  .$book_lds_url |> unique()

bibble <- data.table::rbindlist(map(bom_books, gswc))|> 
  mutate(book = book |> fct_inorder())

bibble |> 
ggplot(aes(x = word_count, y = book |> fct_rev(), label = book)) +
  geom_boxplot(alpha = .5, fill = "lightblue") +
  scale_x_continuous(trans = 'log10') +
  theme_bw() +
  theme(legend.position = "none") +
  labs(title = "Distribution of "words between Savior references" between books in the Book of Mormon.",
    x = "Distribution of words between Savior references",
    y = "Books in the Book of Mormon")

