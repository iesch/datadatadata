

library(tidyverse)
library(maps)

coordinates <- map_data("world")

ggplot() +
  geom_map(
    data = coordinates, map = coordinates,
    aes(long, lat, map_id = region),
    color = "black", fill = "lightgreen", linewidth = 0.2 )+
  theme(panel.background = element_rect(fill = "lightblue"),
      panel.grid.minor = element_line(color="lightblue"),
      panel.grid.major= element_line(color="lightblue"),
      axis.ticks.y = element_blank(),
      axis.ticks.x = element_blank()) +
  scale_x_continuous(labels = NULL) +
  scale_y_continuous(labels = NULL) +
  labs(x = NULL, y = NULL)
 
#data_19 <- read_csv
#data_20 <- read_csv