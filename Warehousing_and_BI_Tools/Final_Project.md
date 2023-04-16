
## Create Table DimDate
CREATE TABLE DimDate (
    dateid INTEGER NOT NULL,
    date DATE NOT NULL,
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    quartername CHAR(2) NOT NULL,
    month INTEGER NOT NULL,
    monthname VARCHAR(10) NOT NULL,
    day INTEGER NOT NULL,
    weekday INTEGER NOT NULL,
    weekdayname VARCHAR(10) NOT NULL,
    PRIMARY KEY (dateid)
);

## Create Table DimTruck
CREATE TABLE DimTruck(
	truckid INTEGER NOT NULL,
	type VARCHAR(50) NOT NULL,
	PRIMARY KEY(truckid)
);

## Create Table DimStation
CREATE TABLE DimStation(
	stationid INTEGER NOT NULL,
	city VARCHAR(50) NOT NULL,
	PRIMARY KEY(stationid)
);

## Create Table FactTrips
CREATE TABLE FactTrips(
	tripid BIGINT NOT NULL,
	dateid INTEGER NOT NULL,
	stationid INTEGER NOT NULL,
	truckid INTEGER NOT NULL,
	wastecollected NUMERIC(10,2),
	PRIMARY KEY(tripid),
	FOREIGN KEY (dateid) REFERENCES DimDate (dateid),
	FOREIGN KEY (stationid) REFERENCES DimStation (stationid),
	FOREIGN KEY (truckid) REFERENCES DimTruck (truckid)
);

## Command
SET INTEGRITY FOR FACTTRIPS IMMEDIATE CHECKED

GROUPING SETS, CUBE, and ROLLUP allow us to easily create subtotals and grand totals in a variety of ways. All these operators are used along with the GROUP BY operator.

GROUPING SETS operator allows us to group data in a number of different ways in a single SELECT statement.

The ROLLUP operator is used to create subtotals and grand totals for a set of columns. The summarized totals are created based on the columns passed to the ROLLUP operator.

The CUBE operator produces subtotals and grand totals. In addition it produces subtotals and grand totals for every permutation of the columns provided to the CUBE operator.

## GROUPING SETS
SELECT 
	s.stationid,
	t.type,
	SUM(f.wastecollected)
FROM FactTrips f
LEFT JOIN DimStation s
ON f.stationid = s.stationid 
LEFT JOIN DimTruck t
ON f.truckid = t.truckid
GROUP BY GROUPING SETS(s.stationid, t.type);

## ROLLUP
SELECT d.year, s.city, s.stationid, SUM(f.wastecollected) as total_waste_collected
FROM FactTrips f
LEFT JOIN DimStation s
ON f.stationid = s.stationid 
LEFT JOIN DimTruck t
ON f.truckid = t.truckid
LEFT JOIN DimDate d
ON f.dateid = d.dateid
GROUP BY ROLLUP(d.year, s.city, s.stationid);

## CUBE
SELECT d.year, s.city, s.stationid, AVG(f.wastecollected) as AVG_waste_collected
FROM FactTrips f
LEFT JOIN DimStation s
ON f.stationid = s.stationid 
LEFT JOIN DimTruck t
ON f.truckid = t.truckid
LEFT JOIN DimDate d
ON f.dateid = d.dateid
GROUP BY CUBE(d.year, s.city, s.stationid);

## MQT (Materialized Query Tables)
CREATE TABLE max_waste_stats (city, stationid, trucktype, totalwastecollected) AS
  (select s.city, s.stationid, t.type, MAX(f.wastecollected)
from facttrips f
left join dimstation s
on f.stationid = s.stationid
left join dimtruck t
on f.truckid=t.truckid
group by s.city,s.stationid,t.type)
     DATA INITIALLY DEFERRED
     REFRESH DEFERRED
     MAINTAINED BY SYSTEM;

The settings

DATA INITIALLY DEFERRED
REFRESH DEFERRED
MAINTAINED BY SYSTEM
Simple mean that data is not initially populated into this MQT. Whenever the underlying data changes, the MQT does NOT automatically refresh. The MQT is system maintained and not user maintained.

Step 2: Populate/refresh data into the MQT.

Execute the sql statement below to populate the MQT countrystats

1
refresh table countrystats;
Copied!
The command above populates the MQT with relevant data.

Step 3: Query the MQT.

Once an MQT is refreshed, you can query it.

Execute the sql statement below to query the MQT countrystats.

1
select * from countrystats

### Refresh MQT
refresh table max_waste_stats;
