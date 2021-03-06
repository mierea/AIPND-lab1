#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# */AIPND/intropylab-classifying-images/check_images.py
#                                                                             
# TODO: 0. Fill in your information in the programming header below
# PROGRAMMER: Ciprian M.
# DATE CREATED: 07/08/2018 23:18
# REVISED DATE:             <=(Date Revised - if any)
# REVISED DATE: 05/14/2018 - added import statement that imports the print 
#                           functions that can be used to check the lab
# PURPOSE: Check images & report results: read them in, predict their
#          content (classifier), compare prediction to actual value labels
#          and output results
#
# Use argparse Expected Call with <> indicating expected user input:
#      python check_images.py --dir <directory with images> --arch <model>
#             --dogfile <file that contains dognames>
#   Example call:
#    python check_images.py --dir pet_images/ --arch vgg --dogfile dognames.txt
##

# Imports python modules
import argparse
from time import time, sleep
from os import listdir

# Imports classifier function for using CNN to classify images 
from classifier import classifier 

# Imports print functions that check the lab
from print_functions_for_lab_checks import *

# Main program function defined below
def main():
    # TODO: 1. Define start_time to measure total program runtime by
    # collecting start time
    start_time = time()
    
    # TODO: 2. Define get_input_args() function to create & retrieve command
    # line arguments
    in_arg = get_input_args()
    
    # TODO: 3. Define get_pet_labels() function to create pet image labels by
    # creating a dictionary with key=filename and value=file label to be used
    # to check the accuracy of the classifier function
    answers_dic = get_pet_labels(in_arg.dir)

    # TODO: 4. Define classify_images() function to create the classifier 
    # labels with the classifier function uisng in_arg.arch, comparing the 
    # labels, and creating a dictionary of results (result_dic)
    result_dic = classify_images(in_arg.dir, answers_dic, in_arg.arch)
    
    # TODO: 5. Define adjust_results4_isadog() function to adjust the results
    # dictionary(result_dic) to determine if classifier correctly classified
    # images as 'a dog' or 'not a dog'. This demonstrates if the model can
    # correctly classify dog images as dogs (regardless of breed)
    adjust_results4_isadog(result_dic, in_arg.dogfile)

    
    # TODO: 6. Define calculates_results_stats() function to calculate
    # results of run and puts statistics in a results statistics
    # dictionary (results_stats_dic)
    results_stats_dic = calculates_results_stats(result_dic)

    # TODO: 7. Define print_results() function to print summary results, 
    # incorrect classifications of dogs and breeds if requested.
    print_results(result_dic, results_stats_dic, in_arg.arch, True, True)

    # TODO: 1. Define end_time to measure total program runtime
    # by collecting end time
    end_time = time()

    # TODO: 1. Define tot_time to computes overall runtime in
    # seconds & prints it in hh:mm:ss format
    tot_time = end_time - start_time
    print("\n** Total Elapsed Runtime:", convertTime(tot_time))

def convertTime(time_passed):
    hours   = int((time_passed/3600))
    minutes = int(((time_passed % 3600) / 60))
    seconds = int(((time_passed % 3600) % 60))
    return ("{}:{}:{}".format(hours, minutes, seconds))


# TODO: 2.-to-7. Define all the function below. Notice that the input 
# paramaters and return values have been left in the function's docstrings. 
# This is to provide guidance for acheiving a solution similar to the 
# instructor provided solution. Feel free to ignore this guidance as long as 
# you are able to acheive the desired outcomes with this lab.

def get_input_args():
    """
    Retrieves and parses the command line arguments created and defined using
    the argparse module. This function returns these arguments as an
    ArgumentParser object. 
     3 command line arguements are created:
       dir - Path to the pet image files(default- 'pet_images/')
       arch - CNN model architecture to use for image classification(default-
              pick any of the following vgg, alexnet, resnet)
       dogfile - Text file that contains all labels associated to dogs(default-
                'dognames.txt'
    Parameters:
     None - simply using argparse module to create & store command line arguments
    Returns:
     parse_args() -data structure that stores the command line arguments object  
    """
    parser = argparse.ArgumentParser()
    # dir - Path to the pet image files(default- 'pet_images/')
    parser.add_argument('--dir', type = str, default = 'pet_images/', help = 'Path to the pet image files(default- \'pet_images/\')');
    # arch - CNN model architecture to use for image classification(default- pick any of the following vgg, alexnet, resnet)
    parser.add_argument('--arch', type = str, default = 'vgg', help = 'CNN model architecture to use for image classification - vgg / alexnet / resnet (default- vgg)');
    # dogfile - Text file that contains all labels associated to dogs(default-'dognames.txt')
    parser.add_argument('--dogfile', type = str, default = 'dognames.txt', help = 'Text file that contains all labels associated to dogs(default \'dognames.txt\')');
    return parser.parse_args()


