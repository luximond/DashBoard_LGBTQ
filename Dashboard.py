import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import folium
import plotly.graph_objects as go

pd.options.mode.chained_assignment = None


f= pd.read_csv('LGBT_Survey_DailyLife.csv')
f=f.replace("United Kingdom","England")
f=f.replace(":","0")
f['percentage']=f['percentage'].astype(int)
f['CountryCode']=f['CountryCode'].astype(str)
holding_hands_lgb=f.query("question_code=='b1_e'")


def label_percentage (row):
   if row['answer'] == "Very widespread" :
      return 1
   if row['answer'] == "Fairly widespread" :
      return 0.5
   if row['answer'] == "I don't know" :
      return 0
   if row['answer'] == "Fairly rare" :
      return -0.5
   if row['answer'] == "Very rare" :
      return -1
   else :
     return 0


holding_hands_lgb['indice'] = holding_hands_lgb.apply (lambda row: label_percentage(row), axis=1)
holding_hands_lgb['indice']=holding_hands_lgb['indice'].astype(float)

for index, row in holding_hands_lgb.iterrows():
    holding_hands_lgb['notes'][index]=  holding_hands_lgb['percentage'][index]* holding_hands_lgb['indice'][index]
holding_hands_lgb['notes']=holding_hands_lgb['notes'].astype(int)

Gay = holding_hands_lgb.query("subset=='Gay'")
Lesbian = holding_hands_lgb.query("subset=='Lesbian'")
Transgender = holding_hands_lgb.query("subset=='Transgender'")
Bisexual_W = holding_hands_lgb.query("subset=='Bisexual women'")
Bisexual_M = holding_hands_lgb.query("subset=='Bisexual men'")


def normalise(data) : 
  a = pd.Series()
  j=0
  val = 0
  quot = 1
  for i in data['notes']:
    val = val + float(i)
    if val != 0:
      quot = quot +1
    if(j%5==0):
      a = a.append(pd.Series([val/quot]))
      val =0
      quot = 1
    j = j +1 
  a = a - a.mean(axis=0)
  a = a / np.abs(a).max(axis=0)
  return a

for index, row in holding_hands_lgb.iterrows():
    holding_hands_lgb['notes'][index]=  holding_hands_lgb['percentage'][index]* holding_hands_lgb['indice'][index]
holding_hands_lgb['notes']=holding_hands_lgb['notes'].astype(int)

Countries = Gay['CountryCode'].unique()
Gay_percentage = normalise(Gay)
Gay_data_map = pd.DataFrame({'Country': Countries, 'Scale': Gay_percentage})
Orientation = holding_hands_lgb['subset'].unique()

Lesbian_percentage = normalise(Lesbian)
Lesbian_data_map = pd.DataFrame({'Country': Countries, 'Scale': Lesbian_percentage})

Bisexual_W_percentage = normalise(Bisexual_W)
Bisexual_W_data_map = pd.DataFrame({'Country': Countries, 'Scale': Bisexual_W_percentage})

Bisexual_M_percentage = normalise(Bisexual_M)
Bisexual_M_data_map = pd.DataFrame({'Country': Countries, 'Scale': Bisexual_M_percentage})

Transgender_percentage = normalise(Transgender)
Transgender_data_map = pd.DataFrame({'Country': Countries, 'Scale': Transgender_percentage})

m = folium.Map(location=[55,20],tiles='Stamen Toner',zoom_start = 4)
country_geo = 'world_countries.json'
folium.Choropleth(
    geo_data=country_geo,
    data = Gay_data_map,
    columns=['Country','Scale'],
    key_on = 'feature.properties.name',
    fill_color = 'Reds',
    fill_opacity = 0.7,
    line_opacity = 0.2,
).add_to(m)

folium.LayerControl().add_to(m)

m.save('Gay.html')

m2 = folium.Map(location=[55,20],tiles='Stamen Toner',zoom_start = 4)
folium.Choropleth(
    geo_data=country_geo,
    data = Lesbian_data_map,
    columns=['Country','Scale'],
    key_on = 'feature.properties.name',
    fill_color = 'Reds',
    fill_opacity = 0.7,
    line_opacity = 0.2,
).add_to(m2)

folium.LayerControl().add_to(m2)

m2.save("Lesbian.html")

m3 = folium.Map(location=[55,20],tiles='Stamen Toner',zoom_start = 4)
folium.Choropleth(
    geo_data=country_geo,
    data = Bisexual_W_data_map,
    columns=['Country','Scale'],
    key_on = 'feature.properties.name',
    fill_color = 'Reds',
    fill_opacity = 0.7,
    line_opacity = 0.2,
).add_to(m3)

