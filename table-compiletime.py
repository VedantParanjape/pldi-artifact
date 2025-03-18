import argparse

parser = argparse.ArgumentParser(description="Generate csv tables and plots from benchmark results.")
parser.add_argument("filepath", type=str, help="Path to the input CSV file (semicolon-separated).")
args = parser.parse_args()

file = open(args.filepath, mode ='r')
filew = open("results/compiletime-stats-table3.csv", "w+")

benchmark_tags = []

for line in file.readlines():
    if "[2/6] Compiling" in line:
        break
    if "Compiling" in line:
        benchmark_tags.append(line.strip())
    elif "codegen...done!" in line:
        benchmark_tags.append(line.strip())
    elif "MergeLUTs" in line:
        benchmark_tags.append(line.strip())

# for i in benchmark_tags:
#     print(i)

mlir_compile_time = []

for i in range(0, len(benchmark_tags), 4):
    if "unopt" in benchmark_tags[i]:
        mlir_compile_time.append([benchmark_tags[i].split(" ")[1].split("...")[0], int(benchmark_tags[i].split("(")[1].split(" ")[0]), 0.0])
    
    if "opt" in benchmark_tags[i+1] and "codegen...done" in benchmark_tags[i+3]:
        mlir_compile_time.append([benchmark_tags[i+1].split(" ")[1].split("...")[0], int(benchmark_tags[i+3].split("(")[1].split(" ")[0]), float(benchmark_tags[i+2].split(" ")[0])])

# print("mlir compile time")
# for i in mlir_compile_time:
#     print(i)

benchmark_tags_part_2 = []
part2 = False
file.seek(0)
for line in file.readlines():
    if "[2/6] Compiling" in line:
        part2 = True

    if part2 and "opt:runtime" in line:
        benchmark_tags_part_2.append(line.strip())

# print("bmk tags")
# for i in benchmark_tags_part_2:
#     print(i)

fhe_compile_time = []

for i in benchmark_tags_part_2:
    temp = i.split(":")
    fhe_compile_time.append([temp[0]+"."+temp[1], float(temp[3])])

# print("fhe compile time")
# for i in fhe_compile_time:
#     print(i)

final_result = []
for i in range(0, len(fhe_compile_time), 2):
    # if fhe_compile_time
    cols = []
    # print(f"debug: {mlir_compile_time[i]}")
    cols.append(mlir_compile_time[i][0].split(".")[0])
    cols.append(mlir_compile_time[i][1])
    cols.append(fhe_compile_time[i][1])
    cols.append(cols[1]+cols[2])

    cols.append(mlir_compile_time[i+1][2])
    cols.append(mlir_compile_time[i+1][1])
    cols.append(fhe_compile_time[i+1][1])
    cols.append(cols[5]+cols[6])

    csv_row = ""
    for row in cols:
        if type(row) is not str:
            csv_row = csv_row + str(round(row, 2)) + ","
        else:
            csv_row = csv_row + row + ","
    csv_row = csv_row.removesuffix(",")
    final_result.append(csv_row + "\n")

filew.write("benchmark,umlir,ufhe,utotal,solver,mlir,fhe,total\n")
for i in final_result:
    filew.write(i)
