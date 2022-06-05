from typing import Optional
import json
import chess.pgn

import openings


class MovesTreeNode :
    def __init__(self, move: str, game : Optional[chess.pgn.Game] = None, starting_node : bool = False ) :
        self.starting_node = starting_node
        self.move = move
        self.children = set()        
        self.games = set()
        if game is not None :
            self.games.add(game)
        self.parent = None
        self.props = {}
        self.moves = []
        if not starting_node : 
            self.moves = [self.move]

    def setParent(self, parent) :
        self.parent = parent
        self.moves = parent.moves + [self.move]

    def getChild(self, move: str) :
        for child in self.children :
            if child.move == move :
                return child
        return None

    def addProp(self, name, value) -> dict :
        self.props[name] = value
        return self.props


    def getStats(self) :
        nb, score  = 0, 0
        for game in self.games :
            nb += 1
            if game.headers['Result'] == '1-0' :
                score += 1
            elif game.headers['Result'] == '1/2-1/2' :
                score += 0.5
            elif game.headers['Result'] == '0-1' :
                score += 0
            else :
                raise Exception('Unkown score', game.headers)
        parent = self.parent
        while parent is not None and parent.parent is not None :
            parent = parent.parent
        nbtotal = len(parent.games) if parent is not None else len(self.games)
        return (score, nb, nbtotal)

    def getMovesAsStr(self) -> str :
        moves = []
        count = 1
        show_count = True
        for move in self.moves :
            if show_count :
                moves.append(f'{int(count)}.')
            moves.append(move)
            count += 0.5
            show_count = not show_count
        moves_str = " ".join(moves)
        moves_str = moves_str.replace('N','C').replace('R','T').replace('B','F').replace('K','R').replace('Q','D')
        return moves_str


    def getLabel(self) :
        (score, nb, nbtotal) = self.getStats()
        prefix = ''
        if len(self.moves) % 2 == 0:
            prefix = f'{int((len(self.moves)+1)/2)}. '
        return f'{prefix}{self.move} {score}/{nb}'

    def addChild(self, move: str, game: chess.pgn.Game) :
        self.games.add(game)
        child = self.getChild(move)
        if child is None :
            child = MovesTreeNode(move, game)
            child.setParent(self)
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
    def to_dict(self) :
        opening_book = openings.OpeningBook().get_openings()
        (score, ngames, nbtotal) = self.getStats()
        movesAsStr = self.getMovesAsStr()
        opening = opening_book.get(movesAsStr, None)
        mydict = {
            "name": self.getLabel(),
            "parent": self.parent.getLabel() if self.parent is not None else None,
            "ngames":ngames,
            "ratio": score/ngames if ngames > 0 else None,
            "nbtotal": nbtotal,
            "moves": self.getMovesAsStr()
        }
        if opening is not None : 
            mydict['opening'] = opening
        mydict.update(self.props)
        if len(self.games) > 1 or self.starting_node == True :
            mydict["children"] = [ child.to_dict() for child in self.children ]
        if len(self.games) == 1 :
            game = list(self.games)[0]
            mydict['url'] = game.headers['Site']
        return mydict

    def __str__(self) -> str :
        return json.dumps(self.to_dict(), indent = 4)