import enum


class Genre(enum.Enum):
    POP = 'POP',
    ELECTRONIC = 'ELECTRONIC',
    DANCE = 'DANCE',
    RAP = 'RAP',
    HIPHOP = 'HIPHOP',
    ROCK = 'ROCK',
    METAL = 'METAL',
    SOUL = 'SOUL',
    JAZZ = 'JAZZ',
    DISCO = 'DISCO',
    FUNK = 'FUNK',
    CLASSICAL = 'CLASSICAL',
    SOUNDTRACK = 'SOUNDTRACK',
    WORLD = 'WORLD',
    FOLK = 'FOLK',
    INDIE = 'INDIE',
    BROADWAY = 'BROADWAY',
    THEATER = 'THEATER',
    MUSICAL = 'MUSICAL',
    VINTAGE = 'VINTAGE',
    BALLAD = 'BALLAD',
    RETRO = 'RETRO',
    MEDITATION = 'MEDITATION',
    FAITH = 'FAITH'


def getListOfGenres():
    return [str(Genre.POP), str(Genre.ELECTRONIC), str(Genre.DANCE), str(Genre.RAP), str(Genre.HIPHOP), str(Genre.ROCK), str(Genre.METAL), str(Genre.SOUL), str(Genre.JAZZ), str(Genre.DISCO), str(Genre.FUNK), str(Genre.CLASSICAL), str(Genre.SOUNDTRACK), str(Genre.WORLD), str(Genre.FOLK), str(Genre.INDIE), str(Genre.BROADWAY), str(Genre.THEATER), str(Genre.MUSICAL), str(Genre.VINTAGE), str(Genre.BALLAD), str(Genre.RETRO), str(Genre.MEDITATION), str(Genre.FAITH)]
