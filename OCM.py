# -*- coding: utf-8 -*-
# Don't touch this stuff
import os, operator, time, sys, datetime, re
import requests
import random
from dotenv import load_dotenv
from plexapi.server import PlexServer
from datetime import date
load_dotenv(verbose=True)

# Don't touch anything above this. Set your script configuration below.

PLAYLIST_TITLE = 'Open Swim' # What do you want your playlist to be called?

# Next episodes set up
# Next episodes are tv shows you want to watch in season order. The script will find the next episode of each TV show in the next episode group and include them in the playlist.
NEXT_EPISODES_ACTIVE = 1 # Set NEXT_EPISODES_ACTIVE to 0 to enable this feature. Set NEXT_EPISODES_ACTIVE to 1 to disable this feature.
NEXT_EPISODES_LIBRARY_TITLE = 'TV Shows'
NEXT_EPISODES_COLLECTION_TITLE = 'Next Episodes' # This should be the name of the collection used for television shows you only want to see the next episode from.

# Reruns set up 
# Reruns are TV shows you want to watch in any order.  The script will find random episodes of each TV show in the rerun group and include them in the playlist.
RERUNS_ACTIVE = 1 # Set RERUNS_ACTIVE to 0 to enable this feature. Set RERUNS_ACTIVE to 1 to disable this feature.
RERUNS_LIBRARY_TITLE = 'TV Shows'
RERUNS_COLLECTION_TITLE = 'Reruns' # This should be the name of the collection used for the television shows you want to see reruns of. If you don't want to include reruns, use '' here.
RERUNS_LOOKBACK = 365 # Number of days before replaying an episode of television. If none are found within this lookback, it will be ignored.
RERUNS_MAXIMUM = 6 # Maximum number of reruns allowed within the playlist. Set to the same number as minimum to always include that many. Set to 999 or any number greater than the number of shows in your reruns collection to include an episode of every show. If this number is greater than the number of shows associated with the reruns collection, you may encounter errors.
RERUNS_MINIMUM = 1 # Minimum number of reruns allowed within the playlist. Set to the same number as maximum to always include that many. Set to 999 or any number greater than the number of shows in your reruns collection to include an episode of every show. If this number is greater than the number of shows associated with the reruns collection, you may encounter errors.
RERUNS_EPISODES_PER_SHOW = 1 # Number of episodes for each show to include.

# Promos set up
# Promos are a catch all for bumpers, interstitials, and so on--any media you want to play between episodes. A random number between the range defined by PROMO_MINIMUM_BW_EPISODES and PROMO_MAXIMUM_BW_EPISODES will be selected and placed between episodes.
PROMO_ACTIVE = 1 # Set PROMO_ACTIVE to 0 to enable this feature. Set PROMO_ACTIVE to 1 to disable this feature.
PROMO_LIBRARY_TITLE = 'Promos'
PROMO_COLLECTION_TITLE = 'Promos'
PROMO_LOOKBACK = 180 # Number of days before replaying a promo. If none are found within this lookback, it will be ignored.
PROMO_MINIMUM_BW_EPISODES = 1 # Minimum number of promos to play between episodes. Set to the same number as maximum to always include that many.
PROMO_MAXIMUM_BW_EPISODES = 3 # Maximum number of promos to play between episodes. Set to the same number as minimum to always include that many.

# Bumpers set up
# Bumpers are a special kind of promo you want to play directly before or after episodes of TV shows.  Exactly one will be randomly selected and placed directly before and after each episode. You can use promos in conjunctions with bumpers if you wish.
BUMPER_ACTIVE = 1 # Set BUMPER_ACTIVE to 0 to enable this feature. Set BUMPER_ACTIVE to 1 to disable this feature.
BUMPER_LIBRARY_TITLE = 'Promos'
BUMPER_COLLECTION_TITLE = 'Bumpers'
BUMPER_LOOKBACK = 365 # Number of days before replaying a bumper. If none are found within this lookback, it will be ignored.
BUMPER_BEFORE = 0 # Set BUMPER_BEFORE to to 0 place a bumper before every episode. Set BUMPER_BEFORE to 1 to disable this feature. If both BUMPER_BEFORE and BUMPER_AFTER are set to 0, then a bumper will be placed on both sides.
BUMPER_AFTER = 0 # Set BUMPER_AFTER to 0 to place a bumper after every episode. Set BUMPER_AFTER to 1 to disable this feature. If both BUMPER_BEFORE and BUMPER_AFTER are set to 0, then a bumper will be placed on both sides.

