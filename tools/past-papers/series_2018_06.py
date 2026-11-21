"""June 2018 (9MA0/01 and 9MA0/02), with the numbers changed."""
import math
import sympy as sp
from common import card, close, same, identity, x, y, t, k, r, theta, h, u

SERIES = {"id": "paper-2018-06", "title": "June 2018", "hue": 15}

CARDS = [
    # ---------------- Paper 1 ----------------
    card(1, 1,
         [r"Given that $\theta$ is small and measured in radians, use the small angle approximations to find an approximate value of",
          r"$\dfrac{1-\cos6\theta}{3\theta\sin2\theta}$"],
         [r"Spot: “$\theta$ is small, in radians” means use the small angle approximations (in the formula booklet).",
          r"Use: $\sin x\approx x$ and $\cos x\approx1-\dfrac{x^2}{2}$, applied to the whole angle.",
          r"Method: $1-\cos6\theta\approx1-\left(1-\dfrac{(6\theta)^2}{2}\right)=18\theta^2$ and $3\theta\sin2\theta\approx3\theta\cdot2\theta=6\theta^2$.",
          r"Answer: $\dfrac{18\theta^2}{6\theta^2}=3$"],
         [r"Use $\cos6\theta\approx1-\dfrac{(6\theta)^2}{2}$ and $\sin2\theta\approx2\theta$, then simplify",
          r"Use $\cos6\theta\approx1-\dfrac{\theta^2}{2}$ and $\sin2\theta\approx\theta$, then simplify",
          r"Use $\cos6\theta\approx1$ and $\sin2\theta\approx2\theta$, then simplify",
          r"Expand $\cos6\theta$ with the compound angle formula first"]),
    card(1, 2,
         [r"A curve $C$ has equation $y=x^2-12x-36\sqrt{x}$, $x>0$.",
          r"(a) Find $\dfrac{dy}{dx}$ and $\dfrac{d^2y}{dx^2}$.",
          r"(b) Verify that $C$ has a stationary point when $x=9$.",
          r"(c) Determine the nature of this stationary point, giving a reason."],
         [r"Spot: “stationary point” means $\dfrac{dy}{dx}=0$. “Nature” means look at the sign of $\dfrac{d^2y}{dx^2}$.",
          r"Use: write $\sqrt{x}=x^{\frac12}$, then the power rule.",
          r"(a) $\dfrac{dy}{dx}=2x-12-18x^{-\frac12}$ and $\dfrac{d^2y}{dx^2}=2+9x^{-\frac32}$",
          r"(b) At $x=9$: $18-12-\dfrac{18}{3}=0$, so it is stationary.",
          r"(c) At $x=9$: $\dfrac{d^2y}{dx^2}=2+\dfrac{9}{27}=\dfrac73>0$, so it is a minimum."],
         [r"Write $\sqrt x$ as $x^{\frac12}$ and differentiate term by term",
          r"Use the quotient rule on $36\sqrt x$",
          r"Integrate $y$, then set the result to zero",
          r"Set $y=0$ and solve for $x$"]),
    card(1, 3,
         [r"A sector $AOB$ of a circle has centre $O$, radius $r$ cm and angle $\theta$ radians.",
          r"The area of the sector is $12\text{ cm}^2$.",
          r"The perimeter of the sector is 5 times the length of the arc $AB$. Find the exact value of $r$."],
         [r"Spot: you're given the area and a fact about the perimeter, so write one equation for each and solve them together.",
          r"Use: arc $=r\theta$, area $=\dfrac12r^2\theta$, perimeter $=2r+r\theta$.",
          r"Method: $2r+r\theta=5r\theta\Rightarrow2=4\theta\Rightarrow\theta=\dfrac12$",
          r"Then $\dfrac12r^2\cdot\dfrac12=12\Rightarrow r^2=48$",
          r"Answer: $r=4\sqrt3$"],
         [r"Write the perimeter as $2r+r\theta=5r\theta$ to find $\theta$, then use the area",
          r"Use the area formula $\pi r^2=12$",
          r"Set the arc length equal to the area",
          r"Use the cosine rule in triangle $AOB$"]),
    card(1, 4,
         [r"The curve $y=3\ln(10-x)$ meets the line $y=x$ at a single point where $x=\alpha$.",
          r"(a) Show that $4<\alpha<5$.",
          r"(b) Starting with $x_1=5$, decide whether the iteration $x_{n+1}=3\ln(10-x_n)$ can be used to find $\alpha$. Justify your answer."],
         [r"Spot: “show that the root lies between” means a change of sign. “Can the iteration be used” means a cobweb or staircase diagram, or the gradient test.",
          r"Use: $f(x)=3\ln(10-x)-x$, which is continuous on $[4,5]$.",
          r"(a) $f(4)=3\ln6-4\approx1.38>0$ and $f(5)=3\ln5-5\approx-0.17<0$. The sign changes, so $4<\alpha<5$.",
          r"(b) For $g(x)=3\ln(10-x)$, $|g'(x)|=\dfrac{3}{10-x}\approx0.59<1$ near $\alpha$, so the cobweb spirals in.",
          r"Answer: yes. $x_2=4.828$ and $x_3=4.930$ converge to $\alpha\approx4.89$."],
         [r"Evaluate $3\ln(10-x)-x$ at $x=4$ and $x=5$ and look for a sign change",
          r"Solve $3\ln(10-x)=x$ exactly using laws of logs",
          r"Differentiate $3\ln(10-x)$ and set it to zero",
          r"Substitute $x=4.5$ and check it gives zero"]),
    card(1, 5,
         [r"Given that $y=\dfrac{5\sin\theta}{3\sin\theta+3\cos\theta}$, $-\dfrac{\pi}{4}<\theta<\dfrac{3\pi}{4}$,",
          r"show that $\dfrac{dy}{d\theta}=\dfrac{A}{1+\sin2\theta}$, where $A$ is a rational constant to be found."],
         [r"Spot: a fraction of trig functions means the quotient rule. The target $1+\sin2\theta$ hints at $(\sin\theta+\cos\theta)^2$.",
          r"Use: quotient rule (booklet), $\sin^2\theta+\cos^2\theta\equiv1$, $2\sin\theta\cos\theta\equiv\sin2\theta$.",
          r"Method: the numerator is $5\cos\theta(3\sin\theta+3\cos\theta)-5\sin\theta(3\cos\theta-3\sin\theta)=15$.",
          r"The denominator is $9(\sin\theta+\cos\theta)^2=9(1+\sin2\theta)$.",
          r"Answer: $A=\dfrac{15}{9}=\dfrac53$"],
         [r"Use the quotient rule, then simplify with $\sin^2\theta+\cos^2\theta\equiv1$",
          r"Use the product rule on $5\sin\theta$ and $3\sin\theta+3\cos\theta$ separately",
          r"Differentiate the top and the bottom separately",
          r"Use the chain rule with $u=\tan\theta$"]),
    card(1, 6,
         [r"The circle $C$ has centre $A(8,3)$. The line $l$ with equation $y=2x-3$ is a tangent to $C$ at the point $P$.",
          r"(a) Show that the line $PA$ has equation $2y+x=14$.",
          r"(b) Find an equation for $C$.",
          r"(c) The line $y=2x+k$, $k\ne-3$, is also a tangent to $C$. Find $k$."],
         [r"Spot: a tangent to a circle is perpendicular to the radius at the point of contact.",
          r"Use: perpendicular gradients multiply to $-1$; $(x-a)^2+(y-b)^2=r^2$.",
          r"(a) Gradient of $PA=-\dfrac12$: $y-3=-\dfrac12(x-8)\Rightarrow2y+x=14$",
          r"(b) Solve with $y=2x-3$: $P=(4,5)$, so $r^2=4^2+2^2=20$ and $(x-8)^2+(y-3)^2=20$.",
          r"(c) The other parallel tangent touches at $2A-P=(12,1)$, so $1=24+k$.",
          r"Answer: $k=-23$"],
         [r"Use the fact that $AP$ is perpendicular to the tangent, so its gradient is $-\frac12$",
          r"Use the fact that $AP$ has the same gradient as the tangent",
          r"Substitute $(8,3)$ into $y=2x-3$",
          r"Find where $y=2x-3$ crosses the $x$-axis"]),
    card(1, 7,
         [r"Given that $k$ is a positive constant,",
          r"(a) show that $\displaystyle\int_k^{4k}\frac{1}{2x-k}\,dx$ is independent of $k$,",
          r"(b) show that $\displaystyle\int_k^{2k}\frac{4}{(2x-k)^2}\,dx$ is inversely proportional to $k$."],
         [r"Spot: “independent of $k$” or “proportional to” means integrate, substitute the limits, then simplify until $k$ cancels or you get $\dfrac{c}{k}$.",
          r"Use: $\displaystyle\int\frac{1}{ax+b}\,dx=\frac1a\ln|ax+b|$ and $\displaystyle\int(ax+b)^{-2}\,dx=-\frac{1}{a(ax+b)}$.",
          r"(a) $\tfrac12\left[\ln(2x-k)\right]_k^{4k}=\tfrac12\ln\dfrac{7k}{k}=\tfrac12\ln7$, which has no $k$.",
          r"(b) $\left[-\dfrac{2}{2x-k}\right]_k^{2k}=-\dfrac{2}{3k}+\dfrac{2}{k}=\dfrac{4}{3k}$, which is proportional to $\dfrac1k$."],
         [r"Integrate to $\tfrac12\ln|2x-k|$, substitute the limits and use the laws of logs",
          r"Use integration by parts with $u=\dfrac{1}{2x-k}$",
          r"Substitute $k=1$ and evaluate",
          r"Differentiate with respect to $k$"]),
    card(1, 8,
         [r"The depth of water, $D$ m, in a harbour is modelled by $D=6+2.5\sin(30t)^\circ$, $0\le t<24$, where $t$ is the number of hours after midnight.",
          r"A boat enters the harbour at 6:45 am and takes 2 hours to load. It needs a depth of at least 5 m before it can leave.",
          r"(a) Find the depth when the boat enters.",
          r"(b) Find, to the nearest minute, the earliest time the boat can leave."],
         [r"Spot: a trig model with a condition on the depth means solve $D=5$, then use the shape of the graph to pick the right solution.",
          r"Use: $\sin x=c$ has solutions $x$ and $180^\circ-x$, plus multiples of $360^\circ$.",
          r"(a) $t=6.75$: $D=6+2.5\sin202.5^\circ\approx5.04$ m",
          r"(b) Loading ends at $t=8.75$, when $D\approx3.52<5$. Solve $\sin(30t)^\circ=-0.4$: $30t=203.6^\circ$ or $336.4^\circ$.",
          r"The depth climbs back to 5 m when $t=\dfrac{336.4}{30}\approx11.21$.",
          r"Answer: 11:13 am"],
         [r"Solve $6+2.5\sin(30t)^\circ=5$ and choose the solution after loading ends",
          r"Find when $D$ is a maximum",
          r"Substitute $t=8.75$ and give that time",
          r"Differentiate $D$ and set the derivative equal to $5$"],
         ask="How do you find the earliest leaving time in (b)?"),
    card(1, 9,
         [r"A curve has equation $x^2-2xy+4y^2=48$.",
          r"(a) Show that $\dfrac{dy}{dx}=\dfrac{y-x}{4y-x}$.",
          r"(b) $P$ is the point on the curve furthest west of the origin. Find the coordinates of $P$.",
          r"(c) Explain briefly how to find the point furthest north."],
         [r"Spot: $x$ and $y$ mixed together means implicit differentiation. Furthest west or east means a vertical tangent, so the denominator of $\dfrac{dy}{dx}$ is $0$.",
          r"Use: $\dfrac{d}{dx}(y^2)=2y\dfrac{dy}{dx}$, and the product rule on $2xy$.",
          r"(a) $2x-2y-2x\dfrac{dy}{dx}+8y\dfrac{dy}{dx}=0\Rightarrow\dfrac{dy}{dx}=\dfrac{y-x}{4y-x}$",
          r"(b) $4y-x=0\Rightarrow x=4y$. Substitute: $16y^2-8y^2+4y^2=48\Rightarrow y=\pm2$. West means $x<0$.",
          r"Answer: $P(-8,-2)$",
          r"(c) Set the numerator to zero ($y=x$), substitute into the curve's equation and take the point with the larger $y$."],
         [r"Differentiate implicitly, then set the denominator of $\dfrac{dy}{dx}$ to zero",
          r"Rearrange to make $y$ the subject first",
          r"Set $\dfrac{dy}{dx}=0$ to find the furthest west point",
          r"Set $x=0$ and solve for $y$"]),
    card(1, 10,
         [r"The height $H$ m of a roller coaster passenger, $t$ seconds after the start, is modelled by $\dfrac{dH}{dt}=\dfrac{H\cos(0.5t)}{20}$.",
          r"The passenger starts 4 m above the ground.",
          r"(a) Show that $H=4e^{0.1\sin(0.5t)}$.",
          r"(b) State the maximum height.",
          r"(c) Find the time when the maximum height is reached for the second time."],
         [r"Spot: $\dfrac{dH}{dt}=f(t)\,g(H)$ means separate the variables.",
          r"Use: $\displaystyle\int\frac1H\,dH=\ln H$ and $\displaystyle\int\cos(0.5t)\,dt=2\sin(0.5t)$.",
          r"(a) $\ln H=\dfrac{2\sin(0.5t)}{20}+c=0.1\sin(0.5t)+c$. At $t=0$, $H=4$, so $c=\ln4$.",
          r"(b) The maximum is when $\sin(0.5t)=1$: $H=4e^{0.1}\approx4.42$ m",
          r"(c) $0.5t=\dfrac{\pi}{2}+2\pi=\dfrac{5\pi}{2}$, so $t=5\pi\approx15.7$ s"],
         [r"Separate the variables: $\displaystyle\int\frac{1}{H}\,dH=\int\frac{\cos(0.5t)}{20}\,dt$",
          r"Integrate both sides with respect to $t$, treating $H$ as a constant",
          r"Differentiate $\dfrac{H\cos(0.5t)}{20}$ with the product rule",
          r"Substitute $t=0$ into the differential equation and stop there"]),
    card(1, 11,
         [r"(a) Use binomial expansions to show that $\sqrt{\dfrac{1+5x}{1-x}}\approx1+3x-\dfrac32x^2$.",
          r"(b) A student substitutes $x=\tfrac12$ into both sides to estimate $\sqrt7$. Explain why this isn't valid.",
          r"(c) Substitute $x=\tfrac19$ to find an approximation to $\sqrt7$, as a fraction in its simplest form."],
         [r"Spot: the square root of a fraction means write it as $(1+5x)^{\frac12}(1-x)^{-\frac12}$, then expand each part with the binomial series.",
          r"Use: $(1+x)^n=1+nx+\dfrac{n(n-1)}{2}x^2+\dots$ (booklet). It's valid when $|5x|<1$ and $|x|<1$.",
          r"(a) $\left(1+\tfrac52x-\tfrac{25}{8}x^2\right)\left(1+\tfrac12x+\tfrac38x^2\right)\approx1+3x-\tfrac32x^2$",
          r"(b) The expansion is only valid for $|x|<\tfrac15$, and $\tfrac12$ is outside that range.",
          r"(c) $\sqrt{\dfrac{14/9}{8/9}}=\dfrac{\sqrt7}{2}\approx1+\tfrac13-\tfrac{1}{54}=\dfrac{71}{54}$",
          r"Answer: $\sqrt7\approx\dfrac{71}{27}$"],
         [r"Write it as $(1+5x)^{\frac12}(1-x)^{-\frac12}$ and expand both brackets",
          r"Expand $(1+5x)^{\frac12}$, then divide by $(1-x)$",
          r"Use partial fractions first",
          r"Square both sides and compare coefficients"]),
    card(1, 12,
         [r"The value £$V$ of a vintage car $t$ years after 1st January 2001 is modelled by $V=Ap^t$.",
          r"It was worth £20 000 on 1st January 2003 and £45 000 on 1st January 2013.",
          r"(a) Find $p$ to 4 decimal places, and show that $A\approx17\,000$.",
          r"(b) Interpret $A$ and $p$ in context.",
          r"(c) Find the year in which the value first exceeds £80 000."],
         [r"Spot: an exponential model with two data points means write two equations and divide to eliminate $A$.",
          r"Use: $t=2$ and $t=12$, then logs to solve for $t$.",
          r"(a) $\dfrac{Ap^{12}}{Ap^2}=\dfrac{45000}{20000}\Rightarrow p^{10}=2.25\Rightarrow p=1.0845$, then $A=\dfrac{20000}{p^2}\approx17\,000$",
          r"(b) $A$ is the value on 1st January 2001. The value is multiplied by $p$ each year, which is an increase of about 8.45% a year.",
          r"(c) $Ap^t>80\,000\Rightarrow t>\dfrac{\ln(80000/A)}{\ln p}\approx19.1$",
          r"Answer: during 2020"],
         [r"Divide $Ap^{12}=45000$ by $Ap^2=20000$ to eliminate $A$",
          r"Take logs of $45000-20000$",
          r"Substitute $t=2003$ and $t=2013$ into the model",
          r"Assume $p=1.1$ and solve for $A$"]),
    card(1, 13,
         [r"Show that $\displaystyle\int_0^6 x\sqrt{x+3}\,dx=\frac{12}{5}\left(18+\sqrt3\right)$."],
         [r"Spot: $x$ times the root of a linear expression means substitute $u=x+3$. Integration by parts also works.",
          r"Use: $x=u-3$, $dx=du$, and change the limits: $x=0\to u=3$, $x=6\to u=9$.",
          r"Method: $\displaystyle\int_3^9(u-3)u^{\frac12}\,du=\left[\tfrac25u^{\frac52}-2u^{\frac32}\right]_3^9$",
          r"$=\left(\tfrac{486}{5}-54\right)-\left(\tfrac{18\sqrt3}{5}-6\sqrt3\right)=\dfrac{216}{5}+\dfrac{12\sqrt3}{5}$",
          r"Answer: $\dfrac{12}{5}(18+\sqrt3)$"],
         [r"Substitute $u=x+3$, so $x=u-3$, and change the limits",
          r"Rewrite $x\sqrt{x+3}$ as $\sqrt{x^2+3x}$",
          r"Work out $\displaystyle\int x\,dx\times\int\sqrt{x+3}\,dx$",
          r"Use the trapezium rule"]),
    card(1, 14,
         [r"A curve $C$ has parametric equations $x=1+\sin t$, $y=2+\cos2t$, $0\le t<2\pi$.",
          r"(a) Show that all points on $C$ satisfy $y=3-2(x-1)^2$.",
          r"(b) Explain why $C$ doesn't include every point of $y=3-2(x-1)^2$, $x\in\mathbb{R}$.",
          r"(c) The line $x+y=k$ meets $C$ at two distinct points. Find the range of possible values of $k$."],
         [r"Spot: $\cos2t$ together with $\sin t$ means use $\cos2t\equiv1-2\sin^2t$ to eliminate $t$.",
          r"Use: $\sin t=x-1$, the discriminant for a tangent, and the endpoints of the curve.",
          r"(a) $y=2+1-2\sin^2t=3-2(x-1)^2$",
          r"(b) $x=1+\sin t$ only takes values $0\le x\le2$, so $C$ is just part of the parabola.",
          r"(c) $x+3-2(x-1)^2=k\Rightarrow2x^2-5x+(k-1)=0$. It's a tangent when $25-8(k-1)=0$, so $k=\dfrac{33}{8}$.",
          r"The line through the endpoint $(2,1)$ has $k=3$, so two points need $3\le k<\dfrac{33}{8}$.",
          r"Answer: $\left\{k:3\le k<\dfrac{33}{8}\right\}$"],
         [r"Use $\cos2t\equiv1-2\sin^2t$, then substitute $\sin t=x-1$",
          r"Use $\cos2t\equiv2\cos^2t-1$ and $\cos t=x-1$",
          r"Square $x$ and $y$ and add them",
          r"Differentiate both equations with respect to $t$"]),

    # ---------------- Paper 2 ----------------
    card(2, 1,
         [r"$g(x)=\dfrac{3x+2}{x-4}$, $x\ge6$",
          r"(a) Find $gg(6)$.",
          r"(b) State the range of $g$.",
          r"(c) Find $g^{-1}(x)$, stating its domain."],
         [r"Spot: for the range, look at the value at the endpoint and the asymptote. The domain of $g^{-1}$ is the range of $g$.",
          r"Use: $g$ is decreasing for $x\ge6$ because $g'(x)=-\dfrac{14}{(x-4)^2}<0$.",
          r"(a) $g(6)=10$, so $gg(6)=g(10)=\dfrac{32}{6}=\dfrac{16}{3}$",
          r"(b) $g(6)=10$ and $g(x)\to3$ as $x\to\infty$, so $3<g(x)\le10$.",
          r"(c) $y(x-4)=3x+2\Rightarrow x=\dfrac{4y+2}{y-3}$, so $g^{-1}(x)=\dfrac{4x+2}{x-3}$ for $3<x\le10$."],
         [r"Work from the inside out: find $g(6)$, then apply $g$ to the result",
          r"Square $g(6)$",
          r"Find $g(6)$ and $g(12)$, then add",
          r"Substitute $x=6$ into $g^{-1}(x)$"]),
    card(2, 2,
         [r"Relative to $O$, $A$ has position vector $\mathbf{i}-2\mathbf{j}+3\mathbf{k}$, $B$ has $3\mathbf{i}+\mathbf{j}-\mathbf{k}$ and $C$ has $a\mathbf{i}+2\mathbf{j}+5\mathbf{k}$, where $a<0$.",
          r"$D$ is the point such that $\overrightarrow{AB}=\overrightarrow{BD}$.",
          r"(a) Find the position vector of $D$.",
          r"(b) Given that $|\overrightarrow{AC}|=6$, find $a$."],
         [r"Spot: $\overrightarrow{AB}=\overrightarrow{BD}$ means $B$ is the midpoint of $AD$.",
          r"Use: $\overrightarrow{OD}=\overrightarrow{OB}+\overrightarrow{AB}$ and $|\mathbf{v}|=\sqrt{x^2+y^2+z^2}$.",
          r"(a) $\overrightarrow{AB}=2\mathbf{i}+3\mathbf{j}-4\mathbf{k}$, so $\overrightarrow{OD}=5\mathbf{i}+4\mathbf{j}-5\mathbf{k}$",
          r"(b) $\overrightarrow{AC}=(a-1)\mathbf{i}+4\mathbf{j}+2\mathbf{k}$, so $(a-1)^2+16+4=36\Rightarrow(a-1)^2=16$",
          r"Answer: $a=-3$, because $a<0$"],
         [r"Use $\overrightarrow{OD}=\overrightarrow{OB}+\overrightarrow{AB}$",
          r"Use $\overrightarrow{OD}=\overrightarrow{OA}+\overrightarrow{OB}$",
          r"Use $\overrightarrow{OD}=\overrightarrow{AB}-\overrightarrow{OB}$",
          r"Find the midpoint of $AB$"]),
    card(2, 3,
         [r"(a) “If $p$ and $q$ are irrational numbers, with $p\ne q$, then $\dfrac{p}{q}$ is also irrational.” Disprove this statement with a counter-example.",
          r"(b)(i) Sketch the graph of $y=|x|-2$.",
          r"(ii) Explain why $|x|-2\le|x-2|$ for all real values of $x$."],
         [r"Spot: “disprove” means one counter-example is enough. Choose irrational numbers that cancel.",
          r"Use: surds with the same root, such as $2\sqrt3$ and $\sqrt3$.",
          r"(a) $p=2\sqrt3$ and $q=\sqrt3$ are irrational and different, but $\dfrac{p}{q}=2$ is rational.",
          r"(b)(i) A V shape with vertex $(0,-2)$, crossing the $x$-axis at $\pm2$.",
          r"(ii) For $x\ge2$, both sides equal $x-2$. For $x<2$, $|x-2|=2-x$, and $|x|-2$ is always smaller than that."],
         [r"Find one pair of irrational numbers whose quotient is rational",
          r"Show it works for $p=\sqrt2$ and $q=\sqrt3$",
          r"Prove it by contradiction",
          r"Check every pair of irrational numbers (proof by exhaustion)"]),
    card(2, 4,
         [r"(i) Show that $\displaystyle\sum_{r=1}^{12}\left(4+3r+3^r\right)=797\,442$.",
          r"(ii) A sequence is defined by $u_{n+1}=\dfrac{2}{u_n}$, $u_1=\dfrac43$. Find the exact value of $\displaystyle\sum_{r=1}^{80}u_r$."],
         [r"Spot: a sum of different kinds of term means split it into a constant part, an arithmetic part and a geometric part. A rule like $\dfrac{2}{u_n}$ makes the sequence repeat with period 2.",
          r"Use: $\displaystyle\sum_{r=1}^{n}r=\frac{n(n+1)}{2}$ and $S_n=\dfrac{a(r^n-1)}{r-1}$ (booklet).",
          r"(i) $48+3\cdot78+\dfrac{3(3^{12}-1)}{2}=48+234+797\,160=797\,442$",
          r"(ii) $u_1=\tfrac43$, $u_2=\tfrac32$, $u_3=\tfrac43$, …. There are 40 pairs, each adding to $\tfrac43+\tfrac32=\tfrac{17}{6}$.",
          r"Answer: $40\times\dfrac{17}{6}=\dfrac{340}{3}$"],
         [r"Split it into $\sum4+3\sum r+\sum3^r$ and use the AP and GP formulas",
          r"Use the AP sum formula for the whole expression",
          r"Work out all 12 terms by hand",
          r"Use the binomial expansion of $(4+3r)^{12}$"]),
    card(2, 5,
         [r"The equation $3x^3-x^2-4=0$ has exactly one real root.",
          r"(a) Show that the Newton–Raphson formula can be written $x_{n+1}=\dfrac{6x_n^3-x_n^2+4}{9x_n^2-2x_n}$.",
          r"(b) Using $x_1=1$, find $x_2$ and $x_3$.",
          r"(c) Explain why the method can't be used with $x_1=0$."],
         [r"Spot: Newton–Raphson (formula in the booklet): $x_{n+1}=x_n-\dfrac{f(x_n)}{f'(x_n)}$.",
          r"Use: $f(x)=3x^3-x^2-4$ and $f'(x)=9x^2-2x$, then combine into a single fraction.",
          r"(a) $x_n-\dfrac{3x_n^3-x_n^2-4}{9x_n^2-2x_n}=\dfrac{9x_n^3-2x_n^2-3x_n^3+x_n^2+4}{9x_n^2-2x_n}$, which simplifies to the formula.",
          r"(b) $x_2=\dfrac97\approx1.286$ and $x_3\approx1.227$",
          r"(c) $f'(0)=0$: the tangent at $x=0$ is horizontal, so the formula would divide by zero."],
         [r"Use $x_{n+1}=x_n-\dfrac{f(x_n)}{f'(x_n)}$ with $f'(x)=9x^2-2x$",
          r"Rearrange $3x^3-x^2-4=0$ into the form $x=g(x)$",
          r"Use $x_{n+1}=x_n-\dfrac{f'(x_n)}{f(x_n)}$",
          r"Use interval bisection between 1 and 2"]),
    card(2, 6,
         [r"$f(x)=-2x^3+7x^2-7x+12$, $x\in\mathbb{R}$",
          r"(a)(i) Calculate $f(3)$. (ii) Write $f(x)$ as a product of two algebraic factors.",
          r"(b) Prove that $-2y^6+7y^4-7y^2+12=0$ has exactly two real solutions.",
          r"(c) Deduce the number of real solutions, for $4\pi\le\theta<8\pi$, of $2\tan^3\theta-7\tan^2\theta+7\tan\theta-12=0$."],
         [r"Spot: $f(3)=0$ means $(x-3)$ is a factor (factor theorem). The later parts are $f$ with $x$ replaced by $y^2$ or by $\tan\theta$.",
          r"Use: algebraic division, and the discriminant $b^2-4ac<0$ to show that the quadratic has no real roots.",
          r"(a) $f(3)=0$ and $f(x)=(x-3)(-2x^2+x-4)$",
          r"(b) With $x=y^2$: $(y^2-3)(-2y^4+y^2-4)=0$. The quadratic in $y^2$ has $1-32<0$, so the only solutions are $y=\pm\sqrt3$.",
          r"(c) The equation is $-f(\tan\theta)=0$, so $\tan\theta=3$, with one solution in each period of length $\pi$.",
          r"Answer: 4 solutions"],
         [r"Use the factor theorem, then divide to find the quadratic factor",
          r"Use the quadratic formula on $f(x)$",
          r"Differentiate $f$ to find its turning points",
          r"Substitute $x=\tan\theta$ straight away"]),
    card(2, 7,
         [r"(i) Solve, for $0\le x<\pi$, $4\sin x=\sqrt3\sec x$.",
          r"(ii) Solve, for $0\le\theta<360^\circ$, $3\sin\theta+4\cos\theta=2$, giving your answers to 1 decimal place."],
         [r"Spot: (i) $\sec x=\dfrac{1}{\cos x}$, and $\sin x\cos x$ points to $\sin2x$. (ii) $a\sin\theta+b\cos\theta$ means use the R-form.",
          r"Use: $2\sin x\cos x\equiv\sin2x$ and $3\sin\theta+4\cos\theta\equiv5\sin(\theta+53.13^\circ)$.",
          r"(i) $4\sin x\cos x=\sqrt3\Rightarrow\sin2x=\dfrac{\sqrt3}{2}$ with $0\le2x<2\pi$, so $2x=\dfrac{\pi}{3},\dfrac{2\pi}{3}$.",
          r"Answer: $x=\dfrac{\pi}{6},\ \dfrac{\pi}{3}$",
          r"(ii) $\sin(\theta+53.13^\circ)=0.4$ with $53.13^\circ\le\theta+53.13^\circ<413.13^\circ$",
          r"Answer: $\theta=103.3^\circ,\ 330.4^\circ$"],
         [r"Multiply by $\cos x$ to get $4\sin x\cos x=\sqrt3$, then use $\sin2x$",
          r"Square both sides",
          r"Divide both sides by $\sin x$",
          r"Replace $\sec x$ with $\dfrac{1}{\sin x}$"],
         ask="How do you start part (i)?"),
    card(2, 8,
         [r"A rugby ball's height $H$ m is modelled as a quadratic function of its horizontal distance $x$ m from where it was kicked.",
          r"It reaches a maximum height of 15 m and lands 50 m from where it was kicked.",
          r"(a) Find an equation linking $H$ and $x$.",
          r"(b) The ball passes over a bar 3 m above the ground. Find the greatest possible horizontal distance of the bar from the kick.",
          r"(c) Give one limitation of the model."],
         [r"Spot: you know the roots and the maximum, so use $H=kx(50-x)$. The maximum is halfway between the roots, at $x=25$.",
          r"Use: roots at $x=0$ and $x=50$, and $H(25)=15$.",
          r"(a) $k\cdot25\cdot25=15\Rightarrow k=0.024$, so $H=0.024x(50-x)$",
          r"(b) $0.024x(50-x)=3\Rightarrow x^2-50x+125=0\Rightarrow x=25\pm10\sqrt5$",
          r"Answer: $25+10\sqrt5\approx47.4$ m",
          r"(c) For example: it ignores air resistance and spin, and treats the ball as a particle."],
         [r"Use the roots: $H=kx(50-x)$, then $H(25)=15$ gives $k$",
          r"Use $H=15-x^2$",
          r"Use $H=kx^2+15$",
          r"Use $H=k(x-15)^2+50$"]),
    card(2, 9,
         [r"Given that $\theta$ is in radians, prove from first principles that $\dfrac{d}{d\theta}(\sin\theta)=\cos\theta$.",
          r"You may assume the formula for $\sin(A\pm B)$, and that as $h\to0$, $\dfrac{\sin h}{h}\to1$ and $\dfrac{\cos h-1}{h}\to0$."],
         [r"Spot: “from first principles” means start from $f'(x)=\displaystyle\lim_{h\to0}\frac{f(x+h)-f(x)}{h}$.",
          r"Use: $\sin(\theta+h)\equiv\sin\theta\cos h+\cos\theta\sin h$.",
          r"Method: $\dfrac{\sin\theta\cos h+\cos\theta\sin h-\sin\theta}{h}=\sin\theta\cdot\dfrac{\cos h-1}{h}+\cos\theta\cdot\dfrac{\sin h}{h}$",
          r"As $h\to0$, this tends to $\sin\theta\cdot0+\cos\theta\cdot1=\cos\theta$."],
         [r"Write $\dfrac{\sin(\theta+h)-\sin\theta}{h}$ and expand $\sin(\theta+h)$",
          r"Use the chain rule on $\sin\theta$",
          r"Use the small angle approximation $\sin\theta\approx\theta$",
          r"Integrate $\cos\theta$"]),
    card(2, 10,
         [r"A spherical sweet of radius 6 mm dissolves in the mouth. After 5 minutes its radius is 4 mm.",
          r"In a simple model, the rate of decrease of the radius is inversely proportional to the square of the radius.",
          r"(a) Find an equation linking the radius $r$ mm and the time $t$ minutes.",
          r"(b) Find the total time for the sweet to dissolve completely, to the nearest second.",
          r"(c) Suggest a limitation of the model."],
         [r"Spot: “rate of decrease … inversely proportional to $r^2$” gives $\dfrac{dr}{dt}=-\dfrac{k}{r^2}$. Separate the variables.",
          r"Use: $\displaystyle\int r^2\,dr=\int-k\,dt$, then use both conditions to find $k$ and $c$.",
          r"(a) $\dfrac{r^3}{3}=-kt+c$. At $t=0$, $r=6$, so $c=72$. At $t=5$, $r=4$, so $k=\dfrac{152}{15}$, giving $r^3=216-\dfrac{152}{5}t$.",
          r"(b) $r=0$ when $t=\dfrac{1080}{152}\approx7.105$ min",
          r"Answer: 7 minutes 6 seconds",
          r"(c) For example: a real sweet won't stay a perfect sphere as it dissolves."],
         [r"Write $\dfrac{dr}{dt}=-\dfrac{k}{r^2}$, then separate the variables",
          r"Write $r=6-kt^2$",
          r"Write $\dfrac{dr}{dt}=-kr^2$",
          r"Differentiate $V=\tfrac43\pi r^3$ and stop there"]),
    card(2, 11,
         [r"$\dfrac{1+3x-4x^2}{(x-2)(1-2x)}\equiv A+\dfrac{B}{x-2}+\dfrac{C}{1-2x}$",
          r"(a) Find the values of the constants $A$, $B$ and $C$.",
          r"(b) $f(x)=\dfrac{1+3x-4x^2}{(x-2)(1-2x)}$, $x>2$. Prove that $f(x)$ is a decreasing function."],
         [r"Spot: the top and bottom have the same degree, so there's a constant term $A$ (the fraction is improper).",
          r"Use: compare the $x^2$ coefficients to find $A$, then substitute $x=2$ and $x=\tfrac12$ to find $B$ and $C$.",
          r"(a) $A=\dfrac{-4}{-2}=2$. Then $x=2$ gives $-9=-3B$, so $B=3$, and $x=\tfrac12$ gives $1.5=-1.5C$, so $C=-1$.",
          r"(b) $f'(x)=-\dfrac{3}{(x-2)^2}-\dfrac{2}{(1-2x)^2}$",
          r"Both terms are negative, so $f'(x)<0$ for all $x>2$, which means $f$ is decreasing."],
         [r"Find $A$ from the $x^2$ coefficients, then substitute $x=2$ and $x=\tfrac12$",
          r"Write it as just $\dfrac{B}{x-2}+\dfrac{C}{1-2x}$",
          r"Use the binomial expansion",
          r"Multiply out the denominator and differentiate"]),
    card(2, 12,
         [r"(a) Prove that $1+\cos2\theta\equiv\cot\theta\sin2\theta$, $\theta\ne n\pi$.",
          r"(b) Hence solve, for $0<x<\pi$, $(\cosec^2x+1)(1+\cos2x)=3\cot^2x\sin2x$.",
          r"Give any non-exact answers to 3 decimal places."],
         [r"Spot: “hence” means use (a) to replace $1+\cos2x$ with $\cot x\sin2x$, then factorise instead of dividing.",
          r"Use: $\cos2\theta\equiv2\cos^2\theta-1$, $\sin2\theta\equiv2\sin\theta\cos\theta$, $\cosec^2x\equiv1+\cot^2x$.",
          r"(a) RHS $=\dfrac{\cos\theta}{\sin\theta}\cdot2\sin\theta\cos\theta=2\cos^2\theta=1+\cos2\theta$",
          r"(b) $\cot x\sin2x\left(\cosec^2x+1-3\cot x\right)=0$",
          r"$\cot x\sin2x=2\cos^2x=0$ gives $x=\dfrac{\pi}{2}$. Otherwise $\cot^2x-3\cot x+2=0$, so $\cot x=1$ or $2$.",
          r"Answer: $x=0.464,\ \dfrac{\pi}{4},\ \dfrac{\pi}{2}$"],
         [r"Replace $1+\cos2x$ using part (a), then factorise",
          r"Divide both sides by $\sin2x$",
          r"Rewrite everything in terms of $\sin x$ only",
          r"Use the R-form"],
         ask="How do you start part (b)?"),
    card(2, 13,
         [r"The curve $C$ has equation $y=2x\ln x$, $x>0$. The line $l$ is the normal to $C$ at the point $P(e,2e)$.",
          r"The region $R$ is bounded by $C$, $l$ and the $x$-axis.",
          r"Show that the exact area of $R$ is $Ae^2+B$, where $A$ and $B$ are rational numbers to be found."],
         [r"Spot: a region bounded by a curve and a straight line means split it at $P$, into the area under the curve plus a triangle.",
          r"Use: $\dfrac{dy}{dx}=2\ln x+2$, and integration by parts with $u=\ln x$.",
          r"The normal at $P$ has gradient $-\dfrac14$ and meets the $x$-axis at $x=9e$. The triangle's area is $\dfrac12(8e)(2e)=8e^2$.",
          r"$C$ crosses the $x$-axis at $x=1$, and $\displaystyle\int_1^e2x\ln x\,dx=\left[x^2\ln x-\frac{x^2}{2}\right]_1^e=\frac{e^2}{2}+\frac12$.",
          r"Answer: $\dfrac{17}{2}e^2+\dfrac12$, so $A=\dfrac{17}{2}$ and $B=\dfrac12$"],
         [r"Split $R$ at $x=e$: integrate the curve from 1 to $e$, then add the triangle under the normal",
          r"Integrate $2x\ln x$ from 0 to $9e$",
          r"Integrate the curve minus the normal from 1 to $9e$",
          r"Use the trapezium rule"]),
    card(2, 14,
         [r"The number of mice $N$, $t$ months after a study starts, is modelled by $N=\dfrac{800}{4+6e^{-0.2t}}$.",
          r"(a) Find the number of mice at the start of the study.",
          r"(b) Show that $\dfrac{dN}{dt}=\dfrac{N(200-N)}{1000}$.",
          r"(c) The rate of growth is greatest after $T$ months. Find $T$.",
          r"(d) State the maximum population $P$ that the model predicts."],
         [r"Spot: this is a logistic model. The growth rate is a quadratic in $N$, so it's greatest halfway, at $N=100$.",
          r"Use: the chain rule on $800(4+6e^{-0.2t})^{-1}$, and $e^{-0.2t}=\dfrac{800-4N}{6N}$ to rewrite it in terms of $N$.",
          r"(a) $N(0)=\dfrac{800}{10}=80$",
          r"(b) $\dfrac{dN}{dt}=\dfrac{960e^{-0.2t}}{(4+6e^{-0.2t})^2}$. Substitute for $e^{-0.2t}$ and simplify.",
          r"(c) $N=100\Rightarrow4+6e^{-0.2T}=8\Rightarrow T=5\ln1.5\approx2.03$ months",
          r"(d) As $t\to\infty$, $e^{-0.2t}\to0$, so $P=\dfrac{800}{4}=200$."],
         [r"Differentiate with the chain rule, then replace $e^{-0.2t}$ with an expression in $N$",
          r"Use the quotient rule and leave the answer in terms of $t$",
          r"Separate the variables in $\dfrac{dN}{dt}$",
          r"Take logs of both sides first"],
         ask="How do you start part (b)?"),
]


