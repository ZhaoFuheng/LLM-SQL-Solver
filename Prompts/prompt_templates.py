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
'''


ExplainAndCompare = '''/* Given the following two SQL queries Q1 and Q2 */
Q1:{Q1}
Q2:{Q2}
/* And the following database schema: */
{schema}
/* Let's think step by step. Are Q1 and Q2 pragmatic equivalent?
1. Explain Q1 and Q2.
2. Do Q1 and Q2 have the same intention or share aligned logic? Write your answer using format decision = "equivalent" or decision = "inequivalent". Let's think step by step. 
*/
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


relax_static_prefix = '''/* some examples are provided */
/* Given the following two SQL examples */
example sql1: SELECT DISTINCT releaseType FROM torrents where groupName != 'Christmas'
example sql2: SELECT releaseType FROM torrents where groupName <> 'christmas'
/* Do they have the same intention or share aligned logic? */
The only differeences are distinct and Christmas v.s. christmas.
Because distinct and case sensitivity do not change the logic, they convey the same meaning.
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