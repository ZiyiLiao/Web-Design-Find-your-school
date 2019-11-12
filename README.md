# Find Your School

+ **Author**: Ziyi Liao (zl2739),  Na Zhuo (nz2297)


        PostgreSQL account: nz2297
        URL: 35.237.146.64 

---
### Introduction

This design implements the school recommendation in New York Area. In part 1, our database mainly contained two parts, the *environment* (external) facet and *school* (internal) facet. 

For internal facet, people can access to the school information including teachers, students, courses, evaluation survey scores as well as school's general information like principle, enrollment and government fund. For external facet, people can see get an insight of the location of the school, including crime information, number of schools.

We have realized both parts. What's more, we made some improvements in part 2 and the final database. The website are conducted according to the modified database. We added `SAT` score table into the database in order to improve the school recommendation feature; `demographic information` to the borough to enrich the data diversity of the database.  In addition, we store crime raw data rather than store the processed data facilitating the database update.

In our Web-End design, people can conduct search in two ways: 

+ search by school name

+ search by the customized criteria among borough, fund amount and SAT score level. 


### Searching

Firstly, if searched by a specific school name, the information about the school will be displayed. When click `more information`, the borough demography information will be available. 

Secondly, in `School Recommendation` module, the user can decide which according to `borough` or `SAT` score or `government fund` level. The choice of criteria can be any combination among them. After the customized conditions set, the school name will be displayed. By clicking the school name, more detailed information will be shown. This design aims to realize a comprehensive recommendation function. Users with first concern about the location can search by borough, while users (especially parents) cares about the academic output could search by SAT level. Last but not lease, if the financial sponsor of a school is really important to the user's choice, he or she can use the third search bar for fund. 

### Update

There are many fancy features to make the website more interactive. For example, log-in page enables school administrators and government administrators view more details. Also if the input of log-in page match the account and password in the database, updates can be made.

A school administrator could see the raw data about students, teachers and courses and is authorized to make some updates. He or she can update the SAT average score, and a government officer can update the fund, borough information. The level of SAT score and fund can be derived automatically according the user’s input.  

A government administrator can also make some updates on the external information. He or she can update the school list and add fund information to database.

With the help of searching and updates, the database becomes not only a storage of information, but also the tool to help people make decisions and get insight of the desired information. 

