import Tile
import random

class Map(object):
    def __init__(self, XSize, YSize, TerrainType, Game):
        self.MapSize = (YSize, XSize)
        self.MapMatrix = [[None for x in range (0,XSize)] for y in range(0,YSize)]
        self.TerrainType = TerrainType
        self.Game = Game

        '''
        Vähän ihmeellinen formaatti matriisille. Mutta y määrittelee mikä rivi on menossa, ja X siitä rivistä paikan.
        Eli on käytettävä käytännössä [Y,X]
        '''
        random.seed()
        for y in range(0,XSize):
            for x in range(0,YSize):
                '''
                Ei käytetä suoraa TileType = random.randint(0,3) koska näin saadaan painotettua
                kuinka todennäköisiä eri terrain tyypit on. Tää on aika karkee tapa tehä tämä.
                Tulevaisuudessa mahdollisesti implementoin map makerin jos aikaa.
                Tai joku tapa joten ruudut asetellaan järkevämmin.
                '''
                RandInt = random.randint(0,10)
                if RandInt <= 1:
                    TileType = 0
                elif 2 < RandInt <= 3:
                    TileType = 1
                elif 3 < RandInt <= 6:
                    TileType = 2
                else:
                    TileType = 3

                '''
                Terrain tyypit:
                0 = Impassable
                1 = Heavy
                2 = Light
                3 = Open
                '''
                self.MapMatrix[y][x] = Tile(TileType, self.TerrainType, y, x)

    def ReturnMap(self):
        return self.MapMatrix

    def ReturnTile(self, X, Y):
        return self.MapMatrix[Y][X]

    def ReturnTerrainType(self):
        return self.TerrainType