# Block preroll set up
# Block preroll are a special kind of promo you want to play at the beginning of your playlsit.  Exactly one will be randomly selected and placed directly at the start of the playlist.
BLOCK_PREROLL_ACTIVE = 1 # Set BLOCK_PREROLL_ACTIVE to 0 to enable this feature. Set BLOCK_PREROLL_ACTIVE to 1 to disable this feature.
BLOCK_PREROLL_LIBRARY_TITLE = 'Promos'
BLOCK_PREROLL_COLLECTION_TITLE = 'Block Preroll'
BLOCK_PREROLL_LOOKBACK = 365 # Number of days before replaying a block preroll. If none are found within this lookback, it will be ignored.

# Movie set up 
MOVIE_ACTIVE = 0 # Set MOVIE_ACTIVE to 0 to enable this feature. Set MOVIE_ACTIVE to 1 to disable this feature. If movies are disabled, all the features below are also disabled.
MOVIE_LIBRARY_TITLE = 'Movies'
MOVIE_COLLECTION_TITLE = 'Open Swim'
MOVIE_LOOKBACK = 365 # Number of days before showing a movie again. If none are found within this lookback, it will be ignored.
MOVIE_MINIMUM = 1 # Minimum number of movies to play in block. Set to the same number as maximum to always include that many.
MOVIE_MAXIMUM = 3 # Maximum number of movies to play in block. Set to the same number as minimum to always include that many.

# Movie prerolls are a special kind of promo (think: "And Now Your Feature Presentation"/theater prerolls) that will play directly before a movie. One will be randomly pulled from the preroll collection defined below. They can be stored in the same library as your promos library, or their own library. Set PREROLL_ACTIVE to 1 to disable this feature.
MOVIE_PREROLL_ACTIVE = 1 # Set PREROLL_ACTIVE to 0 to enable this feature. Set PREROLL_ACTIVE to 1 to disable this feature.
MOVIE_PREROLL_LIBRARY_TITLE = 'Promos'
MOVIE_PREROLL_COLLECTION_TITLE = 'Movie Preroll'
MOVIE_PREROLL_LOOKBACK = 14 # Number of days before showing a preroll again. Set to 0 to remove the lookback. 

# Preshow cartoons are a special kind of promo that will play directly before a movie. One preshow cartoon will be randomly pulled from the preroll collection defined below. They can be stored in the same library as your promos library, or their own library. Set PREROLL_ACTIVE to 1 to disable this feature.
PRESHOW_CARTOON_ACTIVE = 0 # Set PRESHOW_CARTOON_ACTIVE to 0 to enable this feature. Set PRESHOW_CARTOON_ACTIVE to 1 to disable this feature.
PRESHOW_CARTOON_LIBRARY_TITLE = 'TV Shows'
PRESHOW_CARTOON_COLLECTION_TITLE = 'Preshow Cartoon'
PRESHOW_CARTOON_LOOKBACK = 365 # Number of days before showing a preroll again. If none are found within this lookback, it will be ignored.

# Trailers are a special kind of promo that will play before a movie. Trailers will play before the preroll if prerolls are active, and right before the cartoon if cartoons are active. They will be randomly pulled from the trailer collection defined below. They can be stored in the same library as your promos library, or their own library. Set TRAILER_ACTIVE to 1 to disable this feature.
TRAILER_ACTIVE = 0 # Set PREROLL_ACTIVE to 0 to enable this feature. Set PREROLL_ACTIVE to 1 to disable this feature.
TRAILER_LIBRARY_TITLE = 'Promos'
TRAILER_COLLECTION_TITLE = 'Trailers'
TRAILER_LOOKBACK = 180 # Number of days before showing a trailer again. If none are found within this lookback, it will be ignored.
TRAILER_MINIMUM = 2 # Minimum number of traiilers to play before a movie. Set to the same number as maximum to always include that many.
TRAILER_MAXIMUM = 3 # Maximum number of trailers to play before a movie. Set to the same number as minimum to always include that many.

# Don't touch anything underneath this. Set your script configuration above

if NEXT_EPISODES_ACTIVE == RERUNS_ACTIVE == PROMO_ACTIVE == BUMPER_ACTIVE == MOVIE_ACTIVE == PREROLL_ACTIVE == TRAILER_ACTIVE == PRESHOW_CARTOON_ACTIVE == BLOCK_PREROLL_ACTIVE == 1:
    print("No collections are active. Review the '_ACTIVE' options in your script configuration.")
    quit()

baseurl = os.environ['PLEX_URL']
token = os.environ['PLEX_TOKEN']
plex = PlexServer(baseurl, token)
TODAY = date.today()



for playlist in plex.playlists(): # If the playlist already exists, remove all episodes from it.
    removelist = []
    if playlist.title == PLAYLIST_TITLE:
        originalplaylistitems = plex.playlist(PLAYLIST_TITLE).items()
        originalplaylist = plex.playlist(PLAYLIST_TITLE)
        for i in originalplaylistitems:
            removelist.append(i)
        for i  in removelist:
            originalplaylist.removeItem(i)

# Required variables for the rest of the script

