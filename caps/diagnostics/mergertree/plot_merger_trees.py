#!/usr/bin/python

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

from math import fabs
import numpy as np
import pandas as pd

import caps.io.reader as db
from caps.util import utilities as ut

import pydot

simulation = "L500_NR_0"

mt = db.Simulation(simulation+"", db_dir = "/Users/Kaylea/Data/L500_NR_0")


clusters = mt.get_halo_ids(main_halos_only=True)
halos = mt.get_halo_properties(clusters, ["M_hc", "r_hc"], "1.0005")

for cluster in clusters:
    if cluster != 17:
        continue

    dot_object = pydot.Dot(graph_type='graph')
    dot_object.set_node_defaults(shape='circle',fontsize="14")
    dot_object.set_edge_defaults(arrowhead = "diamond")

    print cluster
    z0_mass = halos[halos["id"] == cluster]["M_hc"]
    z0_radius = halos[halos["id"] == cluster]["r_hc"]

    nodes = {}
    edges = []

    node_name = "1.0005_%d" % cluster
    nodes[node_name] = pydot.Node(name=node_name, style="bold", xlabel=str(cluster), label="", height="1")

    tree = mt.get_full_tree(cluster, get_main_line=True)

    edge_nodes = [node_name]
    for row, node in tree.iterrows() :
   

        ratio = node["r_hc"]/float(z0_radius)
        if ratio < 0.01 :
            continue
        #print "%0.4f_%d" % (node["aexp"], node["id"]), ratio, float(node["num_shared_particles"])/float(node["num_particles"])

        this_node_name = "%0.4f_%d" % (node["aexp"], node["id"])
        this_node_label = "%0.4f, %d" % (node["aexp"], node["id"])
        parent_node_name = "%0.4f_%d" % (node["parent_aexp"], node["parent_id"])
      #  print this_node_name

        skip = False
        #exclude very minor mergers from tree
        parent_node = tree[np.logical_and(tree["id"] == node["parent_id"],
                                 tree["aexp"] == node["parent_aexp"])].squeeze()

        #exclude minor mergers
        if isinstance(parent_node, pd.Series) and parent_node["is_main_line"] == 1 and node["is_main_line"] == 0:
            if float(node["M_hc"])/float(parent_node["M_hc"]) < 0.2 :
             #       print this_node_name, "skipped due to merger ratio"
                    continue

        #exclude poor matches
        if float(node["num_shared_particles"])/float(node["num_particles"]) < 0.01 :
           # print this_node_name, "skipped due to particle ratio"
            skip = True

        ratio = str(ratio)


        if parent_node_name in edge_nodes :

            if node["is_main_line"] == 0 and this_node_name not in nodes.keys():
                #nodes[this_node_name] = pydot.Node(name=this_node_name, xlabel=str(node["id"]), label="", height=ratio, width=ratio)
                nodes[this_node_name] = pydot.Node(name=this_node_name, label="", height=ratio, width=ratio)
            elif node["is_main_line"] == 1 :
                #nodes[this_node_name] = pydot.Node(name=this_node_name, xlabel=this_node_label, label="", height=ratio, width=ratio, style="bold")
                nodes[this_node_name] = pydot.Node(name=this_node_name, label="", height=ratio, width=ratio, style="bold")
 
            if not skip :

              #  print "not skipped", this_node_name
                edge_nodes.append(parent_node_name)
                edge_nodes.append(this_node_name)
                if node["is_main_line"] == 0 :
                    edges.append(pydot.Edge(nodes[parent_node_name], nodes[this_node_name], weight="1"))
                else :
                    edges.append(pydot.Edge(nodes[parent_node_name], nodes[this_node_name], style="bold", weight="10"))


    for node in nodes.values() :
        name = node.get_name().replace('"', '').strip()
        if name in edge_nodes :
            dot_object.add_node(node)
    for edge in edges :
        dot_object.add_edge(edge)

    dot_object.write_pdf('images/mergertree_'+str(cluster)+'.pdf')
   # plt.show()

mt.close()
