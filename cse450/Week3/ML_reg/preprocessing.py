#%% Imports
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
from xgboost import XGBRegressor
import geopandas as gpd

df = pd.read_csv('https://raw.githubusercontent.com/byui-cse/cse450-course/master/data/housing.csv')

#%%
def pre_processing(df_):
    
    # Add new features based off of pre-existing columns
    df_ = df_\
        .assign(
            year = lambda x: x.date.str.slice(0,4).astype(int),
            month = lambda x: x.date.str.slice(4,6).astype(int),
            day = lambda x: x.date.str.slice(4,6).astype(int),
            sqftlivXfloor = lambda x: x.sqft_living/x.floors,
            sqftliv15Xfloor = lambda x: x.sqft_living15/x.floors,
            sqftlotXfloor = lambda x: x.sqft_lot/x.floors,
            sqftlot15Xfloor = lambda x: x.sqft_lot15/x.floors,
            bathroomsXfloor = lambda x: x.bathrooms/x.floors,
            bedroomsXfloor = lambda x: x.bedrooms/x.floors,
            bedroomsXbath = lambda x: x.bedrooms/x.bathrooms
            )   

    # Make sure all infinities and NAs are removed from features above
    df_ = df_\
        .assign(
            sqftlivXfloor = lambda x: x.sqftlivXfloor.replace([np.inf,np.nan],0),
            sqftliv15Xfloor = lambda x: x.sqftliv15Xfloor.replace([np.inf,np.nan],0),
            sqftlotXfloor = lambda x: x.sqftlotXfloor.replace([np.inf,np.nan],0),
            sqftlot15Xfloor = lambda x: x.sqftlot15Xfloor.replace([np.inf,np.nan],0),
            bathroomsXfloor = lambda x: x.bathroomsXfloor.replace([np.inf,np.nan],0),
            bedroomsXfloor = lambda x: x.bedroomsXfloor.replace([np.inf,np.nan],0),
            bedroomsXbath = lambda x: x.bedroomsXbath.replace([np.inf,np.nan],0)
        )

    # Hot-encode zipcode, bedrooms, and bathrooms
    df_ = pd.concat([df_,
        pd.get_dummies(df_['zipcode'], prefix="zip_"),
        pd.get_dummies(df_['bedrooms'], prefix="bedrooms_"),
        pd.get_dummies(df_['bathrooms'], prefix="bathrooms_")], axis=1)\
        .drop(columns = ['date'])
    
    x1, y1 = 47.62893975463672, -122.31454386497492 #Coordinates for Seattle Rich area
    
    df_ = df_.assign(
        distance = lambda x: np.sqrt((x.lat - x1)**2 + (x.long - y1)**2)
    )

    # Make a fake df to join shapefiles to
    df_coords_ = df_\
        .pipe(gpd.GeoDataFrame, 
                geometry=gpd.points_from_xy(
                    df_["long"],df_["lat"]))\
        .filter(items = ["id","geometry"])

    ## Add ALAND and AWATER from WA 
    wa_gov = gpd\
        .read_file('shapes2/tl_2016_53_cousub.shp')\
        .set_crs('epsg:4269')\
        .filter(['ALAND','AWATER','geometry'])

    ## Join it to temp df
    wa_gov_join = df_coords_\
        .pipe(gpd.sjoin, 
                right_df = wa_gov, 
                how='left', 
                op="within")\
        .pipe(pd.get_dummies)\
        .drop(columns = ['geometry','index_right'])\
        .filter(['ALAND','AWATER'])   

    # Add urban density
    wa_urban = gpd\
        .read_file('shapes/edge_locale18_nces_WA.shp')\
        .set_crs('epsg:4269')\
        .filter(['LOCALE','geometry'])

    # Join to temp df
    wa_urban_join = df_coords_\
        .pipe(gpd.sjoin, 
                right_df = wa_urban, 
                how='left', 
                op="within")\
        .assign(
            LOCALE = lambda x: 
                x.LOCALE.fillna(0).astype(int))\
        .drop(columns = ['id','geometry','index_right'])
    
    # ACTUALLY JOIN TEMP DFs
    df_ = pd.concat([
            df_,
            wa_gov_join,
            wa_urban_join
            ], axis=1)\
        .pipe(pd.DataFrame)\
        .drop(columns = ['geometry'])
    
    # Weird Part, if dataset doesnt have all the columns, I'll make a dummy column with a zero
    df_cols = ['id', 'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors', 'waterfront', 'view', 'condition', 'grade', 'sqft_above', 'sqft_basement', 'yr_built', 'yr_renovated', 'zipcode', 'lat', 'long', 'sqft_living15', 'sqft_lot15', 'year', 'month', 'day', 'sqftlivXfloor', 'sqftliv15Xfloor',  'sqftlotXfloor', 'sqftlot15Xfloor', 'bathroomsXfloor',  'bedroomsXfloor', 'bedroomsXbath', 'distance', 'zip__98001',  'zip__98002', 'zip__98003', 'zip__98004', 'zip__98005', 'zip__98006', 'zip__98007', 'zip__98008', 'zip__98010', 'zip__98011', 'zip__98014', 'zip__98019', 'zip__98022', 'zip__98023', 'zip__98024', 'zip__98027', 'zip__98028', 'zip__98029', 'zip__98030', 'zip__98031', 'zip__98032', 'zip__98033', 'zip__98034', 'zip__98038', 'zip__98039', 'zip__98040', 'zip__98042', 'zip__98045', 'zip__98052', 'zip__98053', 'zip__98055', 'zip__98056', 'zip__98058', 'zip__98059', 'zip__98065', 'zip__98070', 'zip__98072', 'zip__98074', 'zip__98075', 'zip__98077', 'zip__98092', 'zip__98102', 'zip__98103', 'zip__98105', 'zip__98106', 'zip__98107', 'zip__98108', 'zip__98109', 'zip__98112', 'zip__98115', 'zip__98116', 'zip__98117', 'zip__98118', 'zip__98119', 'zip__98122', 'zip__98125', 'zip__98126', 'zip__98133', 'zip__98136', 'zip__98144', 'zip__98146', 'zip__98148', 'zip__98155', 'zip__98166', 'zip__98168', 'zip__98177', 'zip__98178', 'zip__98188', 'zip__98198', 'zip__98199', 'bedrooms__0', 'bedrooms__1', 'bedrooms__2', 'bedrooms__3', 'bedrooms__4', 'bedrooms__5', 'bedrooms__6', 'bedrooms__7', 'bedrooms__8', 'bedrooms__9', 'bedrooms__10', 'bedrooms__11', 'bedrooms__33', 'bathrooms__0.0', 'bathrooms__0.5', 'bathrooms__0.75', 'bathrooms__1.0', 'bathrooms__1.25', 'bathrooms__1.5', 'bathrooms__1.75', 'bathrooms__2.0', 'bathrooms__2.25', 'bathrooms__2.5', 'bathrooms__2.75', 'bathrooms__3.0', 'bathrooms__3.25', 'bathrooms__3.5', 'bathrooms__3.75', 'bathrooms__4.0', 'bathrooms__4.25', 'bathrooms__4.5', 'bathrooms__4.75', 'bathrooms__5.0', 'bathrooms__5.25', 'bathrooms__5.5', 'bathrooms__5.75', 'bathrooms__6.0', 'bathrooms__6.25', 'bathrooms__6.5', 'bathrooms__6.75', 'bathrooms__7.5', 'bathrooms__7.75', 'bathrooms__8.0', 'ALAND', 'AWATER', 'LOCALE']

    columns_notin_df= list(set(df_cols)-set(list(df_.columns)))

    if columns_notin_df:
        for i in range(len(columns_notin_df)):
            df_[columns_notin_df[i]] = 0 

    #Orders columns alphabetically
    df_ = df_.reindex(sorted(df_.columns), axis=1)
    
    return df_

