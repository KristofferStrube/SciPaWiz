import chart_studio.plotly as py
import plotly.figure_factory as ff
import plotly.graph_objs as go
import plotly.express as px

import pandas as pd
data = pd.read_json("files/IvanDamgaard/citations_by_author.json")
plotdata = pd.DataFrame()
plotdata = data.pivot_table(index = ['score'], aggfunc ='size') 

#print(plotdata)
fig = px.pie(plotdata, values=plotdata, names=plotdata.index, title='How many times people cite Ivan')

#go.Figure(go.Scatter(x = data['author'], y = data['score'],
      #            name='WD-40'))
fig.show()
