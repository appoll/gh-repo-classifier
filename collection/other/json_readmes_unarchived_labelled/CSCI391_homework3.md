# Joins

1.  How many rows would a two-table join produce if one table had
    50,000 rows and the other had 100,000?

2.  What type of join appears in the following select statement?

    select e.name, e.employee_id, ep.salary
    from employee_tbl e,
         employee_pay_tbl ep
    where e.employee_id = ep.employee_id;

1.  Will the following SELECT statements work?

    select name, employee_id, salary
    from employee_tbl e,
         employee_pay_tbl ep
    where employee_id = employee_id
      and name like '%MITH';

    select e.name, e.employee_id, ep.salary
    from employee_tbl e,
         employee_pay_tbl ep
    where name like '%MITH';

    select e.name, e.employee_id, ep.salary
    from employee_tbl e,
         employee_pay_tbl ep
    where e.employee_id = ep.employee_id
     and e.name like '%MITH';

1.  In the WHERE clause, when joining the tables, should you do the join first or the conditions?

1.  In joining tables are you limited to one-column joins, or can you join on more than one column?

2.  Rewrite the following query to make it more readable and shorter.

    select orders.orderedon, orders.name, part.partnum,
             part.price, part.description from orders, part
             where orders.partnum = part.partnum and orders.orderedon
            between '1-SEP-96' and '30-SEP-96'
            order by part.partnum;

# SUBQUERIES: The Embedded SELECT Statement

1.  Are the following statements true or false?

2.  The aggregate functions SUM, COUNT, MIN, MAX, and AVG all return multiple values.

3.  The maximum number of subqueries that can be nested is two.

4.  Correlated subqueries are completely self-contained.

1.  Will the following subqueries work using the ORDERS table and the PART table?

    SELECT *
      FROM PART;

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="right" />

<col  class="left" />

<col  class="right" />
</colgroup>
<thead>
<tr>
<th scope="col" class="right">PARTNUM</th>
<th scope="col" class="left">DESCRIPTION</th>
<th scope="col" class="right">PRICE</th>
</tr>
</thead>

<tbody>
<tr>
<td class="right">54</td>
<td class="left">PEDALS</td>
<td class="right">54.25</td>
</tr>


<tr>
<td class="right">42</td>
<td class="left">SEATS</td>
<td class="right">24.50</td>
</tr>


<tr>
<td class="right">46</td>
<td class="left">TIRES</td>
<td class="right">15.25</td>
</tr>


<tr>
<td class="right">23</td>
<td class="left">MOUNTAIN BIKE</td>
<td class="right">350.45</td>
</tr>


<tr>
<td class="right">76</td>
<td class="left">ROAD BIKE</td>
<td class="right">530.00</td>
</tr>


<tr>
<td class="right">10</td>
<td class="left">TANDEM</td>
<td class="right">1200.00</td>
</tr>
</tbody>
</table>

    SELECT *
     FROM ORDERS;

<table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


<colgroup>
<col  class="left" />

<col  class="left" />

<col  class="right" />

<col  class="right" />

<col  class="left" />
</colgroup>
<thead>
<tr>
<th scope="col" class="left">ORDEREDON</th>
<th scope="col" class="left">NAME</th>
<th scope="col" class="right">PARTNUM</th>
<th scope="col" class="right">QUANITY</th>
<th scope="col" class="left">REMARKS</th>
</tr>
</thead>

<tbody>
<tr>
<td class="left">15-MAY-96</td>
<td class="left">TRUE WHEEL</td>
<td class="right">23</td>
<td class="right">6</td>
<td class="left">PAID</td>
</tr>


<tr>
<td class="left">19-MAY-96</td>
<td class="left">TRUE WHEEL</td>
<td class="right">76</td>
<td class="right">3</td>
<td class="left">PAID</td>
</tr>


<tr>
<td class="left">2-SEP-96</td>
<td class="left">TRUE WHEEL</td>
<td class="right">10</td>
<td class="right">1</td>
<td class="left">PAID</td>
</tr>


<tr>
<td class="left">30-JUN-96</td>
<td class="left">BIKE SPEC</td>
<td class="right">54</td>
<td class="right">10</td>
<td class="left">PAID</td>
</tr>


<tr>
<td class="left">30-MAY-96</td>
<td class="left">BIKE SPEC</td>
<td class="right">10</td>
<td class="right">2</td>
<td class="left">PAID</td>
</tr>


<tr>
<td class="left">30-MAY-96</td>
<td class="left">BIKE SPEC</td>
<td class="right">23</td>
<td class="right">8</td>
<td class="left">PAID</td>
</tr>


<tr>
<td class="left">17-JAN-96</td>
<td class="left">BIKE SPEC</td>
<td class="right">76</td>
<td class="right">11</td>
<td class="left">PAID</td>
</tr>


