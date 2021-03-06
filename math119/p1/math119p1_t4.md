---
title: "P1T4"
author: "Aj Averett"
date: '2022-05-10'
output:
  rmdformats::readthedown:
    code_folding: hide
    keep_md: true
---



# Finding $f_i(t) = 80$

## Background

LEDs don't burn out the way normal light bulbs do- however they do dim after a certain interval of time. The goal of this task is to determine how much time it takes for an LED bulb will take to go to 80 percent of original intensity based on the data. This section will detail the manual process and computational of finding the exact solution, if possible, for where each of the six fitted models is at 80% of the initial intensity.

## Solving $f_0(x) = 80$ and $f_1(x) = 80$

### Manual calculation

![](f0-1.png){width="250px"}

### Computational calculation
Uniroot cannot be used for $f_0$ since there are no values that cross the x-axis. Uniroot can only solve $f_1$ if the domain is allowed to be negative.


```r
f_0 <- function(t, a0 = 100){
  a0 + t*0  
}

f_0a <- function(x){
  f_0(x) - 80
}

f_1 <- function(t, a0  =  100, a1  =  0.00015){
  a0 + a1*t
}

f_1a <- function(x){
  f_1(x) - 80
}
```


```{.r .fold-show}
print(-400000/3)
```

```
## [1] -133333.3
```

```{.r .fold-show}
uniroot(f_1a, c(-134000,-132000))$root
```

```
## [1] -133333.3
```

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

## Solving $f_3(x) = 80$

### Manual calculation
![](f3.png){width="250px"}

<br>

### Computational calculation
Uniroot approximates solving $f_3$. However the only solution is negative and thus not a real solution for this model.



```r
f_3 <- function(t, a0  =  100.77, a1  =  -0.77, a2  =  0.0005){
  a0 + a1*exp(-a2*t)
}

f_3a <- function(x){
  f_3(x) - 80
}
```


```{.r .fold-show}
uniroot(f_3a, c(-7000,-6000))$root
```

```
## [1] -6589.749
```

## Solving $f_4(x) = 80$

### Manual calculation
![](f4.png){width="250px"}

<br>

### Computational calculation
Uniroot approximates solving $f_4$. However the only solution is negative and thus not a real solution for this model.


```r
f_4 <- function(t, a0  =  100, a1  =  0.000005, a2  =  0.14){
  a0 + a1*t + a2*log(0.005*t + 1)
}

f_4a <- function(x){
  f_4(x) - 80
}
```


```{.r .fold-show}
uniroot(f_4a, c(-200,-150))$root
```

```
## [1] -199.9999
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
## Models versus reality

Almost all the models presented do not conform to reality. $f_0$, $f_1$, $f_3$, and $f_4$ all do not decrease as $t$, time, increases. $f_1$, in fact, increases as time increases unlike the above models which continually stay stagnant. $f_2$ and $f_5$ decrease after increasing slightly- similar to the behavior of LED's.