playlist_list = []
episodes_list = []
EpisodesInPlaylistYN = []

# Check if any lists are empty—this will cause errors and must be fixed before running
if NEXT_EPISODES_ACTIVE == 0:
    NextEpisodes = plex.library.section(NEXT_EPISODES_LIBRARY_TITLE)
    episodes_list = []
    if not NextEpisodes.search(collection=NEXT_EPISODES_COLLECTION_TITLE):
        print("No episodes found in",NEXT_EPISODES_COLLECTION_TITLE,"collection. Please check configuration or turn off this feature by changing NEXT_EPISODES_ACTIVE to 1.")
        quit()
if RERUNS_ACTIVE == 0:
    Reruns = plex.library.section(RERUNS_LIBRARY_TITLE)
    episodes_list = []
    if not Reruns.search(collection=RERUNS_COLLECTION_TITLE):
        print("No episodes found in",RERUNS_COLLECTION_TITLE,"collection. Please check configuration or turn off this feature by changing RERUNS_ACTIVE to 1.")
        quit()
if PROMO_ACTIVE == 0:
    Promos = plex.library.section(PROMO_LIBRARY_TITLE)
    promos_list = []
    if not Promos.search(collection=PROMO_COLLECTION_TITLE):
        print("No promos found in",PROMO_COLLECTION_TITLE,"collection. Please check configuration or turn off this feature by changing PROMO_ACTIVE to 1.")
        quit()
if BUMPER_ACTIVE == 0:
    Bumpers = plex.library.section(BUMPER_LIBRARY_TITLE)
    if not Bumpers.search(collection=BUMPER_COLLECTION_TITLE):
        print("No bumpers found in",BUMPER_COLLECTION_TITLE,"collection. Please check configuration or turn off this feature by changing BUMPER_ACTIVE to 1.")
        quit()
if BLOCK_PREROLL_ACTIVE == 0:
    BlockPrerolls = plex.library.section(BUMPER_LIBRARY_TITLE)
    if not BlockPrerolls.search(collection=BLOCK_PREROLL_COLLECTION_TITLE):
        print("No block prerolls found in",BLOCK_PREROLL_COLLECTION_TITLE,"collection. Please check configuration or turn off this feature by changing BLOCK_PREROLL_ACTIVE to 1.")
        quit()
if MOVIE_ACTIVE == 0:
    Movies = plex.library.section(MOVIE_LIBRARY_TITLE)
    movies_list = []
    if not Movies.search(collection=MOVIE_COLLECTION_TITLE): 
        print("No movies found in",MOVIE_COLLECTION_TITLE,"collection. Please check configuration or turn off this feature by changing MOVIE_ACTIVE to 1.")
        quit()
    if PRESHOW_CARTOON_ACTIVE == 0:
         preshowcartoon_list = []
         PreshowCartoon = plex.library.section(PRESHOW_CARTOON_LIBRARY_TITLE)
         if not PreshowCartoon.search(collection=PRESHOW_CARTOON_COLLECTION_TITLE): 
            print("No preshow cartoons found in",PRESHOW_CARTOON_COLLECTION_TITLE,"collection. Please check configuration or turn off this feature by changing PRESHOW_CARTOON_ACTIVE to 1.")
            quit()   
    if MOVIE_PREROLL_ACTIVE == 0:
        MoviePrerolls = plex.library.section(MOVIE_PREROLL_LIBRARY_TITLE)
        movie_prerolls_list = []
        if not MoviePrerolls.search(collection=MOVIE_PREROLL_COLLECTION_TITLE): 
            print("No movie prerolls found in",MOVIE_PREROLL_COLLECTION_TITLE,"collection. Please check configuration or turn off this feature by changing MOVIE_PREROLL_ACTIVE to 1.")
            quit()
    if TRAILER_ACTIVE == 0:
        trailers_list = []
        Trailers = plex.library.section(TRAILER_LIBRARY_TITLE)
        if not Trailers.search(collection=TRAILER_LIBRARY_TITLE):
            print("No trailers found in",TRAILER_COLLECTION_TITLE,"collection. Please check configuration or turn off this feature by changing TRAILER_ACTIVE to 1.")
            quit()

# Collect media
if NEXT_EPISODES_ACTIVE == 0: # Collect all next episodes for the playlist.
    EpisodesInPlaylistYN = 0
    print("Collecting next episodes... Next episodes will come from the shows below.")
    for tv_show in NextEpisodes.search(collection=NEXT_EPISODES_COLLECTION_TITLE): # Add next episodes to episode list
        print(tv_show)
        for episode in tv_show.episodes():
            if episode.seasonNumber > 0: # Excludes specials from the next episode list
                if not episode.isWatched:
                    episodes_list += episode
                    break
    if len(episodes_list) == 0: # Check if next episodes added any media
        if RERUNS_ACTIVE == 0:
            print("No next episodes found. Please add media to the next episodes library/collection. Will proceed by checking for reruns.")
        else:
            if MOVIE_ACTIVE == 0:
                print("No next episodes found. Please add media to the next episodes library/collection. Since reruns are disabled, will proceed by adding films.")
            else:
                print("No next episodes found. Please add media to the next episodes library/collection. Since the reruns and movies functions are both disabled, quitting script.")
                quit()
