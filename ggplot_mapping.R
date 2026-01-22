
library(tidyverse)
library(maps)

coordinates <- map_data("world")

data <- read_csv('Results/deathcount.csv')

coordinates_expanded <- coordinates |>
  expand_grid(century = c(19, 20, 21))

data_mapping <- data |>
  right_join(coordinates_expanded, by = c('region', 'century')) |>
  group_by(century) |>
  mutate(rel_deathcount = deathcount / sum(deathcount, na.rm = TRUE)) |>
  mutate(
    deathcount = replace_na(deathcount, 0),
    rel_deathcount = replace_na(rel_deathcount, 0)
  )


ggplot(data = data_mapping) +
  aes(x=long, y =lat, fill = deathcount, map_id = region) +
  geom_map(map = data_mapping) + 
  scale_x_continuous(labels = NULL) +
  scale_y_continuous(labels = NULL) +
  labs(x = NULL, y = NULL) +
  scale_fill_viridis_c(option = 'rocket', trans = "log10", na.value = 'black') +
  coord_fixed(1.3) +
  facet_wrap('century', ncol = 2)