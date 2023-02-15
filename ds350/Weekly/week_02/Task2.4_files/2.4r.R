library(tidyverse)
library(cowplot)
library(gapminder)

viz2.4a <- gapminder %>% filter(country != "Kuwait") %>%
  ggplot(aes(x=lifeExp, y=gdpPercap, color=continent)) + 
  geom_point(aes(size = pop)) +
  facet_wrap(year~.,ncol =12) +
  theme_bw() +
  scale_y_continuous(trans = "sqrt") 

ggsave('viz2.4a.png', viz2.4a, width = 15)
save_plot('viz2.4.png', viz2.4, base_width = 15)


