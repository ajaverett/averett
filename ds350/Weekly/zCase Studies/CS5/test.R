library(tidyverse)
library(maps)

news <- bind_rows(read_csv("https://storybench.org/reinventingtv/abc7ny.csv"), 
                  read_csv("https://storybench.org/reinventingtv/kcra.csv"))

us.cities |> 
  mutate(citynames = str_sub(name, 1, -4) ) |> 
  select(-c(lat, long, capital, name))

news |> 
  mutate(city = str_extract(headline, pattern = (
      us.cities |> 
      mutate(citynames = str_sub(name, 1, -4) ) |> 
      select(-c(lat, long, capital, name)) |>  
      filter(!country.etc %in% c("CA", "NY"),
             !citynames == "Manhattan") |> 
      select(citynames, country.etc) |>  
      mutate(length = str_length(citynames)) |> 
      arrange(desc(length)) |> 
      select(-length) |> 
      pull(citynames) |> 
      str_c(collapse = "|") |> 
      str_replace("Sandy\\|", "(?<!Superstorm )Sandy(?! Kenyon)(?! Hook)|") |> 
      str_replace("Moore\\|", "(?<!Roy )(?<!Brian )(?<!Bud )(?<!Tyler )(?<!Mandy )Moore|") |> 
      str_replace("Davis\\|", "(?<!Viola )(?<!Kim )Davis|")
      ) 
  )) |> # View()
  count(city) |> 
  na.omit() |> 
  arrange(desc(n)) |> View()

news %>% 
  mutate(keep = str_detect(headline,"Folsom")) %>% 
  filter(keep == TRUE) |> View()