folium.LayerControl().add_to(m3)

m3.save('Bisexual_W.html')

m4 = folium.Map(location=[55,20],tiles='Stamen Toner',zoom_start = 4)

folium.Choropleth(
    geo_data=country_geo,
    data = Bisexual_M_data_map,
    columns=['Country','Scale'],
    key_on = 'feature.properties.name',
    fill_color = 'Reds',
    fill_opacity = 0.7,
    line_opacity = 0.2,
).add_to(m4)

folium.LayerControl().add_to(m4)

m4.save('Bisexual_M.html')

m5 = folium.Map(location=[55,20],tiles='Stamen Toner',zoom_start = 4)
folium.Choropleth(
    geo_data=country_geo,
    data = Transgender_data_map,
    columns=['Country','Scale'],
    key_on = 'feature.properties.name',
    fill_color = 'Reds',
    fill_opacity = 0.7,
    line_opacity = 0.2,
).add_to(m5)

folium.LayerControl().add_to(m5)

m5.save('Transgender.html')

file_test= pd.read_csv('LGBT_Survey_ViolenceAndHarassment.csv')

test = file_test
test=test.replace(':',0)
test2 = file_test.query("question_code=='e2'")
test2 =test2.replace(':','0')
test3 = file_test.query("question_code=='f1_a'")
test3 =test3.replace(':','0')
test4 = file_test.query("question_code=='f1_b'")
test4 =test4.replace(':','0')
test['percentage']=test['percentage'].astype(int)
test2['percentage']=test2['percentage'].astype(int)
test3['percentage']=test3['percentage'].astype(int)
test4['percentage']=test4['percentage'].astype(int)
test = test.query("question_code=='e1'")

test = test[test.CountryCode != "Average"]
test = test[test.answer != "I do not have a same-sex partner"]
test2 = test2[test2.CountryCode != "Average"]
test2 = test2[test2.answer != "I do not have a same-sex partner"]



for index, row in test.iterrows():
  if test['answer'][index] =="Yes":
    test['notes'][index]= -test['percentage'][index]
  if test['answer'][index] == "No":
    test['notes'][index]= test['percentage'][index]
  if test['answer'][index] == "Don`t know": 
    test['notes'][index]= 0


for index, row in test2.iterrows():
  if test2['answer'][index] =="Yes":
    test2['notes'][index]= -test2['percentage'][index]
  if test2['answer'][index] == "No":
    test2['notes'][index]= test2['percentage'][index]
  if test2['answer'][index] == "Don`t know": 
    test2['notes'][index]= 0

for index, row in test3.iterrows():
  if test3['answer'][index] =="Yes":
    test3['notes'][index]= -test3['percentage'][index]
  if test3['answer'][index] == "No":
    test3['notes'][index]= test3['percentage'][index]

for index, row in test4.iterrows():
  if test4['answer'][index] =="Yes":
    test4['notes'][index]= -test4['percentage'][index]
  if test4['answer'][index] == "No":
    test4['notes'][index]= test4['percentage'][index]

def normalise_2(data) : 
  a = pd.Series()
  j=0
  val = 0
  for i in data['notes']:
    val = val + float(i)
    if(j%3==0):
      a = a.append(pd.Series([val/2]))
      val =0
    j = j +1 
  a = a - a.mean(axis=0)
  a = a / np.abs(a).max(axis=0)
  return a
  
Gay_hist_1 = test.query("subset=='Gay'")
Lesbian_hist_1 = test.query("subset=='Lesbian'")
Transgender_hist_1 = test.query("subset=='Transgender'")
BiW_hist_1 = test.query("subset=='Bisexual women'")
BiM_hist_1 = test.query("subset=='Bisexual men'")
e1_data = normalise_2(Gay_hist_1)
e2_data = normalise_2(Lesbian_hist_1)
e3_data = normalise_2(Transgender_hist_1)
e4_data = normalise_2(BiW_hist_1)
e5_data = normalise_2(BiM_hist_1)

Gay_hist_2 = test2.query("subset=='Gay'")
Lesbian_hist_2 = test2.query("subset=='Lesbian'")
Transgender_hist_2 = test2.query("subset=='Transgender'")
BiW_hist_2 = test2.query("subset=='Bisexual women'")
BiM_hist_2 = test2.query("subset=='Bisexual men'")
f1_data = normalise_2(Gay_hist_2)
f2_data = normalise_2(Lesbian_hist_2)
f3_data = normalise_2(Transgender_hist_2)
f4_data = normalise_2(BiW_hist_2)
f5_data = normalise_2(BiM_hist_2)

