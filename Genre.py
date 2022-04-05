import enum


class Genre(enum.Enum):
    POP = 'POP',
    ELECTRONIC = 'ELECTRONIC',
    DANCE = 'DANCE',
    HOUSE = 'HOUSE',
    RAP = 'RAP',
    HIPHOP = 'HIPHOP',
    ROCK = 'ROCK',
    METAL = 'METAL',
    KPOP = 'K-POP',
    SOUL = 'SOUL',
    JAZZ = 'JAZZ',
    DISCO = 'DISCO',
    FUNK = 'FUNK',
    COUNTRY = 'COUNTRY',
    CLASSICAL = 'CLASSICAL',
    SOUNDTRACK = 'SOUNDTRACK',
    WORLD = 'WORLD',
    FOLK = 'FOLK',
    INDIE = 'INDIE',
    BROADWAY = 'BROADWAY',
    THEATER = 'THEATER',
    MUSICAL = 'MUSICAL',
    VINTAGE = 'VINTAGE',
    SWING = 'SWING',
    ELECTRO_SWING = 'ELECTRO SWING',
    BALLAD = 'BALLAD',
    RETRO = 'RETRO',
    DISNEY = 'DISNEY',
    MEDITATION = 'MEDITATION',
    FAITH = 'FAITH'


def getListOfGenres():
    return [str(Genre.POP), str(Genre.ELECTRONIC), str(Genre.DANCE), str(Genre.HOUSE), str(Genre.RAP), str(Genre.HIPHOP), str(Genre.ROCK), str(Genre.METAL), str(Genre.KPOP), str(Genre.SOUL), str(Genre.JAZZ), str(Genre.DISCO), str(Genre.FUNK), str(Genre.COUNTRY), str(Genre.CLASSICAL), str(Genre.SOUNDTRACK), str(Genre.WORLD), str(Genre.FOLK), str(Genre.INDIE), str(Genre.BROADWAY), str(Genre.THEATER), str(Genre.MUSICAL), str(Genre.VINTAGE), str(Genre.SWING), str(Genre.ELECTRO_SWING), str(Genre.BALLAD), str(Genre.RETRO), str(Genre.DISNEY), str(Genre.MEDITATION), str(Genre.FAITH)]
