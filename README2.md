# Project 2 ORDBMS
### Ziyi Liao(zl2739)  Na Zhuo(nz2297)
#### Modifications
We made the following modifications in our school recommandation database in order to improve the searching feature. <br/>

| Object Name | Type | Location | Description |
| ------------- | ------------- | ------------- | ------------- |
| courses | course_type (Array) | Student | In student table we added an array to record all the enrolled courses of a student, with maximum 50 |
| courses | course_type (Array) | Teacher | In teacher table we added an array to record all the courses taught by this teacher, with maximum 50 |
| info | crime_type (composite) | new_crime | In order to maintain data integrity, we make a backup table called new_crime and contribute our attribute "info" with user defined data type called crime_type, which records the crime type and occur date |
| Address | address_type (composite) | School | In oreder to gain a more clear view of the database, we create a composite data type called "address_type" for column Address in table school to store the address information more efficiently. The column contains street, borough and zipcode of each school respectively |
#### Queries
##### 1.Search school with name "Willamsberg" 

This query takes use of the documentation we created in school table. 

##### 2. Find the students who enrolled less than 2 courses


##### 3. Gather the information of assulting crime happened in Manhattan 
