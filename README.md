# SafeHomes - Full Stack Web Application 

Our application aims to provide users with a convenient and concise way to shop for homes while considering factors that most real estate websites do not: the safety of the area the homes are located in and the quality of education within the houses’ associated school districts. We chose to produce this application because we wanted to create something useful and build upon the ideas of great applications such as Zillow, but also take it one step further to provide additional important information with our listings such as crime data. The key components to our project are listing houses, viewing houses and filtering based on school district, county safety data, and city, updating listings, deleting listings, looking at county-wide crime data, and searching for houses on our interactive map.

## **Database Details**

Our tables are in the 3rd normal form.

We accommodated for functional dependencies by dividing our original tables further into lookup tables when necessary. For example, we created a StatisticsOf table to connect our county information to our crime statistics information because including the district number in the crime statistics table provided an unwanted functional dependency. 

### Schema 

**Counties**(DistrictNumber, DistrictName, Grade2022)
Primary Key = DistrictNumber
Dependencies:  DistrictNumber -> DistrictName, Grade2022
  
**Schools**(SchoolID, DistrictNumber, SchoolName, Grade2022)
Primary Key = SchoolID
Foreign Key = DistrictNumber REFERENCES Counties(DistrictNumber) 
Dependencies: SchoolID -> DistrictNumber, SchoolName, Grade2022
 
**CrimeStatistics**(statisticsID, totalCrimeIndex, Total_Arrests, Population, Burglary, Larceny, Motor_Vehicle_Theft, Manslaughter, Kidnap_Abduction, Arson, Simple_Assault, Drug_Arrest, Bribery, Embezzlement, Fraud, Counterfeit_Forgery, Extortion_Blackmail, Intimidation, Prostitution, NonForcible_Sex_Offenses, Stolen_Property, DUI, Destruction_Vandalism, Gambling, Weapons_Violations, Liquor_Law_Violations, Misc)
Primary Key = statisticsID
Dependencies: statisticsID -> totalCrimeIndex, Total_Arrests, Population, Burglary, Larceny, Motor_Vehicle_Theft, Manslaughter, Kidnap_Abduction, Arson, Simple_Assault, Drug_Arrest, Bribery, Embezzlement, Fraud, Counterfeit_Forgery, Extortion_Blackmail, Intimidation, Prostitution, NonForicble_Sex_Offenses, Stolen_Property, DUI, Destruction_Vandalism, Gambling, Weapons_Violations, Liquor_Law_Violations, Misc
 
**Cities**(cityName, countyName, population)
Primary Key = cityName
Foreign Key = countyName REFERENCES Counties(DistrictName)
Dependencies: cityName -> countyName, population
 
**StatisticsOf**(DistrictNumber, statisticsID)  //lookup table
Primary Key = DistrictNumber, statisticsID
Foreign Key = DistrictNumber REFERENCES Counties(DistrictNumber), statisticsID REFERENCES CrimeStatistics(statisticsID)
Dependencies: DistrictNumber -> statisticsID ; statisticsID -> DistrictNumber
 
**Homes**(listingID, ZipCode, property_url, style, street, unit, city, beds, full_baths, half_baths, sqft, year_built, price, photo)
Primary Key = listingID
Foreign Key = ZipCode REFERENCES ZipCodes(ZipCode)
Dependencies: listingID-> ZipCode, property_url, style, street, unit, city, beds, full_baths, half_baths, sqft, year_bult, price, photo
 
**ZipCodes**(ZipCode, City, County) //lookup table
Primary Key = ZipCode
Dependencies: ZipCode -> City, County

## **Functionality Details**

Our basic functions follow the create, read, update, delete functionalities through adding house listings to the database through the add listings page, searching for homes through the view listings page, editing listings’ details on the edit listing page, and removing listings from the database on the delete listings page, as well as a delete option on the house details page.

Our application features functionalities that are dependent on join queries, such as finding the home’s county by joining the ZipCodes table with the Homes table and retrieving crime data for a home by joining the Homes table with the ZipCodes table and the CrimeStatistics table. Another example of a join query we used was in our functionality of searching for homes based on school district grades and safety grades. To do this, we implemented a join on the Homes table on the ZipCodes table on the CrimeStatistics table on the Counties table.

