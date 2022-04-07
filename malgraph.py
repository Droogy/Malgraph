#!/usr/bin/env python3
import pefile
import argparse
import networkx as nx
from networkx.drawing.nx_pydot import write_dot
import matplotlib.pyplot as plt

def main():
    '''
    Parse argument as filename, create dictionary with filename mapped to list-
    of imported functions, use dictionary to instantiate networkx graph and write-
    to .dot file 
    '''
    filename = parseArgs()
    print(f"\n[*] Filename: {filename}")
    getFunctions(filename)
    getSectionNames(filename)
    createGraph()

def createGraph():
    '''
    Generate .dot and .png files
    '''
    pe_graph = nx.Graph(fileAndFunctions)
    graphviz_graph = nx.nx_agraph.to_agraph(pe_graph)
    write_dot(pe_graph, "malgraph.dot")
    graphviz_graph.draw("malgraph.png", prog="fdp")
    print("[*] Created .dot and .png files\n")

def getFunctions(file):
    '''
    Instantiate dictionary that will hold 
    '''
    global fileAndFunctions
    fileAndFunctions = {}
    pe_file = pefile.PE(file)
    for entry in pe_file.DIRECTORY_ENTRY_IMPORT:
        fileAndFunctions.update({file: [function.name.decode() for function in entry.imports]})
    print("=" * 70)
    print(f"[*] Imported functions: \t{list(fileAndFunctions.values())}")

def getSectionNames(file):
    '''
    Get PE section names
    '''
    pe_file = pefile.PE(file)   # instantiate PE file object
    sections = [section.Name.decode().replace("\x00","") for section in pe_file.sections]
    print("=" * 70)
    print(
        "Section Name",
        "Virtual Address",
        "Virtual Size",
        "Raw Size",
        sep="\t"
    )
    for section in pe_file.sections:
        print(
            section.Name.decode(), 
            hex(section.VirtualAddress),
            section.Misc_VirtualSize, 
            section.SizeOfRawData,
            sep="\t\t"
        )
    fileAndFunctions[file].extend(sections) # extend method will append list

def parseArgs():
    '''
    Parse filename from --file argument
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("--file")
    args = parser.parse_args()
    return args.file

if __name__ == "__main__":
    main()