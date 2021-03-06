
library(tidyverse)
library(lubridate)
library(DBI)
library(odbc)
library(RMySQL)
library(leaflet)


crime <- read_csv("C:/Users/Owner/Documents/data-science-projects/ds-squad/crime.csv") %>%
  mutate(incident_date = as.Date(incident_datetime)) %>%
  filter(incident_date >= "2020-01-01")

################################
## Where are crimes occuring? ##
################################

crime %>% 
  #filter(`Neighborhood 1` == "Allentown") %>%
  filter(`Police District 1` %in% c("District A")) %>%
  leaflet() %>%
  addTiles() %>%
  addCircleMarkers(
    ~longitude,
    ~latitude,
    stroke = F,
    opacity = 0.05,
    radius = 4
  )

incidents <- crime %>%
  filter(`Police District 1` %in% c("District A"),
         incident_date >= "2021-01-01") %>%
  group_by(neighborhood) %>%
  summarise(Incidents = n_distinct(case_number)) %>%
  ungroup()

p <- incidents %>%
  ggplot(aes(x = Incidents, y = reorder(neighborhood, Incidents))) +
  geom_col(fill = "orange") +
  labs(title = "Total incidents in the last 3 months by neighborhood",
       y = "") +
  theme_bw()

ggplotly(p)

###########
## Types ##
###########

incident_types <- crime %>%
  filter(`Police District 1` %in% c("District A"),
          incident_date >= "2021-01-01") %>%
  group_by(neighborhood, parent_incident_type) %>%
  summarise(Incidents = n_distinct(case_number)) %>%
  ungroup()

incident_types %>%
  filter(neighborhood == "South Park") %>%
  ggplot(aes(x = Incidents, y = reorder(parent_incident_type, Incidents))) +
  geom_col(fill = "orange") +
  labs(title = "Total incidents in the last 3 months by neighborhood",
       y = "") +
  theme_bw()