if RERUNS_ACTIVE == 0: # Collect reruns
# Reruns will first select a random season to pull all episodes from. All episodes from that season will be added to the first selection pool. Then, random episodes will be added from those seasons to a secondary selection pool, so each tv show has an equal number of reruns in the pool. Finally, the script will pull from the secondary selection pool into the playlist.
    EpisodesInPlaylistYN = 0
    print("Collecting reruns... Reruns will come from the shows below.")
    RandomSeason = 0
    reruns_list = []
    for tv_show in Reruns.search(collection=RERUNS_COLLECTION_TITLE): # Add reruns to episode list
        print(tv_show,"has",tv_show.childCount,"seasons.")
        reruns_seasons_list = []
        for i in range(RERUNS_MINIMUM, RERUNS_MAXIMUM):
            RandomSeason = random.randint(1,tv_show.childCount) # First, select a random season to pull from
            print("Selecting reruns from episode from",tv_show,"season",RandomSeason)
            try:
                for episode in tv_show.season(RandomSeason):
                    if not episode.lastViewedAt: # If episode has not been viewed before, add to reruns list
                        reruns_seasons_list += episode
                    else:
                        days_since_played = (TODAY - episode.lastViewedAt.date()).days # If episode has not been viewed before, add to reruns list
                        if days_since_played > RERUNS_LOOKBACK:
                            reruns_seasons_list += episode
            except Exception as e: # If we land on the last season and there is a special season (season 0)
                RandomSeason = RandomSeason-1
                for episode in tv_show.season(RandomSeason):
                    if not episode.lastViewedAt: # If episode has not been viewed before, add to reruns list
                        reruns_seasons_list += episode
                    else:
                        days_since_played = (TODAY - episode.lastViewedAt.date()).days # If episode has not been viewed before, add to reruns list
                        if days_since_played > RERUNS_LOOKBACK:
                            reruns_seasons_list += episode
            NextRerunFromSeason = random.choice(reruns_seasons_list)
            reruns_list += NextRerunFromSeason
            print("Added ",NextRerunFromSeason,"to rerun pool.")
    if len(reruns_list) < RERUNS_MINIMUM: # Check if reruns added any media. Ignore look back and try again if it didnt.
        print("Found fewer reruns",len(reruns_list),"than the minimum required,",RERUNS_MINIMUM,". Trying again ignoring the lookback.")
        for i in range(RERUNS_MINIMUM, RERUNS_MAXIMUM):
            RandomSeason = random.randint(1,tv_show.childCount) # First, select a random season to pull from
            print("Selecting reruns from episode from",tv_show,"season",RandomSeason)
            try:
                for episode in tv_show.season(RandomSeason):
                    reruns_seasons_list += episode
            except Exception as e: # If we land on the last season and there is a special season (season 0)
                RandomSeason = RandomSeason-1
                for episode in tv_show.season(RandomSeason):
                        reruns_seasons_list += episode
            NextRerunFromSeason = random.choice(reruns_seasons_list)
            reruns_list += NextRerunFromSeason
            print("Added ",NextRerunFromSeason,"to rerun pool. Ignored lookback.")
    if len(reruns_list) < RERUNS_MINIMUM: # Give up and continue if reruns still didn't find any media
        if MOVIE_ACTIVE == 0:
            print("No reruns found. Please add media to the reruns library/collection, or disable the rerun feature by changing RERUN_ACTIVE to 1. Will proceed by checking for movies.")
        else:
            print("No reruns found. Please add media to the reruns library/collection. Since the next episode and movies functions are both disabled, quitting script.")
            quit()
    else:
        RERUNS_LIST_LENGTH = len(reruns_list)
        if RERUNS_LIST_LENGTH < RERUNS_MAXIMUM:
            REAL_RERUNS_MAXIMUM = len(reruns_list)
        else:
            REAL_RERUNS_MAXIMUM = RERUNS_MAXIMUM
        print("There are a total of",REAL_RERUNS_MAXIMUM,"rerun episodes")
        for i in range(RERUNS_MINIMUM, REAL_RERUNS_MAXIMUM): # Add X amount of rerun shows to the episodes playlist
            NextRerun = random.choice(reruns_list)
            episodes_list += NextRerun
            reruns_list.remove(NextRerun)
