---
title: "Project 1"
author: "Aj Averett"
date: '2022-05-11'
output:
  rmdformats::readthedown:
    code_folding: hide
    keep_md: true
---






# Background and an introduction

Throughout this project, we will analyze the brightness of LED light bulbs over time. Interestingly, LED light bulbs will increase in brightness before their steady decrease and ultimate burnout. This process may last up to three years. Since it is not feasible to test the bulb lifetime- this project will utilize mathematical models to predict the lifespan of some of these bulbs.

In this report, the led_bulb function will be used to generate random bulbs for predictions.


```r
library(data4led)
bulb <- led_bulb(1,seed = 196)
```

The "head" function below verifies that the data frame, bulb, includes the columns: id, hours, intensity, demonormalized_intensity, and percent_intensity.



```r
head(bulb)
```

```
##       id hours intensity normalized_intensity percent_intensity
## 5325 122     0  811.4407            1.0000000         100.00000
## 5326 122    26  804.8182            0.9918387          99.18387
## 5327 122    91  816.3557            1.0060571         100.60571
## 5328 122   192  809.9991            0.9982234          99.82234
## 5329 122   293  808.8863            0.9968521          99.68521
## 5330 122   403  810.1699            0.9984339          99.84339
```

The code below creates a plot from the bulb data frame. The plot has hours on the horizontal axis (x-axis) and percent_intensity on the vertical axis (y-axis).


```r
plot(percent_intensity ~ hours, data = bulb)
```

![](Project1_files/figure-html/unnamed-chunk-3-1.png)<!-- -->

In this R Markdown file, the led_bulb function will be used to generate random bulbs for predictions.


```r
library(tidyverse)
library(gridExtra)  
```

## Introduction to the six general models

### Function 0

$f_0(x; a_0) = a_0$ where $x \geq 0$

In this model, $a_0$ seems to vertically translate the function by specifying the y-intercept

<br>

### Function 1

$f_1(x; a_0,a_1) = a_0 + a_1x$ where $x \geq 0$

In this model, $a_0$ seems to vertically translate the function by specifying the y-intercept

$a_1$ seems to change the slope at the y-intercept.

<br>

### Function 2

$f_2(x; a_0,a_1,a_2) = a_0 + a_1x + a_2x^2$ where $x \geq 0$

In this model, $a_0$ seems to vertically translate the function by specifying the y-intercept

$a_1$ seems to change the slope at the y-intercept.

$a_2$ seems to horizontally stretch the function. If negative, $a_2$ seems to reflect the function over the x-axis

<br>

### Function 3

$f_3(x; a_0,a_1,a_2 ) = a_0 + a_1e^{-a_2x}$ where $x \geq 0$

In this model, $a_0$ seems to vertically translate the function by specifying the y-intercept

$a_1$ seems to change the tail of the exponential function. If $a_1$ is negative, as x goes to infinity, y will be negative. If positive, as x goes to infinity, y will be positive.

$a_2$ seems to horizontally stretch the function. If negative, $a_2$ seems to reflect the function over the y-axis

<br>

### Function 4

$f_4(x; a_0,a_1,a_2) = a_0 + a_1x + a_2\ln(0.005x+1)$ where $x \geq 0$

In this model, $a$ seems to vertically translate the function by specifying the y-intercept

$b$ seems to change the slope at the y-intercept. If $b$ is negative, as x goes to infinity, y will be negative. If positive, as x goes to infinity, y will be positive. 

$c$ will vertically stretch the function. If negative, the function will vertically reflect over the x-axis. 

<br>

### Function 5

$f_5(x; a_0,a_1,a_2) = (a_0+a_1x)e^{-a_2x}$ where $x \geq 0$

In this model, $a_0$ seems to vertically manipulate the function by specifying the y-intercept. While some of the function will translate, the end behavior of the function will remain constant

$a_1$ seems to vertically stretch the function. If negative, $a_1$ will vertically reflect over where $a_0$ is at.

$a_2$ seems to horizontally change the end behaviors of the function. If $a_1$ and $a_2$ is positive, each end will display in quadrant 1 and 3. If both negative, the ends will display in quadrant 2 and 4.

<br>

