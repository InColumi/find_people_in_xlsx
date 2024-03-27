import pandas as pd
from pandas import DataFrame
from datetime import datetime


def convert(path):
    df: DataFrame = pd.read_excel(path)
    df['Дата и время визита'] = df['Дата и время визита'].apply(func=lambda x: datetime.strptime(x.split(' ')[0], '%d.%m.%Y'))
    return df


if __name__ == '__main__':
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    year_path = 'Информация за год.xlsx'
    year_data = convert(year_path)

    print('Year data: ', year_data.shape)
    date_in = year_data['Дата и время визита']
    summer_date = year_data.loc[(date_in > '2023-05-31') & (date_in < '2023-09-01')]
    another_date:DataFrame = year_data.loc[(date_in <= '2023-05-31') | (date_in >= '2023-09-01')]
    print('Summer: ', summer_date.shape)
    print('Another_date: ', another_date.shape)
    print('Summ: ', year_data.shape[0], '=' ,summer_date.shape[0] + another_date.shape[0])
    answer: DataFrame = another_date.loc[~another_date['ФИО пациента'].isin(summer_date['ФИО пациента'])]
    answer.drop(['Дата и время визита'], axis=1, inplace=True)
    grouped = answer.groupby(['ФИО пациента', 'Номер телефона']).sum()
    grouped.to_excel('answer.xlsx')