Gay_hist_3 = test3.query("subset=='Gay'")
Lesbian_hist_3 = test3.query("subset=='Lesbian'")
Transgender_hist_3 = test3.query("subset=='Transgender'")
BiW_hist_3 = test3.query("subset=='Bisexual women'")
BiM_hist_3 = test3.query("subset=='Bisexual men'")
g1_data = normalise_2(Gay_hist_3)
g2_data = normalise_2(Lesbian_hist_3)
g3_data = normalise_2(Transgender_hist_3)
g4_data = normalise_2(BiW_hist_3)
g5_data = normalise_2(BiM_hist_3)

Gay_hist_4 = test4.query("subset=='Gay'")
Lesbian_hist_4 = test4.query("subset=='Lesbian'")
Transgender_hist_4 = test4.query("subset=='Transgender'")
BiW_hist_4 = test4.query("subset=='Bisexual women'")
BiM_hist_4 = test4.query("subset=='Bisexual men'")
h1_data = normalise_2(Gay_hist_4)
h2_data = normalise_2(Lesbian_hist_4)
h3_data = normalise_2(Transgender_hist_4)
h4_data = normalise_2(BiW_hist_4)
h5_data = normalise_2(BiM_hist_4)

figure1 = go.Figure()
figure1.add_trace(go.Histogram(x=e2_data,xbins=dict(start = -1.0, size = 0.2, end = 1.0),name='Lesbian',showlegend=True))
figure1.add_trace(go.Histogram(x=e1_data,xbins=dict(start = -1.0, size = 0.2, end = 1.0),name='Gay',showlegend=True))
figure1.add_trace(go.Histogram(x=e3_data,xbins=dict(start = -1.0, size = 0.2, end = 1.0),name='Transgender',showlegend=True))
figure1.add_trace(go.Histogram(x=e4_data,xbins=dict(start = -1.0, size = 0.2, end = 1.0),name='Bisexual Women',showlegend=True))
figure1.add_trace(go.Histogram(x=e5_data,xbins=dict(start = -1.0, size = 0.2, end = 1.0),name='Bisexual Men',showlegend=True))
figure1.update_traces(opacity=0.75)

figure2 = go.Figure()
figure2.add_trace(go.Histogram(x=f2_data,xbins=dict(start = -1.0, size = 0.2, end = 1.0),name='Lesbian',showlegend=True))
figure2.add_trace(go.Histogram(x=f1_data,xbins=dict(start = -1.0, size = 0.2, end = 1.0),name='Gay',showlegend=True))
figure2.add_trace(go.Histogram(x=f3_data,xbins=dict(start = -1.0, size = 0.2, end = 1.0),name='Transgender',showlegend=True))
figure2.add_trace(go.Histogram(x=f4_data,xbins=dict(start = -1.0, size = 0.2, end = 1.0),name='Bisexual Women',showlegend=True))
figure2.add_trace(go.Histogram(x=f5_data,xbins=dict(start = -1.0, size = 0.2, end = 1.0),name='Bisexual Men',showlegend=True))
figure2.update_traces(opacity=0.75)

figure3 = go.Figure()
figure3.add_trace(go.Histogram(x=g2_data,xbins=dict(start = -1.0, size = 0.2, end = 1.0),name='Lesbian',showlegend=True))
figure3.add_trace(go.Histogram(x=g1_data,xbins=dict(start = -1.0, size = 0.2, end = 1.0),name='Gay',showlegend=True))
figure3.add_trace(go.Histogram(x=g3_data,xbins=dict(start = -1.0, size = 0.2, end = 1.0),name='Transgender',showlegend=True))
figure3.add_trace(go.Histogram(x=g4_data,xbins=dict(start = -1.0, size = 0.2, end = 1.0),name='Bisexual Women',showlegend=True))
figure3.add_trace(go.Histogram(x=g5_data,xbins=dict(start = -1.0, size = 0.2, end = 1.0),name='Bisexual Men',showlegend=True))
figure3.update_traces(opacity=0.75)

figure4 = go.Figure()
figure4.add_trace(go.Histogram(x=h2_data,xbins=dict(start = -1.0, size = 0.2, end = 1.0),name='Lesbian',showlegend=True))
figure4.add_trace(go.Histogram(x=h1_data,xbins=dict(start = -1.0, size = 0.2, end = 1.0),name='Gay',showlegend=True))
figure4.add_trace(go.Histogram(x=h3_data,xbins=dict(start = -1.0, size = 0.2, end = 1.0),name='Transgender',showlegend=True))
figure4.add_trace(go.Histogram(x=h4_data,xbins=dict(start = -1.0, size = 0.2, end = 1.0),name='Bisexual Women',showlegend=True))
figure4.add_trace(go.Histogram(x=h5_data,xbins=dict(start = -1.0, size = 0.2, end = 1.0),name='Bisexual Men',showlegend=True))
figure4.update_traces(opacity=0.75)

