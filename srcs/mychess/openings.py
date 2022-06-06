import os

class OpeningBook :
    _opening_book = None
    def __init__(self) :
        pass

    def get_openings(self) -> dict[str, str] :
        if OpeningBook._opening_book is None :
            dir_path = os.path.dirname(os.path.realpath(__file__))
            project_dir = os.sep.join([dir_path, '..', '..','srcs','codes_eco','eco.fr.txt'])
            openings = {}
            with open(os.sep.join([project_dir])) as f:
                for line in f:
                    line = line.rstrip()
                    # line = "'C58' 'Défense des deux Cavaliers' 'Variante Bogolyubov ' 1. e4 e5 2. Cf3 Cc6 3. Fc4 Cf6 4. Cg5 d5 5. exd5 Ca5 6. Fb5+ c6 7. dxc6 bxc6 8. Df3"
                    opening = [ x.strip().encode('cp1252').decode('utf8') for x in line.split("'") if len(x.strip())>0 ]
                    # opening = ['C58', 'Défense des deux Cavaliers', 'Variante Bogolyubov', '1. e4 e5 2. Cf3 Cc6 3. Fc4 Cf6 4. Cg5 d5 5. exd5 Ca5 6. Fb5+ c6 7. dxc6 bxc6 8. Df3']
                    openings[opening[-1]] = ", ".join(opening[1:-1])
            OpeningBook._opening_book = openings
        return OpeningBook._opening_book
