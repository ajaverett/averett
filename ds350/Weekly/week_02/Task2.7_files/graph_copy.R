library(tidyverse)
library(dplyr)
library(cowplot)
library(gapminder)
library(stats)

viz2.4a <- gapminder %>% filter(country != "Kuwait")

ggsave('viz2.4a.png', viz2.4a, width = 15)
save_plot('viz2.4.png', viz2.4, base_width = 15)


temp1 <- viz2.4a %>% 
  group_by(continent, year) %>% 
  mutate(weighted = weighted.mean(gdpPercap,pop = sum(pop))) #%>% View()


viz2.4a %>% 
  ggplot(aes(x = year, y = gdpPercap, group = country, fill = continent, color = continent)) +
  geom_line() +
  geom_point(shape = 21) +
  facet_wrap(.~continent, nrow = 1) +
  geom_line(temp1, mapping = aes(x = year, y = weighted)) +
  geom_point(temp1, mapping = aes(x = year, y = weighted, size = pop/25000
                                  ),color = 'black', fill = 'black') +
  theme_bw() +
  labs(x = 'Year', y = 'GDP per Capita') 
  
