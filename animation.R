install.packages('gganimate')
library(tidyverse)
library(maps)
library(gganimate)


coordinates <- map_data("world")

data <- read_csv('Results/time_deathcount.csv') |>
    mutate(year = as.integer(year))

data_mapping <- data |>
  right_join(coordinates, by = 'region')|>
  group_by(year) |>
  mutate(rel_deathcount = deathcount / sum(deathcount, na.rm = TRUE)) |>
  mutate(
    deathcount = replace_na(deathcount, 0),
    rel_deathcount = replace_na(rel_deathcount, 0)
  )

ggplot(data = data_mapping) +
  aes(x=long, y=lat, fill = deathcount, map_id = region) +
  geom_map(map = data_mapping) + 
  scale_x_continuous(labels = NULL) +
  scale_y_continuous(labels = NULL) +
  labs(x = NULL, y = NULL) +
  scale_fill_viridis_c(option = 'rocket', trans = 'log10', na.value = 'black') +
  coord_fixed(1.3) +
  facet_wrap('year', ncol = 2) +
  transition_time(year) +
  ease_aes('linear')

