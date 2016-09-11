from disqusapi import DisqusAPI
import pprint

disqus_secret_key = 'gEsLGMfIJ2Wy8Ft2nE84ANSoIJ61kLmNRQlRukgHEwfGb69ngZnRbyAhzPyeZv2G'
disqus_public_key = '7JIzndWon2HyoEnL8LUyaAIBLaDS8323wQ3qgbbAEPh3Hn4Ywgb3Cl04kJaWhmDW'

google_key = 'AIzaSyDuV5zNTz8T7jwKf6X6MVDfjZQoDN1PQ6g' #developers.google.com
goole_search_engine = '011263252709623880646:fr2q4yl60bo' #cse.google.com

pp = pprint.PrettyPrinter(indent=1)

disqus = DisqusAPI(disqus_secret_key, disqus_public_key)
for result in disqus.get('threads.list',  method='GET'):
    pp.pprint(result)
