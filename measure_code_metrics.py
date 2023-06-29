import os
import subprocess
import csv
import xml.etree.ElementTree as ET

def measure_dotnet_system(root_path, csv_file):
    # find all solutions with projects
    solutions = get_solution_paths(root_path)

    for solution_file in sorted(solutions):
        solution_dir, _ = get_solution_info(solution_file)
        arguments = ["/solution:" + solution_file, "/out:"+ solution_dir + "/tmp_report.xml"]
        subprocess.run(["C:/tools/Metrics/Metrics.exe"] + arguments, check=True)

    with open(csv_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Solution", "Assembly Name", "MaintainabilityIndex", "CyclomaticComplexity", "ClassCoupling",
                         "DepthOfInheritance", "SourceLines", "ExecutableLines", "Methods"])

        for solution_file in sorted(solutions):
            solution_dir, solution_name = get_solution_info(solution_file)
            write_code_metrics(solution_name, solution_dir + "/tmp_report.xml", writer)


    print(f"CSV file generated: {csv_file}")

def get_solution_info(solution_file):
    return (solution_file.rsplit('/', 1)[0], solution_file.rsplit('/', 2)[1])

        
def get_solution_paths(root_path):
    solutions = []
    print(root_path)
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith(".sln"):
                solutions.append(os.path.join(root, file).replace('\\', '/'))
    return solutions


def write_code_metrics(solution_name, xml_file, writer):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for assembly_elem in root.findall("./Targets/Target/Assembly"):
        assembly_name = assembly_elem.get("Name").split(',')[0]
        metrics = assembly_elem.find("Metrics")

        maintainability_index = metrics.find("Metric[@Name='MaintainabilityIndex']").get("Value")
        cyclomatic_complexity = metrics.find("Metric[@Name='CyclomaticComplexity']").get("Value")
        class_coupling = metrics.find("Metric[@Name='ClassCoupling']").get("Value")
        depth_of_inheritance = metrics.find("Metric[@Name='DepthOfInheritance']").get("Value")
        source_lines = metrics.find("Metric[@Name='SourceLines']").get("Value")
        executable_lines = metrics.find("Metric[@Name='ExecutableLines']").get("Value")
        member_count = len(list(assembly_elem.iter("Method")))  # Count the number of <Method> elements

        writer.writerow([solution_name, assembly_name, maintainability_index, cyclomatic_complexity, class_coupling,
                            depth_of_inheritance, source_lines, executable_lines, member_count])



# Example usage
root_path = "C:/Users/rolandgerm/projects/admiral/asw.betting.svc.engine"
root_path = "C:/Users/rolandgerm/projects/admiral/admiral.programengine"
root_path = "C:/Users/rolandgerm/projects/icagile-prg-archive/icagile-prg-admiral-2022/SupermarketReceipt-Refactoring-Kata/csharp"

root_path = "C:/Users/rolandgerm/projects/B_and_R/Subsystems"
csv_file = "csv_file.csv"
workspace = measure_dotnet_system(root_path, csv_file)
