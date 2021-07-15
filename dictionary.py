import requests
import json

def lang( language ):
  if( language == 'english' or language == 'en_us' ):
    language = 'en_US'
  elif( language == 'hindi' or language == 'hi' ):
    language = 'hi'
  elif( language == 'spanish' or language == 'es' ):
    language == 'es'
  elif( language == 'french' or language == 'fr' ):
    language = 'fr'
  elif( language == 'japanese' or language == 'ja' or language == 'jp' ):
    language = 'ja'
  elif( language == 'russian' or language == 'ru' ):
    language = 'ru'
  elif( language == 'en_gb' or language == 'uk' or language == 'british'):
    language = 'en_GB'
  elif( language == 'german' or language == 'de' or language == 'deutch' ):
    language = 'de'
  elif( language == 'italian' or language == 'it' ):
    language = 'it'
  elif( language == 'korean' or language == 'ko' or language == 'kor' ):
    language = 'ko'
  elif( language == 'brazilian portuguese' or language == 'portuguese' or language == 'pt_br' ):
    language = 'pt-BR'
  elif( language == 'arabic' or language == 'ar' ):
    language = 'ar'
  elif( language == 'turkish' or language == 'tr' ):
    language = 'tr'
  else:
    language = 'unsupp'
  return language

def define( word, language='english' ):
  language = lang( language.lower() )
  if( language == 'unsupp' ):
    return "Language not yet supported."
  
  response = requests.get( 'https://api.dictionaryapi.dev/api/v2/entries/' + language + '/' + word )
  content = json.loads( response.text )
  
  def cont( name, content ):
    result = []
    index = 0
    for i in content:
      res = i[name]
      index = index + 1
      result.append(res)
    return result

  x = []
  for i in content:
    word = i['word']
    phone = cont( 'text', i['phonetics'] )
    pos = cont( 'partOfSpeech', i['meanings'] )
    defn = cont( 'definitions', i['meanings'] )
    x.append()

  """
  word = content[0]['word']
  phone = content[0]['phonetics'][0]['text']
  return meaning
  """