We implemented an aggregate function through the part of our application where it provides how many listings match your filter specifications. We did this by using COUNT to count the amount of tuples returned by our queries, which processes all the returned listings and sums them up to provide one result. This is helpful for users as they can see how many possible houses they have to look at. We also implemented the aggregate query of AVG to find the average crime statistics per crime across the state on the crime mapping page.

We created two advanced functions for our SafeHomes application: A filtering system to search for houses based on city, safety grade, and school district grade and an interactive map that allows users to search for houses by navigating a map. Our filtering system uses multiple join and aggregate queries to provide the correct search results and provide the user with house listings matching their specifications. Our filtering system searches through 200,000 listings to provide 24 listings that reflect the user’s selection and reselecting your options and hitting generate will provide a new 24 each time. We chose to just show 24 listings at a time on one page for simplicity purposes as we have a vast collection of house data and our queries return over 100 + possible house matches. Our map populates listings based on their longitude and latitude coordinates and allows users to search for houses geographically. The map filters through over 200,000 listings and utilizes a Google Maps API and is integrated into the frontend of our application using HTML and Javascript.

## **Implementation Details**

Our database was created using MySQL, our front-end with HTML, CSS, and Javascript, and our database communication through Python, Flask, and the “mysql-connector” python library. Our project was also hosted on Github and Amazon Web Services to allow the three of us to work simultaneously and organize our code. We created logical backups of the database using MySQL periodically as well. 

The front end Web interface was made entirely with HTML, CSS, and Javascript. We chose to create a separate HTML page for each section such as the index.html(homepage), addlisting.html, crimemap.html, deletelisting.html, editlisting.html, house.html, and viewlisting.html, and used a single styles.css to format all of it. All of the pages are linked together using search buttons, as well as a navigation bar on each page. Javascript is used to retrieve the crime maps for each county, as well as populating the Google Map. Fonts were pulled from Google Fonts, and the Google Map is pulled from the Google Map API. 

The front and back interaction is done using Python and Flask. We created a file, app.py, to retrieve and edit data from the database using query statements passed in. The HTML pages include forms that connect to the app.py. When the forms are submitted, that form’s data is passed into app.py and interacts with the database. We then display this data directly into the HTML pages, replacing the placeholder objects initially made. This way, we can have a single HTML page for the house details that just updates the data accordingly per house. 

## Data Retrieval 

Our crime information is gathered from an official 2021 statewide county crime report located from the Florida Department of Law Enforcement website. Python scripts were written to add all the data from the .csv files to the database automatically. This populated our database with over 200,000 listings from Florida alone. For the sake of the project’s scope, the house listings will not be dynamically updated as it would for sites like Zillow. 

List of cities within each Florida County: https://www.fl-counties.com/about-floridas-counties/florida-cities-by-county/ 
List of schools districts in Florida: https://sss.usf.edu/resources/floridamap/index.html 
List of all schools In Florida by county: https://web03.fldoe.org/schools/schoolmap_text.asp/
Florida Crime Grades: https://crimegrade.org/ 

## Experiences

Through this project we have learned more about designing databases and got first hand experience in normalizing tables into 3rd normal form. We learned how to interact with a database through libraries such as mysql connector to communicate our data from backend to front end.  This was also our first experience using AWS to allow the three of us to access the database from multiple computers. Developing a full application has taught us a lot about bringing all of our skills together to create a full software product. We also learned about communication and working as a team.

The most challenging problems of the project came from developing the schemas and database, as well as implementing the flask to correctly render all of the data onto the HTML pages. We spent many hours learning how to communicate with one another and reading documentations to come up with solutions to the code successfully. Thankfully, the three of us had different skill sets that complimented each other well, so we were able to learn from one-another. We were able to learn how to navigate having multiple people working on the project at the same time utilizing Github and AWS, strengthening these vital industry skills for our future careers. 

We could extend our project to pertain to houses all across the United States instead of just Florida. This would entail a much larger amount of listings and therefore our database would need to be able to support it. We could also implement a housing API so our listings are actively updated and do not need to be stored manually in our database. Our database is currently powered by a student aws account and therefore has the limitations associated with the database services provided at the free level. We could also put our project on a permanent domain instead of running on a localhost development server. 