if MOVIE_ACTIVE == 0: # Collect movies
    print("Collecting movies... Movies will be selected from the films below.")
    for movie in Movies.search(collection=MOVIE_COLLECTION_TITLE): # Add movies to episode list
        print(movie)
        if not movie.lastViewedAt: # If movie has not been viewed before, add to movies list
            movies_list += [movie]
        else:
            days_since_played = (TODAY - movie.lastViewedAt.date()).days # If movie has not been viewed before, add to movies list
            if days_since_played > MOVIE_LOOKBACK:
                movies_list += [movie]

    if len(movies_list) < MOVIE_MINIMUM: # Check if movies added any media. Ignore look back and try again if it didnt.
        print("Found fewer movies",len(movies_list),"than the minimum required,",MOVIE_MINIMUM,". Trying again ignoring the lookback.")
        for movie in Movies.search(collection=MOVIE_COLLECTION_TITLE): # Add movies to episode list
            print(movie)
            movies_list += [movie]

    if len(movies_list) < MOVIE_MINIMUM: # Check if movies are still less than minumum. Ignore look back and try again if it didnt.
        print("Found fewer movies",len(movies_list),"than the minimum required,",MOVIE_MINIMUM,". Tried to find movies a second time ignoring the lookback, but still didn't find enough. Try reducing the MOVIE_MINIMUM, or adding more media.")
        if len(episodes_list) > 0:
            print("Continuing script with episodes list only.")
            MOVIE_PREROLL_ACTIVE = 1
            PRESHOW_CARTOON_ACTIVE = 1
            TRAILER_ACTIVE = 1
        else:
            quit()

    MOVIES_LIST_LENGTH = len(movies_list)

    if MOVIE_MAXIMUM == 1: # - [ ] Is this even doing anything... Do i need to do this...
        MOVIE_MAXIMUM += 1

    if MOVIES_LIST_LENGTH < MOVIE_MAXIMUM:
        REAL_MOVIE_MAXIMUM = len(movies_list)
    else:
        REAL_MOVIE_MAXIMUM = MOVIE_MAXIMUM

    if MOVIE_PREROLL_ACTIVE == 0:
        MoviePrerollsAmount = REAL_MOVIE_MAXIMUM*3
        for tv_show in MoviePrerolls.search(collection=MOVIE_PREROLL_COLLECTION_TITLE): # Collect prerolls
            print(tv_show)
            for episode in tv_show.episodes():
                if len(movie_prerolls_list) > MoviePrerollsAmount:
                    break
                else:
                    if not episode.isWatched:
                        movie_prerolls_list += episode
                    else:
                        days_since_played = (TODAY - episode.lastViewedAt.date()).days
                        if days_since_played > MOVIE_PREROLL_LOOKBACK:
                            movie_prerolls_list += episode

    if PRESHOW_CARTOON_ACTIVE == 0: # Collect preshow cartoons
        PreShowCartoonAmount = REAL_MOVIE_MAXIMUM
        for tv_show in PreshowCartoon.search(collection=PRESHOW_CARTOON_COLLECTION_TITLE): # Collect preshow cartoons
            print(tv_show)
            preshowcartoon_list = []
            preshowcartoon_show_list = []
            RandomSeason = random.randint(1,tv_show.childCount)
            print("Selecting preshow cartoon from",tv_show,"season",RandomSeason)
            try:
                for episode in tv_show.season(RandomSeason):
                    if len(preshowcartoon_show_list) > PreShowCartoonAmount:
                        preshowcartoon_list += preshowcartoon_show_list
                        break
                    else:
                        if not episode.isWatched:
                            preshowcartoon_show_list += episode
                        else:
                            days_since_played = (TODAY - episode.lastViewedAt.date()).days
                            if days_since_played > preshowcartoon_LOOKBACK:
                                preshowcartoon_show_list += episode
            except Exception as e: # If we land on the last season and there is a special season (season 0)
                RandomSeason = RandomSeason-1
                for episode in tv_show.season(RandomSeason):
                    if not episode.lastViewedAt: # If episode has not been viewed before, add to reruns list
                        preshowcartoon_show_list += episode
                    else:
                        days_since_played = (TODAY - episode.lastViewedAt.date()).days # If episode has not been viewed before, add to reruns list
                        if days_since_played > preshowcartoon_LOOKBACK:
                            preshowcartoon_show_list += episode
        if len(preshowcartoon_list) < PreShowCartoonAmount:
            print("Not enough preshowcartoon found for preshowcartoon amount. Trying again without lookback.")
            try:
                for episode in tv_show.season(RandomSeason):
                    if len(preshowcartoon_show_list) > PreShowCartoonAmount:
                        preshowcartoon_list += preshowcartoon_show_list
                        break
                    else:
                        preshowcartoon_show_list += episode
            except Exception as e: # If we land on the last season and there is a special season (season 0)
                RandomSeason = RandomSeason-1
                for episode in tv_show.season(RandomSeason):
                    if len(preshowcartoon_show_list) > PreShowCartoonAmount:
                        preshowcartoon_list += preshowcartoon_show_list
                        break
                    else:
                        preshowcartoon_show_list += episode
        if len(preshowcartoon_list) < PreShowCartoonAmount:
            print("Not enough preshowcartoon found, even ignoring lookback. Please add content, or disable this feature by changing preshowcartoon_ACTIVE to 1. Quitting script.")
            quit()

    if TRAILER_ACTIVE == 0:  # Collect trailers
        TrailerAmount = REAL_MOVIE_MAXIMUM*TRAILER_MAXIMUM
        for tv_show in Trailers.search(collection=TRAILER_COLLECTION_TITLE): # Collect trailers
            print(tv_show)
            for episode in tv_show.episodes():
                print(episode)
                if len(trailers_list) > TrailerAmount:
                    break
                else:
                    if not episode.isWatched:
                        trailers_list += episode
                    else:
                        days_since_played = (TODAY - episode.lastViewedAt.date()).days
                        if days_since_played > TRAILER_LOOKBACK:
                            trailers_list += episode
        if len(trailers_list) < TrailerAmount:
            for tv_show in Trailers.search(collection=TRAILER_COLLECTION_TITLE): # Collect trailers ignoring lookback
                print(tv_show)
                for episode in tv_show.episodes():
                    print(episode)
                    if len(trailers_list) > TrailerAmount:
                        break
                    else:
                        trailers_list += episode
            REAL_TRAILERS_MAXIMUM = len(trailers_list)
        else:
            REAL_TRAILERS_MAXIMUM = TRAILER_MAXIMUM
        print("Trailers selected this run:",trailers_list)
