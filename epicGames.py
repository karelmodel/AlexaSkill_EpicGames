from epicstore_api import EpicGamesStoreAPI, OfferData
from datetime import datetime
import locale


locale.setlocale(locale.LC_ALL, 'pt_br.UTF-8')

api = EpicGamesStoreAPI()
promotions = api.get_free_games()

date_format = '%Y-%m-%d'


freeGames = []

for game in promotions['data']['Catalog']['searchStore']['elements']:
    if game.get('promotions') != None:
        if game['promotions'].get('promotionalOffers') != None:
            if game['promotions']['promotionalOffers'] != []:
                if(game['title'] != 'Mystery Game'):
                    startDate=datetime.strptime(game['promotions']['promotionalOffers'][0]['promotionalOffers'][0]['startDate'][0:10], date_format)
                    endDate=datetime.strptime(game['promotions']['promotionalOffers'][0]['promotionalOffers'][0]['endDate'][0:10], date_format)
                    discountPercentage=game['promotions']['promotionalOffers'][0]['promotionalOffers'][0]['discountSetting']['discountPercentage']
                
                    if endDate > datetime.today() and discountPercentage == 0:
                        freeGames.append(game['title'])
    
speak_output = "Os jogos que estão de graça hoje são: " + freeGames[0] + " e " + freeGames[1] + "."

speak_output