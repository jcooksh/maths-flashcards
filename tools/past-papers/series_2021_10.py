"""October 2021 (9MA0/01 and 9MA0/02), with the numbers changed."""
import math
import sympy as sp
from common import card, close, same, identity, x, y, t, k, theta, u

SERIES = {"id": "paper-2021-10", "title": "October 2021", "hue": 120}

CARDS = [
    # ---------------- Paper 1 ----------------
    card(1, 1,
         [r"$f(x)=ax^3+7x^2-2ax-12$",
          r"Given that $(x-2)$ is a factor of $f(x)$, find the value of the constant $a$."],
         [r"Spot: “$(x-2)$ is a factor” means $f(2)=0$ (factor theorem).",
          r"Use: substitute $x=2$ and solve for $a$.",
          r"Method: $8a+28-4a-12=4a+16=0$",
          r"Answer: $a=-4$"],
         [r"Set $f(2)=0$ and solve for $a$",
          r"Set $f(-2)=0$ and solve for $a$",
          r"Set $f(0)=2$",
          r"Differentiate and set $f'(2)=0$"]),
    card(1, 2,
         [r"$f(x)=x^2+6x+14$, $x\in\mathbb{R}$",
          r"(a) Express $f(x)$ in the form $(x+a)^2+b$.",
          r"(b) The curve $y=f(x)$ meets the $y$-axis at $P$ and has a minimum at $Q$. Write down the coordinates of $P$ and $Q$."],
         [r"Spot: the form $(x+a)^2+b$ means complete the square. The vertex comes straight out of it.",
          r"Use: halve the coefficient of $x$: $(x+3)^2-9+14$.",
          r"(a) $(x+3)^2+5$",
          r"(b) $P=(0,14)$ and $Q=(-3,5)$"],
         [r"Halve the 6 and complete the square",
          r"Use the quadratic formula",
          r"Factorise $x^2+6x+14$",
          r"Differentiate and integrate"]),
    card(1, 3,
         [r"A sequence is defined by $u_{n+1}=k-\dfrac{30}{u_n}$, $u_1=3$, where $k$ is an integer.",
          r"Given that $u_1+2u_2+u_3=0$,",
          r"(a) show that $3k^2-47k+140=0$,",
          r"(b) find the value of $k$, giving a reason,",
          r"(c) find $u_3$."],
         [r"Spot: a recurrence with an unknown constant means write $u_2$ and $u_3$ in terms of $k$, then substitute into the condition.",
          r"Use: $u_2=k-10$ and $u_3=k-\dfrac{30}{k-10}$.",
          r"(a) $3+2(k-10)+k-\dfrac{30}{k-10}=0\Rightarrow(3k-17)(k-10)-30=0\Rightarrow3k^2-47k+140=0$",
          r"(b) $(3k-35)(k-4)=0$. $k$ must be an integer, so $k=4$.",
          r"(c) $u_3=4-\dfrac{30}{-6}=9$"],
         [r"Write $u_2$ and $u_3$ in terms of $k$ and substitute into $u_1+2u_2+u_3=0$",
          r"Assume $k=u_1$",
          r"Use the arithmetic series formula",
          r"Set $u_2=0$"]),
    card(1, 4,
         [r"$f(x)=x^2+\ln(x^2-2x+3)$ has a single turning point at $x=\alpha$.",
          r"(a) Show that $\alpha$ is a solution of $x^3-2x^2+4x-1=0$.",
          r"(b) Using $x_{n+1}=\dfrac{1+2x_n^2-x_n^3}{4}$ with $x_1=0.25$, find $x_2$ and $x_4$ to 4 decimal places.",
          r"(c) Using a suitable interval and function, show that $\alpha=0.285$ to 3 decimal places."],
         [r"Spot: a turning point means $f'(x)=0$. “Show it is 0.285 to 3 d.p.” means a sign change over $[0.2845,0.2855]$.",
          r"Use: $\dfrac{d}{dx}\ln(g(x))=\dfrac{g'(x)}{g(x)}$.",
          r"(a) $2x+\dfrac{2x-2}{x^2-2x+3}=0\Rightarrow2x^3-4x^2+6x+2x-2=0\Rightarrow x^3-2x^2+4x-1=0$",
          r"(b) $x_2=0.2773$ and $x_4=0.2844$",
          r"(c) With $g(x)=x^3-2x^2+4x-1$: $g(0.2845)<0$ and $g(0.2855)>0$, and $g$ is continuous, so $\alpha=0.285$ to 3 d.p."],
         [r"Differentiate using $\dfrac{g'(x)}{g(x)}$ for the log term and set $f'(x)=0$",
          r"Set $f(x)=0$",
          r"Differentiate $\ln(x^2-2x+3)$ as $\dfrac{1}{x^2-2x+3}$",
          r"Take $e$ to the power of both sides"]),
    card(1, 5,
         [r"A company's profit is £15 000 in Year 1. A model predicts that the yearly profit will increase by 6% each year.",
          r"(a) Show that the profit in Year 3 is £16 854.",
          r"(b) Find the first year in which the yearly profit exceeds £40 000.",
          r"(c) Find the total profit for the first 25 years, to the nearest £1000."],
         [r"Spot: “increase by 6% each year” means a geometric sequence with $r=1.06$.",
          r"Use: $u_n=ar^{n-1}$, then logs for (b), and $S_n=\dfrac{a(r^n-1)}{r-1}$ for (c).",
          r"(a) $15000\times1.06^2=16854$",
          r"(b) $15000\times1.06^{n-1}>40000\Rightarrow n-1>\dfrac{\ln(8/3)}{\ln1.06}\approx16.8\Rightarrow n=18$",
          r"Answer: Year 18",
          r"(c) $\dfrac{15000(1.06^{25}-1)}{0.06}\approx£823\,000$"],
         [r"Use a geometric sequence with $a=15000$ and $r=1.06$",
          r"Use an arithmetic sequence with $d=0.06$",
          r"Use $r=0.06$",
          r"Use $15000\times1.06n$"]),
    card(1, 6,
         [r"In triangle $ABC$, $\overrightarrow{AB}=-2\mathbf{i}-\mathbf{j}-2\mathbf{k}$ and $\overrightarrow{BC}=4\mathbf{i}+3\mathbf{k}$.",
          r"(a) Find $\overrightarrow{AC}$.",
          r"(b) Show that $\cos ABC=\dfrac{14}{15}$."],
         [r"Spot: angle $ABC$ is at $B$, so use the two vectors that point away from $B$: $\overrightarrow{BA}$ and $\overrightarrow{BC}$.",
          r"Use: $\cos\theta=\dfrac{\mathbf{a}\cdot\mathbf{b}}{|\mathbf{a}||\mathbf{b}|}$, or the cosine rule.",
          r"(a) $\overrightarrow{AC}=\overrightarrow{AB}+\overrightarrow{BC}=2\mathbf{i}-\mathbf{j}+\mathbf{k}$",
          r"(b) $\overrightarrow{BA}=2\mathbf{i}+\mathbf{j}+2\mathbf{k}$, so $\overrightarrow{BA}\cdot\overrightarrow{BC}=8+0+6=14$, with $|\overrightarrow{BA}|=3$ and $|\overrightarrow{BC}|=5$.",
          r"Answer: $\cos ABC=\dfrac{14}{15}$"],
         [r"Use $\overrightarrow{BA}$ and $\overrightarrow{BC}$, the vectors from $B$, in the cosine formula",
          r"Use $\overrightarrow{AB}$ and $\overrightarrow{BC}$ as given",
          r"Use the sine rule",
          r"Add the lengths $|AB|+|BC|$"],
         ask="How do you find $\\cos ABC$?"),
    card(1, 7,
         [r"The circle $C$ has equation $x^2+y^2+6x-8y+5=0$.",
          r"(a) Find the centre of $C$ and its exact radius as a simplified surd.",
          r"(b) The line $y=x+k$ is a tangent to $C$. Find the possible values of $k$ as simplified surds."],
         [r"Spot: an expanded circle equation means complete the square in $x$ and in $y$. “Tangent” means either the discriminant is $0$ or the distance from the centre equals the radius.",
          r"Use: $(x+3)^2+(y-4)^2=20$.",
          r"(a) The centre is $(-3,4)$ and $r=\sqrt{20}=2\sqrt5$.",
          r"(b) Substitute $y=x+k$: $2x^2+(2k-2)x+(k^2-8k+5)=0$. Setting the discriminant to 0 gives $k^2-14k+9=0$.",
          r"Answer: $k=7\pm2\sqrt{10}$"],
         [r"Complete the square in $x$ and $y$ to get $(x+3)^2+(y-4)^2=20$",
          r"Read the centre as $(6,-8)$",
          r"Read the radius as $\sqrt5$",
          r"Differentiate the circle's equation"]),
    card(1, 8,
         [r"A bacteria population is modelled by $N=Ae^{kt}$, $t\ge0$ hours. There are 800 bacteria at the start, and the population triples in exactly 6 hours.",
          r"(a) Find a complete equation for the model.",
          r"(b) Find the rate of increase at exactly 4 hours, to 2 s.f.",
          r"(c) A second population is modelled by $M=200e^{1.5kt}$. Find the time $T$ when the two populations are equal."],
         [r"Spot: exponential growth with “triples in 6 hours” means use $e^{6k}=3$. “Rate of increase” means $\dfrac{dN}{dt}$.",
          r"Use: $\dfrac{d}{dt}Ae^{kt}=kAe^{kt}$, and logs to solve.",
          r"(a) $A=800$ and $k=\dfrac{\ln3}{6}$, so $N=800e^{\frac{\ln3}{6}t}$",
          r"(b) $\dfrac{dN}{dt}=kN=\dfrac{\ln3}{6}\times800\times3^{\frac46}\approx300$ bacteria per hour",
          r"(c) $800e^{kT}=200e^{1.5kT}\Rightarrow4=e^{0.5kT}\Rightarrow T=\dfrac{2\ln4}{k}\approx15.1$ hours"],
         [r"Use $N(0)=800$ for $A$, then $e^{6k}=3$ for $k$",
          r"Use $e^{3k}=6$",
          r"Use $k=\dfrac{3}{6}$",
          r"Use $N=800\times3t$"]),
    card(1, 9,
         [r"$f(x)=\dfrac{27x^2+16x+5}{(3x+1)^2(1-x)}$, $x\ne-\dfrac13$, $x\ne1$",
          r"$f(x)$ can be written as $\dfrac{A}{3x+1}+\dfrac{B}{(3x+1)^2}+\dfrac{C}{1-x}$.",
          r"(a) Find $B$ and $C$, and show that $A=0$.",
          r"(b) Use binomial expansions to find the expansion of $f(x)$ up to the $x^2$ term, and state when it is valid."],
         [r"Spot: a repeated factor in the denominator means you need both $\dfrac{A}{3x+1}$ and $\dfrac{B}{(3x+1)^2}$. Then expand each fraction as $(1+\dots)^n$.",
          r"Use: substitute $x=-\tfrac13$ and $x=1$, then compare the $x^2$ coefficients.",
          r"(a) $x=-\tfrac13$: $3-\tfrac{16}{3}+5=\tfrac43B$, so $B=2$. $x=1$: $48=16C$, so $C=3$. The $x^2$ terms give $27=-3A+9C$, so $A=0$.",
          r"(b) $2(1+3x)^{-2}+3(1-x)^{-1}=(2-12x+54x^2)+(3+3x+3x^2)$",
          r"Answer: $5-9x+57x^2$, valid for $|x|<\tfrac13$"],
         [r"Use $x=-\tfrac13$ and $x=1$ to find $B$ and $C$, then compare coefficients for $A$",
          r"Ignore the $\dfrac{A}{3x+1}$ term from the start",
          r"Expand the top and divide by the bottom",
          r"Use $x=0$ only"]),
    card(1, 10,
         [r"(a) Prove that $\dfrac{1+\cos2\theta-\sin2\theta}{1-\cos2\theta-\sin2\theta}\equiv-\cot\theta$, where the denominator is not zero.",
          r"(b) Hence solve, for $0<x<180^\circ$, $\dfrac{1+\cos4x-\sin4x}{1-\cos4x-\sin4x}=4\cos2x$, to 1 decimal place."],
         [r"Spot: $1\pm\cos2\theta$ means use $\cos2\theta\equiv2\cos^2\theta-1$ or $1-2\sin^2\theta$ so the 1s cancel. Then factorise.",
          r"Use: $1+\cos2\theta\equiv2\cos^2\theta$, $1-\cos2\theta\equiv2\sin^2\theta$, $\sin2\theta\equiv2\sin\theta\cos\theta$.",
          r"(a) $\dfrac{2\cos\theta(\cos\theta-\sin\theta)}{2\sin\theta(\sin\theta-\cos\theta)}=-\dfrac{\cos\theta}{\sin\theta}=-\cot\theta$",
          r"(b) With $\theta=2x$: $-\cot2x=4\cos2x\Rightarrow\cos2x\left(\dfrac{1}{\sin2x}+4\right)=0$",
          r"$\cos2x=0$ or $\sin2x=-\tfrac14$",
          r"Answer: $x=45^\circ,\ 97.2^\circ,\ 135^\circ,\ 172.8^\circ$"],
         [r"Replace $1+\cos2\theta$ with $2\cos^2\theta$ and $1-\cos2\theta$ with $2\sin^2\theta$, then factorise",
          r"Cancel the 1s on the top and bottom",
          r"Divide the top and bottom by $\cos2\theta$",
          r"Use the R-form on the numerator"]),
    card(1, 11,
         [r"The region $R$ is bounded by $y=(\ln x)^2$, the $x$-axis and the lines $x=1$ and $x=3$.",
          r"$x$: 1, 1.5, 2, 2.5, 3. $y$: 0, 0.1644, 0.4805, 0.8396, 1.2069",
          r"(a) Use the trapezium rule with all the values in the table to estimate the area of $R$ to 3 s.f.",
          r"(b) Use algebraic integration to find the exact area, in the form $a(\ln3)^2+b\ln3+c$."],
         [r"Spot: $(\ln x)^2$ has no standard integral, so use integration by parts with $u=(\ln x)^2$ and $\dfrac{dv}{dx}=1$. You'll need parts again.",
          r"Use: $\displaystyle\int u\frac{dv}{dx}dx=uv-\int v\frac{du}{dx}dx$ (booklet).",
          r"(a) $0.25\left[(0+1.2069)+2(0.1644+0.4805+0.8396)\right]\approx1.04$",
          r"(b) $\displaystyle\int(\ln x)^2dx=x(\ln x)^2-2x\ln x+2x$, so $\left[\;\right]_1^3=3(\ln3)^2-6\ln3+6-2$",
          r"Answer: $3(\ln3)^2-6\ln3+4$"],
         [r"Use integration by parts with $u=(\ln x)^2$ and $\dfrac{dv}{dx}=1$",
          r"Integrate to $\dfrac{(\ln x)^3}{3}$",
          r"Use the substitution $u=x^2$",
          r"Write $(\ln x)^2$ as $\ln(x^2)$"],
         ask="How do you start part (b)?"),
    card(1, 12,
         [r"A golf ball is hit from a platform 4 m high. Its height $H$ m is modelled as a quadratic in its horizontal distance $x$ m.",
          r"It reaches its maximum height after travelling 60 m horizontally, and it is 19 m high after travelling 90 m.",
          r"(a) Find $H$ in terms of $x$.",
          r"(b) Find the maximum height and the horizontal distance when the ball hits the ground, to the nearest metre.",
          r"(c) Give one limitation of the model other than wind or air resistance."],
         [r"Spot: you know where the maximum is, so use vertex form $H=a(x-60)^2+c$. Then use the two points.",
          r"Use: $H(0)=4$ and $H(90)=19$.",
          r"(a) $3600a+c=4$ and $900a+c=19$, so $a=-\dfrac{1}{180}$ and $c=24$: $H=24-\dfrac{(x-60)^2}{180}$",
          r"(b) The maximum is 24 m. $H=0\Rightarrow(x-60)^2=4320\Rightarrow x\approx126$ m",
          r"(c) For example: it treats the ball as a particle, or assumes the ground is horizontal."],
         [r"Write $H=a(x-60)^2+c$, then use $H(0)=4$ and $H(90)=19$",
          r"Write $H=ax(x-60)$",
          r"Write $H=a(x-90)^2+4$",
          r"Write $H=-x^2+60x+4$"]),
    card(1, 13,
         [r"A curve $C$ has parametric equations $x=\dfrac{5-t^2}{t^2+1}$, $y=\dfrac{6t}{t^2+1}$, $t\in\mathbb{R}$.",
          r"Show that all points on $C$ satisfy $(x-2)^2+y^2=9$."],
         [r"Spot: “show all points satisfy” means substitute the parametric expressions into the left-hand side and simplify to 9.",
          r"Use: $x-2=\dfrac{5-t^2-2t^2-2}{t^2+1}=\dfrac{3(1-t^2)}{t^2+1}$.",
          r"Method: $(x-2)^2+y^2=\dfrac{9(1-t^2)^2+36t^2}{(t^2+1)^2}=\dfrac{9(1+t^2)^2}{(t^2+1)^2}=9$"],
         [r"Work out $x-2$ as a single fraction, then add $y^2$",
          r"Solve for $t$ in terms of $x$, then substitute into $y$",
          r"Differentiate both equations",
          r"Set $t=0$ and check"]),
    card(1, 14,
         [r"Given that $y=\dfrac{\sqrt x-3}{1+\sqrt x}$, $x>0$, show that $\dfrac{dy}{dx}=\dfrac{A}{\sqrt x(1+\sqrt x)^2}$, where $A$ is a constant to be found."],
         [r"Spot: a quotient involving $\sqrt x$ means the quotient rule, with $\dfrac{d}{dx}\sqrt x=\dfrac{1}{2\sqrt x}$.",
          r"Use: $\dfrac{du}{dx}=\dfrac{dv}{dx}=\dfrac{1}{2\sqrt x}$.",
          r"Method: $\dfrac{\frac{1}{2\sqrt x}(1+\sqrt x)-(\sqrt x-3)\frac{1}{2\sqrt x}}{(1+\sqrt x)^2}=\dfrac{\frac{4}{2\sqrt x}}{(1+\sqrt x)^2}$",
          r"Answer: $A=2$"],
         [r"Use the quotient rule with $\dfrac{d}{dx}\sqrt x=\dfrac{1}{2\sqrt x}$",
          r"Differentiate the top and bottom separately",
          r"Cancel the $\sqrt x$ first",
          r"Use the product rule without the chain rule"]),
    card(1, 15,
         [r"(i) Use proof by exhaustion to show that $2^n<(n+1)^2$ for $n\in\mathbb{N}$, $n\le5$.",
          r"(ii) Given that $m^3-2$ is odd, use proof by contradiction to show that $m$ is odd."],
         [r"Spot: (i) “exhaustion” means check every case. (ii) “Contradiction” means assume the opposite ($m$ even) and show it's impossible.",
          r"Use: even $=2k$, and even $\times$ even is even.",
          r"(i) $n=1$: $2<4$. $n=2$: $4<9$. $n=3$: $8<16$. $n=4$: $16<25$. $n=5$: $32<36$. It's true in every case.",
          r"(ii) Suppose $m=2k$. Then $m^3-2=8k^3-2=2(4k^3-1)$ is even, which contradicts $m^3-2$ being odd. So $m$ is odd."],
         [r"Check $n=1,2,3,4,5$ one by one",
          r"Prove it for $n=1$ and assume the rest",
          r"Use the binomial expansion of $(n+1)^2$",
          r"Take logs of both sides"]),

    # ---------------- Paper 2 ----------------
    card(2, 1,
         [r"In an arithmetic series, the first term is 7 and the 31st term is 22.",
          r"(a) Find the common difference.",
          r"(b) Hence find the sum of the first 400 terms."],
         [r"Spot: an arithmetic series means use $u_n=a+(n-1)d$, then $S_n$.",
          r"Use: $S_n=\dfrac n2\left[2a+(n-1)d\right]$ (booklet).",
          r"(a) $7+30d=22\Rightarrow d=0.5$",
          r"(b) $S_{400}=200\left[14+399(0.5)\right]=42\,700$"],
         [r"Use $u_{31}=a+30d$ to find $d$",
          r"Use $u_{31}=a+31d$",
          r"Divide 22 by 31",
          r"Use the geometric series formula"]),
    card(2, 2,
         [r"$f(x)=9-3x^2$, $x\in\mathbb{R}$, and $g(x)=\dfrac{2x}{4x-1}$, $x\ne\tfrac14$.",
          r"(a) State the range of $f$.",
          r"(b) Find $gf(1.5)$.",
          r"(c) Find $g^{-1}(x)$."],
         [r"Spot: $gf(1.5)$ means apply $f$ first, then $g$. For the inverse, swap the roles and make $x$ the subject.",
          r"Use: $y(4x-1)=2x$, then collect the $x$ terms.",
          r"(a) $f(x)\le9$",
          r"(b) $f(1.5)=2.25$, so $g(2.25)=\dfrac{4.5}{8}=\dfrac{9}{16}$",
          r"(c) $x(4y-2)=y\Rightarrow g^{-1}(x)=\dfrac{x}{4x-2}$"],
         [r"Find $f(1.5)$ first, then put the result into $g$",
          r"Find $g(1.5)$ first, then put the result into $f$",
          r"Multiply $f(1.5)$ by $g(1.5)$",
          r"Add $f(1.5)$ and $g(1.5)$"],
         ask="How do you find $gf(1.5)$?"),
    card(2, 3,
         [r"Using the laws of logarithms, solve $\log_2(7y+1)-\log_2(1-2y)=4$."],
         [r"Spot: a difference of logs with the same base means combine them into one log with $\log a-\log b=\log\dfrac ab$.",
          r"Use: $\log_2X=4\Rightarrow X=2^4$.",
          r"Method: $\dfrac{7y+1}{1-2y}=16\Rightarrow7y+1=16-32y\Rightarrow39y=15$",
          r"Answer: $y=\dfrac{5}{13}$ (and $1-2y>0$, so it's valid)"],
         [r"Combine into $\log_2\dfrac{7y+1}{1-2y}=4$",
          r"Write it as $\dfrac{\log_2(7y+1)}{\log_2(1-2y)}=4$",
          r"Subtract the insides: $\log_2(9y)=4$",
          r"Use $2^4=8$"]),
    card(2, 4,
         [r"Given that $\theta$ is small and in radians, use small angle approximations to show that $5\tan\dfrac{\theta}{5}+4\cos^2\dfrac{\theta}{2}\approx a+b\theta+c\theta^2$, where $a$, $b$ and $c$ are integers to be found."],
         [r"Spot: small $\theta$ in radians means the booklet approximations, applied to the whole angle.",
          r"Use: $\tan x\approx x$ and $\cos x\approx1-\dfrac{x^2}{2}$. Drop terms beyond $\theta^2$.",
          r"Method: $5\cdot\dfrac{\theta}{5}=\theta$ and $\cos^2\dfrac\theta2\approx\left(1-\dfrac{\theta^2}{8}\right)^2\approx1-\dfrac{\theta^2}{4}$",
          r"Answer: $4+\theta-\theta^2$, so $a=4$, $b=1$, $c=-1$"],
         [r"Use $\tan\frac\theta5\approx\frac\theta5$ and $\cos\frac\theta2\approx1-\frac{\theta^2}{8}$",
          r"Use $\cos\frac\theta2\approx1-\frac{\theta^2}{2}$",
          r"Use $\tan\frac\theta5\approx\theta$",
          r"Use $\cos^2\frac\theta2\approx1$"]),
    card(2, 5,
         [r"The curve $C$ has equation $y=3x^4-16x^3+30x^2-24x+7$.",
          r"(a) Find $\dfrac{dy}{dx}$ and $\dfrac{d^2y}{dx^2}$.",
          r"(b) Verify that $C$ has a stationary point at $x=1$, and show that it is a point of inflection."],
         [r"Spot: a stationary point of inflection means $\dfrac{dy}{dx}=0$ and $\dfrac{d^2y}{dx^2}=0$, but the gradient doesn't change sign. Check either side.",
          r"Use: $\dfrac{dy}{dx}=12(x-1)^2(x-2)$.",
          r"(a) $\dfrac{dy}{dx}=12x^3-48x^2+60x-24$ and $\dfrac{d^2y}{dx^2}=36x^2-96x+60$",
          r"(b) At $x=1$, both are 0. $\dfrac{dy}{dx}<0$ just before and just after $x=1$, so it's a stationary point of inflection."],
         [r"Differentiate twice, then check the sign of $\dfrac{dy}{dx}$ either side of $x=1$",
          r"Show that $\dfrac{d^2y}{dx^2}=0$ and stop",
          r"Show that $\dfrac{d^2y}{dx^2}>0$",
          r"Set $y=0$"],
         ask="How do you show it's a point of inflection?"),
    card(2, 6,
         [r"A logo is made from two congruent sectors $OAB$ and $OFE$ of radius $r$, and a sector $ODC$ of radius $3r$ with angle $COD=\theta$. $AOF$ is a straight line.",
          r"(a) Write down angle $AOB$ in terms of $\theta$.",
          r"(b) Show that the area of the logo is $\dfrac12r^2(\pi+8\theta)$.",
          r"(c) Find the perimeter of the logo in terms of $r$, $\theta$ and $\pi$."],
         [r"Spot: angles on a straight line add up to $\pi$. Each sector uses its own radius in $\tfrac12r^2\theta$ and $r\theta$.",
          r"Use: angle $AOB=\dfrac{\pi-\theta}{2}$.",
          r"(b) $2\times\dfrac12r^2\cdot\dfrac{\pi-\theta}{2}+\dfrac12(3r)^2\theta=\dfrac12r^2(\pi-\theta+9\theta)$",
          r"(c) Arcs: $r(\pi-\theta)+3r\theta$. Straight edges: $r+2r+2r+r=6r$.",
          r"Answer: $r(6+\pi+2\theta)$"],
         [r"Use $\angle AOB=\dfrac{\pi-\theta}{2}$, then $\tfrac12r^2\theta$ for each sector",
          r"Use $\angle AOB=\pi-\theta$",
          r"Use radius $r$ for all three sectors",
          r"Use degrees in the sector formulas"]),
    card(2, 7,
         [r"$C$ has equation $y=x^3-8x^2+19x-10$, and $P(4,2)$ lies on $C$. The line $l$ is the tangent to $C$ at $P$.",
          r"(a) Find the equation of $l$ in the form $y=mx+c$.",
          r"(b) Verify that $l$ meets $C$ again on the $y$-axis.",
          r"(c) Find the exact area of the region $R$ between $C$ and $l$."],
         [r"Spot: area between a curve and a line means integrate (top $-$ bottom) between the intersections.",
          r"Use: $\dfrac{dy}{dx}=3x^2-16x+19$, and curve $-$ line $=x(x-4)^2$.",
          r"(a) The gradient at $x=4$ is $3$, so $y=3x-10$.",
          r"(b) $x^3-8x^2+16x=0\Rightarrow x(x-4)^2=0$, so they meet again at $x=0$.",
          r"(c) $\displaystyle\int_0^4\left(x^3-8x^2+16x\right)dx=64-\frac{512}{3}+128$",
          r"Answer: $\dfrac{64}{3}$"],
         [r"Differentiate, find the gradient at $x=4$, then use $y-2=m(x-4)$",
          r"Use the gradient of the line joining $P$ to the origin",
          r"Integrate the curve to find the tangent",
          r"Set $y=0$"]),
    card(2, 8,
         [r"The curve $C$ has equation $px^3+qxy+2y^2=7$, where $p$ and $q$ are constants.",
          r"(a) Show that $\dfrac{dy}{dx}=\dfrac{apx^2+bqy}{qx+cy}$, where $a$, $b$ and $c$ are integers.",
          r"(b) $P(1,2)$ lies on $C$, and the normal to $C$ at $P$ has equation $6x-5y+4=0$. Find $p$ and $q$."],
         [r"Spot: $x$ and $y$ mixed together means implicit differentiation. A point on $C$ and a normal gradient give two equations.",
          r"Use: product rule on $qxy$; normal gradient $\tfrac65$, so tangent gradient $-\tfrac56$.",
          r"(a) $3px^2+qy+qx\dfrac{dy}{dx}+4y\dfrac{dy}{dx}=0\Rightarrow\dfrac{dy}{dx}=\dfrac{-3px^2-qy}{qx+4y}$",
          r"(b) On $C$: $p+2q=-1$. Gradient: $\dfrac{-3p-2q}{q+8}=-\dfrac56\Rightarrow18p+7q=40$.",
          r"Answer: $p=3$ and $q=-2$"],
         [r"Differentiate implicitly, using the product rule on $qxy$",
          r"Treat $q$ and $y$ as constants",
          r"Rearrange for $y$ first",
          r"Differentiate $2y^2$ as $4y$"]),
    card(2, 9,
         [r"Show that $\displaystyle\sum_{n=3}^{\infty}\left(\frac25\right)^n\cos(180n^\circ)=-\frac{8}{175}$."],
         [r"Spot: $\cos(180n^\circ)$ alternates $-1,1,-1,\dots$, so the sum is a geometric series with ratio $-\tfrac25$.",
          r"Use: $S_\infty=\dfrac{a}{1-r}$ with the first term at $n=3$.",
          r"Method: $\displaystyle\sum_{n=3}^{\infty}\left(-\frac25\right)^n$ has $a=-\dfrac{8}{125}$ and $r=-\dfrac25$",
          r"$S_\infty=\dfrac{-8/125}{1+2/5}=-\dfrac{8}{175}$"],
         [r"Notice $\cos(180n^\circ)=(-1)^n$, so the ratio is $-\tfrac25$",
          r"Use the ratio $\tfrac25$",
          r"Notice $\cos(180n^\circ)=1$ for every $n$",
          r"Use the arithmetic series formula"]),
    card(2, 10,
         [r"The time $T$ s for one swing of a pendulum of length $l$ m is modelled by $T=al^b$.",
          r"(a) Show that $\log_{10}T=b\log_{10}l+\log_{10}a$.",
          r"(b) A graph of $\log_{10}T$ against $\log_{10}l$ is a straight line through $(-0.5,0)$ and $(0.3,0.4)$. Find $a$ and $b$ to 3 s.f.",
          r"(c) Interpret the value of $a$."],
         [r"Spot: a power law $T=al^b$ becomes a straight line on a log–log graph. The gradient is $b$ and the intercept is $\log a$.",
          r"Use: $\log(al^b)=\log a+b\log l$.",
          r"(b) $b=\dfrac{0.4-0}{0.3+0.5}=0.5$. Then $\log a=0.4-0.5(0.3)=0.25$, so $a=10^{0.25}\approx1.78$.",
          r"Answer: $T=1.78\,l^{0.5}$",
          r"(c) $a$ is the time, in seconds, for one swing of a pendulum 1 m long."],
         [r"Take logs of both sides and use $\log al^b=\log a+b\log l$",
          r"Write $\log T=a\log l+b$",
          r"Use $\log(al^b)=b\log(al)$",
          r"Differentiate both sides"]),
    card(2, 11,
         [r"$k$ is a positive constant, and $f(x)=k-|3x-2k|$.",
          r"(a) Sketch $y=f(x)$, giving the maximum point and where the graph cuts the axes.",
          r"(b) Find, in set notation, the values of $x$ for which $k-|3x-2k|>x-k$.",
          r"(c) Find the minimum point of $y=2-4f\left(\dfrac x3\right)$."],
         [r"Spot: $k-|\dots|$ is an upside-down V. Solve modulus inequalities by splitting at $3x-2k=0$.",
          r"Use: for $x\ge\tfrac{2k}{3}$, $|3x-2k|=3x-2k$, and for $x<\tfrac{2k}{3}$, $|3x-2k|=2k-3x$.",
          r"(a) The maximum is $\left(\tfrac{2k}{3},k\right)$. It cuts the $y$-axis at $(0,-k)$ and the $x$-axis at $\left(\tfrac k3,0\right)$ and $(k,0)$.",
          r"(b) The two cases give $\tfrac{2k}3\le x<k$ and $0<x<\tfrac{2k}{3}$, so $\{x:0<x<k\}$",
          r"(c) $x$ is stretched by 3 and $y$ by $-4$, then shifted up by 2: $(2k,\,2-4k)$"],
         [r"Split at $3x-2k=0$ and solve each case, keeping its condition",
          r"Square both sides",
          r"Remove the modulus and solve once",
          r"Set $x=k$"],
         ask="How do you solve part (b)?"),
    card(2, 12,
         [r"(a) Use the substitution $u=1+\sqrt x$ to show that $\displaystyle\int_0^9\frac{x}{1+\sqrt x}\,dx=\int_p^q\frac{2(u-1)^3}{u}\,du$, where $p$ and $q$ are constants.",
          r"(b) Hence show that the integral equals $A-B\ln2$, where $A$ and $B$ are constants to be found."],
         [r"Spot: a substitution question means change $x$, $dx$ and the limits. Then split the fraction into separate powers of $u$.",
          r"Use: $x=(u-1)^2$, $dx=2(u-1)\,du$; $x=0\to u=1$, $x=9\to u=4$.",
          r"(a) $\dfrac{(u-1)^2}{u}\cdot2(u-1)\,du$, with $p=1$ and $q=4$",
          r"(b) $\displaystyle2\int_1^4\left(u^2-3u+3-\frac1u\right)du=2\left[\frac{u^3}{3}-\frac{3u^2}{2}+3u-\ln u\right]_1^4$",
          r"Answer: $15-4\ln2$"],
         [r"Write $x=(u-1)^2$ and $dx=2(u-1)\,du$, and change the limits",
          r"Write $x=u-1$ and $dx=du$",
          r"Keep the limits 0 and 9",
          r"Use integration by parts"]),
    card(2, 13,
         [r"The curve $C$ has parametric equations $x=\cos2\theta$, $y=\sec^3\theta$, $0<\theta<\dfrac{\pi}{2}$.",
          r"(a) Find $\dfrac{dy}{dx}$ in terms of $\theta$.",
          r"(b) Find the exact gradient of the tangent where $y=8$."],
         [r"Spot: parametric equations mean $\dfrac{dy}{dx}=\dfrac{dy/d\theta}{dx/d\theta}$. Then use $y=8$ to find $\theta$.",
          r"Use: $\dfrac{d}{d\theta}\sec^3\theta=3\sec^3\theta\tan\theta$ (chain rule) and $\dfrac{d}{d\theta}\cos2\theta=-2\sin2\theta$.",
          r"(a) $\dfrac{dy}{dx}=\dfrac{3\sec^3\theta\tan\theta}{-2\sin2\theta}$",
          r"(b) $\sec^3\theta=8\Rightarrow\sec\theta=2\Rightarrow\theta=\dfrac{\pi}{3}$",
          r"Answer: $\dfrac{3\cdot8\cdot\sqrt3}{-2\cdot\frac{\sqrt3}{2}}=-24$"],
         [r"Use $\dfrac{dy}{dx}=\dfrac{dy/d\theta}{dx/d\theta}$",
          r"Use $\dfrac{dy}{dx}=\dfrac{dx/d\theta}{dy/d\theta}$",
          r"Eliminate $\theta$ first",
          r"Differentiate $y$ with respect to $x$ directly, treating $\theta$ as a constant"]),
    card(2, 14,
         [r"A cuboid tank has a base of 6 m by 4 m and a height of 4 m. Water flows in at $0.6\text{ m}^3$ per minute and leaves through a tap at $0.2h\text{ m}^3$ per minute, where $h$ m is the depth.",
          r"(a) Show that $120\dfrac{dh}{dt}=3-h$.",
          r"(b) The depth is 1 m when the tap is opened. Show that $h=A+Be^{-kt}$, and find $A$, $B$ and $k$.",
          r"(c) Will the tank ever become full? Give a reason."],
         [r"Spot: rate in $-$ rate out $=\dfrac{dV}{dt}$, and $V=24h$. Then separate the variables.",
          r"Use: $\dfrac{dV}{dt}=24\dfrac{dh}{dt}$, and $\displaystyle\int\frac{dh}{3-h}=-\ln|3-h|$.",
          r"(a) $24\dfrac{dh}{dt}=0.6-0.2h$. Multiply by 5: $120\dfrac{dh}{dt}=3-h$.",
          r"(b) $-\ln|3-h|=\dfrac{t}{120}+c\Rightarrow3-h=2e^{-\frac{t}{120}}$, so $h=3-2e^{-\frac{t}{120}}$, with $A=3$, $B=-2$ and $k=\tfrac{1}{120}$.",
          r"(c) No: $h\to3$ m, which is below the 4 m height of the tank."],
         [r"Use rate in $-$ rate out $=24\dfrac{dh}{dt}$",
          r"Use rate in $+$ rate out",
          r"Use $V=h^3$",
          r"Set $\dfrac{dh}{dt}=0.6$"]),
    card(2, 15,
         [r"(a) Express $3\cos\theta-2\sin\theta$ as $R\cos(\theta+\alpha)$, with $R>0$ and $0<\alpha<\dfrac{\pi}{2}$. Give $R$ exactly and $\alpha$ to 3 d.p.",
          r"The height $H$ m of a point $P$ on a water wheel above the water level is modelled by $H=2+6\cos(0.4t)-4\sin(0.4t)$.",
          r"(b) Find the maximum height, and the value of $t$ when it first occurs, to 1 d.p.",
          r"(c) Find the time $T$ that $P$ spends below the water in each revolution, to 3 s.f."],
         [r"Spot: $a\cos\theta-b\sin\theta$ means use the R-form $R\cos(\theta+\alpha)$. The maximum is when the cosine equals 1.",
          r"Use: $R\cos\alpha=3$, $R\sin\alpha=2$, so $R=\sqrt{13}$ and $\alpha=0.588$. Then $H=2+2\sqrt{13}\cos(0.4t+0.588)$.",
          r"(b) The maximum is $2+2\sqrt{13}\approx9.21$ m, when $0.4t+0.588=2\pi$, so $t\approx14.2$ s.",
          r"(c) $H<0\Rightarrow\cos(0.4t+\alpha)<-\dfrac{1}{\sqrt{13}}$. That's an angle range of $2\arccos\dfrac{1}{\sqrt{13}}\approx2.580$.",
          r"Answer: $T=\dfrac{2.580}{0.4}\approx6.45$ s"],
         [r"Use $R\cos\alpha=3$ and $R\sin\alpha=2$",
          r"Use $R\cos\alpha=2$ and $R\sin\alpha=3$",
          r"Use $R=3+2$",
          r"Use $\tan\alpha=\tfrac32$"]),
]


