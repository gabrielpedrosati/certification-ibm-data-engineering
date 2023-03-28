# Normalization, Keys and Constraints in Relational Database

## Introduction
In this project we will minimize data redundancy and inconsistency in a database by normalizing tables, uniquely identify a record in a table and establish relationship between tables.

## **Normalization**

### **First Normal Form (1NF)**
We will be working with the Bookshop table. The following image shows the Bookshop table:
!["Bookshop Table"](introduction-to-relational-databases/imgs/bookshop_table.png)

- Does the above table have unique rows? 
> Yes, it does.
- Does each cell of the above table have single/atomic values? 
> No, it doesn't. The columns AUTHOR_NAME and AUTHOR_ID contain multi valued cell.
- How can we normalize the table to ensure first normal form?
> To normalize this table, add an extra row, and split the multiple author names as well as multiple author IDs of the row containing multi-valued data into their own row.

The multi valued attribute after applying the 1st NF should look like this:
!["1FN"](/imgs/1FN.png)

### **Second Normal Form (2NF)**
By definition, a relation is in second form if it is already in 1NF and does not contain any partial dependencies. If you look at the BookShop table, you will find every column in the table is single or atomic valued, but it has multiple books by the same author.
As the number of rows in the table increase, you will be needlessly storing more and more occurences of these same pieces of information. And if the author updates their bio, you must update all of these occurences.

!["Bookshop Table 1FN"](/imgs/2FN.png)

So, we need to take the author information (AUTHOR_ID, AUTHOR_NAME, AUTHOR_BIO) out of the Bookshop table into another table, for example a table named BookShop_AuthorDetails. We then link each book in the BookShop table to the relevant row in the BookShop_AuthorDetails, using a unique common column such as AUTHOR_ID to link the tables.

Let's create the new table BookShop_AuthorDetails:

```
CREATE TABLE BookShop_AuthorDetails
AS (SELECT DISTINCT AUTHOR_ID, AUTHOR_NAME, AUTHOR_BIO FROM BookShop);
```

!["BookShop_AuthorDetails"](/imgs/bookshop_authordetails.png)

Now we can drop, the redundant author information related columns from the BookShop table.
```
ALTER TABLE BookShop
DROP COLUMN AUTHOR_BIO,
DROP COLUMN AUTHOR_NAME;
```
!["BookShop_DropColumn"](/imgs/bookshop_dropcolumn.png)

Now we are only storing the author information once per author and only have to update it in one place; reducing redundancy and increasing consistency of data. Thus 2NF is ensured.

## **Keys**

### **Primary Key**
Let's set the primary keys for our tables.

```
ALTER TABLE BookShop
ADD PRIMARY KEY (BOOK_ID);


ALTER TABLE BookShop_AuthorDetails
ADD PRIMARY KEY (AUTHOR_ID);
``` 
!["Book_PK"](/imgs/bookshop_pk.png)
!["Author_PK"](/imgs/author_pk.png)

### Foreign Key
A foreign key is a column that establishes a relationship between two tables.

```
ALTER TABLE BookShop
ADD CONSTRAINT fk_BookShop FOREIGN KEY (AUTHOR_ID) REFERENCES BookShop_AuthorDetails(AUTHOR_ID) 
ON UPDATE NO ACTION 
ON DELETE NO ACTION;
```

> Referential actions
> - ON UPDATE NO ACTION - it means that if any existing row is updated in the foreign key column of the referencing table (the table containing the foreign key), the update will only be allowed if the new value of the foreign key column exists in the referenced primary key column of the referenced table.
> - ON DELETE NO ACTION - means if any row in the referenced table (the table containing the primary key) is deleted, that row in the referenced table and the corresponding row in the referencing table (the table containing the foreign key) are not deleted.
> - More at: [FK Constraints](https://dev.mysql.com/doc/refman/8.0/en/create-table-foreign-keys.html)

Let's check our DDL:

![FK](/imgs/fk.png)

## **Constraints**

In this project, we implemented 3 types of constraint:
1. Entity Integrity Constraint
> The existence of a primary key in both the BookShop and BookShop_AuthorDetails tables satifies this integrity constraint because a primary key mandates **NOT NULL** constraint as well as ensuring that every row in the table has a value that uniquely denotes the row.
2. Referential Integrity Constraint:
> Referential Integrity ensures the existence of a referenced value if a value of one column of a table references a value of another column. The existence of the Foreign Key (AUTHOR_ID) in the BookShop table satisfies this integrity.
3. Domain Integrity Constraint:
> Domain Integrity ensures that the purpose of a column is clear and the values of a column are consistent as well as valid. The existence of data types, length, date format, check and null constraints make sure this integrity is satisfied.

![Constraints](/imgs/constraints.png)