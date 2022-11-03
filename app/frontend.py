import streamlit as st
import pandas as pd
import numpy as np
import backend as backend

# load data
@st.cache
def load_data(filepath: str):
    return backend.read_csv(filepath)

fp = './data/kc_house_data.csv'
df = load_data(fp)

# Build UI
with st.sidebar:
    st.title('What are you looking for?')
    # intent = st.radio('I want to:', ['Buy', 'Sell'])
    budget = st.slider('Budget ($ in millions)',
                        min_value=float(df['price'].min()/1e6),
                        max_value=float(df['price'].max()/1e6 + 1),
                        value=(float(df['price'].min()/1e6 + 1),
                                float(df['price'].max()/1e6 - 1)
                            ),
                        step=0.1)
    sqft_living = st.slider('Livingspace (in hundreds of sqft)',
                            min_value=int(df['sqft_living'].min()/1e2),
                            max_value=int(df['sqft_living'].max()/1e2 + 1),
                            value=(int(df['sqft_living'].min()/1e2 + (df['sqft_living'].max()-df['sqft_living'].min())/1e2/2 - 10),
                                    int(df['sqft_living'].min()/1e2 + (df['sqft_living'].max()-df['sqft_living'].min())/1e2/2 + 10)
                                ),
                            step=1)
    
    bedrooms = st.slider('Bedrooms',
                min_value=int(df['bedrooms'].min()),
                max_value=int(df['bedrooms'].max()),
                value=(int(df['bedrooms'].min()),
                        int(df['bedrooms'].min() + 2)
                    ),
                step=1)
    
    bathrooms = st.slider('Bathrooms',
                min_value=int(df['bathrooms'].min()),
                max_value=int(df['bathrooms'].max()),
                value=(int(df['bathrooms'].min() + (df['bathrooms'].max()-df['bathrooms'].min())/2 - 1),
                        int(df['bathrooms'].min() + (df['bathrooms'].max()-df['bathrooms'].min())/2 + 1)
                    ),
                step=1)
    
    built = st.slider('Built between',
                min_value=int(df['yr_built'].min()),
                max_value=int(df['yr_built'].max()),
                value=(int(df['yr_built'].min() + (df['yr_built'].max()-df['yr_built'].min())/2 - 20),
                        int(df['yr_built'].min() + (df['yr_built'].max()-df['yr_built'].min())/2 + 20)
                    ),
                step=1)
    # waterfront = st.checkbox('Waterfront')
    # basement = st.checkbox('Basement')
    zipcodes = st.multiselect('Preferred zipcodes', df['zipcode'].unique())
    
    d = {#'intent': intent,
        'price': tuple(b*1e6 for b in budget),
        'sqft_living': tuple(s*1e2 for s in sqft_living),
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'yr_built': built,
        # 'waterfront': waterfront,
        # 'sqft_basement': basement,
        'zipcode': zipcodes}

    find = st.button('Show my recommendations')

if find:
    df_recommend = backend.recommendations(df=df,
                                        filter=d,
                                        specialBool={'waterfront': (1, 0), 
                                                        'sqft_basement': (np.nan,)
                                                        }
                                        )
    n_recs = df_recommend.shape[0]
    if n_recs == 0:
        st.error('No recommendations found :(')
        st.subheader('Oh no!')
    else:
        if n_recs > 100:
            st.warning(f'There are a lot of recommendations! Consider optimizing your filtering.')
        else: 
            if n_recs == 1: st.success(f'There is {n_recs} recommendation')
            if n_recs > 1: st.success(f'There are {n_recs} recommendations')
        st.subheader('Here are your recommendations:')
        n_recs = df_recommend.shape[0]
        st.dataframe(df_recommend)
        st.subheader('This is where you could live:')
        st.plotly_chart(backend.plot(df_recommend))