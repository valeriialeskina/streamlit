import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache
def load_data():
    dfs= []
    for file in ['population_total.csv', 'life_expectancy_years.csv', 'ny_gnp_pcap_pp_cd.csv']:
        dataset = pd.read_csv(file).fillna(method = 'ffill', axis = 0).melt(id_vars='country', var_name='year').rename(columns={"value": file})#.set_index(['country', 'year'])
        dfs.append(dataset)
    df = pd.DataFrame(columns=['country','year'])
    df = pd.merge(dfs[2], dfs[1], how="left", on=['country','year'])
    dff = pd.merge(df, dfs[0], how="left", on=['country','year'])
    return dff.rename(columns={"population_total.csv": "population", 'life_expectancy_years.csv':'life_exp', 'ny_gnp_pcap_pp_cd.csv':'gnp'})

df = load_data()

st.title('Gapminder')


year = st.sidebar.slider('Year', min_value=int(df['year'].min()), max_value=int(df['year'].max()), step=1)

multiselect = st.sidebar.multiselect('Countries',pd.unique(df['country']))

subset = df.loc[(df.year==str(year)) & (df.country.isin(multiselect))]
st.write(subset)
fig, ax = plt.subplots()
ax.set(xscale="log")
ax.set_xlim([10**2, 10**5])

sns.scatterplot(data=subset, x="gnp", y="life_exp", size="population", legend='brief',hue='country', sizes = (subset.population.min()/1000000, subset.population.max()/1000000))
st.pyplot(fig)


