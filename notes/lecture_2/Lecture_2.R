
# define the row matrix of t = 0 prices B_0 and S_0
# in R c() means "combine" , that creates a vector!
A0 = matrix(c(100,100), nrow = 1, ncol = 2)

# Add dimension names for rows and columns 

dimnames(A0) <- list(c("Price_0"),c("Bond","Stock"))

# define the matrix of t= T payoffs/prices  for B_T and S_T
# where row 1 corresponds to state 1, omega = d and 
# row 2 corresponds to state 2, omega = u
# column 1 corresponds to the bond and column 2 to the stock

A = cbind(as.matrix(c(103,103)),as.matrix(c(90,130)))

dimnames(A)<-list(c("Payoff_T_d","Payoff_T_u"),c("Bond","Stock"))
# When suing ggplot2, data are represented in dataframes
is.data.frame(A)
A.df <- data.frame(A)
Atranspose.df <- data.frame(t(A))

# Add Asset_Name as variable/field in Atranspoe.df

Atranspose.df$Asset_name <- dimnames(Atranspose.df)[[1]]

# plotting simple

plot(
  x = c(0,1), y = c(1,0),
  type = 'n',
  xlim = c(-2,2),
  ylim = c(-2,2),
  xlab = "x",
  ylab = 'y',
  main = "Vector (1,1)"
)

arrows(
  x0 = 0,y0 = 0,
  x1 = 1,y1 =1,
  length = 0.1,
  lwd = 2,
  col = 'blue'
)


# lets plot the payoff vectors of two assets at t=T
# Note: the function arrow() specifies the head of the arrows

g1 <- ggplot(data = Atranspose.df,
             x = Payoff_T_d, y = Payoff_T_u,
             label = Asset_name, color = Asset_name)

g1 +
  geom_segment(
    aes(
      x = 0, y = 0,
      xend = Payoff_T_d, yend = Payoff_T_u
    ), size = 3,arrow = arrow(length = unit(0.5, "cm"))) +
  geom_text(aes(
      x = Payoff_T_d,
      y = Payoff_T_u,
      label = Asset_name
    ), hjust = 0, vjust = 1, nudge_x = 5, nudge_y = 7
  ) + xlim(-140, 140) + ylim(-140, 140) +
  labs( title = "Fig 1. Payoff_T Vectors of Two Assets",
    x = "Payoff in Down State",
    y = "Payoff in Up State"
  ) + theme_minimal()

# Create a data frame data.portfolios
# with rows corresponding to
# portfolio cases which contain variables
# pi_B portfolio weights of B
# pi_S portfolio weight of S
# Value_0 value/cost of portfolio at t=0
# Payoff_T_u payoff of portfolio at t=T for \omega=u
# Payoff_T_d payoff of portfolio at t=T for \omega=d
# Profit_T_u profit of portfolio at t=T for \omega=u
  # Profit_T_d profit of portfolio at t=T for \omega=d
## pi_B and pi_S correspond to $\pi_B $ and $\pi_S$
# Consider evaluating portfolios that let these fractions vary

# For different cases of sets of portfolios, create a data frame
# of the portfolio vectors in different

list.pi_S = seq(0,1,.1)
df.pivecs.1<-data.frame(pi_B=1-list.pi_S,pi_S=list.pi_S)
df.pivecs.1

# Create the data frame data.portfolios
# with portfolio variables in the columns/fields

data.portfolios <- NULL

for (i in 1:NROW(df.pivecs.1)) {
  pivec <- as.numeric(df.pivecs.1[i, ])
  
  Value_0 <- sum(as.numeric(A0) * pivec)
  Payoff_T_d <- sum(as.numeric(A[1, ]) * pivec)
  Payoff_T_u <- sum(as.numeric(A[2, ]) * pivec)
  
  Profit_T_d <- Payoff_T_d - Value_0
  Profit_T_u <- Payoff_T_u - Value_0
  
  new.data.portfolios <- data.frame(
    pi_B = pivec[1],
    pi_S = pivec[2],
    Value_0 = Value_0,
    Payoff_T_d = Payoff_T_d,
    Payoff_T_u = Payoff_T_u,
    Profit_T_d = Profit_T_d,
    Profit_T_u = Profit_T_u
  )
  
  if (i == 1) {
    data.portfolios <- new.data.portfolios
  } else {
    data.portfolios <- rbind(data.portfolios, new.data.portfolios)
  }
}

