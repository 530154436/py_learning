#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
@author:zhengchubin
@function:
"""
import pandas as pd
from config import DATA_DIR

def load_movie():
    """ 加载电影 """
    movie = pd.read_csv(DATA_DIR.joinpath('movie.csv'),
                        sep=',',
                        converters={'mid': str},
                        error_bad_lines=False)
    movie = movie.fillna('')
    print('movie', movie.shape, movie.columns)
    return movie


def load_genre():
    """ 电影风格 """
    genre = pd.read_csv(DATA_DIR.joinpath('genre.csv'),
                        sep=',',
                        converters={'gid': str},
                        error_bad_lines=False)
    genre = genre.fillna('')
    print('genre', genre.shape, genre.columns)
    return genre


def load_movie_to_genre():
    """ 电影-风格 """
    movie_to_genre = pd.read_csv(DATA_DIR.joinpath('movie_to_genre.csv'),
                                 sep=',',
                                 converters={'mid': str, 'gid': str})
    movie_to_genre = movie_to_genre.dropna()

    # movie = pd.merge(movie, movie_to_genre, on='mid', how='left')
    # movie = pd.merge(movie, genre, on='gid', how='left')
    print('movie_to_genre', movie_to_genre.shape, movie_to_genre.columns)
    return movie_to_genre


def load_person():
    """ 加载演员 """
    person = pd.read_csv(DATA_DIR.joinpath('person.csv'),
                        sep=',',
                        converters={'pid': str},
                        error_bad_lines=False)
    person = person.fillna('')
    print('person', person.shape, person.columns)
    return person


def load_person_to_movie():
    """ 加载演员-电影 """
    person_to_movie = pd.read_csv(DATA_DIR.joinpath('person_to_movie.csv'),
                                  sep=',',
                                  converters={'pid': str, 'mid': str},
                                  error_bad_lines=False)
    person_to_movie = person_to_movie.dropna()
    print('person_to_movie', person_to_movie.shape, person_to_movie.columns)
    return person_to_movie


def load_questions_template():
    """ 加载问题模板 """
    question_template = pd.read_excel(DATA_DIR.joinpath('questions', 'dataset.xlsx'))
    print('question_template', question_template.shape, question_template.columns)
    return question_template


if __name__ == '__main__':
    pd.set_option('display.width', 1000)  # 设置打印宽度
    pd.set_option('display.unicode.ambiguous_as_wide', True)
    pd.set_option('display.unicode.east_asian_width', True)
    pd.set_option('max_colwidth', 100)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    load_movie()
    load_genre()
    load_movie_to_genre()
    load_person()
    load_person_to_movie()
    load_questions_template()