import pandas as pd
import plotly.express as px
from sklearn.metrics import confusion_matrix

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

def output_confusion_matrix(model, X, y):
    """Given a model, a feature set, and a corresponding target, this will output a pretty confusion matrix"""
    y_pred = model.predict(X)
    cm = confusion_matrix(y, y_pred)
    cm_df = pd.DataFrame(cm, columns=['Pred: Charged Off', 'Pred: Fully Paid'], index=['True: Charged Off', 'True: Fully Paid'])
    return cm_df

def calculate_PnL_return(model, X, y, PnL_series):
    """
    When taking in a predicting model, the features, the target, and the Profit and Loss series,
    this function will return the return for that portfolio.
    """
    model_results = pd.Series(model.predict(X), index=X.index, name='prediction')
    df = pd.concat([X, y, model_results], axis=1)
    portfolio_df = df.loc[df['prediction']==1,:]
    full_df = portfolio_df.merge(PnL_series, how='inner', left_index=True, right_index=True)
    return full_df.PnL.sum()/full_df.loan_amnt.sum()