bar_graph = file_test
bar_graph = bar_graph[bar_graph.question_code != 'e1']
bar_graph = bar_graph[bar_graph.question_code != 'e2']
bar_graph = bar_graph[bar_graph.question_code != 'f1_a']
bar_graph = bar_graph[bar_graph.question_code != 'f1_b']
bar_graph = bar_graph.replace(':','0')
bar_graph['percentage'] = bar_graph['percentage'].astype(int)
bar_graph1 = bar_graph[bar_graph['question_code'].isin(['f1_4', 'fa2_4','fb1_4','fb2_4'])]
bar_graph2 = bar_graph[bar_graph['question_code'].isin(['f1_7', 'fa2_7','fb1_7','fb2_7'])]
bar_graph3 = bar_graph[bar_graph['question_code'].isin(['f1_8', 'fa2_8','fb1_8','fb2_8'])]
bar_graph4 = bar_graph[bar_graph['question_code'].isin(['f1_10', 'fa2_10','fb1_10','fb2_10'])]
bar_graph5 = bar_graph[bar_graph['question_code'].isin(['f1_12', 'fa2_12','fb1_12','fb2_12'])]


bar_graph_gay = bar_graph.query("subset=='Gay'")
bar_graph_lesbian = bar_graph.query("subset=='Lesbian'")
bar_graph_biW = bar_graph.query("subset=='Bisexual women'")
bar_graph_biM = bar_graph.query("subset=='Bisexual men'")
bar_graph_transgender = bar_graph.query("subset=='Transgender'")

means_gay= bar_graph_gay.groupby('answer')['percentage'].mean()
means_lesbian= bar_graph_lesbian.groupby('answer')['percentage'].mean()
means_biW= bar_graph_biW.groupby('answer')['percentage'].mean()
means_biM= bar_graph_biM.groupby('answer')['percentage'].mean()
means_transgender= bar_graph_transgender.groupby('answer')['percentage'].mean()

means_gay=means_gay.astype(int)
means_lesbian= means_lesbian.astype(int)
means_biW= means_biW.astype(int)
means_biM= means_biM.astype(int)
means_transgender= means_transgender.astype(int)

bar_graph2_gay = bar_graph2.query("subset=='Gay'")
bar_graph2_lesbian = bar_graph2.query("subset=='Lesbian'")
bar_graph2_biW = bar_graph2.query("subset=='Bisexual women'")
bar_graph2_biM = bar_graph2.query("subset=='Bisexual men'")
bar_graph2_transgender = bar_graph2.query("subset=='Transgender'")

means2_gay= bar_graph2_gay.groupby('answer')['percentage'].mean()
means2_lesbian= bar_graph2_lesbian.groupby('answer')['percentage'].mean()
means2_biW= bar_graph2_biW.groupby('answer')['percentage'].mean()
means2_biM= bar_graph2_biM.groupby('answer')['percentage'].mean()
means2_transgender= bar_graph2_transgender.groupby('answer')['percentage'].mean()

means2_gay=means2_gay.astype(int)
means2_lesbian= means2_lesbian.astype(int)
means2_biW= means2_biW.astype(int)
means2_biM= means2_biM.astype(int)
means2_transgender= means2_transgender.astype(int)

figure_gr1_gay = go.Figure()
figure_gr1_lesbian = go.Figure()
figure_gr1_biW = go.Figure()
figure_gr1_biM = go.Figure()
figure_gr1_transgender = go.Figure()

answers_1 = ['Aggressive gestures (such as pointing)','Bullying','Don`t know','Excessive /constant negative comments',
           'Isolation from something or somebody; ignoring','Name calling','Other','Other non-verbal insult, abuse, humiliation (such as text or image)',
          'Other verbal insult/abuse/humiliation','Physical and sexual attack','Physical attack','Ridiculing (making jokes about you)','Sexual attack',
           'Threat of both physical and sexual violence','Threat of physical violence','Threat of sexual violence']
           
