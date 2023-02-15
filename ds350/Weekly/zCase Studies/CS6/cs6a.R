
library(tidyverse)
library(lubridate)

sales <- read_csv("https://byuistats.github.io/M335/data/sales.csv") |> 
  mutate(Time = with_tz(Time, tzone = "America/Denver"),
    month = month(Time),
    day = day(Time),
    hour = hour(Time),
    minutes = minute(Time),
    date = as_date(Time)) |> 
  filter(Name != 'Missing') |> 
  mutate(date = date |> as.character(),
    date = recode(date, "2016-04-20" = "2016-05-12"),
    date = ymd(date))
    
sales1 <- sales  |>
  group_by(Name, date) |> 
  summarise(revenue = sum(Amount)) |> 
  mutate(date = ceiling_date(date, "week")) 

sales1 %>% 
  ggplot(aes(x = date, y = Name, fill = revenue)) +
  geom_tile() +
  theme_classic()+
  theme(panel.background = element_rect(
    fill = "black",
    colour = "darkgray",
    size = 1, 
    linetype = "solid"),
  ) +
  labs(title = 'Sales Over Time for Each Company',
       x = "Date",
       y = "Company Name") #+ facet_wrap(.~Name, scales = 'free')

subtract <- function(x,y){x - y}

sales2 <- sales  |>
  select(Name, hour, minutes, Amount) |> 
  mutate(
    minutes = case_when(
        minutes %in% 0:9 ~ str_c('0',minutes),
        TRUE ~ str_c(minutes)),
    hour = case_when(
        hour %in% 0:9 ~ str_c('0',hour),
        TRUE ~ str_c(hour)),
    meridiem = case_when(
        hour %in% 1:11 ~ "AM",
        hour %in% 12:23 ~ "PM",
        TRUE ~ "AM"),
    hour = hour |> as.numeric(),
    hour = case_when(
        hour %in% 13:23 ~ str_c(hour-12),
        TRUE ~ str_c(hour))
    ) |> 
  mutate(Datetime = str_c("01/01/2000 ", hour,":",minutes,":00 ",meridiem)) |> #View()
  # mutate(Datetime1 = as_datetime(Datetime)) |> View()
  mutate(Datetime = as.POSIXct(Datetime, format="%m/%d/%Y %I:%M:%S %p")
) |> 
  group_by(Name, Datetime) |>
  summarise(revenue = mean(Amount)) |>
  mutate(Datetime = ceiling_date(Datetime, "15 minutes"))

sales2 |> 
  ggplot(aes(x = Datetime, y = Name)) +
  geom_jitter(alpha = .5, size = 2, height = .2, color = "darkred") +
  theme_classic() +
  scale_x_datetime(breaks = "hour", 
                   #labels = "%I %p"   # NOT WORKING
                   ) +
  theme(axis.text.x = element_text(angle = 90))