## Description on how I will fit the models

## Background

LED bulb data is collected for the first few thousand hours in which intensity is measured as a percent of the original measurement. Therefore, the first measurement will be 100 percent tautologically. In order to predict the lifespan of these bulbs, we can use various types of models to represent the intensity over time. Below is the data for the LED intensity.

I will visually explore the parameters with Desmos to create the models below


```r
library(data4led)
bulb <- led_bulb(1,seed = 196)

t <- bulb$hours
y1 <- bulb$percent_intensity

par(mfrow = c(1,2),mar = c(2,2,3,0.25),oma = rep(0.5,4))
plot(t,y1,xlab = "Hour ", ylab = "Intensity(%) ", pch = 16,main = '')
#lines(x,yM,col = 2)
plot(t,y1,xlab = "Hour ", ylab = "Intensity(%) ", pch = 16, xlim  =  c(-10,80000),ylim  =  c(-10,120))
```

![](Project1_files/figure-html/unnamed-chunk-5-1.png)<!-- -->

```r
#lines(x,yM,col = 2)

x <- 0:80000
```

## Functions as lightbulb intensity models

### Function Zero
$f_0(t; a_0)  =  a_0$ where $t \geq 0$

Given the function above, in order to make the model visually accurate, the parameters specified in the function must be values that allow the above to be so. For example, since $f_0(x)$ must be equal to 100 when $t = 0$, $a_0$ is set to "100".


```r
# f_0(t; a_0)  =  a_0
f_0 <- function(t, a0 = 100){
  a0 + t*0  
}

par(mfrow = c(1,2),mar = c(2,2,3,0.25),oma = rep(0.5,4))
plot(t,y1,xlab = "Hour ", ylab = "Intensity(%) ", pch = 16,main = '')
lines(x,f_0(x),col = 2)
plot(t,y1,xlab = "Hour ", ylab = "Intensity(%) ", pch = 16, xlim  =  c(-10,80000),ylim  =  c(-10,120))
lines(x,f_0(x),col = 2)
```

![](Project1_files/figure-html/unnamed-chunk-6-1.png)<!-- -->

### Function One
$f_1(t; a_0,a_1)  =  a_0 + a_1t$ where $t \geq 0$

Given the function above, in order to make the model visually accurate, the parameters specified in the function must be values that allow the above to be so. For example, since $f_1(x)$ must be equal to 100 when $t = 0$, $a_0$ is set to "100".

 

$a_1$ is set to the positive value, "0.00015" since the curve of the LED data seems to be positive 



```r
# f_1(t; a_0,a_1)  =  a_0 + a_1t
f_1 <- function(t, a0  =  100, a1  =  0.00015){
  a0 + a1*t
}

par(mfrow = c(1,2),mar = c(2,2,3,0.25),oma = rep(0.5,4))
plot(t,y1,xlab = "Hour ", ylab = "Intensity(%) ", pch = 16,main = '')
lines(x,f_1(x),col = 2)
plot(t,y1,xlab = "Hour ", ylab = "Intensity(%) ", pch = 16, xlim  =  c(-10,80000),ylim  =  c(-10,120))
lines(x,f_1(x),col = 2)
```

![](Project1_files/figure-html/unnamed-chunk-7-1.png)<!-- -->

### Function Two
$f_2(t; a_0,a_1)  =  a_0 + a_1t$ where $t \geq 0$

Given the function above, in order to make the model visually accurate, the parameters specified in the function must be values that allow the above to be so. For example, since $f_2(x)$ must be equal to 100 when $t = 0$, $a_0$ is set to "100".

$a_1$ and $a_2$ are set as "0.00035" and "-0.00000005" respectively such that the curve visually matches the data. Since $a_2$ changes whether the parabola opens up or down, this is set to negative such that as the value of x increases, the value of y will first increase, then decrease.


```r
# f_2(t; a_0,a_1)  =  a_0 + a_1t
f_2 <- function(t, a0  =  100, a1  =  0.00035, a2  =  -0.00000005){
  a0 + a1*t + a2*t^2
}

par(mfrow = c(1,2),mar = c(2,2,3,0.25),oma = rep(0.5,4))
plot(t,y1,xlab = "Hour ", ylab = "Intensity(%) ", pch = 16,main = '')
lines(x,f_2(x),col = 2)
plot(t,y1,xlab = "Hour ", ylab = "Intensity(%) ", pch = 16, xlim  =  c(-10,80000),ylim  =  c(-10,120))
lines(x,f_2(x),col = 2)
```

