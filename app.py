# import pckgs
import streamlit as st
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
from statistics import mean
import csv
import tempfile


title_1 = '<p style="font-family:Courier; color:Black; font-size: 60px; font-weight:bold;">Psychopy Data Reader</p>'
st.markdown(title_1, unsafe_allow_html=True)
st.text('Work hard... Play hard')

data = st.file_uploader("Upload a Dataset", type=["csv"])
results = {}

def reversals(l_values):
    '''function to calculate reversal happening on the staircaise'''
    l_reversals = []
    if len(l_values) < 3:
        return l_reversals
    # an initial state/trend is defined
    asc = False
    desc = True
    for idx, (key, value) in enumerate(zip(l_values, r_values)):
        if idx == 0 and value == 0: #We change inital state if first answer is wrong
            asc = True
            desc = False
        if idx == len(l_values) - 1:
            if (asc and r_values[-3:].all()) or (desc and value == 0):
                l_reversals.append([idx, key, value])
        elif (asc and l_values[idx+1] < l_values[idx]) or (desc and l_values[idx+1] > l_values[idx]): #a trend and then if a value goes agains the trend is considered reversal and the state of trend is changed
            desc, asc = asc, desc
            l_reversals.append([idx, key, value])
    return l_reversals   

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

if data is not None:
    df = pd.read_csv(data)
    
    with st.container():
        subtitle_2 = '<p style="font-family:Courier; color:Black; font-size: 40px; font-weight:bold;">Stage 2 = No noise</p>'
        st.markdown(subtitle_2, unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)

        with col1:

            s2_r1_trials = df['repkata1.keys'].loc[df['repkata1.keys'].isin(['right', 'left']) ].count()
            s2_r1_answers = df.loc[df['repkata1.keys'].isin(['right', 'left']), ['repkata1.keys', 'repkata1.corr']]
            s2_r1_errors = s2_r1_answers[s2_r1_answers['repkata1.corr'] == 0].value_counts()

            subheader_1 = '<p style="font-family:Courier; color:Black; font-size: 24px; font-weight:bold;">Round 1</p>'
            st.markdown(subheader_1, unsafe_allow_html=True)
            
            st.subheader(f'Total Trials \n {str(s2_r1_trials)}') 

            st.subheader('List Answers')
            st.write(s2_r1_answers)

            st.subheader('Total incorrect answers')
            st.write(s2_r1_errors)
            results.update({'stage2_1_trials' : [s2_r1_trials] , s2_r1_answers.columns[0] : [s2_r1_answers['repkata1.corr'].to_string(index=False)],s2_r1_answers.columns[1] : [s2_r1_answers['repkata1.keys'].to_string(index=False)] , 'srage2_1_incorrect' : [[s2_r1_errors]]})

     with col2:
            if 'repkata1bis.keys' in df:
                s2_r2_trials = df['repkata1bis.keys'].loc[df['repkata1bis.keys'].isin(['right', 'left']) ].count()
                s2_r2_answers = df.loc[df['repkata1bis.keys'].isin(['right', 'left']), ['repkata1bis.keys', 'repkata1bis.corr']]
                s2_r2_errors = s2_r2_answers[s2_r2_answers['repkata1bis.corr'] == 0].value_counts()

                if int(s2_r2_trials) > 1:

                    subheader_2 = '<p style="font-family:Courier; color:Black; font-size: 24px; font-weight:bold;">Round 2</p>'
                    st.markdown(subheader_2, unsafe_allow_html=True)
                    
                    st.subheader(f'Total Trials \n {str(s2_r2_trials)}') 

                    st.subheader('List Answers')
                    st.write(s2_r2_answers)

                    st.subheader('Total incorrect answers')
                    st.write(s2_r2_errors)
                    results.update({'stage2_2_trials' : [s2_r2_trials] , s2_r2_answers.columns[0] : [s2_r2_answers['repkata1bis.corr'].to_string(index=False)],s2_r2_answers.columns[1] : [s2_r2_answers['repkata1bis.keys'].to_string(index=False)] , 'srage2_2_incorrect' : [[s2_r2_errors]]})
                else: 
                    subheader_3 = '<p style="font-family:Courier; color:Black; font-size: 24px; font-weight:bold;">No Repetition needed</p>'
                    st.markdown(subheader_3, unsafe_allow_html=True)
            else:
                subheader_3 = '<p style="font-family:Courier; color:Black; font-size: 24px; font-weight:bold;">No Repetition needed</p>'
                st.markdown(subheader_3, unsafe_allow_html=True)
    
    with st.container():
        subtitle_3 = '<p style="font-family:Courier; color:Black; font-size: 40px; font-weight:bold;">Stage 3 = Noise</p>'
        st.markdown(subtitle_3, unsafe_allow_html=True)
        
        s3_r1_trials = df['repkata2.keys'].loc[df['repkata2.keys'].isin(['right', 'left']) ].count()
        s3_r1_answers = df.loc[df['repkata2.keys'].isin(['right', 'left']), ['repkata2.keys', 'repkata2.corr']]
        s3_r1_errors = s3_r1_answers[s3_r1_answers['repkata2.corr'] == 0].value_counts()
        
        st.subheader(f'Total Trials \n {str(s3_r1_trials)}') 

        st.subheader('List Answers')
        st.write(s3_r1_answers)

        st.subheader('Total incorrect answers')
        st.write(s3_r1_errors)
        results.update({'stage3_1_trials' : [s3_r1_trials] , s3_r1_answers.columns[0] : [s3_r1_answers['repkata2.corr'].to_string(index=False)],s3_r1_answers.columns[1] : [s3_r1_answers['repkata2.keys'].to_string(index=False)] , 'srage3_1_incorrect' : [[s3_r1_errors]]})

     with col2:
            if 'repkata2bis.keys' in df:
                s2_r2_trials = df['repkata2bis.keys'].loc[df['repkata2bis.keys'].isin(['right', 'left']) ].count()
                s2_r2_answers = df.loc[df['repkata2bis.keys'].isin(['right', 'left']), ['repkata2bis.keys', 'repkata2bis.corr']]
                s2_r2_errors = s2_r2_answers[s2_r2_answers['repkata2bis.corr'] == 0].value_counts()

                if int(s2_r2_trials) > 1:

                    subheader_2 = '<p style="font-family:Courier; color:Black; font-size: 24px; font-weight:bold;">Round 2</p>'
                    st.markdown(subheader_2, unsafe_allow_html=True)
                    
                    st.subheader(f'Total Trials \n {str(s2_r2_trials)}') 

                    st.subheader('List Answers')
                    st.write(s2_r2_answers)

                    st.subheader('Total incorrect answers')
                    st.write(s2_r2_errors)
                    results.update({'stage2_2_trials' : [s2_r2_trials] , s2_r2_answers.columns[0] : [s2_r2_answers['repkata2bis.corr'].to_string(index=False)],s2_r2_answers.columns[1] : [s2_r2_answers['repkata2bis.keys'].to_string(index=False)] , 'srage2_2_incorrect' : [[s2_r2_errors]]})
                else: 
                    subheader_3 = '<p style="font-family:Courier; color:Black; font-size: 24px; font-weight:bold;">No Repetition needed</p>'
                    st.markdown(subheader_3, unsafe_allow_html=True)
            else:
                subheader_3 = '<p style="font-family:Courier; color:Black; font-size: 24px; font-weight:bold;">No Repetition needed</p>'
                st.markdown(subheader_3, unsafe_allow_html=True)
                
    with st.container():
        subtitle_4 = '<p style="font-family:Courier; color:Black; font-size: 40px; font-weight:bold;">Stage 4 = Staircase</p>'
        st.markdown(subtitle_4, unsafe_allow_html=True)

        l_values = df.loc[df['trials_2.intensity'].isna() == False, 'trials_2.intensity'].reset_index(drop=True)
        r_values = df.loc[df['trials_2.response'].isna() == False, 'trials_2.response'].reset_index(drop=True)
        
        col1, col2 = st.columns(2)
        col = ['trials_2.thisTrialN', 'trials_2.intensity', 'trials_2.response']
        new_df = pd.DataFrame(reversals(l_values), columns=col)

        with col1:
            st.subheader('Full staircase')
            st.write(df.loc[df['trials_2.response'].isna() == False, ['trials_2.intensity','CorrectAns','trials_2.response']].reset_index(drop=True))
        
        with col2:
            total_s_trial = df['trials_2.thisTrialN'].loc[df['trials_2.thisTrialN'].isna() == False].count()
            st.subheader(f'Total Staircase Trials = {total_s_trial}')
            fig, ax = plt.subplots()
            ax.plot(l_values.index.to_list(), l_values )
            st.pyplot(fig)

    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            st.subheader('List of reversal values')
            st.dataframe(new_df)

        with col2:
            st.subheader('Mean of last reversals')
            st.write(f'Last two = {mean([i[1] for i in reversals(l_values)][-2:])}')
            st.write(f'Last three = {mean([i[1] for i in reversals(l_values)][-3:])}')
            st.write(f'Last four = {mean([i[1] for i in reversals(l_values)][-4:])}')
    
            st.subheader('Total incorrect answers')
            staircase_answers = df.loc[df['trials_2.response'].isna() == False, ['CorrectAns','trials_2.response']].reset_index(drop=True)
            staircas_incorrect = staircase_answers[staircase_answers['trials_2.response'] == 0.0].value_counts()
            st.write(staircas_incorrect)
            results.update({'staircase_trials' : [total_s_trial] , staircase_answers.columns[0] : [staircase_answers['CorrectAns'].to_string(index=False)],staircase_answers.columns[1] : [staircase_answers['trials_2.response'].to_string(index=False)] , 'staircase_incorrect' : [[staircas_incorrect]]})

            st.subheader('Total correct answers')
            staircase_answers = df.loc[df['trials_2.response'].isna() == False, ['CorrectAns','trials_2.response']].reset_index(drop=True)
            staircas_correct = staircase_answers[staircase_answers['trials_2.response'] == 1.0].value_counts()
            st.write(staircas_correct)
            results.update({'staircase_trials' : [total_s_trial] , staircase_answers.columns[0] : [staircase_answers['CorrectAns'].to_string(index=False)],staircase_answers.columns[1] : [staircase_answers['trials_2.response'].to_string(index=False)] , 'staircase_correct' : [[staircas_correct]]})

    with st.container():
        col1,col2,col3 = st.columns(3)

        with col2:
            results_df = pd.DataFrame.from_dict(results)

            csv = convert_df(results_df)

            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name=f'analysis_{data.name}',
                mime='text/csv')