def get_pet_labels(image_dir):
    """
    Creates a dictionary of pet labels based upon the filenames of the image 
    files. Reads in pet filenames and extracts the pet image labels from the 
    filenames and returns these label as petlabel_dic. This is used to check 
    the accuracy of the image classifier model.
    Parameters:
     image_dir - The (full) path to the folder of images that are to be
                 classified by pretrained CNN models (string)
    Returns:
     petlabels_dic - Dictionary storing image filename (as key) and Pet Image
                     Labels (as value)  
    """
    # Retrieve the filenames from image_dir
    filename_list = listdir(image_dir)
    # Create petlabels_dic empty dictionary
    petlabels_dic = dict()
    for index in range(len(filename_list)):
        if filename_list[index] not in petlabels_dic:
            label_value = ""
            for word in filename_list[index].lower().split('_'):
                if word.isalpha():
                    label_value += word + " "
            petlabels_dic[filename_list[index]] = label_value.strip()
        else:
            print("Warning: Duplicate files exist in directory", filename_list[index])
    return petlabels_dic


def classify_images(images_dir, petlabel_dic, model):
    """
    Creates classifier labels with classifier function, compares labels, and 
    creates a dictionary containing both labels and comparison of them to be
    returned.
     PLEASE NOTE: This function uses the classifier() function defined in 
     classifier.py within this function. The proper use of this function is
     in test_classifier.py Please refer to this program prior to using the 
     classifier() function to classify images in this function. 
     Parameters: 
      images_dir - The (full) path to the folder of images that are to be
                   classified by pretrained CNN models (string)
      petlabel_dic - Dictionary that contains the pet image(true) labels
                     that classify what's in the image, where its' key is the
                     pet image filename & it's value is pet image label where
                     label is lowercase with space between each word in label 
      model - pretrained CNN whose architecture is indicated by this parameter,
              values must be: resnet alexnet vgg (string)
     Returns:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)   where 1 = match between pet image and 
                    classifer labels and 0 = no match between labels
    """
    results_dic = dict()

    for key, value in petlabel_dic.items():
        image_classification = classifier(images_dir + key, model).lower().strip()
        if value in image_classification.split(", "):
            results_dic[key] = [value, image_classification, 1]
        else:
            found = False
            for label in image_classification.split(", "):
                word = label.split(" ")
                if (not found) and value in word:
                    found = True
                    results_dic[key] = [value, image_classification, 1]
                    break
            if not found:
                results_dic[key] = [value, image_classification, 0]
    # print(results_dic)
    return results_dic
    


def adjust_results4_isadog(results_dic, dogsfile):
    """
    Adjusts the results dictionary to determine if classifier correctly 
    classified images 'as a dog' or 'not a dog' especially when not a match. 
    Demonstrates if model architecture correctly classifies dog images even if
    it gets dog breed wrong (not a match).
    Parameters:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)  where 1 = match between pet image and 
                            classifer labels and 0 = no match between labels
                    --- where idx 3 & idx 4 are added by this function ---
                    idx 3 = 1/0 (int)  where 1 = pet image 'is-a' dog and 
                            0 = pet Image 'is-NOT-a' dog. 
                    idx 4 = 1/0 (int)  where 1 = Classifier classifies image 
                            'as-a' dog and 0 = Classifier classifies image  
                            'as-NOT-a' dog.
     dogsfile - A text file that contains names of all dogs from ImageNet 
                1000 labels (used by classifier model) and dog names from
                the pet image files. This file has one dog name per line
                dog names are all in lowercase with spaces separating the 
                distinct words of the dogname. This file should have been
                passed in as a command line argument. (string - indicates 
                text file's name)
    Returns:
           None - results_dic is mutable data type so no return needed.
    """          
    dognames_dic = dict()
    with open(dogsfile) as f:
        for line in f:
            if line.rstrip() in dognames_dic:
                print("Warning! Duplicate dogname in dognames_dic " + line)
            else:
                dognames_dic[line.rstrip()] = 1
    # print(dognames_dic)
    for key in results_dic:
        # pet image label was found in dognames dic => is a dog
        if results_dic[key][0] in dognames_dic:
            # classifier label is in dognames_dic => is a dog
            # append 1,1 because both labels are dogs
            if results_dic[key][1] in dognames_dic:
                results_dic[key].extend((1,1)) 
            else:
                # classifier image is not in dognames_dic => is not a dog
                # append 1,0
                results_dic[key].extend([1,0])
        # pet image label is not in dognames_dic => not a dog
        else:
            # classifier image is a dog
            if results_dic[key][1] in dognames_dic:
                results_dic[key].extend((0,1))
            # classifier image is not a dog
            else:
                results_dic[key].extend((0,0))
    


