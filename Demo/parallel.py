import concurrent.futures
import json  
from features import ( 
    LLM_decision, trustworthiness_all, title_trust_all, semantic,
    relevant_sent, calculate_quantity_score, temporal_similarity,
    calculate_quant_presence_score, calculate_quant_agreement,
    temp_agreement, temp_trust, sentence_contain_quant_tolerance
)

from gemini import (
    LLM_decision, trustworthiness_all, title_trust_all)


def read_input_file(file_path):
    with open(file_path, "r") as file:
        data = json.load(file) 
    return data


def get_function_args(input_data):
    return [
        (LLM_decision, (input_data[""],)),
        (trustworthiness_all, (input_data[""],)),
        (title_trust_all, (input_data[""],)),
        (semantic, (input_data[""],)),
        (relevant_sent, (input_data[""],)),
        (calculate_quantity_score, (input_data[""],)),
        (temporal_similarity, (input_data[""],)),
        (calculate_quant_presence_score, (input_data[""],)),
        (calculate_quant_agreement, (input_data[""],)),
        (temp_agreement, (input_data[""],)),
        (temp_trust, (input_data[""],)),
        (sentence_contain_quant_tolerance, (input_data[""],))
    ]


def execute_function(func_args):
    func, args = func_args
    return func(*args)  # Unpacking arguments


def main(input_file):
    input_data = read_input_file(input_file)
    func_args_list = get_function_args(input_data)

    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = list(executor.map(execute_function, func_args_list))


    for (func, _), result in zip(func_args_list, results):
        print(f"{func.__name__}: {result}")


if __name__ == "__main__":
    main("/home/user/Pictures/proofs.json")  # Change "input.json" to your actual file path

