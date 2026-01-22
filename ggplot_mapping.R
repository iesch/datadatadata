
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
    rel_deathcount = replace_na(rel_deathcount, 0),
    century = case_match(century,
      19 ~ "19th",
      20 ~ "20th",
      21 ~ "21st"
    )
  )


ggplot(data = data_mapping) +
  aes(x=long, y =lat, fill = deathcount, map_id = region) +
  geom_map(map = data_mapping) + 
  scale_x_continuous(labels = NULL) +
  scale_y_continuous(labels = NULL) +
  labs(x = NULL, y = NULL) +
  scale_fill_viridis_c(name = 'Death Count', option = 'rocket', trans = "log10", na.value = 'black', guide = guide_colorbar(position = "bottom")) +
  ggtitle('Amount of Deaths per Country', 'From the 19th until the 21st century')+
  theme(text = element_text(size = 10, family = 'serif'))+
  coord_fixed(1.3) +
  facet_wrap('century', ncol = 3)