figure_gr1_gay.add_trace(go.Bar(x=answers_1,y=means_gay,name='Gay',showlegend=True))
figure_gr1_lesbian.add_trace(go.Bar(x=answers_1,y=means_lesbian,name='Lesbian',showlegend=True))
figure_gr1_biW.add_trace(go.Bar(x=answers_1,y=means_biW,name='Bisexual Women',showlegend=True))
figure_gr1_biM.add_trace(go.Bar(x=answers_1,y=means_biM,name='Bisexual Men',showlegend=True))
figure_gr1_transgender.add_trace(go.Bar(x=answers_1,y=means_transgender,name='Transgender',showlegend=True))


figure2_gay = go.Figure()
figure2_lesbian = go.Figure()
figure2_biW = go.Figure()
figure2_biM = go.Figure()
figure2_transgender = go.Figure()

answers2 = ['A customer, client or patient','Colleague at work','Family/household member',
            'Member of an extremist/racist group','Neighbour','Other','Other public official (e.g. border guard, civil servant)',
            'Police officer','Security officer/bouncer','Someone else you didn`t know','Someone else you know','Someone from school, college or university',
            'Teenager or group of teenagers']

figure2_gay.add_trace(go.Bar(x=answers2,y=means2_gay,name='Gay',showlegend=True))
figure2_lesbian.add_trace(go.Bar(x=answers2,y=means2_lesbian,name='Lesbian',showlegend=True))
figure2_biW.add_trace(go.Bar(x=answers2,y=means2_biW,name='Bisexual Women',showlegend=True))
figure2_biM.add_trace(go.Bar(x=answers2,y=means2_biM,name='Bisexual Men',showlegend=True))
figure2_transgender.add_trace(go.Bar(x=answers2,y=means2_transgender,name='Transgender',showlegend=True))

bar_graph3_gay = bar_graph3.query("subset=='Gay'")
bar_graph3_lesbian = bar_graph3.query("subset=='Lesbian'")
bar_graph3_biW = bar_graph3.query("subset=='Bisexual women'")
bar_graph3_biM = bar_graph3.query("subset=='Bisexual men'")
bar_graph3_transgender = bar_graph3.query("subset=='Transgender'")

means3_gay= bar_graph3_gay.groupby('answer')['percentage'].mean()
means3_lesbian= bar_graph3_lesbian.groupby('answer')['percentage'].mean()
means3_biW= bar_graph3_biW.groupby('answer')['percentage'].mean()
means3_biM= bar_graph3_biM.groupby('answer')['percentage'].mean()
means3_transgender= bar_graph3_transgender.groupby('answer')['percentage'].mean()

means3_gay=means3_gay.astype(int)
means3_lesbian= means3_lesbian.astype(int)
means3_biW= means3_biW.astype(int)
means3_biM= means3_biM.astype(int)
means3_transgender= means3_transgender.astype(int)

answers3 = ['Both male and female','Don`t know','Female','Male']

figure3_gay = go.Figure()
figure3_lesbian = go.Figure()
figure3_biW = go.Figure()
figure3_biM = go.Figure()
figure3_transgender= go.Figure()

figure3_gay.add_trace(go.Bar(x=answers3,y=means3_gay,name='Gay',showlegend=True))
figure3_lesbian.add_trace(go.Bar(x=answers3,y=means3_lesbian,name='Lesbian',showlegend=True))
figure3_biW.add_trace(go.Bar(x=answers3,y=means3_biW,name='Bisexual Women',showlegend=True))
figure3_biM.add_trace(go.Bar(x=answers3,y=means3_biM,name='Bisexual Men',showlegend=True))
figure3_transgender.add_trace(go.Bar(x=answers3,y=means3_transgender,name='Transgender',showlegend=True))

bar_graph4_gay = bar_graph4.query("subset=='Gay'")
bar_graph4_lesbian = bar_graph4.query("subset=='Lesbian'")
bar_graph4_biW = bar_graph4.query("subset=='Bisexual women'")
bar_graph4_biM = bar_graph4.query("subset=='Bisexual men'")
bar_graph4_transgender = bar_graph4.query("subset=='Transgender'")

means4_gay= bar_graph4_gay.groupby('answer')['percentage'].mean()
means4_lesbian= bar_graph4_lesbian.groupby('answer')['percentage'].mean()
means4_biW= bar_graph4_biW.groupby('answer')['percentage'].mean()
means4_biM= bar_graph4_biM.groupby('answer')['percentage'].mean()
means4_transgender= bar_graph4_transgender.groupby('answer')['percentage'].mean()

means4_gay=means4_gay.astype(int)
means4_lesbian= means4_lesbian.astype(int)
means4_biW= means4_biW.astype(int)
means4_biM= means4_biM.astype(int)
means4_transgender= means4_transgender.astype(int)

