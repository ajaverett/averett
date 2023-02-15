library(tidyverse)
library(stringi)

sentences[1]
stri_stats_latex(sentences[1])
stri_stats_latex(sentences[1])["Words"]

tibble(sentence =  sentences[1:4]) %>% 
  rowwise() %>% 
  mutate(words = stri_stats_latex(sentence)["Words"])

bom <- rio::import("http://scriptures.nephi.org/downloads/lds-scriptures.csv.zip") %>% as_tibble()

# unique(bom$volume_short_title)
# colnames(bom)
# bom %>% head() %>% View()


bom_len <- bom %>% 
  filter(volume_short_title == "BoM") %>% 
  mutate(book = book_lds_url) %>% 
  rowwise() %>% 
  mutate(words = stri_stats_latex(scripture_text)["Words"]) %>% 
  group_by(book) %>% 
  summarize(book.length = sum(words),
         average.length = mean(words)) %>% 
  arrange(desc(book.length)) %>% 
  pull(book.length) %>% 
  .[5]




bom %>% 
  filter(volume_short_title == "BoM") %>% 
  mutate(book = fct_inorder(book_lds_url)) %>% 
  select(c(book,scripture_text)) %>% 
  rowwise() %>% 
  mutate(words = stri_stats_latex(scripture_text)["Words"]) %>% 
  group_by(book) %>% 
  mutate(book.length = sum(words),
            average.length = mean(words)) %>% 
  filter(book.length >= bom_len) %>% 
  ggplot(aes(x = words, fill = book)) +
  geom_density(alpha = .4) + theme_test()
  

ggplot(aes(x = average.length, y = book ,fill = book)) +
  geom_col() + theme_test()

  
  


