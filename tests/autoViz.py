import re
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot


class autoViz:
    """This class implements model visualization.
    
    Parameters
    ----------
    preprocess_dict : dict, default = None
        Value in ["reg","cls"]. The "reg" for regression problem, and "cls" for classification problem.

    report : df, default = None
        Should be set to "True" when using autoPipe module to build Pipeline Cluster Traveral Experiments.

    Example
    -------
    
    .. [Example]: 
    
    References
    ----------
    
    """
    def __init__(self,preprocess_dict = None,report = None ):
        self.DICT_PREPROCESSING = preprocess_dict
        self.dyna_report = report

    def clf_model_retrieval(self,metrics = None):
        """This function implements classification model retrieval visualization.
    
        Parameters
        ----------
        metrics : str, default = None
            Value in ["accuracy","precision","recall"].

        Example
        -------
        
        .. [Example] 
        
        References
        ----------
        
        """
        columns = ["Dataset","Encode_low_dimension","Encode_high_dimension","Winsorize","Scale"]
        df_pp = pd.DataFrame(columns=columns)

        for i in list(self.DICT_PREPROCESSING.keys()):
            row_pp = [i]
            s = self.DICT_PREPROCESSING[i]
            ext = re.search("Encoded Features:(.*)']", s).group(1)
            if "onehot_" in ext:
                row_pp.append('Low Dim_onehot')
            elif "label_" in ext:
                row_pp.append('Low Dim_label')
            else:
                row_pp.append('Low Dim_No Encoder')

            if "frequency_" in ext:
                row_pp.append('High Dim_frequency')
            elif "mean_" in ext:
                row_pp.append('High Dim_mean')
            else:
                row_pp.append('High Dim_No Encoder')

            row_pp.append(re.search('winsor_(.*)-Scaler', s).group(1))
            row_pp.append(re.search('winsor_0-Scaler_(.*)-- ', s).group(1))
            df_pp.loc[len(df_pp)] = row_pp

        if metrics == "accuracy":
            df_report_Accuracy = df_pp.merge(self.dyna_report[['Dataset','Accuracy']], how = 'left', on = 'Dataset')
            bins = [0, 0.70, 0.90, 1]
            labels = ["Low Accuracy","High Accuracy","Top Accuracy"]
            df_report_Accuracy['Level'] = pd.cut(df_report_Accuracy['Accuracy'], bins=bins, labels=labels)
            df_report_Accuracy['cnt'] = 1
            df_report_Accuracy.loc[df_report_Accuracy['Scale'] == 'None','Scale'] = "No Scaler"
            df_report_Accuracy['Scale'] = 'Scale_'+df_report_Accuracy['Scale']
            df_report_Accuracy['Winsorize'] = 'Winsorize_' + df_report_Accuracy['Winsorize']

            step1_df = df_report_Accuracy.groupby(['Encode_low_dimension','Dataset'], as_index=False)['cnt'].count().rename({"cnt":"Total","Dataset":"antecedentIndex","Encode_low_dimension":"consequentIndex"},axis = 1)[['antecedentIndex','consequentIndex','Total']]
            step2_df = df_report_Accuracy.groupby(['Encode_low_dimension','Encode_high_dimension'], as_index=False)['cnt'].count().rename({"cnt":"Total","Encode_low_dimension":"antecedentIndex","Encode_high_dimension":"consequentIndex"},axis = 1)[['antecedentIndex','consequentIndex','Total']]
            step3_df = df_report_Accuracy.groupby(['Encode_high_dimension','Winsorize'], as_index=False)['cnt'].count().rename({"cnt":"Total","Encode_high_dimension":"antecedentIndex","Winsorize":"consequentIndex"},axis = 1)[['antecedentIndex','consequentIndex','Total']]
            step4_df = df_report_Accuracy.groupby(['Winsorize','Scale'], as_index=False)['cnt'].count().rename({"cnt":"Total","Winsorize":"antecedentIndex","Scale":"consequentIndex"},axis = 1)[['antecedentIndex','consequentIndex','Total']]
            step5_df = df_report_Accuracy.groupby(['Scale','Level'], as_index=False)['cnt'].count().rename({"cnt":"Total","Scale":"antecedentIndex","Level":"consequentIndex"},axis = 1)[['antecedentIndex','consequentIndex','Total']].dropna()
            integrated_df = pd.concat([step1_df,step2_df,step3_df,step4_df,step5_df],axis = 0)

            label_df = pd.DataFrame(integrated_df['antecedentIndex'].append(integrated_df['consequentIndex']).drop_duplicates(),columns = {"label"})
            label_df['Number'] = label_df.reset_index().index
            label_list = list(label_df.label)

            source_df = pd.DataFrame(integrated_df['antecedentIndex'])
            source_df = source_df.merge(label_df, left_on=['antecedentIndex'], right_on = ['label'],how = 'left')
            source_list = list(source_df['Number'])

            target_df = pd.DataFrame(integrated_df['consequentIndex'])
            target_df = target_df.merge(label_df, left_on=['consequentIndex'], right_on = ['label'],how = 'left')
            target_list = list(target_df['Number'])

            value_list = [int(i) for i in list(integrated_df.Total)]

            fig = go.Figure(data=[go.Sankey(
                node = dict(
                pad = 15,
                thickness = 10,
                line = dict(color = 'rgb(25,100,90)', width = 0.5),
                label = label_list,
                color = 'rgb(71,172,55)'
                ),
                link = dict(
                source = source_list, 
                target = target_list,
                value = value_list
            ))])

            fig.update_layout(title = f'Pipeline Cluster Traversal Experiments - autoViz {metrics} Retrieval Diagram <a href="https://www.linkedin.com/in/lei-tony-dong/"> ©Tony Dong</a>', font_size=8)
            plot(fig)

        elif metrics == "precision":
            df_report_Precision = df_pp.merge(self.dyna_report[['Dataset','Precision']], how = 'left', on = 'Dataset')
            bins = [0, 0.70, 0.90, 1]
            labels = ["Low Precision","High Precision","Top Precision"]
            df_report_Precision['Level'] = pd.cut(df_report_Precision['Precision'], bins=bins, labels=labels)
            df_report_Precision['cnt'] = 1
            df_report_Precision.loc[df_report_Precision['Scale'] == 'None','Scale'] = "No Scaler"
            df_report_Precision['Scale'] = 'Scale_'+df_report_Precision['Scale']
            df_report_Precision['Winsorize'] = 'Winsorize_' + df_report_Precision['Winsorize']
            
            step1_df = df_report_Precision.groupby(['Encode_low_dimension','Dataset'], as_index=False)['cnt'].count().rename({"cnt":"Total","Dataset":"antecedentIndex","Encode_low_dimension":"consequentIndex"},axis = 1)[['antecedentIndex','consequentIndex','Total']]
            step2_df = df_report_Precision.groupby(['Encode_low_dimension','Encode_high_dimension'], as_index=False)['cnt'].count().rename({"cnt":"Total","Encode_low_dimension":"antecedentIndex","Encode_high_dimension":"consequentIndex"},axis = 1)[['antecedentIndex','consequentIndex','Total']]
            step3_df = df_report_Precision.groupby(['Encode_high_dimension','Winsorize'], as_index=False)['cnt'].count().rename({"cnt":"Total","Encode_high_dimension":"antecedentIndex","Winsorize":"consequentIndex"},axis = 1)[['antecedentIndex','consequentIndex','Total']]
            step4_df = df_report_Precision.groupby(['Winsorize','Scale'], as_index=False)['cnt'].count().rename({"cnt":"Total","Winsorize":"antecedentIndex","Scale":"consequentIndex"},axis = 1)[['antecedentIndex','consequentIndex','Total']]
            step5_df = df_report_Precision.groupby(['Scale','Level'], as_index=False)['cnt'].count().rename({"cnt":"Total","Scale":"antecedentIndex","Level":"consequentIndex"},axis = 1)[['antecedentIndex','consequentIndex','Total']].dropna()
            integrated_df = pd.concat([step1_df,step2_df,step3_df,step4_df,step5_df],axis = 0)

            label_df = pd.DataFrame(integrated_df['antecedentIndex'].append(integrated_df['consequentIndex']).drop_duplicates(),columns = {"label"})
            label_df['Number'] = label_df.reset_index().index
            label_list = list(label_df.label)

            source_df = pd.DataFrame(integrated_df['antecedentIndex'])
            source_df = source_df.merge(label_df, left_on=['antecedentIndex'], right_on = ['label'],how = 'left')
            source_list = list(source_df['Number'])

            target_df = pd.DataFrame(integrated_df['consequentIndex'])
            target_df = target_df.merge(label_df, left_on=['consequentIndex'], right_on = ['label'],how = 'left')
            target_list = list(target_df['Number'])

            value_list = [int(i) for i in list(integrated_df.Total)]

            fig = go.Figure(data=[go.Sankey(
                node = dict(
                pad = 15,
                thickness = 10,
                line = dict(color = 'rgb(25,100,90)', width = 0.5),
                label = label_list,
                color = 'rgb(71,172,55)'
                ),
                link = dict(
                source = source_list, 
                target = target_list,
                value = value_list
            ))])

            fig.update_layout(title = f'Pipeline Cluster Traversal Experiments - autoViz {metrics} Retrieval Diagram <a href="https://www.linkedin.com/in/lei-tony-dong/"> ©Tony Dong</a>', font_size=8)
            plot(fig)

        elif metrics == "recall":
            df_report_Recall = df_pp.merge(dyna_report[['Dataset','Recall']], how = 'left', on = 'Dataset')
            bins = [0, 0.70, 0.90, 1]
            labels = ["Low Recall","High Recall","Top Recall"]
            df_report_Recall['Level'] = pd.cut(df_report_Recall['Recall'], bins=bins, labels=labels)
            df_report_Recall['cnt'] = 1
            df_report_Recall.loc[df_report_Recall['Scale'] == 'None','Scale'] = "No Scaler"
            df_report_Recall['Scale'] = 'Scale_'+df_report_Recall['Scale']
            df_report_Recall['Winsorize'] = 'Winsorize_' + df_report_Recall['Winsorize']

            step1_df = df_report_Recall.groupby(['Encode_low_dimension','Dataset'], as_index=False)['cnt'].count().rename({"cnt":"Total","Dataset":"antecedentIndex","Encode_low_dimension":"consequentIndex"},axis = 1)[['antecedentIndex','consequentIndex','Total']]
            step2_df = df_report_Recall.groupby(['Encode_low_dimension','Encode_high_dimension'], as_index=False)['cnt'].count().rename({"cnt":"Total","Encode_low_dimension":"antecedentIndex","Encode_high_dimension":"consequentIndex"},axis = 1)[['antecedentIndex','consequentIndex','Total']]
            step3_df = df_report_Recall.groupby(['Encode_high_dimension','Winsorize'], as_index=False)['cnt'].count().rename({"cnt":"Total","Encode_high_dimension":"antecedentIndex","Winsorize":"consequentIndex"},axis = 1)[['antecedentIndex','consequentIndex','Total']]
            step4_df = df_report_Recall.groupby(['Winsorize','Scale'], as_index=False)['cnt'].count().rename({"cnt":"Total","Winsorize":"antecedentIndex","Scale":"consequentIndex"},axis = 1)[['antecedentIndex','consequentIndex','Total']]
            step5_df = df_report_Recall.groupby(['Scale','Level'], as_index=False)['cnt'].count().rename({"cnt":"Total","Scale":"antecedentIndex","Level":"consequentIndex"},axis = 1)[['antecedentIndex','consequentIndex','Total']].dropna()
            integrated_df = pd.concat([step1_df,step2_df,step3_df,step4_df,step5_df],axis = 0)

            label_df = pd.DataFrame(integrated_df['antecedentIndex'].append(integrated_df['consequentIndex']).drop_duplicates(),columns = {"label"})
            label_df['Number'] = label_df.reset_index().index
            label_list = list(label_df.label)

            source_df = pd.DataFrame(integrated_df['antecedentIndex'])
            source_df = source_df.merge(label_df, left_on=['antecedentIndex'], right_on = ['label'],how = 'left')
            source_list = list(source_df['Number'])

            target_df = pd.DataFrame(integrated_df['consequentIndex'])
            target_df = target_df.merge(label_df, left_on=['consequentIndex'], right_on = ['label'],how = 'left')
            target_list = list(target_df['Number'])

            value_list = [int(i) for i in list(integrated_df.Total)]

            fig = go.Figure(data=[go.Sankey(
                node = dict(
                pad = 15,
                thickness = 10,
                line = dict(color = 'rgb(25,100,90)', width = 0.5),
                label = label_list,
                color = 'rgb(71,172,55)'
                ),
                link = dict(
                source = source_list, 
                target = target_list,
                value = value_list
            ))])

            fig.update_layout(title = f'Pipeline Cluster Traversal Experiments - autoViz {metrics} Retrieval Diagram <a href="https://www.linkedin.com/in/lei-tony-dong/"> ©Tony Dong</a>', font_size=8)
            plot(fig)



