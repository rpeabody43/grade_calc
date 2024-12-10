from math import floor, ceil
from statistics import fmean
import argparse
import json

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser("grade_calc")
    parser.add_argument(
        "filename", 
        help="The name of the json file with grade info",
        type=str
    )
    parser.add_argument(
        "--scaffold",
        help="Create a skeleton json file to fill in with your grade info",
        action="store_true"
    )
    return parser.parse_args()

def scaffold (filename: str):
    print('List each type of assignment in the class, seperated by commas:')
    print('e.g. homeworks, midterms, final')
    names = input().split(",")
    names = map(lambda x: x.strip(), names)
    template = {
        "weight": 0.0,
        "each": True,
        "grades": []
    }
    base = {name: template for name in names}
    if filename[-5:] != ".json":
        add_extension_yn = input(
            "The filename you provided does not end in .json, should .json be added? [y/n]: "
        ).lower()
        while add_extension_yn not in ['y', 'n']:
            add_extension_yn = input('Invalid: ').lower()

        if add_extension_yn == 'y':
            filename += ".json"
            
    print(f'Writing to \'{filename}\'')
    with open (filename, "w", encoding='utf-8') as f:
        json_string = json.dumps(base,
                      indent=4,
                      separators=(',', ': '), ensure_ascii=False)
        f.write(json_string)

def main ():
    args = parse_arguments()

    if args.scaffold:
        scaffold(args.filename)
        return
    
    grade_data = {}
    with open(args.filename, "r") as f:
        grade_data = json.load(f)

    sum = 0.0
    total_percent = 0.0
    max_name_len = 0
    for assignment_name, data in grade_data.items():
        grade_list = data["grades"]
        grade_avg = fmean(grade_list)
        weight = data["weight"]
        if data["each"]:
            weight *= len(grade_list)

        total_percent += weight
        percentage = grade_avg * weight
        sum += percentage
        grade_data[assignment_name]["assignment_avg"] = grade_avg
        
        if len(assignment_name) > max_name_len:
            max_name_len = len(assignment_name)

    if ceil(total_percent) != 1 and floor(total_percent) != 1:
        print(f"! WEIGHTS DO NOT ADD TO 100% ({total_percent*100}%) !")
        print("Double check the weights of each assignment group")
        print(ceil(total_percent))
        return

    print("Total")
    print("-----")
    print(f'{sum*100:.1f}%')
    print()
    print("Assignment breakdown")
    print("--------------------")

    for assignment_name, data in grade_data.items():
        weight = data["weight"]
        if data["each"]:
            weight *= len(data["grades"])
        avg = data["assignment_avg"]
        percent_fmt = f'{avg*100:.1f}%'
        print(
            f'{assignment_name:<{max_name_len}} | {percent_fmt:<6} * {weight*100:.0f}%'
        )

if __name__ == "__main__":
    main()