EpisodeCount = len(episodes_list)

if PROMO_ACTIVE == 0: # Collect promos
    PromosCount = 0
    PromosAmount = EpisodeCount*PROMO_MAXIMUM_BW_EPISODES
    for tv_show in Promos.search(collection=PROMO_COLLECTION_TITLE): # Collect promos
        print(tv_show)
        promo_show_list = []
        promo_seasons_list = []
        RandomSeason = random.randint(1,tv_show.childCount)
        print("Selecting promo from",tv_show,"season",RandomSeason)
        try:
            for episode in tv_show.season(RandomSeason):
            
                if len(promo_show_list) > PromosAmount:
                    promos_list += promo_show_list
                    break
                else:
                    if not episode.isWatched:
                        promo_show_list += episode
                    else:
                        days_since_played = (TODAY - episode.lastViewedAt.date()).days
                        if days_since_played > PROMO_LOOKBACK:
                            promo_show_list += episode
        except Exception as e: # If we land on the last season and there is a special season (season 0)
            RandomSeason = RandomSeason-1
            for episode in tv_show.season(RandomSeason):
                if not episode.lastViewedAt: # If episode has not been viewed before, add to reruns list
                    promo_show_list += episode
                else:
                    days_since_played = (TODAY - episode.lastViewedAt.date()).days # If episode has not been viewed before, add to reruns list
                    if days_since_played > PROMO_LOOKBACK:
                        promo_show_list += episode
    if len(promos_list) < PromosAmount:
        print("Not enough episodes found for promos. Trying again without lookback.")
        try:
            for episode in tv_show.season(RandomSeason):
                if len(promo_show_list) > PromosAmount:
                    promos_list += promo_show_list
                    break
                else:
                    promo_show_list += episode
        except Exception as e: # If we land on the last season and there is a special season (season 0)
            RandomSeason = RandomSeason-1
            for episode in tv_show.season(RandomSeason):
                if len(promo_show_list) > PromosAmount:
                    promos_list += promo_show_list
                    break
                else:
                    promo_show_list += episode
    if len(promos_list) < PromosAmount:
        print("No episodes found for promos, even ignoring lookback. Please add content, or disable this feature by changing PROMO_ACTIVE to 1. Quitting script.")
        quit()
if BLOCK_PREROLL_ACTIVE == 0: # Collect block pre rolls
    BlockPrerollAmount = EpisodeCount*2
    for tv_show in BlockPrerolls.search(collection=BLOCK_PREROLL_COLLECTION_TITLE): # Collect block prerolls
        print(tv_show)
        block_preroll_list = []
        for episode in tv_show.episodes():
            if len(block_preroll_list) > BlockPrerollAmount:
                block_preroll_list += episode
                break
            else:
                if not episode.isWatched:
                    block_preroll_list += episode
                else:
                    days_since_played = (TODAY - episode.lastViewedAt.date()).days
                    if days_since_played > BLOCK_PREROLL_LOOKBACK:
                        block_preroll_list += episode
    if len(block_preroll_list) == 0:
        print("No episodes found for block preroll. Trying again without lookback.")
        for tv_show in BlockPrerolls.search(collection=BLOCK_PREROLL_COLLECTION_TITLE): # Collect block prerolls ignoring lookback
            print(tv_show)
            block_preroll_list = []
            for episode in tv_show.episodes():
                block_preroll_list += episode
                if len(block_preroll_list) > BlockPrerollAmount:
                    block_preroll_list += episode
                    break
    if len(block_preroll_list) == 0:
        print("No episodes found for block preroll, even ignoring lookback. Please add content, or disable this feature by changing BLOCK_PREROLL_ACTIVE to 1. Quitting script.")
        quit()
