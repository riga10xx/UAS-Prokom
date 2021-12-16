#import library

import streamlit as st
import time
import numpy as np
import pandas as pd
import altair as alt

import inspect
import textwrap
from collections import OrderedDict
import streamlit as st
from streamlit.logger import get_logger

from PIL import Image

#-------create function def-------------

page_bg_img = '''
<style>
body {
background-image: url("https://images.unsplash.com/photo-1491183672482-d0af0e44929d?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80");
background-size: cover;
}
</style>
'''

st.markdown(page_bg_img, unsafe_allow_html=True)

#home
def home():

    #box command
    st.sidebar.success("Please select the available features")
    
    image = Image.open('images.jpg')
    st.image(image, width=200)
    #desc
    st.markdown(

        """
        ### Harigama Putra
        ### 12220112 - Teknik Perminyakan
        Streamlit produksi minyak mentah. 
        \n
        """
        
    )

#No 1.A
def nomor1a():

    df1 = pd.read_json("kode_negara_lengkap.json")
    df2 = pd.read_csv("produksi_minyak_mentah.csv")
    df = pd.merge(df2,df1,left_on='kode_negara',right_on='alpha-3')

    data_negara = df["name"].unique().tolist()
    data_negara.sort()

    negara = st.sidebar.selectbox("Select country", data_negara)

    kode = df1[(df1["name"] == negara)]["alpha-3"].to_list()[0]
    df_states = df2[(df2.kode_negara == kode)].copy().set_index("tahun")
    st.subheader(f'Berikut adalah grafik berbentuk line dari negara {negara}.')

    origin = df[(df["name"] == negara)]
    
    chart = alt.Chart(origin).mark_line(opacity=1).encode(
        x='tahun:N',
        y='produksi'
    )
    st.altair_chart(chart, use_container_width=True)

    a = origin.set_index("tahun").rename(columns={"produksi": "Produksi"})["Produksi"]

#No 1.B
def fitur_b():

    #import & linking json with csv
    df = pd.read_json("kode_negara_lengkap.json")
    df_prod = pd.read_csv("produksi_minyak_mentah.csv")
    df_merge = pd.merge(df_prod,df,left_on='kode_negara',right_on='alpha-3')
    
    #sorting
    list_negara = df_merge["name"].unique().tolist()
    list_negara.sort()

    #command control streamlit
    jumlah_negara = st.sidebar.selectbox("Pilih negara", range(1, len(list_negara)), 9)
    tahun = st.sidebar.selectbox("Pilih tahun", range(1971, 2016), 44)

    st.subheader(f'{jumlah_negara} besar negara dengan jumlah produksi terbesar pada tahun {tahun}')

    res = df_merge[(df_merge.tahun == tahun)][["name", "produksi"]].sort_values(by=['produksi'], ascending=False).reset_index(drop=True)
    res.index += 1

    source = res.iloc[:jumlah_negara]
    
    #making graph with altair
    bars = alt.Chart(source).mark_bar().encode(
        x='produksi',
        y=alt.Y(
                "name",
                sort=alt.EncodingSortField(field="produksi", order="descending"),
                title="Negara",
            )
    )


    text = bars.mark_text(
        align='left',
        baseline='middle',
        color='white',
        dx=3 
    ).encode(
        text='produksi'
    )
    chart = (bars+text).configure_view(
    strokeWidth=0
)
    
    st.altair_chart(chart, use_container_width=True)
    st.dataframe(source.rename(columns={"name": "Negara", "produksi":"Jumlah Produksi"}))