def check():
    a = sp.symbols("a")
    # P1 Q1
    assert sp.solve((a * x**3 + 7 * x**2 - 2 * a * x - 12).subs(x, 2), a) == [-4]
    # P1 Q2
    assert same(x**2 + 6 * x + 14, (x + 3)**2 + 5)
    # P1 Q3
    kk = sp.symbols("kk")
    u2 = kk - 10
    u3 = kk - 30 / u2
    assert same(sp.numer(sp.together(3 + 2 * u2 + u3)), 3 * kk**2 - 47 * kk + 140)
    assert sorted(sp.solve(3 * kk**2 - 47 * kk + 140, kk)) == [4, sp.Rational(35, 3)]
    assert u3.subs(kk, 4) == 9
    # P1 Q4
    F = x**2 + sp.log(x**2 - 2 * x + 3)
    assert same(sp.numer(sp.together(sp.diff(F, x))), 2 * (x**3 - 2 * x**2 + 4 * x - 1))
    xs = [0.25]
    for _ in range(3):
        xs.append((1 + 2 * xs[-1]**2 - xs[-1]**3) / 4)
    assert round(xs[1], 4) == 0.2773 and round(xs[3], 4) == 0.2844
    g = lambda v: v**3 - 2 * v**2 + 4 * v - 1
    assert g(0.2845) < 0 < g(0.2855)
    # P1 Q5
    assert round(15000 * 1.06**2) == 16854
    n = math.log(8 / 3) / math.log(1.06)
    assert round(n, 1) == 16.8 and math.floor(n) + 2 == 18
    assert 15000 * 1.06**16 <= 40000 < 15000 * 1.06**17
    assert round(15000 * (1.06**25 - 1) / 0.06, -3) == 823000
    # P1 Q6
    AB, BC = sp.Matrix([-2, -1, -2]), sp.Matrix([4, 0, 3])
    assert AB + BC == sp.Matrix([2, -1, 1])
    BA = -AB
    assert BA.dot(BC) / (BA.norm() * BC.norm()) == sp.Rational(14, 15)
    # P1 Q7
    assert same(x**2 + y**2 + 6 * x - 8 * y + 5, (x + 3)**2 + (y - 4)**2 - 20)
    quad = sp.expand((x + 3)**2 + (x + k - 4)**2 - 20)
    disc = sp.discriminant(quad, x)
    assert sorted(sp.solve(disc, k), key=float) == [7 - 2 * sp.sqrt(10), 7 + 2 * sp.sqrt(10)]
    assert same(quad, 2 * x**2 + (2 * k - 2) * x + k**2 - 8 * k + 5)
    # P1 Q8
    kr = math.log(3) / 6
    assert round(kr * 800 * 3**(4 / 6), -1) == 300
    T = 2 * math.log(4) / kr
    assert round(T, 1) == 15.1 and close(800 * math.exp(kr * T), 200 * math.exp(1.5 * kr * T))
    # P1 Q9
    f9 = (27 * x**2 + 16 * x + 5) / ((3 * x + 1)**2 * (1 - x))
    assert same(f9, 2 / (3 * x + 1)**2 + 3 / (1 - x))
    assert same(sp.series(f9, x, 0, 3).removeO(), 5 - 9 * x + 57 * x**2)
    # P1 Q10
    lhs = (1 + sp.cos(2 * theta) - sp.sin(2 * theta)) / (1 - sp.cos(2 * theta) - sp.sin(2 * theta))
    assert identity(lhs + sp.cot(theta), theta, 0.9, 1.5)
    sols = [45, 135, 180 + math.degrees(math.asin(0.25)), 360 - math.degrees(math.asin(0.25))]
    sols = [s if s < 180 else s / 2 for s in sols]
    sols = [45, 135, (180 + math.degrees(math.asin(0.25))) / 2, (360 - math.degrees(math.asin(0.25))) / 2]
    for d in sols:
        xr = math.radians(d)
        den = 1 - math.cos(4 * xr) - math.sin(4 * xr)
        assert abs(den) > 1e-6
        assert abs((1 + math.cos(4 * xr) - math.sin(4 * xr)) / den - 4 * math.cos(2 * xr)) < 1e-9
    assert sorted(round(d, 1) for d in sols) == [45, 97.2, 135, 172.8]
    # P1 Q11
    ys = [math.log(v)**2 for v in (1, 1.5, 2, 2.5, 3)]
    assert [round(v, 4) for v in ys] == [0, 0.1644, 0.4805, 0.8396, 1.2069]
    assert round(0.25 * ((0 + 1.2069) + 2 * (0.1644 + 0.4805 + 0.8396)), 2) == 1.04
    assert same(sp.integrate(sp.log(x)**2, (x, 1, 3)), 3 * sp.log(3)**2 - 6 * sp.log(3) + 4)
    # P1 Q12
    H = 24 - (x - 60)**2 / 180
    assert H.subs(x, 0) == 4 and H.subs(x, 90) == 19
    land = 60 + math.sqrt(4320)
    assert round(land) == 126
    # P1 Q13
    X = (5 - t**2) / (t**2 + 1)
    Y = 6 * t / (t**2 + 1)
    assert same((X - 2)**2 + Y**2, 9)
    # P1 Q14
    Yq = (sp.sqrt(x) - 3) / (1 + sp.sqrt(x))
    assert same(sp.diff(Yq, x), 2 / (sp.sqrt(x) * (1 + sp.sqrt(x))**2))
    # P1 Q15
    assert all(2**m < (m + 1)**2 for m in range(1, 6)) and not 2**6 < 49
    assert all((m**3 - 2) % 2 == 0 for m in range(-50, 51, 2))

    # P2 Q1
    d = sp.Rational(15, 30)
    assert 7 + 30 * d == 22 and 200 * (14 + 399 * d) == 42700
    # P2 Q2
    fv = 9 - 3 * sp.Rational(3, 2)**2
    assert fv == sp.Rational(9, 4) and 2 * fv / (4 * fv - 1) == sp.Rational(9, 16)
    gi = x / (4 * x - 2)
    assert same(gi.subs(x, 2 * y / (4 * y - 1)), y)
    # P2 Q3
    yy = sp.solve(sp.Eq((7 * y + 1) / (1 - 2 * y), 16), y)
    assert yy == [sp.Rational(5, 13)] and 1 - 2 * yy[0] > 0
    # P2 Q4
    expr = 5 * sp.tan(theta / 5) + 4 * sp.cos(theta / 2)**2
    ser = sp.series(expr, theta, 0, 3).removeO()
    assert same(ser, 4 + theta - theta**2)
    # P2 Q5
    Yc = 3 * x**4 - 16 * x**3 + 30 * x**2 - 24 * x + 7
    d1 = sp.diff(Yc, x)
    assert same(d1, 12 * (x - 1)**2 * (x - 2)) and d1.subs(x, 1) == 0 and sp.diff(Yc, x, 2).subs(x, 1) == 0
    assert d1.subs(x, 0.9) < 0 and d1.subs(x, 1.1) < 0
    # P2 Q6
    r_ = sp.symbols("r_", positive=True)
    area = 2 * sp.Rational(1, 2) * r_**2 * (sp.pi - theta) / 2 + sp.Rational(1, 2) * (3 * r_)**2 * theta
    assert same(area, r_**2 * (sp.pi + 8 * theta) / 2)
    perim = 2 * r_ * (sp.pi - theta) / 2 + 3 * r_ * theta + r_ + 2 * r_ + 2 * r_ + r_
    assert same(perim, r_ * (6 + sp.pi + 2 * theta))
    # P2 Q7
    Yr = x**3 - 8 * x**2 + 19 * x - 10
    assert Yr.subs(x, 4) == 2 and sp.diff(Yr, x).subs(x, 4) == 3
    assert same(Yr - (3 * x - 10), x * (x - 4)**2)
    assert sp.integrate(Yr - (3 * x - 10), (x, 0, 4)) == sp.Rational(64, 3)
    # P2 Q8
    p, q = sp.symbols("p q")
    Fc = p * x**3 + q * x * y + 2 * y**2 - 7
    dydx = -sp.diff(Fc, x) / sp.diff(Fc, y)
    assert same(dydx, (-3 * p * x**2 - q * y) / (q * x + 4 * y))
    sol = sp.solve([Fc.subs({x: 1, y: 2}), dydx.subs({x: 1, y: 2}) + sp.Rational(5, 6)], [p, q])
    assert sol == {p: 3, q: -2}
    # normal at (1,2) with tangent gradient -5/6 has gradient 6/5: 6x - 5y + 4 = 0
    assert 6 * 1 - 5 * 2 + 4 == 0
    # P2 Q9
    nn = sp.Symbol("nn", integer=True)
    assert sp.summation(sp.Rational(2, 5)**nn * sp.cos(sp.pi * nn), (nn, 3, sp.oo)) == -sp.Rational(8, 175)
    # P2 Q10
    assert round(10**0.25, 2) == 1.78 and (0.4 - 0) / (0.3 + 0.5) == 0.5
    # P2 Q11
    kv = 3.0
    f = lambda v: kv - abs(3 * v - 2 * kv)
    assert f(2 * kv / 3) == kv and f(0) == -kv and abs(f(kv / 3)) < 1e-12 and f(kv) == 0
    xs_ok = [v / 100 for v in range(-300, 900) if f(v / 100) > v / 100 - kv]
    assert min(xs_ok) > 0 and max(xs_ok) < kv and min(xs_ok) <= 0.02 and max(xs_ok) >= kv - 0.02
    # min of 2 - 4 f(x/3): at x/3 = 2k/3
    assert 2 - 4 * f((2 * kv) / 3) == 2 - 4 * kv
    # P2 Q12
    us = sp.Symbol("us", positive=True)
    val = sp.integrate(2 * (us - 1)**3 / us, (us, 1, 4))
    assert same(val, 15 - 4 * sp.log(2))
    assert close(sp.Integral(x / (1 + sp.sqrt(x)), (x, 0, 9)).evalf(), float(15 - 4 * sp.log(2)), 1e-8)
    # P2 Q13
    th = sp.pi / 3
    dydx = sp.diff(1 / sp.cos(theta)**3, theta) / sp.diff(sp.cos(2 * theta), theta)
    assert same(dydx.subs(theta, th), -24) and same((1 / sp.cos(th))**3, 8)
    # P2 Q14
    hh = 3 - 2 * sp.exp(-t / 120)
    assert hh.subs(t, 0) == 1 and same(120 * sp.diff(hh, t) - (3 - hh), 0)
    # P2 Q15
    al = math.atan2(2, 3)
    assert round(al, 3) == 0.588
    assert identity(3 * sp.cos(x) - 2 * sp.sin(x) - sp.sqrt(13) * sp.cos(x + sp.atan(sp.Rational(2, 3))), x)
    assert round(2 + 2 * math.sqrt(13), 2) == 9.21
    tmax = (2 * math.pi - al) / 0.4
    assert round(tmax, 1) == 14.2
    width = 2 * math.acos(1 / math.sqrt(13))
    assert round(width, 3) == 2.580 and round(width / 0.4, 2) == 6.45
    ts = [i / 1000 for i in range(0, int(2 * math.pi / 0.4 * 1000))]
    below = sum(1 for tt in ts if 2 + 6 * math.cos(0.4 * tt) - 4 * math.sin(0.4 * tt) < 0) / 1000
    assert abs(below - 6.45) < 0.01
