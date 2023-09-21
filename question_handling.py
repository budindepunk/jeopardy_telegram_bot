import pandas as pd
import random

# arreglando el dataframe etc
questions = pd.read_csv('jeopardy.csv')
pd.set_option('display.max_colwidth', None)
questions.rename(columns =
                {'Show Number':'show_number',
                 ' Air Date': 'air_date',
                 ' Round': 'game_round',
                 ' Category': 'category',
                 ' Value': 'value',
                 ' Question': 'question',
                 ' Answer': 'answer'}, inplace = True)



#deberia devolver un objeto con la pregunta y la respuesta, capaz el ID.
# imprime la pregunta y luego compara la respuesta del usuario con la que tiene aca


#info de la pregunta: año, tipo de ronda, valor