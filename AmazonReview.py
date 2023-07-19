import string
from collections import Counter
from bs4 import BeautifulSoup
import requests
import pandas as pd

#words that don't add meaning to string
stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
              "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
              "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these",
              "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do",
              "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while",
              "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before",
              "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again",
              "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
              "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
              "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

def article_helper(text) :
    #make string lower case
    lower_case = text.lower()
    #remove puncuation from string
    cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))
    
    #put each word into an array
    tokenized_words = cleaned_text.split()
    
    #remove stop_words and put words that matter into an array
    final_words = []
    for word in tokenized_words:
        if word not in stop_words:
            final_words.append(word)
    pos = 0
    neg = 0
    for word in final_words:
        if pos_neg(word) == "positive":
            pos += 1
        if pos_neg(word) == "negative":
            neg += 1
    #return if review is pos or neg
    if (pos > neg) :
        return "positive"
    if (neg > pos):
        return "negative"
    else :
        return "null"
def pos_neg(word):
    #check if emotion word is positive or negative
    with open('pos_list2.txt', 'r') as file:
        for line in file:
            if word == line[0:len(word)].lower():
                return "positive"
    with open('neg_list2.txt', 'r') as file:
        for line in file:
            if word == line[0:len(word)].lower():
                return "negative"
    return ""

def article_review(input) :
    custom_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'accept-language': 'en-GB,en;q=0.9',
    }
    proxies = {'http': 'http://190.64.18.177:80'} 
    url = input
    r = requests.get(url, headers = custom_headers, proxies=proxies)
    soup = BeautifulSoup(r.content, "html.parser")
    mydivs = soup.find_all("div", class_="article-body")
    pos = 0
    neg = 0
    for div in mydivs:
        text = div.text
        if article_helper(text) == "positive":
            pos += 1
        if article_helper(text) == "negative":
            neg += 1
    if (pos > neg) :
        return "positive"
    if (neg > pos):
        return "negative"
    else :
        return "null"
  

import pygame
import sys
import tkinter as tk
from tkinter import Tk

# Initialize Pygame
pygame.init()

# Initialize Tkinter
root = Tk()
root.withdraw()  # Hide the main Tkinter window

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 24

# Function to display text on the screen
def draw_text(surface, text, color, font_size, x, y):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

# Main function
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Article Review")

    input_text = ""
    result_text = ""
    clock = pygame.time.Clock()

    ctrl_pressed = False  # To keep track of the Ctrl key status

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    result_text = article_review(input_text)
                    input_text = ""
                elif event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    ctrl_pressed = True
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]  # Remove the last character from input_text
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                    ctrl_pressed = False
                elif event.key == pygame.K_v and ctrl_pressed:
                    clipboard_text = root.clipboard_get()
                    if clipboard_text:
                        input_text += clipboard_text

            elif event.type == pygame.TEXTINPUT:
                input_text += event.text

        screen.fill(WHITE)

        # Draw the textbox
        pygame.draw.rect(screen, BLACK, (100, 200, 600, 200))

        # Display the input_text in the textbox
        draw_text(screen, input_text, WHITE, FONT_SIZE, 110, 210)

        # Draw the result
        draw_text(screen, result_text, BLACK, FONT_SIZE, 110, 450)

        # Draw the "Enter" button
        pygame.draw.rect(screen, BLACK, (350, 450, 100, 50))
        draw_text(screen, "Enter", WHITE, FONT_SIZE, 360, 460)

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()





print(article_review("https://www.nbcnews.com/health/health-news/new-malaria-case-florida-brings-national-total-8-first-us-cases-20-yea-rcna94899"))