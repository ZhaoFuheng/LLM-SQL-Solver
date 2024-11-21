cot_prompt = '''/* Given the following two SQL queries Q1 and Q2 */
Q1:{Q1}
Q2:{Q2}
/* And the following database schema: */
{schema}
Note: The SQL predicate is case-sensitive when comparing string values.
/* Are Q1 and Q2 semantically equivalent? Write your final answer using format decision = "equivalent" or decision = "inequivalent" */
/* Let's think step by step. */
'''


MiniatureAndMull = '''/* Given the following two SQL queries Q1 and Q2 */
Q1:{Q1}
Q2:{Q2}
/* And the following database schema: */
{schema}
/* Are Q1 and Q2 semantically equivalent?
1. Try one example database and check the output table of Q1 and Q2. Database is case-sensitive when comparing string values.
2. If the outputs are identical, adjust the database to see how output tables of Q1 and Q2 change.
3. After evaluating whether there exists a database such Q1 and Q2 output different tables, write your answer using format decision = "equivalent" or decision = "inequivalent".
*/
/* Let's think step by step. */
1. Consider the following example database instance, which is string value case-sensitive, and execute Q1 and Q2.
'''


ExplainAndCompare = '''/* Given the following two SQL queries Q1 and Q2 */
Q1:{Q1}
Q2:{Q2}
/* And the following database schema: */
{schema}
/* Let's think step by step. Are Q1 and Q2 pragmatic equivalent (with same intention)?
1. You can assume database contain no NULL values and is not case sensitive.
2. Explain Q1 and Q2 and understand their objective high-levely.
3. Do Q1 and Q2 share aligned logic or Q1 and Q2 have significant differences? Write your answer using format decision = "equivalent" or decision = "inequivalent". Let's think step by step. 
*/
1. Database contain no NULL values and is not case sensitive.
2. 
'''


semantic_static_prefix = '''/* some examples are provided */
/* Given the following two SQL examples */
example sql1: select distinct T1.id from customer AS T1, customer AS T2 where T1.id = T2.id and T1.order_id = 1
example sql2: select distinct T1.id from customer AS T1, customer AS T2, customer AS T3 where T1.id = T2.id and T2.id = T3.id and T1.order_id = 1
/* Are they semantically equivalent? */
decision = "equivalent"

/* Given the following two SQL examples */
example sql1: select T1.avg_sale from singer AS T1
example sql2: select AVG(T1.sale) from singer AS T1
/* Are they semantically equivalent? */
decision = "inequivalent"

/* Given the following two SQL examples */
example sql1: SELECT * FROM emp WHERE sal = 3 AND comm = sal + 5
example sql2: SELECT * FROM emp WHERE sal = 3 AND comm = 8
/* Are they semantically equivalent? */
decision = "equivalent"

/* Given the following two SQL examples */
example sql1: select dept.name from dept where dept.id = 1
example sql2: select dept.name from dept where dept.id = 10
/* Are they semantically equivalent? */
decision = "inequivalent"

/* Given the following two SQL examples */
example sql1: SELECT dept.deptno FROM dept AS dept GROUP BY dept.deptno, dept.deptno
example sql2: SELECT dept.deptno FROM dept AS dept GROUP BY dept.deptno
/* Are they semantically equivalent? */
decision = "equivalent"
'''


relax_static_prefix = '''/* some examples are provided */
/* Given the following two SQL examples */
example sql1: SELECT COUNT(DISTINCT Country) FROM countries
example sql2: SELECT COUNT(*) FROM countries
/* Do they have the same intention or share aligned logic? */
They are both determining how many rows in the countries table
decision = "equivalent"

/* Given the following two SQL examples */
example sql1: select player from football where player.id = 1
example sql2: select player from football where player.id = 1 and player.height > 100
/* Do they have the same intention or share aligned logic? */
They have different filter conditions and hence different meaning.
decision = "inequivalent"

/* Given the following two SQL examples */
example sql1: SELECT league_id FROM salary GROUP BY league_id ORDER BY SUM(salary) DESC LIMIT 1
example sql2: SELECT league_id FROM salary GROUP BY league_id ORDER BY AVG(salary) DESC LIMIT 1
/* Do they have the same intention or share aligned logic? */
They have different order by condition, but they are both ranking the players based on functions of salary.
They have closely aligned logic.
decision = "equivalent"

/* Given the following two SQL examples */
example sql1: select MAX(value) from order
example sql2: select MIN(value) from order
/* Do they have the same intention or share aligned logic? */
They are selecting the maxium or minimum value.
decision = "inequivalent"

/* Given the following two SQL examples */
example sql1: select birth_country from player, hall_of_fame where player.player_id = hall_of_fame.playerid and hall_of_fame.yearid>=1871
example sql2: select birth_city from player, hall_of_fame where player.player_id = hall_of_fame.playerid and hall_of_fame.yearid>=1871
/* Do they have the same intention or share aligned logic? */
One select birth country and the other select birth city. They are both considering the birth location.
decision = "equivalent"
'''