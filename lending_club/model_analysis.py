import pandas as pd
import plotly.express as px

def get_feature_importance(model, X: pd.DataFrame) -> pd.Series:
    """
    Given a tree-based model and a dataframe with column names,
    this will return a pandas series with the feature importances.
    """
    feats = pd.Series(model.feature_importances_, X.columns)
    feats = feats[feats>0].sort_values(ascending=False)
    return feats

def graph_importance(feats: pd.Series, model_name: str =''):
    """
    Given a pandas Series of feature importances and an optional model name,
    this will return a Plotly bar graph showing the importances.
    """
    fig = px.bar(feats[feats>0].sort_values(ascending=False), orientation='h', title=f'{model_name} Feature Importance',
            labels={
                     "index": "Feature",
                     "value": "Importance Value"
                 })
    fig.update_layout(showlegend=False) 
    return fig