data.portfolios.1 <- data.portfolios

data.portfolios.1$pi_S <-as.factor(data.portfolios.1$pi_S)
# Figure 2A: Plot payoffs as vectors
g1<-ggplot(data=data.portfolios.1,aes(x=Payoff_T_d,y=Payoff_T_u))
g2<-g1 + geom_segment(aes(x=0,y=0,xend=Payoff_T_d,yend=Payoff_T_u,
                           col=pi_S),size=.5, arrow = arrow(length = unit(0.2, "cm")))+
   xlim(c(-140,140)) +ylim(c(-140,140))
 g2 + ggtitle("Figure 2A. Payoff Vectors at t=T (as vectors)",
                subtitle="Portfolios (Pi_B=1-Pi_S)")
 
g1 <- ggplot(data = data.portfolios.1, aes(x = Payoff_T_d, y = Payoff_T_u))

g2 <- g1 +
  geom_point(aes(color = pi_S), size = 1) +
  xlim(-140, 140) +
  ylim(-140, 140)

g2 +
  ggtitle("Figure 2B. Payoff Vectors at t = T (as points)",
          subtitle = "Portfolios (π_B = 1 − π_S)")


list.pi_S <- seq(0, 1, 0.1)
list.pi_B <- seq(0, 1, 0.1)

for (i in 1:length(list.pi_B)) {
  for (j in 1:length(list.pi_S)) {
    pivec <- c(list.pi_B[i], list.pi_S[j])
    if (i == 1 && j == 1) {
      df.pivecs <- data.frame(pi_B = pivec[1], pi_S = pivec[2])
    } else {
      df.pivecs <- rbind(df.pivecs,
                         data.frame(pi_B = pivec[1], pi_S = pivec[2]))
    }
  }
}

df.pivecs.2 <- df.pivecs
head(df.pivecs.2)

fcn.data.portfolios <- function(df.pivecs) {
  for (i in 1:NROW(df.pivecs)) {
    pivec <- as.numeric(df.pivecs[i, ])
    
    Value_0 <- sum(as.numeric(A0) * pivec)
    Payoff_T_d <- sum(as.numeric(A[1, ]) * pivec)
    Payoff_T_u <- sum(as.numeric(A[2, ]) * pivec)
    
    Profit_T_d <- Payoff_T_d - Value_0
    Profit_T_u <- Payoff_T_u - Value_0
    
    new.data.portfolios <- data.frame(
      pi_B = pivec[1],
      pi_S = pivec[2],
      Value_0 = Value_0,
      Payoff_T_d = Payoff_T_d,
      Payoff_T_u = Payoff_T_u,
      Profit_T_d = Profit_T_d,
      Profit_T_u = Profit_T_u
    )
    
    if (i == 1) {
      data.portfolios <- new.data.portfolios
    } else {
      data.portfolios <- rbind(data.portfolios, new.data.portfolios)
    }
  }
  
  return(data.portfolios)
}


data.portfolios.2<-fcn.data.portfolios(df.pivecs.2)
# Figure 3: Plot payoffs as points for data.portfolios.2
g1<-ggplot(data=data.portfolios.2,aes(x=Payoff_T_d,y=Payoff_T_u))
g2<-g1+ geom_point(aes(col=Value_0),size=1) + xlim(c(-140,250)) +ylim(c(-140,250))
# Note, the xlim and ylim values are set manually
g2 + ggtitle("Figure 3. Payoff Vectors at t=T (as points)",
                 + subtitle="Portfolios (0 <=Pi_B, Pi_S <=1)")


print(
  g2 + ggtitle(
    "Figure 3. Payoff Vectors at t=T (as points)",
    subtitle = "Portfolios (0 <= Pi_B, Pi_S <= 1)"
  )
)

