# LGBT VIOLENCE AND HARASSMENT IN EUROPE<br>
## Description :<br>
This project aims at, with help of two dahsboards (created with Python and R), exhibiting violences and harassment the LGBT (Lesbian, Gay, Bixesual and Transgender) community is going through. In addition, analysis and interpretation of obtained graphs are provided, leading to a better comprehension on the possible fears and assaults that victims of systemic homophobia and/or transphobia suffer from.

This project leans on two surveys directed to European LGBT volonteers, and forms our data sets :

        - one about their daily life, and another one regarding the assaults (sexual or non sexual) and harassments they can suffer (Pyhton -> Dash)
        - only the data set about violences and harassments (R -> Shiny)
## Used data :<br>
1/ "LGBT_Survey_DailyLife.csv"

        This raw data set is of size 34021*6.
        The 6 variables are :
                - The country (CountryCode) -> European countries
                - The LGBT community's subset (subset) -> Lesbian, Gay, Bisexual Woman, etc...
                - The question code (question_code)
                - The written question (question_label)
                - The answer (answer)<br>
2/ "LGBT_Survey_ViolenceAndHarassment.csv" (renommé "LGBT_Survey")

This raw data set is of size 45356*6.
The 6 variables are the same as for the first data set.
## R packages setup :
Code : 
    
    install.packages("shiny")
    install.packages("dplyr")
    install.packages("geojsonio")
    install.packages("leaflet")
    install.packages("ggplot2")
    install.packages("shinythemes")
## Python packages setup :
Code : 
    
    pip install folium
    OR
    conda install -c conda-forge folium
## Script :
R : Simply open the app.R file with RStudio and then "Run App" for its execution.

Pyhton : Run with the command "python Dashboard.py".