if BUMPER_ACTIVE == 0: # Collect bumpers
    if BUMPER_AFTER == BUMPER_BEFORE == 0:
        BumpersAmount = EpisodeCount*2
    else:
        BumpersAmount = EpisodeCount
    for tv_show in Bumpers.search(collection=BUMPER_COLLECTION_TITLE): # Collect bumpers
        print(tv_show)
        bumpers_list = []
        bumpers_show_list = []
        bumpers_seasons_list = []
        RandomSeason = random.randint(1,tv_show.childCount)
        print("Selecting bumpers from",tv_show,"season",RandomSeason)
        try:
            for episode in tv_show.season(RandomSeason):
                if len(bumpers_show_list) > BumpersAmount:
                    bumpers_list += bumpers_show_list
                    break
                else:
                    if not episode.isWatched:
                        bumpers_show_list += episode
                    else:
                        days_since_played = (TODAY - episode.lastViewedAt.date()).days
                        if days_since_played > BUMPER_LOOKBACK:
                            bumpers_show_list += episode
        except Exception as e: # If we land on the last season and there is a special season (season 0)
            RandomSeason = RandomSeason-1
            for episode in tv_show.season(RandomSeason):
                if not episode.lastViewedAt: # If episode has not been viewed before, add to reruns list
                    bumpers_show_list += episode
                else:
                    days_since_played = (TODAY - episode.lastViewedAt.date()).days # If episode has not been viewed before, add to reruns list
                    if days_since_played > BUMPER_LOOKBACK:
                        bumpers_show_list += episode
    if len(bumpers_list) < BumpersAmount:
        print("Not enough bumpers found for bumpers amount. Trying again without lookback.")
        for tv_show in Bumpers.search(collection=BUMPER_COLLECTION_TITLE):
            try:
                for episode in tv_show.season(RandomSeason):
                    if len(bumpers_show_list) > BumpersAmount:
                        bumpers_list += bumpers_show_list
                        break
                    else:
                        bumpers_show_list += episode
            except Exception as e: # If we land on the last season and there is a special season (season 0)
                RandomSeason = RandomSeason-1
                for episode in tv_show.season(RandomSeason):
                    if len(bumpers_show_list) > BumpersAmount:
                        bumpers_list += bumpers_show_list
                        break
                    else:
                        bumpers_show_list += episode
    if len(bumpers_list) < BumpersAmount:
        print("Not enough bumpers found, even ignoring lookback. Please add content, or disable this feature by changing BUMPER_ACTIVE to 1. Quitting script.")
        quit()
    print("Bumpers count:",len(bumpers_list))
# Put the playlist together
playlist_list = []
for i in range(EpisodeCount): # Put promos and episodes together
    NextEpisode = random.choice(episodes_list)
    if BUMPER_ACTIVE == 0:
        if BUMPER_BEFORE == 0:
            NextBumper = random.choice(bumpers_list)
            playlist_list += NextBumper
            bumpers_list.remove(NextBumper)
        playlist_list += NextEpisode
        episodes_list.remove(NextEpisode)
        if BUMPER_AFTER == 0:
            NextBumper = random.choice(bumpers_list)
            playlist_list += NextBumper
            bumpers_list.remove(NextBumper)
    else:
        playlist_list += NextEpisode
        episodes_list.remove(NextEpisode)
    if PROMO_ACTIVE == 0:
        PromosAmountInI = random.randint(PROMO_MINIMUM_BW_EPISODES, PROMO_MAXIMUM_BW_EPISODES)
        for x in range(PromosAmountInI):
            NextPromo = random.choice(promos_list)
            playlist_list += NextPromo
            promos_list.remove(NextPromo)
