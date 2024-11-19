cot_prompt = '''/* Given the following two SQL queries Q1 and Q2 */
Q1:{Q1}
Q2:{Q2}
/* And the following database schema: */
{schema}
/* Are Q1 and Q2 sematically equivalent? Write your final answer using format decision = "equivalent" or decision = "inequivalent" */
/* Let's think step by step. */
'''


MiniatureAndMull = '''/* Given the following two SQL queries Q1 and Q2 */
Q1:{Q1}
Q2:{Q2}
/* And the following database schema: */
{schema}
/* Let's think step by step. Are Q1 and Q2 sematically equivalent?
1. Try one example database and check the output table of Q1 and Q2.
2. If the outputs are identical, can you modify the example database such that the outputs of Q1 and Q2 are not identical?
3. After evaluating whether there exists a database such Q1 and Q2 output different tables, write your answer using format decision = "equivalent" or decision = "inequivalent".
*/
1.
'''


ExplainAndCompare = '''/* Given the following two SQL queries Q1 and Q2 */
Q1:{Q1}
Q2:{Q2}
/* And the following database schema: */
{schema}
/* Let's think step by step. Are Q1 and Q2 pragmatic equivalent (with same intention)?
1. Explain Q1 and Q2.
2. Do Q1 and Q2 share aligned logic or Q1 and Q2 have significant differences? Write your answer using format decision = "equivalent" or decision = "inequivalent". Let's think step by step. 
*/
1.
'''


semantic_static_prefix = '''/* some examples are provided */
/* Given the following two SQL examples */
example sql1: select distinct T1.id from customer AS T1, customer AS T2 where T1.id = T2.id and T1.order_id = 1
example sql2: select distinct T1.id from customer AS T1, customer AS T2, customer AS T3 where T1.id = T2.id and T2.id = T3.id and T1.order_id = 1
/* Are they sematically equivalent? */
decision = "equivalent"

/* Given the following two SQL examples */
example sql1: select T1.avg_sale from singer AS T1
example sql2: select AVG(T1.sale) from singer AS T1
/* Are they sematically equivalent? */
decision = "inequivalent"

/* Given the following two SQL examples */
example sql1: SELECT * FROM emp WHERE sal = 3 AND comm = sal + 5
example sql2: SELECT * FROM emp WHERE sal = 3 AND comm = 8
/* Are they sematically equivalent? */
decision = "equivalent"

/* Given the following two SQL examples */
example sql1: select dept.name from dept where dept.id = 1
example sql2: select dept.name from dept where dept.id = 10
/* Are they sematically equivalent? */
decision = "inequivalent"

/* Given the following two SQL examples */
example sql1: SELECT dept.deptno FROM dept AS dept GROUP BY dept.deptno, dept.deptno
example sql2: SELECT dept.deptno FROM dept AS dept GROUP BY dept.deptno
/* Are they sematically equivalent? */
decision = "equivalent"
'''


relax_static_prefix = '''/* some examples are provided */
/* Given the following two SQL examples */
example sql1: SELECT DISTINCT releaseType FROM torrents where groupName != 'Christmas'
example sql2: SELECT releaseType FROM torrents where groupName <> 'christmas'
/* Do they have the same intention or share aligned logic? */
The only differeences are distinct and Christmas v.s. christmas.
Because distinct and case sensitivity do not change the logic, they have no significant difference and they convey the same meaning.
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