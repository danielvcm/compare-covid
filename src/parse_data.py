import pandas as pd

class ParseData:
    UFS = ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO']
    REGIOES= ['Brasil','Norte', 'Nordeste', 'Centro-Oeste', 'Sul', 'Sudeste']

    def __init__(self, start_date, end_date) -> None:
        self.total_df = pd.read_csv('../../data/clean_data.csv')
        self.start_date = start_date
        self.end_date = end_date

    def get_data_with_metrics(self, df_uf):
        populacao = df_uf["populacaoTCU2019"].iloc[0]
        casos_periodo = df_uf["casosNovos"].sum()
        obitos_periodo = df_uf["obitosNovos"].sum()
        obitos_por_casos = obitos_periodo/casos_periodo*100
        casos_100_mil = casos_periodo/populacao*100000
        obitos_100_mil = obitos_periodo/populacao*100000
        linha = {"população": populacao,
                "casosPeríodo": casos_periodo,
                "óbitosPeríodo": obitos_periodo,
                "óbitosPorCasos": obitos_por_casos,
                "casosPorCemMilHab": casos_100_mil,
                "óbitosPorCemMilHab": obitos_100_mil}
        return linha

    def generate_states_results(self):
        df_parcial = self.total_df.loc[(self.total_df['data']>= self.start_date) & (self.total_df['data']<= self.end_date)]
        lista_resultados = []
        dict_br = {"UF": 'Brasil', 'região': "Brasil"}
        df_br = df_parcial.loc[(pd.isna(df_parcial["estado"]))]
        dict_br.update(self.get_data_with_metrics(df_br))
        lista_resultados.append(dict_br)
        for uf in self.UFS:
            df_uf = df_parcial.loc[(df_parcial["estado"]==uf)]
            dict_uf = {"UF": uf, "região": df_uf["regiao"].iloc[0]}
            dict_uf.update(self.get_data_with_metrics(df_uf))
            lista_resultados.append(dict_uf)
        df_resultados = pd.DataFrame.from_records(lista_resultados)
        return df_resultados

    def generate_regions_results(self, df_uf = pd.DataFrame()):
        lista_resultados = []
        if df_uf.empty:
            df_uf = self.generate_states_results()
        for regiao in self.REGIOES:
            df_reg = df_uf.loc[(df_uf["região"]==regiao)]
            dict_reg = {"região": regiao}
            dict_reg['população'] = df_reg['população'].sum()
            dict_reg['casosPeríodo'] = df_reg["casosPeríodo"].sum()
            dict_reg['óbitosPeríodo'] = df_reg["óbitosPeríodo"].sum()
            dict_reg['óbitosPorCasos'] = dict_reg['óbitosPeríodo']/dict_reg['casosPeríodo']*100
            dict_reg['casosPorCemMilHab'] = dict_reg['casosPeríodo']/dict_reg['população']*100000
            dict_reg['óbitosPorCemMilHab'] = dict_reg['óbitosPeríodo']/dict_reg['população']*100000
            lista_resultados.append(dict_reg)
        df_resultados = pd.DataFrame.from_records(lista_resultados)
        return df_resultados