answers4 = ['At an LGBT specific venue (e.g. club, bar) or event (e.g. pride)','At my home','At school, university','At the workplace',
            'Elsewhere indoors','Elsewhere outdoors','In a cafe, restaurant, pub, club','In a car','In a park, forest','In a sports club',
            'In a street, square, car parking lot or other public place','In public transport','In some other residential building, apartment',
            'On the internet / email (including Facebook, Twitter, etc.)','Other']
figure4_gay = go.Figure()
figure4_lesbian = go.Figure()
figure4_biW = go.Figure()
figure4_biM = go.Figure()
figure4_transgender= go.Figure()

figure4_gay.add_trace(go.Bar(x=answers4,y=means4_gay,name='Gay',showlegend=True))
figure4_lesbian.add_trace(go.Bar(x=answers4,y=means4_lesbian,name='Lesbian',showlegend=True))
figure4_biW.add_trace(go.Bar(x=answers4,y=means4_biW,name='Bisexual Women',showlegend=True))
figure4_biM.add_trace(go.Bar(x=answers4,y=means4_biM,name='Bisexual Men',showlegend=True))
figure4_transgender.add_trace(go.Bar(x=answers4,y=means4_transgender,name='Transgender',showlegend=True))

bar_graph5_gay = bar_graph5.query("subset=='Gay'")
bar_graph5_lesbian = bar_graph5.query("subset=='Lesbian'")
bar_graph5_biW = bar_graph5.query("subset=='Bisexual women'")
bar_graph5_biM = bar_graph5.query("subset=='Bisexual men'")
bar_graph5_transgender = bar_graph5.query("subset=='Transgender'")

means5_gay= bar_graph5_gay.groupby('answer')['percentage'].mean()
means5_lesbian= bar_graph5_lesbian.groupby('answer')['percentage'].mean()
means5_biW= bar_graph5_biW.groupby('answer')['percentage'].mean()
means5_biM= bar_graph5_biM.groupby('answer')['percentage'].mean()
means5_transgender= bar_graph5_transgender.groupby('answer')['percentage'].mean()

means5_gay=means5_gay.astype(int)
means5_lesbian= means5_lesbian.astype(int)
means5_biW= means5_biW.astype(int)
means5_biM= means5_biM.astype(int)
means5_transgender= means5_transgender.astype(int)

answers5 = ['Dealt with it myself/involved a friend/family matter','Did not think they could do anything','Did not think they would do anything','Didn`t want the offender arrested or to get in trouble with the police',
            'Fear of a homophobic and/or transphobic reaction from the police','Fear of offender, fear of reprisal','Other reason','Shame, embarrassment, didn`t want anyone to know',
            'Somebody stopped me or discouraged me','Thought it was my fault','Too emotionally upset to contact the police','Too minor / not serious enough / never occurred to me',
            'Went directly to a magistrate or judge to report the incident','Went someplace else for help','Would not be believed','Somebody stopped me or discouraged me']

figure5_gay = go.Figure()
figure5_lesbian = go.Figure()
figure5_biW = go.Figure()
figure5_biM = go.Figure()
figure5_transgender= go.Figure()

figure5_gay.add_trace(go.Bar(x=answers5,y=means5_gay,name='Gay',showlegend=True))
figure5_lesbian.add_trace(go.Bar(x=answers5,y=means5_lesbian,name='Lesbian',showlegend=True))
figure5_biW.add_trace(go.Bar(x=answers5,y=means5_biW,name='Bisexual Women',showlegend=True))
figure5_biM.add_trace(go.Bar(x=answers5,y=means5_biM,name='Bisexual Men',showlegend=True))
figure5_transgender.add_trace(go.Bar(x=answers5,y=means5_transgender,name='Transgender',showlegend=True))

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
  'backgroundColor' : '#111111',
  'text' : '#727272'
}

