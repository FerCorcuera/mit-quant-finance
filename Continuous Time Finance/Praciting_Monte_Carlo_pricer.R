# initial paramters
S0 <- 100
mu <- 0.05 #misleading
sigma <- 0.3

K <- 100
T <- 1
rf <- 0.1

Nt <- 252
Np <- 1e4
dt <- T / Nt
#generate random normal numbers
Z <- matrix(
  rnorm(Nt*Np),
  nrow = Nt,
  ncol = Np
)
# generate our matrix with palce hodlers for our simulations
S <- matrix(
  0,
  nrow = Nt + 1,
  ncol = Np,
  
)
# initial price
S[1, ] <- S0
# recurisve to create our paths
for (t in 1:Nt) {
  
  S[t + 1, ] <- S[t, ] *
    exp(
      (rf - 0.5 * sigma^2) * dt +
        sigma * sqrt(dt) * Z[t, ]
    )
}
#plot
matplot(
  S[, 1:10],
  type = "l",
  lty = 1,
  xlab = "Time Step",
  ylab = "Stock Price",
  main = "Monte Carlo Stock Paths"
)

#payoff:
payoff_paths <- pmax(S - K, 0)

# the paths that survived:
itm <- payoff_paths[Nt + 1, ] > 0
itm_paths <- which(itm)

matplot(
  payoff_paths[, itm_paths[1:6]],
  type = "l",
  lty = 1,
  ylim = c(0, max(payoff_paths[, itm_paths[1:6]])),
  xlab = "Time Step",
  ylab = "Payoff",
  main = "Monte Carlo Payoff Paths"
)
