#! /usr/bin/env python3

from typing import Optional
import chess
import chess.pgn
import chess.engine

import os

chess_user = 'metaheuristic'
moves_limit = 3
filename_games = '100games.txt'

class MovesTreeNode :
    def __init__(self, move: str, game : Optional[chess.pgn.Game] = None) :
        self.move = move
        self.children = set()        
        self.games = set()
        if game is not None :
            self.games.add(game)
        self.parent = None

    def setParent(self, parent) :
        self.parent = parent

    def getChild(self, move: str) :
        for child in self.children :
            if child.move == move :
                return child
        return None

    def addChild(self, move: str, game: chess.pgn.Game) :
        child = self.getChild(move)
        if child is None :
            child = MovesTreeNode(move, game)
            child.setParent = self
            self.children.add(child)
        else : 
            child.games.add(game)
        return child

    """
    {
        "name": "Top Level",
        "parent": "null",
        "children": [
        {
            "name": "Level 2: A",
            "parent": "Top Level",
            "children": [
            {
                "name": "Son of A",
                "parent": "Level 2: A"
            },
            {
                "name": "Daughter of A",
                "parent": "Level 2: A"
            }
            ]
        },
        {
            "name": "Level 2: B",
            "parent": "Top Level"
        }
        ]
    }
    """

    def mystr(self, indent:str = " ") -> str :
        txt = f'{indent}{{\n'
        txt += f'{indent}{indent}"name":"{self.move}",\n'
        txt += f'{indent}{indent}"parent":'
        if self.parent is None :
            txt += f'null'
        else :
            txt += f'{self.parent.move}'
        if len(self.children) > 0 :
            txt += ",\n"
            txt += f'{indent}{indent}"children":[\n'
            txtchildren = [ child.mystr(indent + "  ") for child in self.children]
            txt += ','.join(txtchildren)
            txt += f'{indent}{indent}]\n'
        else :
            txt += "\n"
        txt += f'{indent}{indent}}}\n'
        return txt

    def __str__(self) -> str :
        return self.mystr()

moves_tree = MovesTreeNode("start")

dir_path = os.path.dirname(os.path.realpath(__file__))
project_dir = os.sep.join([dir_path, '..'])

#stockfish = os.sep.join([project_dir, 'stockfish_15_win_x64_avx2','stockfish_15_x64_avx2.exe'])
#engine = chess.engine.SimpleEngine.popen_uci(stockfish)

pgn_file = os.sep.join([project_dir,'games',filename_games])
with open(pgn_file) as pgn_games :
    for game in iter(lambda: chess.pgn.read_game(pgn_games), None):
        headers = game.headers
        if headers['White'] != chess_user :
            continue
        board = chess.Board()
        current_node = moves_tree
        move_count = 0
        for move in game.mainline_moves() :
            move_count += 1
            if move_count/2 >= moves_limit :
                break
            move_str = board.san(move)
            board.push(move)
            current_node = current_node.addChild(move_str, game)
print(moves_tree)

html_txt = open(os.sep.join([dir_path, 'template_opening_tree.html'])).read()

html_txt = html_txt.replace('{MYOPENINGTREE}', str(moves_tree))
with open(os.sep.join([dir_path, 'opening_tree.html']),'w') as tree_html_file :
    print(html_txt, file = tree_html_file)