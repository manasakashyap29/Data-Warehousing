##### 
## This section imports the necessary classes and methods from the SQLAlchemy library
####
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

######## IMPORTANT! Change this to your metric number for grading
student_no = 'A0178462W'
#########################

#####
## This section creates an engine for the PostgreSQL
## and creates a database session s.
#####
username = 'postgres'
password = 'postgres'
dbname = 'cs4221'
engine = create_engine('postgres://%s:%s@localhost:5432/%s' % (username, password, dbname))

Session = sessionmaker(bind=engine)
s = Session()

#####
## Query 
#####

query1 = """SELECT LO.LO_ORDERKEY, P.P_NAME,S.S_NAME,LO.LO_ORDERDATE,LO.LO_EXTENDEDPRICE
            FROM FACT_LINEORDER LO,DIM_SUPPLIER S,DIM_PART P,DIM_CUSTOMER C WHERE LO.LO_SUPPKEY = S.S_SUPPKEY  AND P.P_PARTKEY= LO.LO_PARTKEY AND LO.LO_CUSTKEY=C.C_CUSTKEY AND C.C_NAME = 'Customer#000000001' """

s.execute(query1)


query2 = """SELECT C.C_REGION,C.C_NATION,C.C_MKTSEGMENT,SUM(LO.LO_EXTENDEDPRICE) FROM FACT_LINEORDER LO, DIM_CUSTOMER C,DIM_PART P WHERE P.P_PARTKEY = LO.LO_PARTKEY AND C.C_CUSTKEY = LO.LO_CUSTKEY AND P_BRAND = 'Brand#13' GROUP BY CUBE(C.C_MKTSEGMENT,C.C_REGION,C.C_NATION);"""

s.execute(query2)

query3 = """SELECT D.d_month_actual,D.d_year_actual,COUNT(LO.LO_LINENUMBER),SUM(LO.LO_EXTENDEDPRICE),SUM(LO.LO_EXTENDEDPRICE * (1-LO.LO_DISCOUNT)), SUM(LO.LO_EXTENDEDPRICE *(1-LO.LO_DISCOUNT) *(1 +LO.LO_TAX)), AVG(LO.LO_QUANTITY), AVG(LO.LO_EXTENDEDPRICE),AVG(LO.LO_DISCOUNT) FROM FACT_LINEORDER LO, DIM_DATE D WHERE LO.LO_ORDERDATE = D.d_date_actual GROUP BY ROLLUP(D.d_year_actual,D.d_month_actual) ORDER BY (D.d_year_actual,D.d_month_actual) ASC;"""

s.execute(query3)


query4 = """SELECT O.O_ORDERPRIORITY, COUNT(*)  FROM ORDERS O
WHERE EXISTS (SELECT * FROM FACT_LINEORDER LO WHERE LO.LO_ORDERKEY = O.O_ORDERKEY AND LO.LO_COMMITDATE < LO.LO_RECEIPTDATE)
GROUP BY O.O_ORDERPRIORITY
ORDER BY O.O_ORDERPRIORITY;"""

s.execute(query4)

s.commit()





