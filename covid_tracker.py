from h2o_wave import main, app, Q, ui,data
import requests
import json
import random

response_API = requests.get(
    'https://www.hpb.health.gov.lk/api/get-current-statistical')
#print(response_API.status_code)
data2 = response_API.text
parse_json = json.loads(data2)

response_API_us = requests.get(
    'https://api.apify.com/v2/key-value-stores/moxA3Q0aZh5LosewB/records/LATEST?disableRedirect=true')
usData = response_API_us.text
parse_json_us = json.loads(usData)


response_API_india = requests.get(
    'https://api.apify.com/v2/key-value-stores/toDWvRj1JpTXiM8FF/records/LATEST?disableRedirect=true')
indiaData = response_API_india.text
parse_json_india = json.loads(indiaData)

response_API_brasil = requests.get('https://api.apify.com/v2/key-value-stores/TyToNta7jGKkpszMZ/records/LATEST?disableRedirect=true')
brasitData = response_API_brasil.text
parse_json_brasil = json.loads(brasitData)




update_date_time = parse_json['data']['update_date_time']
local_total_cases = parse_json['data']['local_total_cases']
local_new_cases = parse_json['data']['local_new_cases']
local_total_number_of_individuals_in_hospitals = parse_json[
    'data']['local_total_number_of_individuals_in_hospitals']
local_deaths = parse_json['data']['local_deaths']
local_new_deaths = parse_json['data']['local_new_deaths']
local_recovered = parse_json['data']['local_recovered']
local_active_cases = parse_json['data']['local_active_cases']
global_new_deaths = parse_json['data']['global_new_deaths']
global_new_cases = parse_json['data']['global_new_cases']
global_deaths = parse_json['data']['global_deaths']
global_total_cases = parse_json['data']['global_total_cases']
global_recovered = parse_json['data']['global_recovered']
total_pcr_testing_count = parse_json['data']['total_pcr_testing_count']
daily_pcr_testing_data = parse_json['data']['daily_pcr_testing_data']
total_antigen_testing_count = parse_json['data']['total_antigen_testing_count']
daily_antigen_testing_data = parse_json['data']['daily_antigen_testing_data']



@app('/covid')
async def serve(q: Q):
    print(q.args)
    if 'Local' in q.args:
        q.page['header1'] = ui.header_card(
            box='1 1 3 1',
            title='Local Covid Tracker',
            subtitle="Updated Time : "+update_date_time,

        )
        q.page['button'] = ui.form_card(box='8 1 1 1', items=[
            ui.button(name='Global', label='Global',primary=True),

           
        ])

        n = 150
        v = q.page.add('PCR', ui.plot_card(
            box='1 2 4 5',
            title='PCR Count',
            data=data('date pcr_count', n),
            plot=ui.plot([ui.mark(type='line', x_scale='time', x='=date',
                        y='=pcr_count', curve='smooth', y_min=0)])
        ))
       

        v.data = [(data['date'], int(data['pcr_count']))
                for data in daily_pcr_testing_data][:150]

        v = q.page.add('Antigen', ui.plot_card(
            box='5 2 4 5',
            title='Antigen Count',
            data=data('date pcr_count', n),
            plot=ui.plot([ui.mark(type='line', x_scale='time', x='=date',
                        y='=pcr_count', curve='smooth', y_min=0)])
        ))
  


        v.data = [(data['date'], int(data['antigen_count']))
                for data in daily_antigen_testing_data][:150]


        c = q.page.add('a1', ui.small_stat_card(
            box='1 7 1 1',
            title="Total cases",
            value=str(local_total_cases),
        ))
        c = q.page.add('a2', ui.small_stat_card(
            box='2 7 1 1',
            title="New cases",
            value=str(local_new_cases),
        ))
        c = q.page.add('a3', ui.small_stat_card(
            box='3 7 1 1',
            title="Total deaths",
            value=str(local_deaths),
        ))
        c = q.page.add('a4', ui.small_stat_card(
            box='4 7 1 1',
            title="New deaths",
            value=str(local_new_deaths),
        ))
        c = q.page.add('a5', ui.small_stat_card(
            box='5 7 1 1',
            title="Recovered",
            value=str(local_recovered),
        ))
        c = q.page.add('a6', ui.small_stat_card(
            box='6 7 1 1',
            title="Active cases",
            value=str(local_active_cases),

        ))


    else:
        q.page['header1'] = ui.header_card(
            box='1 1 3 1',
            title='Global Covid Tracker',
            subtitle="Updated Time : "+update_date_time,

        )
        q.page['button'] = ui.form_card(box='8 1 1 1', items=[
            ui.button(name='Local', label='Local'),
        ])
       
        us_reported_data = [(data['name'], data['casesReported'])
                            for data in parse_json_us['casesByState']]
        us_reported_data.sort(key=lambda s: s[1])
        us_reported_data= us_reported_data[::-1]
        n = 24
        v = q.page.add('PCR', ui.plot_card(
        box='1 2 4 5',
        title='Cases Reported in US',
        data=data('name casesReported',n),
        plot=ui.plot([ui.mark(coord='polar', type='interval', x='=name', y='=casesReported', y_min=0)])
        ))
        top_24 = us_reported_data[:24]
        random.shuffle(top_24)
        v.data = top_24



        brasil_data = [(data['state'], data['count'])
                       for data in parse_json_brasil['infectedByRegion']]
        brasil_data.sort(key=lambda s: s[1])
        brasil_data =brasil_data[::-1]
        n = 24
        v = q.page.add('Antigen', ui.plot_card(
            box='5 2 4 5',
            title='Cases Reported in Brasil',
            data=data('state count', n),
            plot=ui.plot([ui.mark(coord='polar', type='interval',
                         x='=state', y='=count', y_min=0)])
        ))

        top_24 = brasil_data[:24]
        random.shuffle(top_24)
        v.data =top_24



        c = q.page.add('a1', ui.small_stat_card(
            box='1 7 2 1',
            title="Total cases",
            value=str(global_total_cases),
        ))
        c = q.page.add('a2', ui.small_stat_card(
            box='3 7 2 1',
            title="New cases",
            value=str(global_new_cases),
        ))
        c = q.page.add('a3', ui.small_stat_card(
            box='5 7 2 1',
            title="Total deaths",
            value=str(global_deaths),
        ))
        c = q.page.add('a4', ui.small_stat_card(
            box='7 7 2 1',
            title="New deaths",
            value=str(global_new_deaths),
        ))
        c = q.page.add('a5', ui.small_stat_card(
            box='5 7 2 1',
            title="Recovered",
            value=str(global_recovered),
        ))
      
        c = q.page.add('a6', ui.small_stat_card(
            box='6 7 2 1',
            title="Active cases",
            value=str(local_active_cases),

        ))
        del q.page['a6']
    await q.page.save()
