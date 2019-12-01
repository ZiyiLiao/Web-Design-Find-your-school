# Project 2 ORDBMS
### Ziyi Liao(zl2739)  Na Zhuo(nz2297)
#### Modifications
We made the following modifications in our school recommandation database in order to improve the searching feature. <br/>

| Object Name | Type | Location | Description |
| ------------- | ------------- | ------------- | ------------- |
| courses | course_type (Array) | Student | In student table we added an array to record all the enrolled courses of a student, with maximum 50 |
| courses | course_type (Array) | Teacher | In teacher table we added an array to record all the courses taught by this teacher, with maximum 50 |
| info | crime_type (composite) | new_crime | In order to maintain data integrity, we make a backup table called new_crime and contribute our attribute "info" with user defined data type called crime_type, which records the crime type and occur date |
| address | address_type (composite) | School | In oreder to gain a more clear view of the database, we create a composite data type called "address_type" for column Address in table school to store the address information more efficiently. The column contains street, borough and zipcode of each school respectively |
| search | Documentation | Student and School | We created the documentation for names of schools and students in table School and Student respectively. |
#### Queries
##### 1.Search school with name "Willamsberg" 

This query takes use of the documentation we created in school table. Users can modify the query according to their requirements in both table School and Student. 

##### 2. Find the students who enrolled less than 2 courses

This query operates on the course array in student table. We filter the data by setting a limitation less than 2. 

##### 3. Gather the information of assulting crime happened in Manhattan 

This query works for the new composite column "info" in new_crime table. We conduct DQL on info by setting the matching certeria in each part of the composite column. Here we set part 1: type = assult and part 2: bid = M, which will point to the assulting crime in Manhattan. 
