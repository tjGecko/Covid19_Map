# https://www.doh.wa.gov/Emergencies/Coronavirus
# https://docs.bokeh.org/en/latest/docs/gallery/texas.html

# import bokeh
# bokeh.sampledata.download()

from bokeh.io import show
from bokeh.models import CategoricalColorMapper
from bokeh.palettes import PiYG as colors
from bokeh.plotting import figure
import pandas as pd
from bokeh.sampledata.us_counties import data as counties
import time
import json
import os


class DataPlot:
    def __init__(self, config):
        self.d = config
        self.county_data = None
        self.state_counties = None
        self.county_xs = None
        self.county_ys = None
        self.county_names = None
        self.county_rates = None
        self.rate_categories = None

    def run(self):
        self._load_covid_data()
        self._init_viz_schema()
        self._plot_state_data()

    def _load_covid_data(self):
        import plots.Selenium_Scraper as ss
        scraper = ss.SeleniumScraper()
        self.county_data = scraper.load()

        filename = f'History_{time.time()}.json'
        abs_path = os.path.join(self.d['history_dir'], filename)

        with open(abs_path, 'w') as fout:
            json.dump(self.county_data, fout, indent=4, sort_keys=True)

        print(f'Wrote: {abs_path}')


    # def _load_covid_data(self):
    #     # dfs = pd.read_html(self.d['url'])
    #     rows = self.d['raw'].split('\n')
    #     self.county_data = {}
    #
    #     for idx, row in enumerate(rows):
    #         cols = row.split('\t')
    #
    #         if len(cols) < 3:
    #             continue
    #
    #         key = cols[0]
    #         if len(key) < 1:
    #             continue
    #
    #         cfg = {
    #             'Confirmed_Cases': int(cols[1]),
    #             'Deaths': cols[2],
    #         }
    #
    #         self.county_data[key] = cfg

    def _init_viz_schema(self):
        self.state_counties = {
            code: county for code, county in counties.items() if county["state"] == "wa"
        }

        self.county_xs = [county["lons"] for county in self.state_counties.values()]
        self.county_ys = [county["lats"] for county in self.state_counties.values()]

        self.county_names = [county['name'] for county in self.state_counties.values()]

        self.county_rates = []
        self.rate_categories = []

        for county_name in self.county_names:
            cfg = self.county_data.get(county_name, {'Confirmed_Cases': 0})
            val = cfg['Confirmed_Cases']
            self.county_rates.append(val)

            if val is 0:
                self.rate_categories.append('OK')
            elif 0 < val <= 10:
                self.rate_categories.append('Arriving')
            elif 10 < val <= 50:
                self.rate_categories.append('Warn')
            else:
                self.rate_categories.append('Severe')

    def _plot_state_data(self):
        factors = ['OK', 'Arriving', 'Warn', 'Severe']
        palette = [colors[4][0], colors[4][1], colors[4][2], colors[4][3]]
        color_mapper = CategoricalColorMapper(factors=factors, palette=palette)
        # color_mapper = LinearColorMapper(palette=palette)
        # color_mapper = LogColorMapper(palette=palette)

        viz_schema = dict(
            x=self.county_xs,
            y=self.county_ys,
            name=self.county_names,
            rate=self.county_rates,
            cats=self.rate_categories,
        )

        TOOLS = "pan,wheel_zoom,reset,hover,save"

        p = figure(
            title="WA State, Covid19 Cases",
            tools=TOOLS,
            x_axis_location=None,
            y_axis_location=None,
            plot_width=800,
            plot_height=500,
            tooltips=[
                ("Name", "@name"), ("Status", "@cats"), ("Confirmed Cases", "@rate"), ("(Long, Lat)", "($x, $y)")
            ])
        p.grid.grid_line_color = None
        p.hover.point_policy = "follow_mouse"

        p.patches('x', 'y', source=viz_schema,
                  fill_color={'field': 'cats', 'transform': color_mapper},
                  fill_alpha=0.7, line_color="white", line_width=0.5)

        show(p)


if __name__ == '__main__':


    raw = '''
Clark	1	0
Columbia	1	0
Grant	1	1
Grays Harbor	1	0
Island	3	0
Jefferson	1	0
King	328	32
Kitsap	3	0
Kittitas	3	0
Pierce	19	0
Skagit	3	0
Snohomish	133	4
Thurston	1	0
Whatcom	1	0
Yakima	2	0
    '''

    d = {
        'url': 'https://www.doh.wa.gov/Emergencies/Coronavirus',
        'raw': raw,
        'history_dir': 'C:/Users/TJ Hoeft/Python_Projects/Covid19/history'
    }

    plt = DataPlot(config=d)
    plt.run()


