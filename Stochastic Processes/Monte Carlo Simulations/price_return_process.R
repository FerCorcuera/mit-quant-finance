# ===========================================================================
# Simulating a lognormal price process

Nt <- 252
Np <- 10000
sigma <- 0.3 #set annualized volatility to 30% (sd )
mu <- 0.1 # set annaulized drift/return to 10%
dt <- 1/252 # Time step scale factor to one day (252 td per year)
z <- matrix(rnorm(Nt*Np), nrow = Nt) # generate a set of normal random draws

r <- mu * dt + z * sigma * sqrt(dt) # we want the serie in daily steps!
# if one step represetned 1 year:
r_annual <- mu + z*sigma # like a normal generalized random walk

# another way to generate the daily steps:

r <- matrix(rnorm(
  Nt*Np,
  mean = mu*dt,
  sd = sigma * sqrt(dt)
  ), nrow = Nt
  )

s <- matrix(0, Nt+1, Np) # placeholders

# we fill the placeholders with the random normal numbers
# now is not a random walk, are the returns, and we are adding them
# because we are recreating the P_t = e ^ (rt_1...) equation

for (t in 1:Nt) {
  s[t+1,] <- s[t,] + r[t,]
}


P <- exp(s) # finally we create a log normal process

matplot(P[,1:3], type = "l") # it is interesting how the simulated series
# are different and could be the returns of any company, 
# but they are draw from the same distribution!

R <- P[Nt+1,] - 1 # terminal compounded growth factors from every simulated path

# exp(s) reconstructs the compounded growth factor P_T / P_0
# subtracting 1 converts gross return into simple return

mean(R) # lets compute the mean of the lats period paths
(exp(mu+sigma^2/2) -1) # it is really close to the theoretical mean 


sd(R) # now lets compare the standard deviatoin
sqrt(exp(2*mu + sigma^2) * (exp(sigma^2) - 1)) 

# so again montecarlo simulation is really useful to calculate or approximate
# theorical parameters, and as we increase the number of paths the gap closes

hist(R , breaks=50) # distribution of the returns (looks like a log normal)
hist(log(1+R)) # we are ploting the logaritmic returns (looks like a normal)
plot.ecdf(1+R) # now the cumulative distribution function
barplot(sort(1+R)) # another way to see the distribution

# with qq plots we can visualize hwo differnt is the distribution
# compared to a normal distribution (straight line)
qqnorm(1+R)

# ===========================================================================

# Simulating an AR(1)-style simple return process

lambda <- 0.4 # we define the weight of the effect of the previous values
mu <- 0.1 # the expected value (mean) of the returns is 10%

R <- matrix(0, Nt, Np) #placeholders, start with 0 

# Simulate IID Gaussian shocks (innovations/noise)
epsilon <- matrix(
  rnorm(Nt*Np, sd = sigma*sqrt(dt)), #note that is the sigma from the GRW
  nrow = Nt
)

## now we create the AR(1) process is terms of lambda and mu
## if we retrasform this in terms of deviations we will have the common formula
for (t in 2:Nt) {
  R[t,] <- (1 + lambda) * (mu * dt) - lambda * R[t-1,] + epsilon[t,]
}

matplot(R[,1:3], type = "l") 

# Convert simple returns to log-returns, if 1 + R > 0
r <- log(1 + R)
matplot(r[,1:3], type = "l") 
acf(R[,1]) # MOST IMPORTANTLY:
## when we analyze the autocorrelations we can see how the first one is 
## -0.4, the paratmeters that we defined earlier, and the coreraltiosn
## with the other periods are just the noise that we integrated
## it is an important and clear example of mean reversion
## lets see how it changes when we change lambda: 

lambda <- 0.8 
for (t in 2:Nt) {
  R[t,] <- (1 + lambda) * (mu * dt) - lambda * R[t-1,] + epsilon[t,]
}
acf(R[,1]) # stronger the weight of the previous value
# stronger the autocorerlation with the previous t values