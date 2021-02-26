from pydot import Dot, Node, Edge
from ...core.declarations.contract import Contract
from ...core.declarations.function import Function
from collections import defaultdict
# SPDX-License-Identifier: MIT
# PyDot useful links
# https://pythonhaven.wordpress.com/tag/pydot/
# https://www.programcreek.com/python/example/5579/pydot.Dot
# https://gist.github.com/aboSamoor/1140942
# https://stackoverflow.com/questions/606191/convert-bytes-to-a-string
# https://stackoverflow.com/questions/16671966/multiline-tooltip-for-pydot-graph

# def change_label(edge, svs):
#     sv_names = [sv.name for sv in svs]
#     old_label = edge.get_label()
#     labels = old_label.split(', ')
#     for i, label in enumerate(labels):
#         temp_label = label.strip()
#         if temp_label not in sv_names:
#             labels[i].replace(temp_label, f'<{temp_label}>')
#     new_label = ', '.join(labels)
#     edge.set_label(new_label)


def remove_edge(edge):
    edge.set('style', 'dashed')
    edge.set('color', 'red')
    edge.set('fontcolor', 'red')


class DependencyGraph:
    def __init__(self, _contract: Contract):
        """
        Takes a Contract object and constructs the DDG for it.

        *** To be completed
            Currently cannot detect indirect read.
            Indirect write can be detected.
        """
        self.contract = _contract
        self.node_dic = {}
        self.edge_dic = {}
        self.graph = Dot()

        for f in _contract.functions + _contract.constructor_as_list:
            if f.name in ['slitherConstructorVariables', 'slitherConstructorConstantVariables'] or not f.is_public_or_external:
                continue
            self.construct_node(f)

        self.construct_graph(_contract)

    @property
    def html(self):
        return svg_to_html(self.graph.create_svg().decode('utf-8'))

    def construct_graph(self, _contract):
        """
        Constructs the graph by connecting nodes with edges.
        """
        for f in _contract.functions + _contract.constructor_as_list:
            if f.name in ['slitherConstructorVariables', 'slitherConstructorConstantVariables'] or not f.is_public_or_external:
                continue

            for dependency in f.depends_on:
                written_f, sr = dependency[0], dependency[1]
                n1 = self.get_node(f.name)
                n2 = self.get_node(written_f.name)
                if self.edge_dic.get((n1, n2)):
                    e = self.edge_dic[(n1, n2)]
                    old_label = e.get_label()
                    e.set_label(f'{old_label.strip()}, {sr.name}        ')
                else:
                    self.construct_edge(n1, n2)
                    e = self.edge_dic[(n1, n2)]
                    e.set_label(f'{sr.name}        ')

    def update_graph(self):
        remaining_edges_dic = defaultdict(list)
        for f in self.contract.functions + self.contract.constructor_as_list:
            if f.name in ['slitherConstructorVariables', 'slitherConstructorConstantVariables'] or not f.is_public_or_external:
                continue

            for dependency in f.depends_on:
                written_f, sr = dependency[0], dependency[1]
                n1 = self.get_node(f.name)
                n2 = self.get_node(written_f.name)
                remaining_edges_dic[(n1, n2)].append(sr)

        existing_edges = self.edge_dic.keys()
        remaining_edges = remaining_edges_dic.keys()

        for ex_edge in existing_edges:
            if ex_edge not in remaining_edges:
                remove_edge(self.edge_dic[ex_edge])
            # no need to check if only one state variable dependency is remove
            # because if a dependency between two functions is removed
            # all of its dependency based on whatever variable will be removed.

    def construct_node(self, _function: Function):
        """
        Takes a Function object and constructs a Dot Node object for it.
        Adds the created object to the dictionary.

        Finished.
        """
        n = Node(_function.name)
        n.set_tooltip(construct_tooltip(_function))
        self.node_dic[_function.name] = n
        self.graph.add_node(n)

    def get_node(self, _name):
        return self.node_dic.get(_name)

    def construct_edge(self, _n1: Node, _n2: Node):
        """
        Takes two nodes
        n1 depends on n2
        n1 points to n2
        Constructs the edge object and adds it to the dictionary.

        Finished.
        """
        e = Edge(_n1, _n2, fontsize="8", fontcolor="#2E86C1", arrowsize="0.7")
        self.edge_dic[(_n1, _n2)] = e
        # e.set('color', 'green')
        self.graph.add_edge(e)


# utility functions

def construct_tooltip(_function: Function):
    """
    Takes a Function object and constructs the tooltip for it to be displayed in the DOT graph.

    Finished.
    """
    res = list()

    res.append('Function: ')
    res.append(f'\t{_function.signature}')

    res.append('---')
    res.append('Modifiers: ')
    for m in _function.modifiers:
        res.append(f'\t{m.signature}')

    res.append('---')
    res.append('Requires: ')
    for r in _function.requires:
        res.append(f'\t{r.code}')

    res.append('---')
    res.append('State Variables Read: ')
    for sv in _function.state_variables_read:
        res.append(f'\t{sv.name}({sv.type})')

    res.append('---')
    res.append('State Variables Written: ')
    for sv in _function.state_variables_written:
        res.append(f'\t{sv.name}({sv.type})')

    return '\n'.join(res)


