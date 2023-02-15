# 28.2.1 Exercises
# Create one plot on the fuel economy data
# with customised title, subtitle, caption,
# x, y, and colour labels.

library(mosaic)
library(RColorBrewer)

View(mpg)

mpg %>% 
  ggplot(aes(x = fct_reorder(drv, hwy, .fun = median), y = hwy, fill = fct_reorder(drv, hwy, .fun=median))) +
  geom_boxplot() +
  scale_fill_brewer(palette = 12)+
  labs() +
  theme_bw() +
  theme(legend.position = 0) +
  labs(title = 'Highway miles per gallon by drive train type',
       x = 'Highway miles per gallon',
       y = 'Type of drive train',
       caption = 'f = front-wheel drive\nr = rear wheel drive\n4 = 4wd'
       ) 



