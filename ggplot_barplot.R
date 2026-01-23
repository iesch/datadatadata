### Script Plotting the Bar Plot ###

library(tidyverse)

#Load in data
data <- read_csv('Results/deathcount.csv')
pivoted_df <- pivot_wider(data, names_from = century, values_from = deathcount)

#Selecting for the top 5 deathcount countries per century
df19 <- select(pivoted_df, region, `19`) |> arrange(desc(`19`)) |> slice_head(n = 5)
df20 <- select(pivoted_df, region, `20`) |> arrange(desc(`20`)) |> slice_head(n = 5)
df21 <- select(pivoted_df, region, `21`) |> arrange(desc(`21`)) |> slice_head(n = 5)
#Binding the dfs back into a single table
df19 <- rename(df19, deathcount = `19`) |> mutate(century = '19th Century')
df20 <- rename(df20, deathcount = `20`) |> mutate(century = '20th Century')
df21 <- rename(df21, deathcount = `21`) |> mutate(century = '21th Century')
deathcount_df <- bind_rows(df19, df20, df21)

#Plotting
barplot <- ggplot(data = deathcount_df) +
    aes(x = century, y = deathcount, fill = region) +
    labs(x = NULL, y = 'Number of Deaths', fill = NULL) +
    expand_limits(y=0:6250) +
    geom_col(stat = 'identity', position = 'dodge') +
    geom_text(aes(label = region), position = position_dodge(width = 0.9),
      angle = 90, vjust = 0.5, hjust = -0.1, size = 5, family = 'serif') +
    scale_fill_viridis_d(option = 'turbo') +
    theme_minimal() +  
    theme(legend.position = 'none',
      text = element_text(family = 'serif'),
      axis.text.y = element_text(face = 'bold', color = 'black', size = 13, hjust = 1.1),
      axis.line.y.left = element_line(color = 'black', linewidth = 0.5, linetype = 'solid'),
      axis.text.x = element_text(face = 'bold', color = 'black', size = 14, vjust = 3),
      axis.title.y = element_text(face = 'bold', color = 'black', size = 12, margin = margin(r = 2)),
      panel.grid.major = element_blank(),
      panel.grid.minor = element_blank())
ggsave('Results/top_5_century.pdf', plot = barplot, width = 15, height = 10, units = 'cm')