print('test')

library(ggplot2)

x <- seq(1,100)
f <- function(x) {
    x*2 + 5
}

plot(x, f(x))
