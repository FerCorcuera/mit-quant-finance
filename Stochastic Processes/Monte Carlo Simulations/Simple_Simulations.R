# How a matrix works in R
matrix(1:4,ncol = 2, nrow = 2)
# Sign gives values of 1, -1 or 0, if the value is positive, negative or 0 
sign(0)

# 20 - step simple random walk simulation
p <- 0.5 # probability of an upward step
q <- 1 - p # probability of an downward step
Nt <- 20 # number of time steps
Np <- 1 # number of paths
z <- matrix(runif(Nt*Np), nrow = Nt) # we crate a matrix of random numbers
x <- sign(p-z) # here we transform uniform numbers into binomial (1, -1)
s <- matrix(0, Nt+1, Np) # we create the place holders


for (k in 1:Nt) {
  s[k+1,] <- s[k,] + x[k,]
}

# now we fill the matrix s with the random binomial numbers of x
# note how we are starting from 0 (k+1)
# each value will be the previous plus a random shock

plot(s, type="b")

runif()


# Many simulations of a one-year daily walk

Nt <- 252 # number of trading years in a year (no holidays and weekends)
Np <- 1e4 # 10,000 possible paths
z <- matrix(runif(Nt*Np), nrow = Nt) # we crate a matrix of u-random numbers
x <- sign(p-z) # here we transform uniform numbers into binomial (1, -1)
s <- matrix(0, Nt+1, Np) # we create the place holders

for (k in 1:Nt) {
  s[k+1,] <- s[k,] + x[k,]
}

matplot(s[,1:3], type = "b")

