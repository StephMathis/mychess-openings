#! /usr/bin/env python3

from multiprocessing import set_forkserver_preload
import chess
import chess.pgn
import chess.engine

import os

import movestreenode

chess_user = 'metaheuristic'
moves_limit = 6
filename_games = '100games.txt'


moves_tree = movestreenode.MovesTreeNode("start", starting_node = True)
moves_tree.addProp("moves_limit", moves_limit)

dir_path = os.path.dirname(os.path.realpath(__file__))
project_dir = os.sep.join([dir_path, '..', '..'])

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

#print(moves_tree, flush=True)

javascript_tree = f'var treeData = [{moves_tree}];'

javascript_tree_file = open(os.sep.join([project_dir, 'srcs', 'html', 'mytreegames.js']), 'w')
print(javascript_tree, file=javascript_tree_file)
javascript_tree_file.close()
