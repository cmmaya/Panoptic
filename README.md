## Description
We simulate a rewards mechanism to Panopic smart contract in order in incentivize different behaviours, here are some of the results obtained:

**PLPs:**

There are 2 options: Points are proportional to assets  or proportional to a fraction of the square root of total assets.

>**Option 1:**
$$P_\text{PLP}=\sum_{j\in\text{Tokens}}\int_{0}^{T} a_j(t) A_j(t) \, dt$$
>**Option 2:**
$$P_\text{PLP}=\sum_{j\in\text{Tokens}} \int_{0}^{T}a_j(t) \frac{A_j(t)}{\sqrt{\sum_{u\in\text{users}}A_j^{u}(t)}} \, dt$$


Where $P_\text{PLP}$ is points given, $A_j$ the amount of shares of token $j$, $a(t_j)>0$  is a factor depending on the phase and $t_j$ is the duration that such liquidity for token $j$ has been deployed.

![image](https://github.com/user-attachments/assets/17c14573-2ba1-4925-80bb-fb0b3907e18b)

**Figure 1**: net balance deposited vs total points given in log scale
## Stremia-based

For simplicity, we present the points on a per-position basis

**Sellers:**      

Sellers receive points proportionally to the streamia they accumulate by selling options and buyers get points for the stremia they pay at excercising the option, this way we also reward users for providing liquidity to Uni v3 pools. Since sellers don’t need to exercise the option to earn points, they are more rewarded than buyers.
>**Option 1:**
$$P_\text{seller}=\sum_{j\in\text{Tokens}}b_j(t) S_{seller}(t) $$
>**Option 2:**
$$P_\text{seller}=\sum_{j\in\text{Tokens}} b_j(t)\frac{S_{seller}(t)}{\sqrt{\sum_{u\in\text{users}}S_{seller}^{u}(t)}}  $$


where $b_j(t)>0$ is a parameter depending on the phase, $S_\text{seller}(t)$ refers to the stremia fees (in USD) received by the seller. 

sellers describes the total Streamia collected in a period T, after selling the option

**Buyers:**

>**Option 1:**
$$P_\text{buyer}=\sum_{j\in\text{Tokens}}b_j(t) S_{buyer}(t) $$
>**Option 2:**
$$P_\text{buyer}=\sum_{j\in\text{Tokens}} b_j(t)\frac{S_{buyer}(t)}{\sqrt{\sum_{u\in\text{users}}S_{buyer}^{u}(t)}}  $$
where $b_j(t)>0$ is a parameter depending on the phase, $S_\text{buyer}(t)$ refers to the stremia fees (in USD) paid by the buyer. 

![image](https://github.com/user-attachments/assets/4be78816-2f99-4fb4-9b50-fe4abe251fad)



**Figure 2:** Graphs for:  a. Stremia collected (in USD) by sellers or paid by buyers at excercising ITM vs Points and b. Stremia collected vs total legs amount in log scale
## Position-based

For simplicity, we present the points on a per-position basis

**Sellers:**      

Buyers and sellers receive points proportionally to the streamia they accumulate by selling options or paying stremia to excercise, this way we also reward users for providing liquidity to Uni v3 pools. Since sellers don’t need to exercise the option to earn points, they are more rewarded than buyers
>**Option 1:**
$$P_\text{position}=\sum_{j\in\text{Tokens}}\int_{0}^{T} c_j(t) L_j(t) \, dt$$
>**Option 2:**
$$P_\text{position}=\sum_{j\in\text{Tokens}} \int_{0}^{T}c_j(t)\frac{L_j(t)}{\sqrt{\sum_{u\in\text{users}}L_j^{u}(t)}}\, dt  $$
>**Option 3:**
$$P_\text{position}=\sum_{j\in\text{Tokens}} \int_{0}^{T}c_j(t)\frac{\sqrt{L_j(t)}}{\sum_{u\in\text{users}}L_j^{u}(t)}\, dt  $$

\
where $c_j(t)>0$ is a parameter depending on the phase, $L_\text{j}(t)$ refers to the liquidity deployed by each seller for a token j, and the the duration.

![image](https://github.com/user-attachments/assets/68fc4a99-35ef-4de4-9fbf-39d902a12a98)

**Figure 3**: Contour of Points given vs holding time in log scale, with color representing the total amount of money put in the legs of the option for Options 1 and 3 (In general, there is a tendency to get more points with more total legs amount )



## Multipliers and add-ons



Using the following multipliers and add-ons, we want to reward desirable behaviours:

- **Longer positions held**:

A points multiplier is given every certain number of days (e.g  x1.1 multipler every 10 days); something like: 

$$P_\text{new} = m^tP$$

![image](https://github.com/user-attachments/assets/18e335ca-3e29-4dbe-9448-cc9d2515210a)


**Figure 4:** Total points given vs holding time in log scale

Where $t$ is the accumulated chunk of days (e. g every 10 days t = t+1)
 
