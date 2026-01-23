### Script Plotting the Top 5 Countries Bar Plot and Total Death Count Bar Plot ###
#Imports
library(tidyverse)
library(tidytext)

# ----------------
#  FIRST BARPLOT
# ----------------

#Load in data
data <- read_csv('Results/CSV/deathcount.csv')
pivoted_df <- pivot_wider(data, names_from = century, values_from = deathcount)

#Selecting for the top 5 deathcount countries per century
df19 <- select(pivoted_df, region, `19`) |> arrange(desc(`19`)) |> slice_head(n = 5)
df20 <- select(pivoted_df, region, `20`) |> arrange(desc(`20`)) |> slice_head(n = 5)
df21 <- select(pivoted_df, region, `21`) |> arrange(desc(`21`)) |> slice_head(n = 5)
#Binding the dfs back into a single table. century as numerical value for possible reordering
df19 <- rename(df19, deathcount = `19`) |> mutate(century = 19)
df20 <- rename(df20, deathcount = `20`) |> mutate(century = 20)
df21 <- rename(df21, deathcount = `21`) |> mutate(century = 21)
deathcount_df <- bind_rows(df19, df20, df21)

#Reordering regions within each century by deathcount
deathcount_df <- deathcount_df %>%
  mutate(region_reordered = reorder_within(region, deathcount, century))
#Changing numerical values back to factors so that scale_x_discrete works later on
deathcount_df$century <- factor(deathcount_df$century) #works for mysterious reasons

#Plotting top_5_century barplot
barplot_top5 <- ggplot(data = deathcount_df) +
    #X-scale is century, Y-scale is deathcount
    #Give each region an individual color, but order based on region_reordered variable
    aes(x = century, y = deathcount, fill = region, group = region_reordered) +
    #Remove all scale labels and legends except the Y-scale
    labs(x = NULL, y = 'Number of Deaths', fill = NULL) +
    #Expand limits so all geom_texts are clearly visible and legible
    expand_limits(y=0:6250) +
    
    #Plot the columns representing numerical death counts side by side per century  
    geom_col(stat = 'identity', position = 'dodge') +
    #Attach text to each col at an appropriate and aesthetically pleasing location
    geom_text(aes(label = region), position = position_dodge(width = 0.9),
      angle = 90, vjust = 0.5, hjust = -0.1, size = 5, family = 'serif') +
  
    #Color scheme that is beautiful but not misinterpretable as a gradient
    scale_fill_viridis_d(option = 'turbo') +
    #Replacing numerical centuries by informative labels
    scale_x_discrete(labels = c('19th Century', '20th Century', '21st Century')) +
    
    #Customizing our theme until we are happy
    theme_minimal() +  
    theme(legend.position = 'none',
      text = element_text(family = 'serif'),
      axis.text.y = element_text(face = 'bold', color = 'black', size = 13, hjust = 1.1),
      axis.line.y.left = element_line(color = 'black', linewidth = 0.5, linetype = 'solid'),
      axis.text.x = element_text(face = 'bold', color = 'black', size = 14, vjust = 3),
      axis.title.y = element_text(face = 'bold', color = 'black', size = 12, margin = margin(r = 2)),
      panel.grid.major = element_blank(),
      panel.grid.minor = element_blank())
#Save result as pdf
ggsave('Results/Figures/top_5_century.pdf', plot = barplot_top5, width = 17, height = 10, units = 'cm')

# ----------------
#  SECOND BARPLOT
# ----------------

#Overwrite data with new totals.csv
data <- read_csv('Results/CSV/totals.csv')
refined_df <- select(data, -countries_recorded)

#Plotting totals_century barplot
barplot_totals <- ggplot(data = refined_df) +
    #X-scale is century, Y-scale is total deathcount, adding color to columns for flavor using 'fill'
    aes(x = century, y = total_deathcount) +
    #Remove all scale labels and legends except the Y-scale
    labs(x = NULL, y = 'Number of Deaths') +
    
    #Plot the columns representing numerical death counts per century
    geom_col(stat = 'identity', width = 0.9, fill = 'dark gray') +
  
    #Replacing numerical centuries by informative labels
    scale_x_discrete(labels = c('19th Century', '20th Century', '21st Century')) +
    
    #Customizing our theme until we are happy
    theme_minimal() +  
    theme(legend.position = 'none',
      text = element_text(family = 'serif'),
      axis.text.y = element_text(color = 'black', size = 13, hjust = 1.1),
      axis.line.y.left = element_line(color = 'black', linewidth = 0.5, linetype = 'solid'),
      axis.text.x = element_text(face = 'bold', color = 'black', size = 10, vjust = 5),
      axis.title.y = element_text(face = 'bold', color = 'black', size = 12, margin = margin(r = 4)),
      panel.grid.major = element_blank(),
      panel.grid.minor = element_blank())
#Save the result as a pdf 
ggsave('Results/Figures/totals_century.pdf', plot = barplot_totals, width = 10, height = 12, units = 'cm')