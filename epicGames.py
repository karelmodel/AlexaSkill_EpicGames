from epicstore_api import EpicGamesStoreAPI, OfferData
from datetime import datetime
import locale


locale.setlocale(locale.LC_ALL, 'pt_br.UTF-8')

api = EpicGamesStoreAPI()
promotions = api.get_free_games()


freeGames = []

for game in promotions['data']['Catalog']['searchStore']['elements']:
    if game['promotions'] is not None:        
        if "promotionalOffers" in game['promotions']:
            if game['promotions']['promotionalOffers']:
                if(game['title'] != 'Mystery Game'):
                    freeGames.append(game['title'])
    
#endDate = datetime.fromisoformat(game['promotions']['promotionalOffers'][0]['promotionalOffers'][0]['endDate'][:-1])
#validPromotionMessage = "A promoção será válida somente até o dia " + datetime.strptime(str(endDate), '%Y-%m-%d %H:%M:%S').strftime('%d de %B')

speak_output = "Os jogos que estão de graça hoje são: " + freeGames[0] + " e " + freeGames[1] + "."

speak_output


for game in promotions['data']['Catalog']['searchStore']['elements']:
    if game.get('promotions') != None:
        if game['promotions'].get('promotionalOffers') != None:
            if game['promotions']['promotionalOffers'] != []:
                print(game['title'])
                print(game['promotions']['promotionalOffers'][0]['promotionalOffers'][0]['startDate'])
                print(game['promotions']['promotionalOffers'][0]['promotionalOffers'][0]['endDate'])