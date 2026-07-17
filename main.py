# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

eve=pd.read_sql("""SELECT * FROM sqlite_master""", conn)
conn.commit()
print (eve)

df_bostons = pd.read_sql("""SELECT * FROM employees""",conn)
conn.commit()
print(df_bostons)

df_customers = pd.read_sql("""SELECT * FROM customers""",conn)
conn.commit()
print(df_customers)


df_orders = pd.read_sql("""SELECT * FROM orders""",conn)
conn.commit()
print(df_orders)

# STEP 1
# Replace None with your code
df_boston = pd.read_sql("""SELECT e.firstName, e.lastName
                        FROM employees e 
                        INNER JOIN offices o 
                        ON e.officeCode = o.officeCode
                        WHERE o.city = 'Boston'""", conn)
conn.commit()
print(df_boston)

# STEP 2
# Replace None with your code
df_zero_emp = pd.read_sql("""SELECT o.* FROM offices o
                          LEFT JOIN employees e 
                          ON o.officeCode = e.officeCode 
                          WHERE e.officeCode IS NULL""", conn)

conn.commit()
print(df_zero_emp)


# STEP 3
# Replace None with your code
df_employee = pd.read_sql("""SELECT e.firstName, e.lastName, o.city, o.state 
                          FROM employees e
                          LEFT JOIN offices o 
                          ON e.officeCode = o.officeCode 
                          ORDER BY e.firstName, e.lastName """, conn)
conn.commit()
print(df_employee)


# STEP 4
# Replace None with your code
df_contacts = pd.read_sql("""SELECT c.contactFirstName, c.contactLastName, c.phone, c.salesRepEmployeeNumber
                           FROM customers c
                           LEFT JOIN orders o  ON c.customerNumber = o.customerNumber 
                           WHERE o.customerNumber IS NULL
                           ORDER BY c.contactLastName ASC """, conn)
conn.commit()       
print (df_contacts)

# STEP 5
# Replace None with your code
df_payment = pd.read_sql("""SELECT c.contactFirstName, c.contactLastName, p.amount, p.paymentDate 
                         FROM customers c 
                         JOIN payments p ON c.customerNumber = p.customerNumber
                         ORDER BY c.contactFirstName DESC """, conn)
conn.commit()
print (df_payment)

# STEP 6
# Replace None with your code
df_credit = pd.read_sql("""SELECT e.employeeNumber, e.firstName, e.lastName ,COUNT(c.customerName) AS customer_num 
                        FROM employees e 
                        LEFT JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber 
                        GROUP BY e.employeeNumber, e.firstName, e.lastName 
                        HAVING AVG(c.creditLimit) > 90000
                        ORDER BY customer_num DESC""", conn)

conn.commit()
print(df_credit)

# STEP 7
# Replace None with your code
df_product_sold = pd.read_sql("""SELECT p.productCode, p.productName,  SUM(od.quantityOrdered) AS totalunits FROM orders o 
                              JOIN orderDetails od ON o.orderNumber = od.orderNumber
                              JOIN products p ON od.productcode = p.productCode
                              GROUP BY p.productCode, p.productName
                              ORDER BY totalunits DESC""", conn)
conn.commit()
print(df_product_sold)

# # STEP 8
# Replace None with your code
df_total_customers = pd.read_sql("""SELECT p.productCode, p.productName, COUNT(DISTINCT o.customerNumber) AS numpurchasers FROM products p
                              JOIN orderDetails od ON p.productCode = od.productCode
                              JOIN orders o ON o.orderNumber = od.orderNumber
                              GROUP BY p.productCode, p.productName
                              ORDER BY numpurchasers DESC """, conn)
conn.commit()
print(df_total_customers)

# STEP 9
# Replace None with your code
df_customers = pd.read_sql("""SELECT o.officeCode, o.city, COUNT(c.customerNumber) AS n_customers
                            FROM offices o
                            JOIN employees e ON o.officeCode = e.officeCode
                            JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
                            GROUP BY o.officeCode, o.city
                            """, conn)
conn.commit()
print(df_customers)

# # STEP 10
# Replace None with your code 
df_under_20 = pd.read_sql(""" SELECT e.employeeNumber, e.firstName, e.lastName, o.city, e.officeCode
                         FROM   employees e
                         JOIN offices o ON e.officeCode = o.officeCode
                         WHERE e.employeeNumber IN (
                            SELECT c.salesRepEmployeeNumber
                                FROM customers c
                                JOIN orders ord ON c.customerNumber = ord.customerNumber
                                JOIN orderDetails od ON ord.orderNumber = od.orderNumber
                                WHERE od.productCode IN (
                                     SELECT od2.productCode
                                     FROM orderDetails od2
                                     JOIN orders ord2 ON od2.orderNumber = ord2.orderNumber
                                     GROUP BY od2.productCode
                                     HAVING COUNT(DISTINCT ord2.customerNumber) < 20))
                           ORDER BY e.lastName ASC""", conn)
conn.commit()
print(df_under_20)
                        

conn.close()