def calculates_results_stats(results_dic):
    """
    Calculates statistics of the results of the run using classifier's model 
    architecture on classifying images. Then puts the results statistics in a 
    dictionary (results_stats) so that it's returned for printing as to help
    the user to determine the 'best' model for classifying images. Note that 
    the statistics calculated as the results are either percentages or counts.
    Parameters:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)  where 1 = match between pet image and 
                            classifer labels and 0 = no match between labels
                    idx 3 = 1/0 (int)  where 1 = pet image 'is-a' dog and 
                            0 = pet Image 'is-NOT-a' dog. 
                    idx 4 = 1/0 (int)  where 1 = Classifier classifies image 
                            'as-a' dog and 0 = Classifier classifies image  
                            'as-NOT-a' dog.
    Returns:
     results_stats - Dictionary that contains the results statistics (either a
                     percentage or a count) where the key is the statistic's 
                     name (starting with 'pct' for percentage or 'n' for count)
                     and the value is the statistic's value 
    """
    results_stats = dict()
    
    n_number_of_images = len(results_dic) # Z - done
    n_correct_dogs     = 0 # A
    n_dog_images       = 0 # B
    n_correct_non_dog  = 0 # C
    n_non_dogs         = 0 # D
    n_correct_breed    = 0 # E
    n_label_matches    = 0 # Y
    
    pct_correct_dogs     = 0.0
    pct_correct_non_dogs = 0.0
    pct_correct_breed    = 0.0
    pct_label_matches    = 0.0
    
    for key in results_dic:
        # A
        if results_dic[key][3] == 1 and results_dic[key][4] == 1:
            n_correct_dogs += 1
        # B
        if results_dic[key][3] == 1:
            n_dog_images += 1
        # C
        if results_dic[key][3] == 0 and results_dic[key][4] == 0:
            n_correct_non_dog += 1
        # D
        if results_dic[key][3] == 0:
            n_non_dogs += 1
        # E
        if results_dic[key][3] == 1 and results_dic[key][2] == 1:
            n_correct_breed += 1        
        # Y
        if results_dic[key][2] == 1:
            n_label_matches += 1
    
    if n_dog_images > 0:
        pct_correct_dogs     = n_correct_dogs / n_dog_images * 100
    if n_non_dogs > 0:
        pct_correct_non_dogs = n_correct_non_dog / n_non_dogs * 100
    if n_dog_images > 0:
        pct_correct_breed    = n_correct_breed / n_dog_images * 100
    if n_number_of_images > 0:
        pct_label_matches    = n_label_matches / n_number_of_images * 100

    results_stats['n_number_of_images']   = n_number_of_images
    results_stats['n_correct_dogs']       = n_correct_dogs
    results_stats['n_dog_images']         = n_dog_images
    results_stats['n_correct_non_dog']    = n_correct_non_dog
    results_stats['n_non_dogs']           = n_non_dogs
    results_stats['n_correct_breed']      = n_correct_breed
    results_stats['n_label_matches']      = n_label_matches
    results_stats['pct_correct_dogs']     = pct_correct_dogs
    results_stats['pct_correct_non_dogs'] = pct_correct_non_dogs
    results_stats['pct_correct_breed']    = pct_correct_breed
    results_stats['pct_label_matches']    = pct_label_matches
    
    return results_stats


def print_results(results_dic, results_stats, model, print_incorrect_dogs=False, print_incorrect_breed=False):
    """
    Prints summary results on the classification and then prints incorrectly 
    classified dogs and incorrectly classified dog breeds if user indicates 
    they want those printouts (use non-default values)
    Parameters:
      results_dic - Dictionary with key as image filename and value as a List 
             (index)idx 0 = pet image label (string)
                    idx 1 = classifier label (string)
                    idx 2 = 1/0 (int)  where 1 = match between pet image and 
                            classifer labels and 0 = no match between labels
                    idx 3 = 1/0 (int)  where 1 = pet image 'is-a' dog and 
                            0 = pet Image 'is-NOT-a' dog. 
                    idx 4 = 1/0 (int)  where 1 = Classifier classifies image 
                            'as-a' dog and 0 = Classifier classifies image  
                            'as-NOT-a' dog.
      results_stats - Dictionary that contains the results statistics (either a
                     percentage or a count) where the key is the statistic's 
                     name (starting with 'pct' for percentage or 'n' for count)
                     and the value is the statistic's value 
      model - pretrained CNN whose architecture is indicated by this parameter,
              values must be: resnet alexnet vgg (string)
      print_incorrect_dogs - True prints incorrectly classified dog images and 
                             False doesn't print anything(default) (bool)  
      print_incorrect_breed - True prints incorrectly classified dog breeds and 
                              False doesn't print anything(default) (bool) 
    Returns:
           None - simply printing results.
    """    
    print("Model used was {}".format(model))
    print("Number of images: {} \nNumber of dog images: {} \nNumber of 'Not-a' Dog images: {}".format(
        results_stats['n_number_of_images'], results_stats['n_dog_images'], results_stats['n_non_dogs']
    ))
    print("Percentage Calculations:")
    print("% Correct Dogs: {}".format(results_stats['pct_correct_dogs']))
    print("% Correct BREED: {}".format(results_stats['pct_correct_non_dogs']))
    print("% Correct not-a Dog: {}".format(results_stats['pct_correct_breed']))
    print("% Match: {}".format(results_stats['pct_label_matches']))
    

# Call to main function to run the program
if __name__ == "__main__":
    main()
