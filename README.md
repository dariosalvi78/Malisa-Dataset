# Malmo-Pisa-Clermont 

This work was carried out by Selin Yildirim, Noa Pothier, Hicham Lamrani and Kévin Merle under the supervision of Dario Salvi. 

## Introduction
We work with data collected during physical tests.

In practice, the tests were numbered so that the participants did them in the same order :
-	test 01 : TUG at normal speed 
-	test 02 : TUG at normal speed (repeated) 
-	test 03 : TUG at slow speed (controlled cadence) 
-	test 04 : TUG at slow speed (controlled cadence, repeated) 
-	test 05 : 30CST 
-	test 06 : Locomo challenge 
-	test 07 : 10MWT 
-	test 08 : 10MWT (repeated) 
-	test 09 : partial 6MWT
-	test 10 : partial 6MWT (repeated)

The files collected by the different sensors did not all have the same format, some were recorded continuously... We started by splitting the files to have one file per sensor and per test for each participant and we decided to work only with CSV files.

The main objective of the project is to develop a data visualisation tool that will enable the results of the various tests to be compared.

## Structure of the folders
On GitHub there are 2 folders :

Data : basic data (except for data on mats and shoes, which were cut beforehand).

Results : data broken down by test in relation to the time of the phone in the hand with 5 seconds of insertions (5 seconds before the start and 5 seconds after the end). The following codes are used to cut the data: cutfile_mats_shoes (for mats and shoes) and cut_aut (for the phones and the smartwatches), kinect data and code to be added soon.
For each participant there is a file for each test and for each test there is a file for each metric.

## Structure of the files
We will now look at the structure of the files : 
We have made an excel file (details_CSV.xlsx) grouping together all the files that are empty and the exact order of the columns (some columns are interchanged in certain tests).
We have made an excel file (KinectInfo.xlsx) which explains how skeleton files are created.

In all files, the first column contains the absolute timestamps. 
#### Back phone :
- back_motion : we find an interval, acceleration without gravitation (accx, accy, accz), acceleration with gravitation (accGx, accGy, accGz) and rotation (alpha, beta, gamma).
- back_orientation : we find rotation (alpha, beta, gamma).
- back_cadence : we find out whether the excutant is running (isRunning), the speed (instantaneousSpeed), cadence (instantaneousCadence), step length (instantaneousStrideLength) and distance covered (totalDistance).

#### Bangle :
- bangle_accel : we find acceleration in g (accGGx, accGGy, accGGz).
- bangle_compass : we find magnetic field (magnRawx, magnRawy, magnRawz).
- bangle_hr : we find heart-rate (hr) and the confidence interval (conf).
- bangle_steps : we find the cadence (steps)

#### Hand phone : 
- hand_cadence : we find out whether the excutant is running (isRunning), the speed (instantaneousSpeed), cadence (instantaneousCadence), step length (instantaneousStrideLength) and distance covered (totalDistance).
- hand_motion : we find an interval, acceleration without gravitation (accx, accy, accz), acceleration with gravitation (accGx, accGy, accGz) and rotation (alpha, beta, gamma).
- hand_orientation : we find rotation (alpha, beta, gamma).

#### Msafety :
- msafety_acc : we find acceleration with gravitation (accGx, accGy, accGz).
- msafety_ppg : we find ppg (ppg).

#### Shoes : 
accRawx, axxRawy, accRawz, rotRawx, rotRawy, rotRawz, magnRawx, magnRawy, magnRawz, pressure1, pressure2, pressure3, pressure4, pressure5.

#### Mats :
We find a matrix where the values represent the pressure applied to the mats.

### Kinect 
We only have the kinect files for DS, and the csvs contain skeleton : points that position the different parts of the body in space. 

## Data visualisation
We created our visualisation tool in Python using the Dash library. 

In the tool you can choose the participant and the test and you have a tab for each metric (acceleration, rotation...), you can place markers to represent key moments in the test (except for the skeleton) and you can retrieve these markers by pressing the show markers button and copying the json displayed.