if MOVIE_ACTIVE == 0: # Add movies to episode list
    MovieLocationOffset = 0
    TryAgainRangeLow = 0
    TryAgainRangeHigh = 0
    TryAgainCount = 0
    for i in range(REAL_MOVIE_MAXIMUM):
        moviesetc_list = []
        if not EpisodesInPlaylistYN == 0:
            MovieLocation = 1
            print("No episodes. Adding movies.")
        else: 
            MovieLocation = random.randint(0, len(playlist_list))
            while MovieLocation in range(TryAgainRangeLow,TryAgainRangeHigh):
                print("Picked a location where a movie already was. Trying again.")
                MovieLocation = random.randint(0, len(playlist_list))
                TryAgainCount += 1
                if TryAgainCount > 10:
                    print("Couldn't find a place to put movie list. Try adding more episodes to playlist, or reduce trailer, preshow cartoon, or movie maximum")
                    quit()
            MovieLocationOffset = 1
        try:
            NextMovie = random.choice(movies_list)
        except Exception as e: (print("There is an error with the movies list. please make sure enough media is assigned to the movies collection. Error:",e))        
        moviesetc_list.insert(1,NextMovie)
        MovieLocationOffset += 1
        movies_list.remove(NextMovie)

        if TRAILER_ACTIVE == 0: # Add trailers in front of movie
            TrailerCountBeforeMovie = random.randint(TRAILER_MINIMUM, REAL_TRAILERS_MAXIMUM)
            for i in range(TrailerCountBeforeMovie):
                try:
                    NextTrailer = random.choice(trailers_list)
                except Exception as e: (print("There is an error with the trailers list. please make sure enough media is assigned to the trailers collection. Error:",e))
                moviesetc_list.insert(1,NextTrailer)
                MovieLocationOffset += 1
                trailers_list.remove(NextTrailer)

        if PRESHOW_CARTOON_ACTIVE == 0: # Add prerolls in front of movie
            try:
                NextPreshowCartoon = random.choice(preshowcartoon_list)
            except Exception as e: (print("There is an error with the preshow cartoon list. please make sure enough media is assigned to the preshow cartoon collection. Error:",e))
            try:
                moviesetc_list.insert(1,NextPreshowCartoon)
                MovieLocationOffset += 1
            except Exception as e: (print("There is an error with the preshow cartoon list. please make sure enough media is assigned to the preshow cartoon collection. Error:",e))
            try:
                preshowcartoon_list.remove(NextPreshowCartoon)
            except Exception as e: (print("There is an error with the preshow cartoon list. please make sure enough media is assigned to the preshow cartoon collection. Error:",e))

        if MOVIE_PREROLL_ACTIVE == 0: # Add prerolls in front of movie
            try:
                NextMoviePreroll = random.choice(movie_prerolls_list)
            except Exception as e: (print("There is an error with the preroll list. please make sure enough media is assigned to the prerolls collection. Error:",e))
            try:
                moviesetc_list.insert(1,NextMoviePreroll)
                MovieLocationOffset += 1
            except Exception as e: (print("There is an error with the preroll list. please make sure enough media is assigned to the prerolls collection. Error:",e))
            try:
                movie_prerolls_list.remove(NextMoviePreroll)
            except Exception as e: (print("There is an error with the preroll list. please make sure enough media is assigned to the prerolls collection. Error:",e))
        TryAgainRangeLow = MovieLocation - MovieLocationOffset
        TryAgainRangeHigh = MovieLocation + MovieLocationOffset
        TryAgainCount = 0
        moviesetc_list.reverse()
        playlist_list.insert(MovieLocation,moviesetc_list)
if BLOCK_PREROLL_ACTIVE == 0: # Add the block preroll to the front of the episode list
    NextBlockPreroll = random.choice(block_preroll_list)
    playlist_list.insert(0,NextBlockPreroll)
print("Full playlist:",playlist_list)
print('Adding {} episodes to playlist.'.format(len(playlist_list)))
 
for playlist in plex.playlists(): # If playlist exists, add items to it. If it doesn't, create the playlist.
    if playlist.title == PLAYLIST_TITLE: # If playlist exists, add items to it
        originalplaylistitems = plex.playlist(PLAYLIST_TITLE).items()
        originalplaylist = plex.playlist(PLAYLIST_TITLE)
        playlistexists = 1
        print("Playlist",PLAYLIST_TITLE,"already exists. Adding items to playlist.")
        for i in playlist_list:
            originalplaylist.addItems(i)
        quit()
    else: # If playlist does not exist, create it and add items
        playlistexists = 0
        playlist_first = playlist_list[0]

if playlistexists == 0: # If the playlist doesn't exist, create it and add the first item
    print("Playlist",PLAYLIST_TITLE,"does not exist. Creating playlist.")
    plex.createPlaylist(PLAYLIST_TITLE,playlist_first)
    for playlist in plex.playlists(): # Try again
        if playlist.title == PLAYLIST_TITLE: # If playlist exists, add items to it
            originalplaylistitems = plex.playlist(PLAYLIST_TITLE).items()
            originalplaylist = plex.playlist(PLAYLIST_TITLE)
            playlistexists = 1
            print("Playlist",PLAYLIST_TITLE,"already exists. Adding items to playlist.")
            for i in playlist_list:
                originalplaylist.addItems(i)
            quit()