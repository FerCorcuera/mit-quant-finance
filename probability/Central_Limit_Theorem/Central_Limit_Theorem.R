# Exercise 1:

# Each random variable has:
#   - success probability p = 0.1
#   - number of trials n

# k contains all possible values that the random variable can take:
# 0, 1, 2, ..., n

# dbinom() computes the probability mass function (PMF):
# P(K = 0), P(K = 1), ..., P(K = n)

# For each Binomial random variable, we compute:
#   - all possible outcomes
#   - their corresponding probabilities

# The goal is to visualize how the probability distribution changes
# as the number of trials n increases.

nlist <- c(1, 2, 5, 10, 20, 50, 100, 1000)
p <- 0.1

for (n in nlist) {
  k <- 0:n
  
  f <- dbinom(
    x = k,
    size = n,
    prob = p
  )
  
  barplot(
    height = f,
    names.arg = k,
    xlab = "Number of successes",
    ylab = "Probability",
    main = paste("Binomial distribution: p =", p, ", n =", n)
  )
  
  readline(prompt = "Press Enter to continue...")
}


# Exercise 2:

# Scaling a binomial distribution (standardize it)

# as we keep increasing the number of trials of our standardize 
# we can note how it looks gaussian
# it is our favorite bell curve
# IT IS NOT EXACT GAUSSIAN (not goes from -inf +inf)
# but it is a great example of the Central Limit Theorem

nlist <- c(1, 2, 5, 10, 20, 50, 100, 1000)
p <- 0.1
zmax <- 5

for (n in nlist) {
  k <- 0:n
  
  z <- (k - n * p) / sqrt(n * p * (1 - p))
  zi <- abs(z) <= zmax
  
  f <- dbinom(
    x = k,
    size = n,
    prob = p
  )
  
  barplot(
    height = f[zi],
    names.arg = round(z[zi], 2),
    xlab = "Standardized variable z",
    ylab = "Probability",
    main = paste("Binomial distribution: p =", p, ", n =", n)
  )
  
  readline(prompt = "Press Enter to continue...")
}

# Exercise 3: bloomberg terminals

# we have 120 students
# 9 bloomberg terminals to use
# we assume the experiment as a binomial distribution
# each student wants or not use the terminal
# Demand independently with probability 7.5%

# We can calculate the probability of k students will want to use at the same time

n <- 120
k <- 0:9
p <- 0.075

sum(dbinom(k,n,p))