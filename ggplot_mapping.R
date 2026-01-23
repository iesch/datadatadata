### Script Plotting the Map ###

#Import tidyverse and maps and reading in the data
library(tidyverse)
library(maps)

coordinates <- map_data("world")
data <- read_csv('Results/deathcount.csv')

# Filter and combine datasets 
coordinates_expanded <- coordinates |>
  expand_grid(century = c(19, 20, 21))
data_mapping <- data |>
  right_join(coordinates_expanded, by = c('region', 'century')) |>
  group_by(century) |>
  #Create a relative death count per century
  mutate(rel_deathcount = deathcount / sum(deathcount, na.rm = TRUE)) |>
  mutate(
    #Remove NA values and rename the centuries
    deathcount = replace_na(deathcount, 0),
    rel_deathcount = replace_na(rel_deathcount, 0),
    century = case_match(century,
      19 ~ "19th",
      20 ~ "20th",
      21 ~ "21st"
    ))

#Plot the figure
ggplot(data = data_mapping) +
  aes(x=long, y =lat, fill = deathcount, map_id = region) +
  geom_map(map = data_mapping) + 
  #Remove labels on axes
  scale_x_continuous(labels = NULL) +
  scale_y_continuous(labels = NULL) +
  labs(x = NULL, y = NULL) +
  #Formatting the plot
  scale_fill_viridis_c(name = 'Death Count', option = 'rocket', trans = "log10", na.value = '#f0e4ccff', 
    guide = guide_colorbar(position = "bottom"), direction = -1) +
  ggtitle('Amount of Deaths per Country', 'From the 19th until the 21st century')+
  theme(text = element_text(size = 10, family = 'serif'))+
  coord_fixed(1.3) +
  #Adding all maps to the figure
  facet_wrap('century', ncol = 3)

ggsave('map_plot.pdf', height = 8, width = 19, units = "cm")
