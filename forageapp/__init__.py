from flask import Flask
from forageapp.config import Config
import pandas as pd
import geopandas as gpd
import os

PRODUCT_GEO_PATH = os.path.join('forageapp', 'static', 'tracts')

tract_table = pd.read_csv(os.path.join(PRODUCT_GEO_PATH, 'tract_table.csv'))
tract_table['GEOID'] = tract_table['GEOID'].astype(str).apply(lambda x: x.zfill(11))
tract_table = tract_table.set_index('GEOID')
city_table = tract_table['city']
tract_table = tract_table.drop(columns=['city'])

polygons = gpd.read_file(os.path.join(PRODUCT_GEO_PATH, 'polygons.geojson'))
polygons['GEOID'] = polygons['GEOID'].astype(str).apply(lambda x: x.zfill(11))
polygons = polygons.set_index('GEOID')

embedding_df = pd.read_csv(os.path.join(PRODUCT_GEO_PATH, 'embedding_df.csv'))
embedding_df['GEOID'] = embedding_df['GEOID'].astype(str).apply(lambda x: x.zfill(11))
embedding_df = embedding_df.set_index('GEOID')


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)


    #from forageapp.users.routes import users
    from forageapp.product.routes import product
    from forageapp.landing.routes import landing

    #app.register_blueprint(users)
    app.register_blueprint(product)
    app.register_blueprint(landing)

    return app