def svg_to_html(_svg: str):
    """
    https://github.com/usyd-blockchain/vandal/blob/07ee51e86ddf6527c6bc39e6cd902b6cc9d6c346/src/exporter.py

    This function is mostly copied from Vandal.

    Finished.
    """
    lines = _svg.split("\n")
    page = list()

    page.append("""
              <html>
              <body>
              <style>
              .node
              {
                transition: all 0.05s ease-out;
              }
              .node:hover
              {
                stroke-width: 1.5;
                cursor:pointer
              }
              .node:hover
              ellipse
              {
                fill: #EEE;
              }
              textarea#infobox {
                position: fixed;
                display: block;
                top: 0;
                right: 0;
              }
              .dropbutton {
                padding: 10px;
                border: none;
              }
              .dropbutton:hover, .dropbutton:focus {
                background-color: #777777;
              }
              .dropdown {
                margin-right: 5px;
                position: fixed;
                top: 5px;
                right: 0px;
              }
              .dropdown-content {
                background-color: white;
                display: none;
                position: absolute;
                width: 70px;
                box-shadow: 0px 5px 10px 0px rgba(0,0,0,0.2);
                z-index: 1;
              }
              .dropdown-content a {
                color: black;
                padding: 8px 10px;
                text-decoration: none;
                font-size: 10px;
                display: block;
              }
              .dropdown-content a:hover { background-color: #f1f1f1; }
              .show { display:block; }
              </style>
              """)

    for line in lines[3:]:
        page.append(line)

    page.append("""<textarea id="infobox" disabled=true rows=40 cols=80></textarea>""")

    page.append("""<script>""")

    page.append("""
               // Set info textbox contents to the title of the given element, with line endings replaced suitably.
               function setInfoContents(element){
                   document.getElementById('infobox').value = element.getAttribute('xlink:title').replace(/\\\\n/g, '\\n');
               }
               // Make all node anchor tags in the svg clickable.
               for (var el of Array.from(document.querySelectorAll(".node a"))) {
                   el.setAttribute("onclick", "setInfoContents(this);");
               }
               const svg = document.querySelector('svg')
               const NS = "http://www.w3.org/2000/svg";
               const defs = document.createElementNS( NS, "defs" );
               // IIFE add filter to svg to allow shadows to be added to nodes within it
               (function(){
                 defs.innerHTML = makeShadowFilter()
                 svg.insertBefore(defs,svg.children[0])
               })()
               function colorToID(color){
                 return color.replace(/[^a-zA-Z0-9]/g,'_')
               }
               function makeShadowFilter({color = 'black',x = 0,y = 0, blur = 3} = {}){
                 return `
                 <filter id="filter_${colorToID(color)}" x="-40%" y="-40%" width="250%" height="250%">
                   <feGaussianBlur in="SourceAlpha" stdDeviation="${blur}"/>
                   <feOffset dx="${x}" dy="${y}" result="offsetblur"/>
                   <feFlood flood-color="${color}"/>
                   <feComposite in2="offsetblur" operator="in"/>
                   <feMerge>
                     <feMergeNode/>
                     <feMergeNode in="SourceGraphic"/>
                   </feMerge>
                 </filter>
                 `
               }
               // Shadow toggle functions, with filter caching
               function addShadow(el, {color = 'black', x = 0, y = 0, blur = 3}){
                 const id = colorToID(color);
                 if(!defs.querySelector(`#filter_${id}`)){
                   const d = document.createElementNS(NS, 'div');
                   d.innerHTML = makeShadowFilter({color, x, y, blur});
                   defs.appendChild(d.children[0]);
                 }
                 el.style.filter = `url(#filter_${id})`
               }
               function removeShadow(el){
                 el.style.filter = ''
               }
               function hash(n) {
                 var str = n + "rainbows" + n + "please" + n;
                 var hash = 0;
                 for (var i = 0; i < str.length; i++) {
                   hash = (((hash << 5) - hash) + str.charCodeAt(i)) | 0;
                 }
                 return hash > 0 ? hash : -hash;
               };
               function getColor(n, sat="80%", light="50%") {
                 const hue = hash(n) % 360;
                 return `hsl(${hue}, ${sat}, ${light})`;
               }
               // Add shadows to function body nodes, and highlight functions in the dropdown list
               function highlightFunction(i) {
                 for (var n of Array.from(document.querySelectorAll(".node ellipse"))) {
                   removeShadow(n);
                 }
                 highlight[i] = !highlight[i];
                 const entry = document.querySelector(`.dropdown-content a[id='f_${i}']`)
                 if (entry.style.backgroundColor) {
                   entry.style.backgroundColor = null;
                 } else {
                   entry.style.backgroundColor = getColor(i, "60%", "90%");
                 }
                 for (var j = 0; j < highlight.length; j++) {
                   if (highlight[j]) {
                     const col = getColor(j);
                     for (var id of func_map[j]) {
                       var n = document.querySelector(`.node[id='${id}'] ellipse`);
                       addShadow(n, {color:`${col}`});
                     }
                   }
                 }
               }
               // Show the dropdown elements when it's clicked.
               function showDropdown() {
                 document.getElementById("func-list").classList.toggle("show");
               }
               window.onclick = function(event) {
                 if (!event.target.matches('.dropbutton')) {
                   var items = Array.from(document.getElementsByClassName("dropdown-content"));
                   for (var item of items) {
                     item.classList.remove('show');
                   }
                 }
               }
              </script>
              </html>
              </body>
              """)

    return "\n".join(page)