<tr>
<td class="left">17-JAN-96</td>
<td class="left">LE SHOPPE</td>
<td class="right">76</td>
<td class="right">5</td>
<td class="left">PAID</td>
</tr>


<tr>
<td class="left">1-JUN-96</td>
<td class="left">LE SHOPPE</td>
<td class="right">10</td>
<td class="right">3</td>
<td class="left">PAID</td>
</tr>


<tr>
<td class="left">1-JUN-96</td>
<td class="left">AAA BIKE</td>
<td class="right">10</td>
<td class="right">1</td>
<td class="left">PAID</td>
</tr>


<tr>
<td class="left">1-JUN-96</td>
<td class="left">AAA BIKE</td>
<td class="right">76</td>
<td class="right">4</td>
<td class="left">PAID</td>
</tr>


<tr>
<td class="left">1-JUN-96</td>
<td class="left">AAA BIKE</td>
<td class="right">46</td>
<td class="right">14</td>
<td class="left">PAID</td>
</tr>


<tr>
<td class="left">11-JUL-96</td>
<td class="left">JACKS BIKE</td>
<td class="right">76</td>
<td class="right">14</td>
<td class="left">PAID</td>
</tr>
</tbody>
</table>

-   a.

    SELECT * FROM ORDERS
    WHERE PARTNUM =
    SELECT PARTNUM FROM PART
    WHERE DESCRIPTION = 'TRUE WHEEL';

-   b.

    SELECT PARTNUM
    FROM ORDERS
    WHERE PARTNUM =
    (SELECT * FROM PART
    WHERE DESCRIPTION = 'LE SHOPPE');

-   c.

    SELECT NAME, PARTNUM
    FROM ORDERS
    WHERE EXISTS
    (SELECT * FROM ORDERS
    WHERE NAME = 'TRUE WHEEL');

# Manipulating Data

1.  What is wrong with the following statement?

    DELETE COLLECTION;

1.  What is wrong with the following statement?

    INSERT INTO COLLECTION SELECT * FROM TABLE_2

1.  What is wrong with the following statement?

    UPDATE COLLECTION ("HONUS WAGNER CARD", 25000, "FOUND IT");

1.  What would happen if you issued the following statement?

    DELETE * FROM COLLECTION;

1.  What would happen if you issued the following statement?

    UPDATE COLLECTION
         SET WORTH = 555
         SET REMARKS = 'UP FROM 525';

1.  Will the following SQL statement work?

    INSERT INTO COLLECTION
        SET VALUES = 900
        WHERE ITEM = 'STRING';

1.  Will the following SQL statement work?

    UPDATE COLLECTION
    SET VALUES = 900
    WHERE ITEM = 'STRING';

1.  Try inserting values with incorrect data types into a table. Note
    the errors and then insert values with correct data types into the
    same table.

1.  Using your database system, try exporting a table (or an entire
    database) to some other format. Then import the data back into your
    database. Familiarize yourself with this capability. Also, export
    the tables to another database format if your DBMS supports this
    feature. Then use the other system to open these files and examine
    them.

# Creating and Maintaining Tables

1.  **True or False:** The ALTER DATABASE statement is often used to
    modify an existing table's structure.

2.  **True or False:** The DROP TABLE command is functionally equivalent
    to the DELETE FROM <table<sub>name</sub>> command.

3.  **True or False:** To add a new table to a database, use the CREATE TABLE command.

4.  What is wrong with the following statement?

    CREATE TABLE new_table (
    ID NUMBER,
    FIELD1 char(40),
    FIELD2 char(80),
    ID char(40);

1.  What is wrong with the following statement?

    ALTER DATABASE BILLS (
    COMPANY char(80));

1.  When a table is created, who is the owner?

1.  If data in a character column has varying lengths, what is the best choice for the data type?

2.  Add two tables to the BILLS database named BANK and ACCOUNT<sub>TYPE</sub>
    using any format you like. The BANK table should contain
    information about the BANK field used in the BANK<sub>ACCOUNTS</sub> table
    in the examples. The ACCOUNT<sub>TYPE</sub> table should contain information
    about the ACCOUNT<sub>TYPE</sub> field in the BANK<sub>ACCOUNTS</sub> table also. Try
    to reduce the data as much as possible.

You should use the CREATE TABLE command to make the tables. Possible
SQL statements would look like this:

    CREATE TABLE BANK
      ( ACCOUNT_ID    NUMBER(30)    NOT NULL,
        BANK_NAME     VARCHAR2(30)  NOT NULL,
        ST_ADDRESS    VARCHAR2(30)  NOT NULL,
        CITY          VARCHAR2(15)  NOT NULL,
        STATE         CHAR(2)       NOT NULL,
        ZIP           NUMBER(5)     NOT NULL;
    
     CREATE TABLE ACCOUNT_TYPE
      ( ACCOUNT_ID   NUMBER(30)    NOT NULL,
        SAVINGS      CHAR(30),
        CHECKING     CHAR(30);