![](Project1_files/figure-html/unnamed-chunk-8-1.png)<!-- -->

### Function Three
$f_3(t; a_0,a_1,a_2 )  =  a_0 + a_1e^{-a_2t}$ where $t \geq 0$

Given the function above, in order to make the model visually accurate, the parameters specified in the function must be values that allow the above to be so. Since $a_1$ and $a_2$ are "-0.77" and "0.0005" respectively, $a_0$ is set to "100.77" so that $f_3(x)$ is equal to zero. $a_1$ and $a_2$ are set as such that the curve visually matches the data. $a_1$ is set to a negative value, "-0.77" to reflect the fact that as the value of x decreases, $f_3(x)$ decreases as well. Finally, $a_2$ is set to "0.0005" to refine the intensity of the curve.



```r
# f_3(t; a_0,a_1,a_2 )  =  a_0 + a_1e^{-a_2t}
f_3 <- function(t, a0  =  100.77, a1  =  -0.77, a2  =  0.0005){
  a0 + a1*exp(-a2*t)
}

par(mfrow = c(1,2),mar = c(2,2,3,0.25),oma = rep(0.5,4))
plot(t,y1,xlab = "Hour ", ylab = "Intensity(%) ", pch = 16,main = '')
lines(x,f_3(x),col = 2)
plot(t,y1,xlab = "Hour ", ylab = "Intensity(%) ", pch = 16, xlim  =  c(-10,80000),ylim  =  c(-10,120))
lines(x,f_3(x),col = 2)
```

![](Project1_files/figure-html/unnamed-chunk-9-1.png)<!-- -->

### Function Four
$f_4(t; a_0,a_1,a_2)  =  a_0 + a_1t + a_2\ln(0.005t+1)$ where $t \geq 0$

Given the function above, in order to make the model visually accurate, the parameters specified in the function must be values that allow the above to be so. For example, since $f_4(x)$ must be equal to 100 when $t = 0$, $a_0$ is set to "100".

$a_1$ and $a_2$ are set as "0.000005" and "0.14" respectively such that the curve visually matches the data. $a_1$ is set to a positive value so that as the x value increases, $f_4(x)$ increases. $a_2$ is set to a positive value so that as the the x value decreases, $f_4(x)$ decreases.



```r
# f_4(t; a_0,a_1,a_2)  =  a_0 + a_1t + a_2\ln(0.005t+1)
f_4 <- function(t, a0  =  100, a1  =  0.000005, a2  =  0.14){
  a0 + a1*t + a2*log(0.005*t + 1)
}

par(mfrow = c(1,2),mar = c(2,2,3,0.25),oma = rep(0.5,4))
plot(t,y1,xlab = "Hour ", ylab = "Intensity(%) ", pch = 16,main = '')
lines(x,f_4(x),col = 2)
plot(t,y1,xlab = "Hour ", ylab = "Intensity(%) ", pch = 16, xlim  =  c(-10,80000),ylim  =  c(-10,120))
lines(x,f_4(x),col = 2)
```

![](Project1_files/figure-html/unnamed-chunk-10-1.png)<!-- -->

### Function Five
$f_5(t; a_0,a_1,a_2) = (a_0+a_1t)e^{-a_2t}$ where $t \geq 0$

Given the function above, in order to make the model visually accurate, the parameters specified in the function must be values that allow the above to be so. For example, since $f_5(x)$ must be equal to 100 when $t = 0$, $a_0$ is set to "100".

$a_1$ and $a_2$ are set as "-0.00374" and "-0.000042" respectively such that the curve visually matches the data. $a_1$ and $a_2$ play off each other such that as these values approach zero together, their curve becomes less intense and wider. 



