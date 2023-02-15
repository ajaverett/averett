library(Lahman)

View(Batting)

ws <- BattingPost %>%
  mutate(BA = 0 + (AB > 0) * round(H/AB, 3),
         TB = H + X2B + 2 * X3B + 3 * HR,
         PA = AB + BB + IBB + HBP + SH + SF,
         OB = H + BB + IBB + HBP,
         OBP = 0 + (AB > 0) * round(OB/PA, 3),
         SLG = TB / AB,
         OPS = OBP + SLG) %>% 
  select()
