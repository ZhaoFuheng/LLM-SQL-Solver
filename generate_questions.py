import argparse
import os
import sys
import json

from tqdm import tqdm
from Prompts.prompt_templates import cot_prompt, MiniatureAndMull, ExplainAndCompare, semantic_static_prefix, relax_static_prefix

if __name__ == '__main__':
    #argument template
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_files", nargs='+', default=[
                        "semantic_equivalent.jsonl", "semantic_inequivalent.jsonl", "relaxed.jsonl"],
                        help="List of data files to process")
    parser.add_argument("--fewshot", type=int, default=0)
    parser.add_argument("--output_dir", type=str, default="./questions",
                        help="Directory to save the output files")
    parser.add_argument("--prompt_template", type=str, default=[
                        "cot", "MiniatureAndMull", "ExplainAndCompare"])
    parser.add_argument("--tokenizer", type=str, default="gpt-3.5-turbo")

    args = parser.parse_args()


    prompt_template = None
    examples = ''
    if args.prompt_template == 'cot':
        prompt_template = cot_prompt
        examples = semantic_static_prefix
    elif args.prompt_template == 'MiniatureAndMull':
        prompt_template = MiniatureAndMull
        examples = semantic_static_prefix
    elif args.prompt_template == 'ExplainAndCompare':
        prompt_template = ExplainAndCompare
        examples = relax_static_prefix
    assert(args.fewshot <= 5 )
    assert prompt_template != None, print(args.prompt_template, type(prompt_template))
    example_list = examples.split('/* Given the following two SQL queries Q1 and Q2 */')
    examples = ''
    if args.fewshot > 0:
        examples = '/* Given the following two SQL queries Q1 and Q2 */'.join(example_list[:args.fewshot+1]) + '\n\n'


    os.makedirs(args.output_dir, exist_ok=True)

    # Open data files and read the file to fill up the argument
    for data_file in args.data_files:
        file_path = os.path.join("data", data_file)
        if not os.path.exists(file_path):
            print(f"File {file_path} does not exist. Skipping.")
            continue

        print(f"Processing {data_file}...")
        questions = []
        token_cnt = 0

        with open(file_path, 'r', encoding='utf-8') as f:
            for line in tqdm(f, desc=f"Processing {data_file}"):
                data_entry = json.loads(line.strip())


                schema = data_entry.get('schema', '')


                if 'semantic' in data_file:
                    sql1 = data_entry.get('sql1', '')
                    sql2 = data_entry.get('sql2', '')
                    semantic_equivalence = data_entry.get('semantic equivalence')
                    dbschema = data_entry.get('schema')
                    prompt_text = prompt_template.format(
                        Q1=sql1,
                        Q2=sql2,
                        schema=dbschema
                    )
                    prompt_text = examples + prompt_text

                    question = {
                        "prompt": prompt_text,
                        "sql1": sql1,
                        "sql2": sql2,
                        "semantic_equivalence": semantic_equivalence,
                    }

                elif 'relaxed' in data_file :
                    gold_sql = data_entry.get('gold_sql', '')
                    pred_sql = data_entry.get('pred_sql', '')
                    dbschema = data_entry.get('schema', '')
                    database = data_entry.get('database', '')
                    execution_match = data_entry.get('execution_match', '')
                    human_preference = data_entry.get('human_preference', '')


                    prompt_text = prompt_template.format(
                        Q1=gold_sql,
                        Q2=pred_sql,
                        schema=dbschema
                    )
                    prompt_text = examples + prompt_text

                    question = {
                        "prompt": prompt_text,
                        "gold_sql": gold_sql,
                        "pred_sql": pred_sql,
                        "database": database,
                        "execution_match": execution_match,
                        "human_preference": human_preference,
                    }

                else:
                    continue

                questions.append(question)
        fname = data_file.replace('.jsonl', '')
        output_file_name = f"{fname}_{args.prompt_template}_{args.fewshot}shot_questions.jsonl"
        output_file_path = os.path.join(args.output_dir, output_file_name)
        with open(output_file_path, 'w', encoding='utf-8') as f_out:
            for item in questions:
                json_line = json.dumps(item)
                f_out.write(json_line + "\n")