```r
# f_5(t; a_0,a_1,a_2) = (a_0+a_1t)e^{-a_2t}
f_5 <- function(t, a0 = 100, a1 = -0.00374, a2 = -0.000042){
  (a0 + a1*t)*exp(-a2*t)
}

par(mfrow = c(1,2),mar = c(2,2,3,0.25),oma = rep(0.5,4))
plot(t,y1,xlab = "Hour ", ylab = "Intensity(%) ", pch = 16,main = '')
lines(x,f_5(x),col = 2)
plot(t,y1,xlab = "Hour ", ylab = "Intensity(%) ", pch = 16, xlim = c(-10,80000),ylim = c(-10,120))
lines(x,f_5(x),col = 2)
```

![](Project1_files/figure-html/unnamed-chunk-11-1.png)<!-- -->

## Models versus reality

__Limitations to models__

The information we get from the data depends on the general model we assume. For example, if the model were to be restricted to be linear, we could only get data dependent on this assumption. While all models are wrong, some models are useful for gaining insights for reality. This is an important concept to understand when predicting things since our predictions could be based on faulty models or models that do not have enough assumptions to make a useful insight.


* $f_0$

The model says that the lightbulb will stay at the same intensity forever

* $f_1$

The model says that the lightbulb will increase intensity forever (scary!)

* $f_2$

The model says that the lightbulb will increase slightly in intensity and then decrease

* $f_3$

The model says that the lightbulb will increase slightly in intensity and then remain at that intensity forever

* $f_4$

The model says that the lightbulb will increase slightly in intensity and then remain at that intensity forever

* $f_5$

The model says that the lightbulb will increase slightly in intensity and then decrease

Almost all the models presented do not conform to reality. $f_0$, $f_1$, $f_3$, and $f_4$ all do not decrease as $t$, time, increases. $f_1$, in fact, increases as time increases unlike the above models which continually stay stagnant. $f_2$ and $f_5$ decrease after increasing slightly- similar to the behavior of LED's. More detail is given below

# Answering the question

## Solving $f_2(x) = 80$

### Manual calculation
![](f2.png){width="250px"}

<br>

### Computational calculation
Uniroot approximates solving $f_2$ given the interval. There is an additional negative solution that is not included.


```r
f_2 <- function(t, a0  =  100, a1  =  0.00035, a2  =  -0.00000005){
  a0 + a1*t + a2*t^2
}

f_2a <- function(x){
  f_2(x) - 80
}
```


```{.r .fold-show}
uniroot(f_2a, c(23000,24000))$root
```

```
## [1] 23803.94
```

```{.r .fold-show}
f2at80 <- uniroot(f_2a, c(23000,24000))$root
```

## Solving $f_5(x) = 80$

### Manual calculation

![](f5.png){width="250px"}

<br>

### Computational calculation
Uniroot approximates solving $f_5$ given the interval. There is an additional negative solution that is not included.   


```r
f_5 <- function(t, a0 = 100, a1 = -0.00374, a2 = -0.000042){
  (a0 + a1*t)*exp(-a2*t)
}

f_5a <- function(x){
  f_5(x) - 80
}
```


```{.r .fold-show}
uniroot(f_5a, c(15000,20000))$root
```

```
## [1] 15654.55
```

```{.r .fold-show}
f5at80 <- uniroot(f_5a, c(15000,20000))$root
```

From my completely subjective estimate, I will average model two and five to get an estimate on when the LED's will decrease to 80 percent of original intensity.


```{.r .fold-show}
mean(c(f2at80, f5at80))
```

```
## [1] 19729.25
```
The LED light bulb will "burn out" after 19,729.25 hours.

# Reflection

From this project the mathematical concepts I learned most about are:

* solving equations with logarithms 
* working with higher degree polynomials

Soft-skills I learned while doing this project include:

* time management
* perseverance

among other skills.

This project was very interesting! While at first I was slightly intimidated, I did not realize how straightforward and easy this project was. It came down to actually putting in some time to write the analysis. This data is pretty straightforward and conveniently put in percentage form already so we don't have to calculate it. The model aspect was not frustrating, but understandably not useful since the model is purposely supposed to teach us about the subjectivity of creating models visually.

I am excited for future projects in which we determine these models with formulas in a way that can be replicated and be used with higher precision. This is a very fun class and I am excited to learn more!