#No 1.C
def fitur_c():

    #import & linking json with csv
    df = pd.read_json("kode_negara_lengkap.json")
    df_prod = pd.read_csv("produksi_minyak_mentah.csv")
    df_merge = pd.merge(df_prod,df,left_on='kode_negara',right_on='alpha-3')
    
    #sorting
    list_negara = df_merge["name"].unique().tolist()
    list_negara.sort()

    #command control streamlit
    jumlah_negara = st.sidebar.selectbox("Pilih negara", range(1, len(list_negara)), 9)

    st.subheader(f'{jumlah_negara} besar negara dengan jumlah produksi keseluruhan terbesar')

    res = df_merge[["name", "produksi"]].groupby(['name'])['produksi'].sum().reset_index().sort_values(by=['produksi'], ascending=False).reset_index(drop=True)
    res.index += 1

    source = res.iloc[:jumlah_negara]
    
    #making graph with altair
    bars = alt.Chart(source).mark_bar().encode(
        x='produksi',
        y=alt.Y(
                "name",
                sort=alt.EncodingSortField(field="produksi", order="descending"),
                title="Negara",
            )
    )


    text = bars.mark_text(
        align='left',
        baseline='middle',
        color='white',
        dx=3 
    ).encode(
        text='produksi'
    )
    chart = (bars+text).configure_view(
    strokeWidth=0
)
    
    st.altair_chart(chart, use_container_width=True)
    st.dataframe(source.rename(columns={"name": "Negara", "produksi":"Total Produksi"}))


#No 1.D
def fitur_d():

    #import & linking json with csv
    df = pd.read_json("kode_negara_lengkap.json")
    df_prod = pd.read_csv("produksi_minyak_mentah.csv")
    df_merge = pd.merge(df_prod,df,left_on='kode_negara',right_on='alpha-3')
    
    #sorting
    list_negara = df_merge["name"].unique().tolist()
    list_negara.sort()

    #command control streamlit
    tahun = st.sidebar.selectbox("Pilih tahun", range(1971, 2016), 44)

    total_produksi = df_merge.groupby(['name', 'kode_negara', 'region', 'sub-region'])['produksi'].sum().reset_index().sort_values(by=['produksi'], ascending=False).reset_index(drop=True)
    total_produksi_max = total_produksi[(total_produksi["produksi"] > 0)].iloc[0]
    total_produksi_min = total_produksi[(total_produksi["produksi"] > 0)].iloc[-1]
    total_produksi_nol = total_produksi[(total_produksi["produksi"] == 0)].sort_values(by=['name']).reset_index(drop=True)
    total_produksi_nol.index += 1

    produksi_tahun = df_merge[(df_merge["tahun"] == tahun)][['name', 'kode_negara', 'region', 'sub-region', 'produksi']].sort_values(by=['produksi'], ascending=False).reset_index(drop=True)
    produksi_tahun_max = produksi_tahun[(produksi_tahun["produksi"] > 0)].iloc[0]
    produksi_tahun_min = produksi_tahun[(produksi_tahun["produksi"] > 0)].iloc[-1]
    produksi_tahun_nol = produksi_tahun[(produksi_tahun["produksi"] == 0)].sort_values(by=['name']).reset_index(drop=True)
    produksi_tahun_nol.index += 1

    
    st.markdown(
        f"""
        #### Negara dengan total produksi keseluruhan tahun terbesar
        Negara: {total_produksi_max["name"]}\n
        Kode negara: {total_produksi_max["kode_negara"]}\n
        Region: {total_produksi_max["region"]}\n
        Sub-region: {total_produksi_max["sub-region"]}\n
        Jumlah produksi: {total_produksi_max["produksi"]}\n

        #### Negara dengan jumlah produksi terbesar pada tahun {tahun}  
        Negara: {produksi_tahun_max["name"]}\n
        Kode negara: {produksi_tahun_max["kode_negara"]}\n
        Region: {produksi_tahun_max["region"]}\n
        Sub-region: {produksi_tahun_max["sub-region"]}\n
        Jumlah produksi: {produksi_tahun_max["produksi"]}\n

        #### Negara dengan total produksi keseluruhan tahun terkecil
        Negara: {total_produksi_min["name"]}\n
        Kode negara: {total_produksi_min["kode_negara"]}\n
        Region: {total_produksi_min["region"]}\n
        Sub-region: {total_produksi_min["sub-region"]}\n
        Jumlah produksi: {total_produksi_min["produksi"]}\n

        #### Negara dengan jumlah produksi terkecil pada tahun {tahun}  
        Negara: {produksi_tahun_min["name"]}\n
        Kode negara: {produksi_tahun_min["kode_negara"]}\n
        Region: {produksi_tahun_min["region"]}\n
        Sub-region: {produksi_tahun_min["sub-region"]}\n
        Jumlah produksi: {produksi_tahun_min["produksi"]}\n
    """
    )
    st.markdown(
        """
        #### Negara dengan total produksi keseluruhan tahun sama dengan nol
        
    """
    )
    total_produksi_nol = total_produksi_nol.drop(['produksi'], axis=1).rename(columns={"name":"Negara", "kode_negara":"Kode Negara", "region":"Region", "sub-region":"Sub Region"})
    st.dataframe(total_produksi_nol)
    st.markdown(
        f"""
        #### Negara dengan jumlah produksi sama dengan nol pada tahun {tahun}
        
    """
    )
    produksi_tahun_nol = produksi_tahun_nol.drop(['produksi'], axis=1).rename(columns={"name":"Negara", "kode_negara":"Kode Negara", "region":"Region", "sub-region":"Sub Region"})
    st.dataframe(produksi_tahun_nol)