app.layout = html.Div([
    html.Div([
        html.Div(dcc.Markdown('''
            ### **LGBT Community : Survey in Europe**
            '''),
          style= {'textAlign':'center','color': colors['text']}),
        html.Br(),
        html.Div([
            html.Div([
              html.Div(dcc.Markdown('''
            ###### **Distribution of European countries on the LGBT tolerance scale :**
            '''),
          style= {'textAlign':'center','color': colors['text']}),
              html.Div(dcc.Dropdown(
        options=[
            {'label': 'Do you avoid holding hands in public with a same-sex partner ?', 'value': '1'},
            {'label': 'Do you avoid certain places for fear or being assaulted / threatened ?', 'value': '2'},
            {'label': 'In the last 5 years, have you been assaulted / attacked for any reason ?', 'value': '3'},
            {'label': 'In the last 5 years, have you been personally harassed for any reason ?', 'value': '4'}
        ],
        value = '1',
        style={'width' : '90%', 'height': 50,'margin-left':'auto','margin-right':'auto'},
        id = 'dropdown_hist'
        )),
        html.Div(
            dcc.Graph(id ='test_histo',
            style={'height': 650,'width': 680}),
            style={'width' : '100%'}),
        html.Div(dcc.Markdown('''
            ###### **Analysis :**

            This histogram is a positivity scale on how the LGBT community feels.

            Bisexual men and women are generally safe when it comes to attacks, even though out bisexual women are more 
            exposed to harassment because their sexuality can be mixed with sexual fantasies. However, their fear of holding hands 
            and certain places is still about the same.

            As said before, lesbians and bisexual women are also victims of mysoginy, and are more likely to get harassed for their
            sexuality. Even though it seems like gays and lesbians who answered the survey are not experiencing a lot of harassment and / or violences,
            they still fear certain places and acts. Indeed as homophobia is still existing in Europe,
            the fear of being targeted is not disappearing.
            However, as transidentity is less understood and tolerated, their feeling of non-safety and the attacks they suffer from are on the same scale.
            '''),
          style= {'textAlign':'center','color': colors['text']})   
            ], 
            className="six columns",
            style = {'margin-left':'auto','margin-right':'auto'}),
            html.Div([
              html.Div(dcc.Markdown('''
                ###### ** Same-sex couples holding hands in public :**
                '''),
                style= {'textAlign':'center','color': colors['text']}),
                html.Div(html.Div(id = 'map_try',style={'margin-left':'auto','margin-right':'auto'})),
                html.Br(),
                html.Div(dcc.Slider(id="test_slider",
                    step= 1,
                    max = 5,
                    min = 1,
                    marks={
                        1: {'label': 'Gay'},
                        2: {'label': 'Lesbian'},
                        3 : {'label': 'Bisexual Women'},
                        4: {'label': 'Bisexual Men'},
                        5: {'label': 'Transgender'}
                          }
                    ),
                    style = {'width' : '90%','margin-left':'auto','margin-right':'auto'},
                    ),
                html.Br(),
                html.Br(),
                html.Div(dcc.Markdown('''
            ###### **Analysis :**

            As we can see with the map, people who are L,G,B,T in Eastern Europe feel less safe regarding their sexualtity
            ( for LGB ) or gender ( transgender people ). Opposite to them, L,G,B,T people coming from Northen Europe feel safer being
            open about it in public ( holding hands ). This is quite coherent as we know Eastern countries are less tolerant regarding
            this subject. However, transgender people seem less tolerated in Europe than people with non-heterosexual orientation,
            and are more likely to be exposed to harassment and violence.
            '''),
          style= {'textAlign':'center','color': colors['text']}),
            ], className="six columns"),
       
       ], className="row")
    ]),
    html.Br(),
    html.Div(dcc.Markdown('''
            #### **Survey results for open questions :**
            '''),style= {'textAlign':'center','color': colors['text']}),
     html.Div([
        html.Div([
          html.Div(dcc.Dropdown(
        options=[
            {'label': 'What was the last incident that happened to you?', 'value': 'gr1'},
            {'label': 'Who was the predator ?', 'value': 'gr2'},
            {'label': 'What gender was the predator ?', 'value': 'gr3'},
            {'label': 'Where did it happen ?', 'value': 'gr4'},
            {'label': 'Why did you not report it to the police ?', 'value': 'gr5'}
        ],
        value = 'gr1',
        style={'width' : '80%', 'height': 50,'margin-left':'auto'},
        id="dropdown_bar2"),
         style={'margin-left':'auto'})
        ], className="six columns"),
        html.Div([
          html.Div(dcc.Dropdown(
        options=[
            {'label': 'Gay', 'value': '1'},
            {'label': 'Lesbian', 'value': '2'},
            {'label': 'Bisexual Women', 'value': '3'},
            {'label': 'Bisexual Men', 'value': '4'},
            {'label': 'Transgender', 'value': '5'}
        ],
        value = '1',
        style={'width' : '40%', 'height': 50,'display':'inline-bloc'},
        id = 'dropdown_bar'
        ))

        ], className="six columns"),
    ], className="row"),
    html.Div(dcc.Graph(id ='test_bar',
              style={'width' : 1300, 'height': 700, 'display' : 'inline-block'}),
        style={'width' : '150%', 'height': 700, 'display' : 'inline-block'}
                ),
    html.Div(dcc.Markdown('''
            ###### **Analysis :**

            Like for every sexual orientation, we can see the predators are mostly male and only a few are female overall.
            Indeed women in general are more tolerant then men regarding the LGBT community. We can see that recurrent types of hrarassment towards
            them are name calling, negative comments, agressive gestures, and isolation. Most of these happened in the street which is quite logical
            as people usually make fun of ones they don't know ( when they see them holding hands, etc..). Usually they did not report it
            because they either felt like they wouldn't / couldn't do anything or felt like the incident was too minor.
            It is a shame to think they feel like the harassment they are a victim of is "too minor" for something to be done.
            
            '''),
          style= {'textAlign':'center','color': colors['text']}),
          html.Br(),
          html.Br(),
  ])
