#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 21:47:37 2024

Created by Cary Colgan, cary.colgan13@imperial.ac.uk
"""
import numpy as np
import matplotlib.pyplot as plt

import pandas
from matplotlib.widgets import Button
from matplotlib.widgets import RadioButtons
import os

class Game:
    def __init__(self, 
                 decks_filedir = "./decks/",
                 #deck_file_location = './decks/test.csv',
                 #deck_file_location = './decks/intermedio_1_vocab.csv',
                 ):
        self.decks_filedir = decks_filedir
        #self.deck_file_location = deck_file_location
        self.button_text = ('Reveal',
                            'Skip',
                            'Bad',
                            'OK',
                            'Good'
                            )
        
        self.button_colours = ('C7',
                          'C0',
                          'C3',
                          'C1',
                          'C2')
        
        self.button_axes = ([0.4, 0.25, 0.2, 0.075],
                       [0.71, 0.25, 0.2, 0.075],
                       [0.09, 0.05, 0.2, 0.075],
                       [0.4, 0.05, 0.2, 0.075],
                       [0.71, 0.05, 0.2, 0.075]
                       )
        
        # initialise first window
        self.deck_selector()
        
    
    def deck_selector(self):
        """First screen to select decks
        
        on_clicked the next screen shown is main_gameplay
        """
        self.draw_frame()
        
        all_decks = self.find_decks(self.decks_filedir)
        
        all_deck_names = [name[:-4] for name in all_decks]
        
        
        # CHANGE HERE to load in all decks  
        # then generate new ones based off of categories
        # bad rpactice to store, just reuse load_deck method as more robust
        all_deck_sizes = self.find_deck_sizes(self.decks_filedir, all_decks)
        
        
        
        all_deck_names = [f"{deck_name}: {deck_size} words" for deck_name, deck_size 
                          in zip(all_deck_names, all_deck_sizes)]
        
        selector_axes = plt.axes([0.1, 0.1, 0.8, 0.8])
        self.selector_axes = selector_axes
        radio_button = RadioButtons(selector_axes,
                                    labels = all_deck_names,
                                    active = None)
        
        self.radio_button = radio_button       
        self.radio_button.on_clicked(self.clear_and_start_game)
    
    def find_decks(self, filedir):
        all_files_and_dirs = os.listdir(filedir)
        all_decks = [name for name in all_files_and_dirs if name[-4:] == ".csv"]
        return all_decks
    
    def find_deck_sizes(self, decks_filedir, all_decks):
        sizes = ["" for deck in all_decks]
        
        for idx, deck in enumerate(all_decks):
            deck_file_location = f"{decks_filedir}{deck}"
            deck = pandas.read_csv(deck_file_location)
            deck = deck.to_numpy(dtype=str)
            N_words = deck.shape[0]
            sizes[idx] = N_words
            
        return sizes
     
    def clear_and_start_game(self, selected_deck_label):
        # clear axes
        self.fig.clear()
        plt.close(self.fig)
        
        # set deck file location
        selected_deck_name = selected_deck_label.split(": ")[0]
        self.selected_deck_file_location = f"{self.decks_filedir}{selected_deck_name}.csv"
        
        # start proper gameplay
        self.main_gameplay()
    
        
    def main_gameplay(self):
        self.draw_frame()
        
        self.draw_progress_bar()
        self.draw_old_progress_bar()
        
        self.show_buttons()
        self.link_buttons()
        
        self.load_deck(self.selected_deck_file_location)
        self.set_deck_status()
        old_deck_status_file_location = self.gen_old_deck_status_file_location(self.selected_deck_file_location)
        self.load_old_deck_status(old_deck_status_file_location)
        
        self.draw_deck_status(self.deck_status, self.progress_bar_subfigure)
        self.draw_deck_status(self.old_deck_status, self.old_progress_bar_subfigure)
        
        self.choose_next_index_and_update_deck_status_and_display(event=False)
        
    
    # Initialisation
    # --------------
    def draw_frame(self):
        fig, ax = plt.subplots()
        self.fig, self.ax = fig, ax        
        self.ax.xaxis.set_ticks(())
        self.ax.yaxis.set_ticks(())        
        
    def draw_progress_bar(self):
        axes = [0.125, 0.9, 0.775, 0.0375]
        progress_bar_subfigure = self.fig.add_axes(axes)
        progress_bar_subfigure.xaxis.set_ticks(())
        progress_bar_subfigure.yaxis.set_ticks(())
        progress_bar_subfigure.set_ylabel('This time:', rotation=0)
        progress_bar_subfigure.yaxis.set_label_coords(-0.075, 0.05)
        self.progress_bar_subfigure = progress_bar_subfigure
        
        
    def draw_old_progress_bar(self):
        axes = [0.125, 0.95, 0.775, 0.0375]
        old_progress_bar_subfigure = self.fig.add_axes(axes)
        old_progress_bar_subfigure.xaxis.set_ticks(())
        old_progress_bar_subfigure.yaxis.set_ticks(()) 
        old_progress_bar_subfigure.set_ylabel('Last time:', rotation=0)
        old_progress_bar_subfigure.yaxis.set_label_coords(-0.075, 0.05)
        self.old_progress_bar_subfigure = old_progress_bar_subfigure
        
        
    def load_deck(self, selected_deck_file_location):
        selected_deck = pandas.read_csv(selected_deck_file_location)
        selected_deck = selected_deck.to_numpy(dtype=str)
        self.loaded_deck = selected_deck
        self.N_words = selected_deck.shape[0]
        self.indexes = list(range(self.N_words)) # this will get popped from
        
    def set_deck_status(self):
        loaded_deck = np.copy(self.loaded_deck)
        blank_status = np.array(['Skip'] * loaded_deck.shape[0])
        
        # dummy test
        #blank_status[1] = 'Good'
        #blank_status[2] = 'Bad'
        self.deck_status = np.hstack((loaded_deck, blank_status[:, np.newaxis]))


    def gen_old_deck_status_file_location(self, deck_file_location):
        everything_but_slash = deck_file_location.split('/')
        
        file_name_and_type = everything_but_slash[-1]
        file_name = file_name_and_type.split(".")[0]
        
        path_as_list = everything_but_slash[:-1]
        path_as_list.append("..") # go up a dir
        path_as_list.append("reports") # currect dir
        path_as_list.append(file_name + ".npy")
        
        old_deck_status_file_location = "/".join(path_as_list) # undo split
        return old_deck_status_file_location

    def load_old_deck_status(self, deck_status_location):
        try: 
            old_deck_status = np.load(deck_status_location)
            print(f"Loaded report from {deck_status_location}")
        except(FileNotFoundError, TypeError):
            old_deck_status = np.copy(self.deck_status)
            old_deck_status[:, -1] = 'Reveal'
            print(f"No old report found.")
        self.old_deck_status = old_deck_status
    
    
    def save_deck_status(self, deck_status_file_location):
        np.save(deck_status_file_location, self.deck_status, allow_pickle=False)
        print(f"Saved report to {deck_status_file_location}")
        
    
    
    def fractions_from_status_for_plot(self, deck):
        N = np.array([sum(deck[:, -1] == i) for i in self.button_text])
        fractions = N / np.sum(N)
        end_points = np.cumsum(fractions)
        start_points = np.array([0] + list(end_points))[:-1]
        return start_points, end_points
    
    def draw_deck_status(self, deck_status, progress_bar_subfigure):
        start_points, end_points = self.fractions_from_status_for_plot(deck_status)
        for start, end_point, colour in zip(start_points, end_points, self.button_colours):
            progress_bar_subfigure.axhspan(0, 1, start, end_point, color=colour)
    
    
    # Buttons
    # -------
    def show_buttons(self):
        self.fig.subplots_adjust(bottom=0.4)
        
        buttons = {}
        for axes, text, colour in zip(self.button_axes, self.button_text, self.button_colours):
            button_axes_subfigure = self.fig.add_axes(axes)
            buttons[text] = Button(button_axes_subfigure, text, color=colour)
        
        self.buttons = buttons
    
    def link_buttons(self):
        self.buttons['Reveal'].on_clicked(self.swap_question_and_answer)
        self.buttons['Skip'].on_clicked(self.choose_next_index_and_update_deck_status_and_display) 
        self.buttons['Bad'].on_clicked(self.choose_next_index_and_update_deck_status_and_display) 
        self.buttons['OK'].on_clicked(self.choose_next_index_and_update_deck_status_and_display) 
        self.buttons['Good'].on_clicked(self.choose_next_index_and_update_deck_status_and_display) 
    
    
    # Workflow
    # --------
    def delete_displayed(self):
        del self.ax.texts[-1]
        
    def select_next_index(self):
        if len(self.indexes) == 0:
            # game finished 
            old_deck_status_file_location = self.gen_old_deck_status_file_location(self.selected_deck_file_location)
            self.save_deck_status(old_deck_status_file_location)
            plt.close()
            raise Exception("Finished Deck.")
        
        self.question_answer_idx = 0 # always reset on new display
        next_term = np.random.choice(range(len(self.indexes)))
        self.curr_idx = self.indexes[next_term]
        self.indexes.pop(next_term)
        self.curr_word = self.loaded_deck[self.curr_idx, :][self.question_answer_idx] 

    
    def display_current_word(self):
        old_word_status = self.old_deck_status[self.curr_idx, -1]
        colour = self.button_colours[self.button_text.index(old_word_status)]
        
        self.curr_text_displayed = self.ax.text(0.5, 0.5, 
                     self.curr_word, 
                     horizontalalignment='center', 
                     verticalalignment='center',
                     size=27,
                     color=colour)
        plt.draw()
    
    def swap_question_answer_current_word(self):
        self.question_answer_idx = abs(self.question_answer_idx - 1)
        self.curr_word = self.loaded_deck[self.curr_idx, :][self.question_answer_idx] 

        
    def choose_next_index_and_update_deck_status_and_display(self, event):      
        if event is not False:
            # user has clicked
            
            # find button clicked by matching axes
            button_pressed = [button_name for button_name in self.buttons 
             if event.inaxes == self.buttons[button_name].ax][0]
            
            # update deck status
            self.deck_status[self.curr_idx, -1] = button_pressed
            
            # redraw progress bar  
            self.draw_deck_status(self.deck_status, self.progress_bar_subfigure)
            
            # remove displayed word
            self.delete_displayed()
            
        self.select_next_index()               
        self.display_current_word()

        
    def swap_question_and_answer(self, event):
        if event is not False:            
            # user has clicked
            self.delete_displayed() 
        self.swap_question_answer_current_word()
        self.display_current_word()
        

if __name__ == "__main__":
    new_game = Game()
    plt.show()