def check():
    # P1 Q1
    assert sp.limit((1 - sp.cos(6 * theta)) / (3 * theta * sp.sin(2 * theta)), theta, 0) == 3
    # P1 Q2
    Y = x**2 - 12 * x - 36 * sp.sqrt(x)
    d1, d2 = sp.diff(Y, x), sp.diff(Y, x, 2)
    assert same(d1, 2 * x - 12 - 18 * x**sp.Rational(-1, 2)) and same(d2, 2 + 9 * x**sp.Rational(-3, 2))
    assert d1.subs(x, 9) == 0 and d2.subs(x, 9) == sp.Rational(7, 3)
    # P1 Q3
    th, R = sp.symbols("th R", positive=True)
    sol = sp.solve([2 * R + R * th - 5 * R * th, R**2 * th / 2 - 12], [R, th], dict=True)
    assert any(same(s[R], 4 * sp.sqrt(3)) for s in sol)
    # P1 Q4
    f = lambda v: 3 * math.log(10 - v) - v
    assert f(4) > 0 > f(5) and close(f(4), 1.375278, 1e-5) and close(f(5), -0.171687, 1e-4)
    alpha = sp.nsolve(3 * sp.log(10 - x) - x, x, 4.9)
    assert close(alpha, 4.89, 2e-3)
    assert close(3 / (10 - alpha), 0.59, 0.02)
    x2 = 3 * math.log(5); x3 = 3 * math.log(10 - x2)
    assert round(x2, 3) == 4.828 and round(x3, 3) == 4.930
    # P1 Q5
    Yt = 5 * sp.sin(theta) / (3 * sp.sin(theta) + 3 * sp.cos(theta))
    assert identity(sp.diff(Yt, theta) * (1 + sp.sin(2 * theta)) - sp.Rational(5, 3), theta)
    # P1 Q6
    P = sp.solve([2 * y + x - 14, y - 2 * x + 3], [x, y])
    assert P == {x: 4, y: 5}
    assert (8 - 4)**2 + (3 - 5)**2 == 20
    # tangent y = 2x + c to circle: distance from centre = sqrt(20)
    c = sp.symbols("c")
    cs = sp.solve(sp.Eq((2 * 8 - 3 + c)**2 / 5, 20), c)
    assert sorted(cs) == [-23, -3]
    # P1 Q7
    kp = sp.symbols("kp", positive=True)
    assert same(sp.integrate(1 / (2 * x - kp), (x, kp, 4 * kp)), sp.log(7) / 2)
    assert same(sp.integrate(4 / (2 * x - kp)**2, (x, kp, 2 * kp)), sp.Rational(4, 3) / kp)
    # P1 Q8
    D = lambda tt: 6 + 2.5 * math.sin(math.radians(30 * tt))
    assert round(D(6.75), 2) == 5.04 and round(D(8.75), 2) == 3.52
    tl = (360 - math.degrees(math.asin(0.4))) / 30
    assert round(tl, 2) == 11.21 and (int(tl), round((tl % 1) * 60)) == (11, 13)
    assert round(180 + math.degrees(math.asin(0.4)), 1) == 203.6 and round(360 - math.degrees(math.asin(0.4)), 1) == 336.4
    # P1 Q9
    Fc = x**2 - 2 * x * y + 4 * y**2 - 48
    dydx = -sp.diff(Fc, x) / sp.diff(Fc, y)
    assert same(dydx, (y - x) / (4 * y - x))
    pts = sp.solve([4 * y - x, Fc], [x, y])
    assert (-8, -2) in pts
    # P1 Q10
    H = 4 * sp.exp(sp.Rational(1, 10) * sp.sin(t / 2))
    assert same(sp.diff(H, t) - H * sp.cos(t / 2) / 20, 0) and H.subs(t, 0) == 4
    assert round(4 * math.exp(0.1), 2) == 4.42 and round(5 * math.pi, 1) == 15.7
    # P1 Q11
    ser = sp.series(sp.sqrt((1 + 5 * x) / (1 - x)), x, 0, 3).removeO()
    assert same(ser, 1 + 3 * x - sp.Rational(3, 2) * x**2)
    assert ((1 + sp.Rational(5, 9)) / (1 - sp.Rational(1, 9))) == sp.Rational(7, 4)
    assert ser.subs(x, sp.Rational(1, 9)) == sp.Rational(71, 54)
    # P1 Q12
    p = 2.25 ** 0.1
    A = 20000 / p**2
    assert round(p, 4) == 1.0845 and abs(A - 17000) < 50
    tt = math.log(80000 / A) / math.log(p)
    assert round(tt, 1) == 19.1 and 2001 + int(tt) == 2020
    # P1 Q13
    assert same(sp.integrate(x * sp.sqrt(x + 3), (x, 0, 6)), sp.Rational(12, 5) * (18 + sp.sqrt(3)))
    # P1 Q14
    tp = sp.symbols("tp")
    assert same((2 + sp.cos(2 * tp)) - (3 - 2 * (sp.sin(tp))**2), 0)
    assert sp.solve(sp.Eq(25 - 8 * (k - 1), 0), k) == [sp.Rational(33, 8)]
    for kk in [3, 3.5, 4.1]:
        rts = [float(v) for v in sp.solve(2 * x**2 - 5 * x + (kk - 1), x)]
        assert sum(0 <= v <= 2 for v in rts) == 2, kk
    for kk in [2.9, 4.2]:
        rts = [complex(v) for v in sp.solve(2 * x**2 - 5 * x + (kk - 1), x)]
        assert sum(abs(v.imag) < 1e-12 and 0 <= v.real <= 2 for v in rts) < 2, kk

    # P2 Q1
    g = lambda v: (3 * v + 2) / (v - 4)
    assert g(sp.Integer(6)) == 10 and g(sp.Integer(10)) == sp.Rational(16, 3)
    gi = (4 * x + 2) / (x - 3)
    assert same(gi.subs(x, (3 * y + 2) / (y - 4)), y)
    assert same(sp.diff((3 * x + 2) / (x - 4), x), -14 / (x - 4)**2)
    # P2 Q2
    Av, Bv = sp.Matrix([1, -2, 3]), sp.Matrix([3, 1, -1])
    assert 2 * Bv - Av == sp.Matrix([5, 4, -5])
    a = sp.symbols("a")
    assert sorted(sp.solve((a - 1)**2 + 4**2 + 2**2 - 36, a)) == [-3, 5]
    # P2 Q3
    assert (2 * sp.sqrt(3)) / sp.sqrt(3) == 2
    for v in [-5, -1, 0, 1, 1.9, 2, 3, 10]:
        assert abs(v) - 2 <= abs(v - 2)
        assert (abs(v) - 2 == abs(v - 2)) == (v >= 2)
    # P2 Q4
    assert sum(4 + 3 * i + 3**i for i in range(1, 13)) == 797442
    us = [sp.Rational(4, 3)]
    for _ in range(79):
        us.append(2 / us[-1])
    assert sum(us) == sp.Rational(340, 3)
    # P2 Q5
    F = 3 * x**3 - x**2 - 4
    nr = sp.simplify(x - F / sp.diff(F, x))
    assert same(nr, (6 * x**3 - x**2 + 4) / (9 * x**2 - 2 * x))
    x2v = nr.subs(x, 1); x3v = nr.subs(x, x2v)
    assert x2v == sp.Rational(9, 7) and round(float(x3v), 3) == 1.227
    assert sp.diff(F, x).subs(x, 0) == 0
    # P2 Q6
    f6 = -2 * x**3 + 7 * x**2 - 7 * x + 12
    assert f6.subs(x, 3) == 0 and same(f6, (x - 3) * (-2 * x**2 + x - 4))
    assert 1 - 4 * (-2) * (-4) < 0
    real_y = [v for v in sp.solve(-2 * y**6 + 7 * y**4 - 7 * y**2 + 12, y) if v.is_real]
    assert sorted(real_y, key=float) == [-sp.sqrt(3), sp.sqrt(3)]
    sols = [math.atan(3) + m * math.pi for m in range(0, 12)]
    assert sum(4 * math.pi <= s < 8 * math.pi for s in sols) == 4
    # P2 Q7
    xs = [s for s in sp.solveset(sp.Eq(4 * sp.sin(x), sp.sqrt(3) / sp.cos(x)), x, sp.Interval.Ropen(0, sp.pi))]
    assert sorted(xs, key=float) == [sp.pi / 6, sp.pi / 3]
    al = math.degrees(math.atan2(4, 3)); s0 = math.degrees(math.asin(0.4))
    th1, th2 = 180 - s0 - al, 360 + s0 - al
    assert round(th1, 1) == 103.3 and round(th2, 1) == 330.4
    for v in (th1, th2):
        assert close(3 * math.sin(math.radians(v)) + 4 * math.cos(math.radians(v)), 2)
    # P2 Q8
    Hq = sp.Rational(24, 1000) * x * (50 - x)
    assert Hq.subs(x, 25) == 15 and Hq.subs(x, 50) == 0
    assert sorted(sp.solve(Hq - 3, x), key=float)[-1] == 25 + 10 * sp.sqrt(5) and round(25 + 10 * math.sqrt(5), 1) == 47.4
    # P2 Q10
    kk = sp.Rational(152, 15)
    rr = (216 - 3 * kk * t)**sp.Rational(1, 3)
    assert rr.subs(t, 0) == 6 and same(rr.subs(t, 5), 4)
    tz = 1080 / 152
    assert int(tz) == 7 and round((tz - 7) * 60) == 6
    # P2 Q11
    lhs = (1 + 3 * x - 4 * x**2) / ((x - 2) * (1 - 2 * x))
    assert same(lhs, 2 + 3 / (x - 2) - 1 / (1 - 2 * x))
    assert same(sp.diff(lhs, x), -3 / (x - 2)**2 - 2 / (1 - 2 * x)**2)
    # P2 Q12
    assert identity(1 + sp.cos(2 * theta) - sp.cot(theta) * sp.sin(2 * theta), theta)
    eq = (1 / sp.sin(x)**2 + 1) * (1 + sp.cos(2 * x)) - 3 * sp.cot(x)**2 * sp.sin(2 * x)
    factored = sp.cot(x) * sp.sin(2 * x) * (sp.cot(x)**2 - 3 * sp.cot(x) + 2)
    assert identity(eq - factored, x, 0.1, 3.0)
    # cot x sin 2x = 2cos^2 x vanishes only at pi/2 in (0, pi); cot x = 1 or 2 give the others
    assert identity(sp.cot(x) * sp.sin(2 * x) - 2 * sp.cos(x)**2, x, 0.1, 3.0)
    assert sorted(sp.solve(sp.Symbol("c")**2 - 3 * sp.Symbol("c") + 2)) == [1, 2]
    for root in (math.atan(0.5), math.pi / 4, math.pi / 2):
        assert abs(sp.lambdify(x, eq)(root)) < 1e-9
    assert round(math.atan(0.5), 3) == 0.464
    # P2 Q13
    Yc = 2 * x * sp.log(x)
    assert sp.diff(Yc, x).subs(x, sp.E) == 4
    xa = sp.solve(sp.Eq(0, 2 * sp.E - sp.Rational(1, 4) * (x - sp.E)), x)[0]
    assert same(xa, 9 * sp.E)
    area = sp.integrate(Yc, (x, 1, sp.E)) + sp.Rational(1, 2) * (xa - sp.E) * 2 * sp.E
    assert same(area, sp.Rational(17, 2) * sp.E**2 + sp.Rational(1, 2))
    # P2 Q14
    N = 800 / (4 + 6 * sp.exp(-sp.Rational(1, 5) * t))
    assert N.subs(t, 0) == 80
    assert same(sp.diff(N, t) - N * (200 - N) / 1000, 0)
    T = sp.solve(sp.Eq(N, 100), t)[0]
    assert same(T, 5 * sp.log(sp.Rational(3, 2))) and round(float(T), 2) == 2.03
    assert sp.limit(N, t, sp.oo) == 200
