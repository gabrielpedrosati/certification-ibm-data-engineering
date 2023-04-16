#

The cloud service provider has given us their billing data in the csv file `cloud-billing-dataset.csv`. This file contains the billing data for the past decade.

Here are the field wise details of the billing data.

| Field Name | Details |
| --- | --- |
customerid	| Id of the customer
category | Category of the customer. Example: Individual or Company
country	| Country of the customer
industry | Which domain/industry the customer belongs to. Example: Legal, Engineering
month | The billed month, stored as YYYY-MM. Example: 2009-01 refers to the month January in the year 2009
billedamount | Amount charged by the cloud services provided for that month in USD


We need to design a data warehouse that can support the queries listed below:
- average billing per customer
- billing by country
- top 10 customers
- top 10 countries
- billing by industry
- billing by category
- billing by year
- billing by month
- billing by quarter
- average billing per industry per month
- average billing per industry per quarter
- average billing per country per quarter
- average billing per country per industry per quarter

![CSV Rows](/Warehousing_and_BI_Tools/imgs/csv-rows.png)

## Design the fact tables

