cot_prompt = '''/* Given the following two SQL queries Q1 and Q2 */
Q1:{Q1}
Q2:{Q2}
/* And the following database schema: */
{schema}
/* Let's think step by step. Are Q1 and Q2 sematically equivalent? */
/* Use the following format for the final answer: decision = "equivalent" or decision = "inequivalent" */
'''


MiniatureAndMull = '''/* Given the following two SQL queries Q1 and Q2 */
Q1:{Q1}
Q2:{Q2}
/* And the following database schema: */
{schema}
/* Let's think step by step. Are Q1 and Q2 sematically equivalent?
1. Try one example database and check the output table of Q1 and Q2.
2. If the outputs are identical, can you modify the example database such that the outputs of Q1 and Q2 are not identical?
3. After evaluating whether there exists a database such Q1 and Q2 output different tables, write your answer.
*/
/* Use the following format for the final answer: decision = "equivalent" or decision = "inequivalent" */
'''


ExplainAndCompare = '''/* Given the following two SQL queries Q1 and Q2 */
Q1:{Q1}
Q2:{Q2}
/* And the following database schema: */
{schema}
/* Let's think step by step. Are Q1 and Q2 equivalent?
1. Explain the logic of Q1 and Q2.
2. Write your answer.
*/
/* Use the following format for the final answer: decision = "equivalent" or decision = "inequivalent" */
'''


semantic_static_prefix = '''/* some examples are provided */
/* Given the following two SQL queries Q1 and Q2 */
Q1: select distinct table_1.x from r1 table_1, r2 table_2 where table_1.id = table_2.id and table_1.x = 1
Q2: select distinct table_1.x from r1 table_1, r1 table_2, r2 table_3 where table_1.x = table_2.x and table_1.id = table_3.id and table_1.x = 1
/* Are Q1 and Q2 sematically equivalent? */
decision = "equivalent"

/* Given the following two SQL queries Q1 and Q2 */
Q1: select table_1.x from r1 table_1
Q2: select table_1.id, table_1.x from r1 table_1
/* Are Q1 and Q2 sematically equivalent? */
decision = "inequivalent"

/* Given the following two SQL queries Q1 and Q2 */
Q1: SELECT x.a as a FROM x x, y y WHERE x.k = y.k
Q2: SELECT x1.a as a
      	  FROM (SELECT x.a as a, x.k as k FROM x x) x1, y y
	  WHERE x1.k = y.k
/* Are Q1 and Q2 sematically equivalent? */
decision = "equivalent"

/* Given the following two SQL queries Q1 and Q2 */
Q1: select r1.x from r1 table_1 where r1.table_id = 1
Q2: select r1.x from r1 table_1 where r1.table_id = 10
/* Are Q1 and Q2 sematically equivalent? */
decision = "inequivalent"

/* Given the following two SQL queries Q1 and Q2 */
Q1: select * from r x where x.id = 1
Q2: select * from (select * from r x where x.id = 1) y where y.id = 1
/* Are Q1 and Q2 sematically equivalent? */
decision = "equivalent"
'''


relax_static_prefix = '''
/* Given the following two SQL queries Q1 and Q2 */
Q1: select table_1.x from r1 table_1
Q2: select table_1.id, table_1.x from r1 table_1
/* Are Q1 and Q2 equivalent? */
decision = "equivalent"

/* Given the following two SQL queries Q1 and Q2 */
Q1: select table_1.x from r1 table_1 where r1.table_id = 1
Q2: select table_1.x from r1 table_1 where table_1.id = 10
/* Are Q1 and equivalent? */
decision = "inequivalent"

/* Given the following two SQL queries Q1 and Q2 */
Q1: select * from r x where x.id = 1
Q2: select * from (select * from r x where x.id = 1) y where y.id = 1
/* Are Q1 and Q2 equivalent? */
decision = "equivalent"

/* Given the following two SQL queries Q1 and Q2 */
Q1: select MAX(table_1.x) from r1 table_1
Q2: select MIN(table_1.x) from r1 table_1
/* Are Q1 and equivalent? */
decision = "inequivalent"

/* Given the following two SQL queries Q1 and Q2 */
Q1: select * from r x where x.id = 1
Q2: select * from (select * from r x where x.id = 1) y where y.id = 1
/* Are Q1 and Q2 equivalent? */
decision = "equivalent"
'''