@app.callback(dash.dependencies.Output('map_try', 'children'),
               [dash.dependencies.Input('test_slider', 'value')])

def map_choice(answer):
     if answer == 1 :
         map = html.Iframe(id='map_with_slider',srcDoc=open('Gay.html','r').read(),width='100%',height='600')
     elif answer == 2 : 
         map=  html.Iframe(id='map_with_slider',srcDoc=open('Lesbian.html','r').read(),width='100%',height='600')
     elif answer == 3 : 
         map = html.Iframe(id='map_with_slider',srcDoc=open('Bisexual_W.html','r').read(),width='100%',height='600')
     elif answer == 4 : 
         map = html.Iframe(id='map_with_slider',srcDoc=open('Bisexual_M.html','r').read(),width='100%',height='600')
     elif answer == 5 :
         map =html.Iframe(id='map_with_slider',srcDoc=open('Transgender.html','r').read(),width='100%',height='600')
     else :
         map =html.Iframe(id='map_with_slider',srcDoc=open('Gay.html','r').read(),width='100%',height='600' )

     return map

def update_map(answer):
     map_update = map_choice(answer)
     map_update.save('right_map.html')
     return html.Iframe(srcDoc=open('right_map.html','r').read(),width='50%',height='600')

@app.callback(dash.dependencies.Output('test_histo', 'figure'),
               [dash.dependencies.Input('dropdown_hist', 'value')])

def hist_choice(value):
    if value == '1' :
         return figure1 
    elif value == '2' : 
         return figure2
    elif value == '3' : 
        return figure3 
    elif value == '4' : 
         return figure4
    else :
        return figure1

def update_hist(value):
    hist_update = figure_choice(value)
    return dcc.Graph(figure = hist_update )

@app.callback(dash.dependencies.Output('test_bar', 'figure'),
               [dash.dependencies.Input('dropdown_bar', 'value'),
               dash.dependencies.Input('dropdown_bar2', 'value')])

def bar_choice(value,gr):
    if gr == 'gr1':
        if value == '1' :
            return figure_gr1_gay 
        elif value == '2' : 
            return figure_gr1_lesbian
        elif value == '3' : 
            return figure_gr1_biW
        elif value == '4' : 
            return figure_gr1_biM
        elif value == '5' : 
            return figure_gr1_transgender
        else :
            return figure_gr1_gay
    elif gr == 'gr2':
        if value == '1' :
            return figure2_gay 
        elif value == '2' : 
            return figure2_lesbian
        elif value == '3' : 
            return figure2_biW
        elif value == '4' : 
            return figure2_biM
        elif value == '5' : 
            return figure2_transgender
        else :
            return figure2_gay
    elif gr == 'gr3':
        if value == '1' :
            return figure3_gay 
        elif value == '2' : 
            return figure3_lesbian
        elif value == '3' : 
            return figure3_biW
        elif value == '4' : 
            return figure3_biM
        elif value == '5' : 
            return figure3_transgender
        else :
            return figure3_gay
    elif gr == 'gr4':
        if value == '1' :
            return figure4_gay 
        elif value == '2' : 
            return figure4_lesbian
        elif value == '3' : 
            return figure4_biW
        elif value == '4' : 
            return figure4_biM
        elif value == '5' : 
            return figure4_transgender
        else :
            return figure4_gay
    elif gr == 'gr5':
        if value == '1' :
            return figure5_gay 
        elif value == '2' : 
            return figure5_lesbian
        elif value == '3' : 
            return figure5_biW
        elif value == '4' : 
            return figure5_biM
        elif value == '5' : 
            return figure5_transgender
        else :
            return figure5_gay
    else :
      return figure_gr1_transgender

def update_bar(value,gr):
    bar_update = bar_choice(value,gr)
    return dcc.Graph(figure = bar_update )


if __name__ == '__main__':
         app.run_server(host= 'localhost',debug=True)