#fungsi fitur tambahan : membandingkan produksi antar 2 negara
def fitur_tambahan():

    #import & linking json with csv
    df = pd.read_json("kode_negara_lengkap.json")
    df_prod = pd.read_csv("produksi_minyak_mentah.csv")
    df_merge = pd.merge(df_prod,df,left_on='kode_negara',right_on='alpha-3')

    #sorting
    list_negara = df_merge["name"].unique().tolist()
    list_negara.sort()

    #command control streamlit
    negara1 = st.sidebar.selectbox("Pilih negara pertama", list_negara, 55)
    negara2 = st.sidebar.selectbox("Pilih negara kedua", list_negara, 75)

    x = df_merge.pivot_table('produksi', ['name'], 'tahun')
    data = x.loc[[negara1, negara2]].fillna(0)
    st.write(f"### Perbandingan 2 negara antara {negara1} dengan {negara2}")

    data = data.T.reset_index()
    data = pd.melt(data, id_vars=["tahun"]).rename(
                    columns={"tahun": "Tahun", "value": "Produksi", "name": "Negara"}
                )
    data['Tahun'] = data['Tahun'].apply(str)

    chart = (
                alt.Chart(data)
                .mark_line(opacity=1)
                .encode(
                    x="Tahun:T",
                    y=alt.Y("Produksi", stack=None),
                    color="Negara:N",
                )
            )
    st.altair_chart(chart, use_container_width=True)

#call function to app

LOGGER = get_logger(__name__)


FITUR = OrderedDict(
    [
        ("HOME", (home, None)),
        (
            "Fitur Nomor 1.a",
            (
                nomor1a,
                """
                Grafik jumlah produksi minyak mentah terhadap waktu (tahun) dari suatu negara
                """,
            ),
        ),
        (
            "Fitur Nomor 1.b",
            (
                fitur_b,
                """
                Negara dengan produksi minyak mentah terbesar pada suatu tahun
                """,
            ),
        ),
        (
            "Fitur Nomor 1.c",
            (
                fitur_c,
                """
                Negara dengan total produksi minyak mentah keseluruhan tahun terbesar
                """,
            ),
        ),
        (
            "Fitur Nomor 1.d",
            (
                fitur_d,
                """
                Summary
                """,
            ),
        ),
        (
            "Fitur tambahan",
            (
                fitur_tambahan,
                """
                Membandingkan produksi minyak mentah antar dua negara tiap tahunnya
                """,
            ),
        ),
    ]
)


def run():
    demo_name = st.sidebar.selectbox("Pilih fitur", list(FITUR.keys()), 0)
    demo = FITUR[demo_name][0]

    if demo_name == "HOME":
        pass
    else:
        st.markdown("# %s" % demo_name)
        description = FITUR[demo_name][1]
        if description:
            st.write(description)

        for i in range(10):
            st.empty()

    demo()


if __name__ == "__main__":
    run()