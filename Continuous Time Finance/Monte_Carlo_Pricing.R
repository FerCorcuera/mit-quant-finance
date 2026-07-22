# In this exercise we are going to apply the Monte Carlo Approach
# For pricing derivatives from the Black-Scholes Solution!

MCprice <- function(
    Price,
    Strike,
    Rate,
    Time, 
    Volatility,
    Steps,
    Paths) {
  
  # Monte Carlo pricer for vanilla options 
  # Input arguments use consistent units, e.g. annualized
  # Price : Current price of underlying
  # Rate: risk - free raet
  # Time: time to expiration
  # Voltaility
  # Steps: number of time steps in dicretization
  # Pahts: number of monte carlo simulation paths for sampling measuer
  
  S0 <- Price
  K  <- Strike
  rf <- Rate
  T  <- Time
  sigma <- Volatility
  Nt <- Steps
  Np <- Paths
  dt <- T/Nt
  
  # Select independent, standardized sohcks, for example,
  z <- matrix(sign(rnorm(Nt*Np)),ncol=Np)
  
  # Define IID returns for each tsep and path under risk-neutral measure
  
  # INSERT CODE HERE
  
  # COnstruct stochatic paths and price process
  
  # INSERT CODE HERE
  
  # COmpute call and put values as discounted expected payoffs under RN measure
  # INSERT CODE HERE
  
  #return values
  
  return(data.frame(call = Call, put = Put))
}

# Set simulation parameters

S0 <- 100
mu <- 0.05
sigma <- 0.3

K <- 100
T <- 1
rf <- 0.1

Nt <- 252
Np <- 1e4
dt <- T / Nt

# Plot sample paths (S has already been simulated using code as MCprice)

matplot(S[, 1:10], type = "l", lty = 1,
        ylab = "Price", xlab = "Time",
        main = "Monte Carlo Simulation")

MCprice = (s0, K, rf, T, sigma, Nt, Np)


library(RQuantLib)

EuropeanOption(
  "call",
  S0,
  K,
  0,
  rf,
  T,
  sigma
)$value

EuropeanOption(
  "put",
  S0,
  K,
  0,
  rf,
  T,
  sigma
)$value