#%% Pre Process Data
X = pre_processing(df.drop(columns = ['price']))
y = df["price"]

# Set and Prepare Model
reg = XGBRegressor(max_depth=5, learning_rate=0.30, objective="reg:squarederror", eval_metric="rmse")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.10, random_state=6)

# Fit Model
reg.fit(X_train, y_train)

# Create predictions
y_pred = reg.predict(X_test)

# Numbers for Training data
rmse, mae, r2 = mean_squared_error(y_test, y_pred, squared=False), mean_absolute_error(y_test, y_pred), r2_score(y_test, y_pred)

print("Root Mean Squared Error: ${:,.2f}".format(rmse))
print("Mean Absolute Error: ${:,.2f}".format(mae))
print("R Squared: {:.3f}".format(r2))


# Testing Holdout Mini Dataset
# Pre Process Holdout Mini
X_mh = pd.read_csv('https://raw.githubusercontent.com/byui-cse/cse450-course/master/data/housing_holdout_test_mini.csv')\
    .pipe(pre_processing)

y_mh = pd.read_csv("https://raw.githubusercontent.com/byui-cse/cse450-course/master/data/housing_holdout_test_mini_answers.csv")

# Create predictions
y_pred_mh = reg.predict(X_mh)

# Numbers for Holdout
rmse, mae, r2= mean_squared_error(y_mh, y_pred_mh, squared=False), mean_absolute_error(y_mh, y_pred_mh), r2_score(y_mh, y_pred_mh)

print("Root Mean Squared Error: ${:,.2f}".format(rmse))
print("Mean Absolute Error: ${:,.2f}".format(mae))
print("R Squared: {:.3f}".format(r2))



holdout = pd.read_csv("https://raw.githubusercontent.com/byui-cse/cse450-course/master/data/housing_holdout_test.csv")\
    .pipe(pre_processing)

holdout_pred = reg.predict(holdout)

pd.DataFrame(holdout_pred)\
    .rename(columns={0: "predictions"})\
    .to_csv("team_6_holdout_predictions.csv",index=False)

# Feature Importances
import xgboost as xgb
ax = xgb.plot_importance(reg, max_num_features=30, importance_type='weight')
fig = ax.figure
fig.set_size_inches(6, 6)



# sns.scatterplot(x=list(y_test), y=list(y_pred))
