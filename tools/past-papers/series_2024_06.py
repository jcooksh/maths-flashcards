"""June 2024 (9MA0/01 and 9MA0/02), with the numbers changed."""
import math
import sympy as sp
from common import card, close, same, identity, x, y, t, k, theta

SERIES = {"id": "paper-2024-06", "title": "June 2024", "hue": 240}

CARDS = [
    # ---------------- Paper 1 ----------------
    card(1, 1,
         [r"$g(x)=2x^3-9x^2+(k-5)x+2k$, where $k$ is a constant.",
          r"Given that $(x-4)$ is a factor of $g(x)$, find the value of $k$."],
         [r"Spot: “$(x-4)$ is a factor” means $g(4)=0$, which gives a linear equation in $k$.",
          r"Use: the factor theorem.",
          r"Method: $2(64)-9(16)+4(k-5)+2k=0\Rightarrow128-144+4k-20+2k=0\Rightarrow6k-36=0$",
          r"Answer: $k=6$"],
         [r"Substitute $x=4$ and set $g(4)=0$",
          r"Substitute $x=-4$ and set $g(-4)=0$",
          r"Set $g(0)=4$",
          r"Divide $g(x)$ by $(x+4)$"]),
    card(1, 2,
         [r"(a) Find, in ascending powers of $x$, the first four terms of the binomial expansion of $\sqrt{1+8x}$, giving each term in its simplest form.",
          r"(b) Give a reason why $x=\tfrac14$ should not be used in this expansion to approximate $\sqrt3$."],
         [r"Spot: $\sqrt{1+8x}=(1+8x)^{\frac12}$, which is $(1+x)^n$ from the formula booklet with $x$ replaced by $8x$. Each power of $x$ gets the matching power of 8.",
          r"Use: $(1+x)^n=1+nx+\dfrac{n(n-1)}{2!}x^2+\dfrac{n(n-1)(n-2)}{3!}x^3+\dots$, valid for $|x|<1$.",
          r"(a) $1+4x-8x^2+32x^3$",
          r"(b) The expansion is only valid for $|8x|<1$, so $|x|<\tfrac18$, and $\tfrac14$ is outside that range."],
         [r"Use $(1+x)^n$ with $n=\frac12$ and $x$ replaced by $8x$",
          r"Use $(1+x)^n$ with $n=2$",
          r"Replace $x$ by $8x$ in the first two terms only",
          r"Use $(1+x)^n$ with $n=-\frac12$"],
         ask="How do you start part (a)?"),
    card(1, 3,
         [r"$f(x)=2x+\tan\left(\dfrac x2\right)$, $\pi<x<\dfrac{3\pi}{2}$. The equation $f(x)=0$ has a single root $\alpha$.",
          r"(a) Show that $\alpha$ lies in the interval $[3.4,3.5]$.",
          r"(b) Find $f'(x)$.",
          r"(c) Using 3.5 as a first approximation for $\alpha$, apply the Newton–Raphson method once to find a second approximation, to 3 d.p."],
         [r"Spot: “show the root is in an interval” means a sign change on a continuous function. Newton–Raphson needs $f'(x)$, and $\tan\left(\dfrac x2\right)$ needs the chain rule.",
          r"Use: $\dfrac{d}{dx}\tan(kx)=k\sec^2(kx)$, and $x_1=x_0-\dfrac{f(x_0)}{f'(x_0)}$ in radians.",
          r"(a) $f(3.4)\approx-0.897<0$ and $f(3.5)\approx1.480>0$. $f$ is continuous on the interval, so there's a root.",
          r"(b) $f'(x)=2+\tfrac12\sec^2\left(\dfrac x2\right)$",
          r"(c) $x_1=3.5-\dfrac{1.480}{17.737}\approx3.417$"],
         [r"Use $x_1=3.5-\frac{f(3.5)}{f'(3.5)}$ with $f'(x)=2+\frac12\sec^2\frac x2$",
          r"Use $f'(x)=2+\sec^2\frac x2$",
          r"Use $x_1=3.5+\frac{f(3.5)}{f'(3.5)}$",
          r"Work in degrees"],
         ask="How do you start part (c)?"),
    card(1, 4,
         [r"Given that $y=x^3$, use differentiation from first principles to show that $\dfrac{dy}{dx}=3x^2$."],
         [r"Spot: “first principles” means start from $\displaystyle\lim_{h\to0}\frac{f(x+h)-f(x)}{h}$.",
          r"Use: $(x+h)^3=x^3+3x^2h+3xh^2+h^3$.",
          r"Method: $\dfrac{(x+h)^3-x^3}{h}=\dfrac{3x^2h+3xh^2+h^3}{h}=3x^2+3xh+h^2$",
          r"As $h\to0$, this tends to $3x^2$."],
         [r"Write $\frac{(x+h)^3-x^3}{h}$, expand, simplify, then let $h\to0$",
          r"Use the power rule",
          r"Substitute $h=0$ first",
          r"Use $(x+h)^3=x^3+h^3$"]),
    card(1, 5,
         [r"$f(x)=\dfrac{3x+2}{x^2+5}$.",
          r"(a) Show that $f'(x)=\dfrac{ax^2+bx+c}{(x^2+5)^2}$, where $a$, $b$ and $c$ are constants to be found.",
          r"(b) Hence, using algebra, find the values of $x$ for which $f$ is decreasing."],
         [r"Spot: a fraction of two functions means the quotient rule. “Decreasing” means $f'(x)<0$, and the denominator is always positive.",
          r"Use: $\dfrac{d}{dx}\left(\dfrac uv\right)=\dfrac{vu'-uv'}{v^2}$.",
          r"(a) $\dfrac{3(x^2+5)-2x(3x+2)}{(x^2+5)^2}=\dfrac{-3x^2-4x+15}{(x^2+5)^2}$, so $a=-3$, $b=-4$, $c=15$",
          r"(b) $-3x^2-4x+15<0\Rightarrow(3x-5)(x+3)>0$",
          r"Answer: $x<-3$ or $x>\tfrac53$"],
         [r"Solve $-3x^2-4x+15<0$, because the denominator is always positive",
          r"Solve $f(x)<0$",
          r"Solve $-3x^2-4x+15>0$",
          r"Solve $3x+2<0$"],
         ask="How do you start part (b)?"),
    card(1, 6,
         [r"The graph of $y=2|x-3|+4$ has its vertex at $P$.",
          r"(a) Find the coordinates of $P$.",
          r"(b) Solve $19-3x=2|x-3|+4$.",
          r"The line $y=kx+1$, where $k$ is a constant, meets $y=2|x-3|+4$ at two distinct points.",
          r"(c) Find the range of values of $k$."],
         [r"Spot: a modulus graph is a V. Sketch it with the line to see which branch the line crosses, and only solve on that branch.",
          r"Use: for $x\ge3$, $y=2x-2$. For $x<3$, $y=10-2x$.",
          r"(a) $P(3,4)$",
          r"(b) Right branch: $19-3x=2x-2\Rightarrow x=\tfrac{21}{5}$. The left branch gives $x=9$, which isn't less than 3, so reject it.",
          r"(c) The line passes through $(0,1)$. It must be steeper than the line to $P$ (gradient 1) but less steep than the right arm (gradient 2): $1<k<2$."],
         [r"Sketch the V and the line through $(0,1)$, then compare its gradient with the line to $P$ and the right arm",
          r"Solve $kx+1=2x-2$ only",
          r"Use $b^2-4ac>0$",
          r"Use $k=2$, the gradient of the right arm"],
         ask="How do you start part (c)?"),
    card(1, 7,
         [r"A cylindrical tank 2 m tall is full of water. Water leaks out through a small hole in its side.",
          r"The depth $H$ m of the water $t$ hours after the leak starts is modelled by $\dfrac{dH}{dt}=-0.15e^{-0.25t}$.",
          r"(a) Show that $H=Ae^{-0.25t}+B$, where $A$ and $B$ are constants to be found.",
          r"(b) Find the time taken for the depth to fall to 1.7 m, in hours and minutes to the nearest minute.",
          r"In the long term, the water level falls to the height of the hole. (c) Find the height of the hole above the bottom of the tank."],
         [r"Spot: $\dfrac{dH}{dt}$ depends on $t$ only, so integrate directly. The tank being full at the start gives the constant.",
          r"Use: $\displaystyle\int e^{-0.25t}\,dt=-4e^{-0.25t}+c$.",
          r"(a) $H=0.6e^{-0.25t}+c$, and $H=2$ at $t=0$ gives $c=1.4$. So $A=0.6$ and $B=1.4$.",
          r"(b) $0.6e^{-0.25t}=0.3\Rightarrow t=4\ln2\approx2.773$ hours, which is 2 hours 46 minutes",
          r"(c) As $t\to\infty$, $H\to1.4$, so the hole is 1.4 m above the bottom."],
         [r"Integrate with respect to $t$, then use $H=2$ at $t=0$",
          r"Separate the variables as $\frac{dH}{H}$",
          r"Use $H=2e^{-0.25t}$",
          r"Differentiate $-0.15e^{-0.25t}$"],
         ask="How do you start part (a)?"),
    card(1, 8,
         [r"$f(x)=3-2x^2$, $x\in\mathbb{R}$, and $g(x)=\dfrac{3}{2x-7}$, $x\ne\dfrac72$.",
          r"(a) Find $fg(4)$. (b) Find $g^{-1}$.",
          r"(c)(i) Find $gf(x)$ as a simplified fraction. (ii) Deduce the range of $gf$.",
          r"$h(x)=x^2-4x+k$, where $k$ is a constant.",
          r"(d) Find the values of $k$ for which $f(x)=h(x)$ has no real solutions."],
         [r"Spot: $gf$ means apply $f$ first. In (d), “no real solutions” means rearrange to a quadratic and use $b^2-4ac<0$.",
          r"Use: for $g^{-1}$, write $y=g(x)$ and make $x$ the subject.",
          r"(a) $g(4)=3$, so $fg(4)=f(3)=-15$",
          r"(b) $g^{-1}(x)=\dfrac{3+7x}{2x}$, $x\ne0$",
          r"(c)(i) $gf(x)=\dfrac{3}{2(3-2x^2)-7}=-\dfrac{3}{1+4x^2}$ (ii) $1+4x^2\ge1$, so $-3\le gf(x)<0$",
          r"(d) $3x^2-4x+k-3=0$, and $16-12(k-3)<0\Rightarrow k>\dfrac{13}{3}$"],
         [r"Rearrange to $3x^2-4x+k-3=0$ and use $b^2-4ac<0$",
          r"Rearrange and use $b^2-4ac>0$",
          r"Solve $f(x)=0$ and $h(x)=0$ separately",
          r"Rearrange and use $b^2-4ac=0$"],
         ask="How do you start part (d)?"),
    card(1, 9,
         [r"The first three terms of a geometric sequence are $2^{4k-5}$, $4^{8-2k}$ and $2^{k-2}$, where $k$ is a constant.",
          r"(a) Using algebra, prove that $k=3$.",
          r"(b) Hence find the sum to infinity of the sequence."],
         [r"Spot: in a geometric sequence $(u_2)^2=u_1u_3$. Write every term as a power of 2, then compare the indices.",
          r"Use: $4^{8-2k}=2^{2(8-2k)}$ and $2^a\times2^b=2^{a+b}$.",
          r"(a) $\left(2^{16-4k}\right)^2=2^{4k-5}\times2^{k-2}\Rightarrow32-8k=5k-7\Rightarrow k=3$",
          r"(b) The terms are $128,16,2$, so $r=\tfrac18$ and $S_\infty=\dfrac{128}{1-\frac18}=\dfrac{1024}{7}$"],
         [r"Write every term as a power of 2 and use $(u_2)^2=u_1u_3$",
          r"Use $u_2-u_1=u_3-u_2$",
          r"Put the indices $4k-5$, $8-2k$ and $k-2$ in an arithmetic sequence",
          r"Take $\log_4$ of each term and add them"],
         ask="How do you start part (a)?"),
    card(1, 10,
         [r"The curve $C$ has equation $y=2x-x^{\frac32}$, $x\ge0$, and crosses the $x$-axis at $A$.",
          r"(a) Verify that the $x$-coordinate of $A$ is 4.",
          r"The line $l_1$ is the tangent to $C$ at $A$. (b) Use calculus to show that $l_1$ has equation $x+y=4$.",
          r"The line $l_2$ has equation $y=2x$. The region $R$ is bounded by $C$, $l_1$ and $l_2$.",
          r"(c) Use algebraic integration to find the exact area of $R$."],
         [r"Spot: $R$ is the triangle under the two lines minus the area under the curve. The lines meet where $2x=4-x$.",
          r"Use: the area under $C$ is $\displaystyle\int_0^4\left(2x-x^{\frac32}\right)dx$, and a triangle is $\tfrac12\times\text{base}\times\text{height}$.",
          r"(a) $8-4^{\frac32}=8-8=0$",
          r"(b) $\dfrac{dy}{dx}=2-\tfrac32x^{\frac12}=-1$ at $x=4$, so $y=-(x-4)$",
          r"(c) The lines meet at $\left(\tfrac43,\tfrac83\right)$, so the triangle with $O$ and $A$ has area $\tfrac12(4)\left(\tfrac83\right)=\tfrac{16}{3}$.",
          r"$\left[x^2-\tfrac25x^{\frac52}\right]_0^4=16-\tfrac{64}{5}=\tfrac{16}{5}$, so the area of $R$ is $\tfrac{16}{3}-\tfrac{16}{5}=\tfrac{32}{15}$."],
         [r"Find the triangle under $l_1$ and $l_2$, then subtract the area under $C$",
          r"Integrate $C$ from 0 to 4 and stop",
          r"Integrate $2x-(4-x)$ from 0 to 4",
          r"Add the area under $C$ to the triangle"],
         ask="How do you start part (c)?"),
    card(1, 11,
         [r"A badge is a semicircle $ABCOA$ with centre $O$ and diameter $AC=12$ cm. $B$ is on the curved edge.",
          r"$OB$ is an arc of the circle with centre $A$ and radius 6 cm. The region $R$ is bounded by the arc $OB$, the arc $BC$ and the line $OC$.",
          r"Find the exact area of $R$, in the form $(a\sqrt3+b\pi)\text{ cm}^2$, where $a$ and $b$ are rational."],
         [r"Spot: $AB=AO=OB=6$, so triangle $AOB$ is equilateral. That gives angle $BAO=\dfrac{\pi}{3}$ and angle $BOC=\dfrac{2\pi}{3}$.",
          r"Use: sector $=\tfrac12r^2\theta$, and segment $=\tfrac12r^2(\theta-\sin\theta)$.",
          r"Method: $R$ is sector $BOC$ minus the segment that chord $OB$ cuts from the circle centred at $A$.",
          r"$\tfrac12(36)\left(\tfrac{2\pi}{3}\right)-\tfrac12(36)\left(\tfrac{\pi}{3}-\sin\tfrac{\pi}{3}\right)=12\pi-6\pi+9\sqrt3$",
          r"Answer: $(9\sqrt3+6\pi)\text{ cm}^2$"],
         [r"Spot the equilateral triangle $AOB$, then take a segment away from sector $BOC$",
          r"Use angle $BOC=\frac{\pi}{3}$",
          r"Use the sector $BOC$ alone",
          r"Use $\frac12r^2\theta$ with $\theta$ in degrees"]),
    card(1, 12,
         [r"(a) Express $120\cos\theta-350\sin\theta$ in the form $K\cos(\theta+\alpha)$, where $K>0$ and $0<\alpha<90^\circ$. Give $\alpha$ to 2 d.p.",
          r"The number of rabbits in a wood $t$ months after the start of a year is modelled by $R=A+120\cos(30t)^\circ-350\sin(30t)^\circ$, where $A$ is a constant. The maximum number during the year is 1200.",
          r"(b)(i) Find a complete equation for the model. (ii) Write down the minimum number of rabbits.",
          r"(c) The actual number of rabbits was lowest in the middle of April. Comment on the model.",
          r"The number of foxes is modelled by $F=90+60\sin(30t+50)^\circ$, and is lowest after $T$ months. (d) Find the number of rabbits at time $T$."],
         [r"Spot: once it's in the form $K\cos(\theta+\alpha)$, the maximum and minimum are $A\pm K$, and you can work out when they happen.",
          r"Use: $K=\sqrt{120^2+350^2}$ and $\tan\alpha=\dfrac{350}{120}$.",
          r"(a) $K=370$ and $\alpha\approx71.08^\circ$",
          r"(b)(i) $A+370=1200$, so $R=830+370\cos(30t+71.08)^\circ$ (ii) $830-370=460$",
          r"(c) The minimum is when $30t+71.08=180$, so $t\approx3.6$, which is in April. The model fits.",
          r"(d) $30T+50=270\Rightarrow T=\tfrac{22}{3}$, so $R=830+370\cos291.08^\circ\approx963$ rabbits"],
         [r"Write it as $K\cos(\theta+\alpha)$ with $K=370$, so the maximum is $A+370$",
          r"Use a maximum of $A+120$",
          r"Use $K=120+350$",
          r"Set $t=0$ for the maximum"],
         ask="How do you start part (b)?"),
    card(1, 13,
         [r"(a) Given that $a$ is a positive constant, use the substitution $x=a\sin^2\theta$ to show that $\displaystyle\int_0^{\frac{3a}{4}}\sqrt{\frac{x}{a-x}}\,dx=2a\int_0^{\frac{\pi}{3}}\sin^2\theta\,d\theta$.",
          r"(b) Hence use algebraic integration to show that the integral equals $a\left(\dfrac{\pi}{3}-\dfrac{\sqrt3}{4}\right)$."],
         [r"Spot: with a given substitution, change all three parts: the integrand, $dx$ and the limits. Then $\sin^2\theta$ needs the double angle formula.",
          r"Use: $dx=2a\sin\theta\cos\theta\,d\theta$, $1-\sin^2\theta=\cos^2\theta$ and $\sin^2\theta=\dfrac{1-\cos2\theta}{2}$.",
          r"(a) $\sqrt{\dfrac{a\sin^2\theta}{a\cos^2\theta}}\times2a\sin\theta\cos\theta=2a\sin^2\theta$. $x=0$ gives $\theta=0$, and $x=\tfrac{3a}{4}$ gives $\sin^2\theta=\tfrac34$, so $\theta=\tfrac{\pi}{3}$.",
          r"(b) $2a\left[\dfrac{\theta}{2}-\dfrac{\sin2\theta}{4}\right]_0^{\frac{\pi}{3}}=2a\left(\dfrac{\pi}{6}-\dfrac{\sqrt3}{8}\right)=a\left(\dfrac{\pi}{3}-\dfrac{\sqrt3}{4}\right)$"],
         [r"Use $\sin^2\theta=\frac{1-\cos2\theta}{2}$, then integrate",
          r"Integrate $\sin^2\theta$ as $\frac13\sin^3\theta$",
          r"Use $\sin^2\theta=\frac{1+\cos2\theta}{2}$",
          r"Integrate $\sin^2\theta$ as $-\cos^2\theta$"],
         ask="How do you start part (b)?"),
    card(1, 14,
         [r"A balloon is being inflated. In a simple model, the balloon is a sphere and the rate of increase of its radius is inversely proportional to its radius. At time $t$ seconds, the radius is $r$ cm.",
          r"(a) Write down a differential equation for this model.",
          r"When $t=5$, the radius is 10 cm and is increasing at 0.8 cm per second.",
          r"(b) Solve the differential equation to show that $r^2=16t+20$.",
          r"(c) Find the radius when $t=12$, to the nearest millimetre. (d) Suggest a limitation of the model."],
         [r"Spot: “inversely proportional to $r$” means $\dfrac{dr}{dt}=\dfrac kr$. Use the given rate to find $k$, then separate the variables.",
          r"Use: $\displaystyle\int r\,dr=\int k\,dt$.",
          r"(a) $\dfrac{dr}{dt}=\dfrac kr$",
          r"(b) $0.8=\dfrac{k}{10}\Rightarrow k=8$. Then $\tfrac12r^2=8t+c$, and $t=5$, $r=10$ gives $c=10$, so $r^2=16t+20$.",
          r"(c) $r=\sqrt{212}\approx14.6$ cm",
          r"(d) The radius keeps growing forever, but a real balloon would burst. A balloon also isn't a perfect sphere."],
         [r"Use $\frac{dr}{dt}=\frac kr$, find $k$ from the given rate, then separate the variables",
          r"Use $\frac{dr}{dt}=kr$",
          r"Use $\frac{dr}{dt}=\frac{k}{r^2}$",
          r"Differentiate $V=\frac43\pi r^3$"],
         ask="How do you start part (b)?"),
    card(1, 15,
         [r"(i) Show that $k^2+6k+11$ is positive for all real values of $k$.",
          r"(ii) Prove by contradiction that there are no positive integers $x$ and $y$ with $(3x+2y)(x-3y)=20$.",
          r"A student starts: assume such $x$ and $y$ exist. If $3x+2y=10$ and $x-3y=2$, then $x=\tfrac{34}{11}$ and $y=\tfrac{4}{11}$, which aren't integers. Complete the proof."],
         [r"Spot: (i) complete the square. (ii) Both brackets are integers, so they must be a factor pair of 20. Check every possible pair.",
          r"Use: $x,y\ge1$ gives $3x+2y\ge5$. The product is positive, so $x-3y$ is positive too.",
          r"(i) $(k+3)^2+2\ge2>0$",
          r"(ii) The pairs left are $(20,1)$ and $(5,4)$. $3x+2y=20$ and $x-3y=1$ give $y=\tfrac{17}{11}$. $3x+2y=5$ and $x-3y=4$ give $y=-\tfrac{7}{11}$. Neither works.",
          r"Every case fails, which contradicts the assumption, so no such $x$ and $y$ exist."],
         [r"List the factor pairs of 20 with $3x+2y\ge5$ and solve each pair",
          r"Expand the brackets and complete the square",
          r"Try $x=1$ and $y=1$",
          r"Assume $x$ and $y$ are both even"],
         ask="How do you complete part (ii)?"),

    # ---------------- Paper 2 ----------------
    card(2, 1,
         [r"$y=2x^3+9x^2-4x+3$.",
          r"(a) Find, in simplest form, (i) $\dfrac{dy}{dx}$ (ii) $\dfrac{d^2y}{dx^2}$.",
          r"(b) Hence find the exact value of $x$ when $\dfrac{d^2y}{dx^2}=0$."],
         [r"Spot: differentiate term by term, twice. $\dfrac{d^2y}{dx^2}=0$ is where the curve could change between concave and convex.",
          r"Use: $\dfrac{d}{dx}(x^n)=nx^{n-1}$, and a constant differentiates to 0.",
          r"(a)(i) $6x^2+18x-4$ (ii) $12x+18$",
          r"(b) $12x+18=0\Rightarrow x=-\tfrac32$"],
         [r"Differentiate twice, then solve $12x+18=0$",
          r"Solve $\frac{dy}{dx}=0$",
          r"Solve $y=0$",
          r"Differentiate once and solve $6x^2+18x-4=0$"],
         ask="How do you answer part (b)?"),
    card(2, 2,
         [r"Sam takes out an interest-free loan of £4500. Sam repays £300 in month 1, £290 in month 2, £280 in month 3, and so on, as an arithmetic sequence.",
          r"(a) Show that Sam repays £190 in month 12.",
          r"After the $N$th payment, the loan is fully repaid.",
          r"(b) Show that $N^2-61N+900=0$. (c) Hence find $N$."],
         [r"Spot: the repayments form an arithmetic sequence, and the total repaid is the sum $S_N$.",
          r"Use: $u_n=a+(n-1)d$ and $S_n=\dfrac n2\left[2a+(n-1)d\right]$, with $a=300$ and $d=-10$.",
          r"(a) $300+11(-10)=190$",
          r"(b) $\dfrac N2\left[600-10(N-1)\right]=4500\Rightarrow N(610-10N)=9000\Rightarrow N^2-61N+900=0$",
          r"(c) $(N-25)(N-36)=0$. A payment in month 36 would be $300-350=-50$, which is impossible, so $N=25$."],
         [r"Set $S_N=4500$ with $a=300$ and $d=-10$",
          r"Set $u_N=4500$",
          r"Use $d=10$",
          r"Use $S_N=\frac N2(300+190)$"],
         ask="How do you start part (b)?"),
    card(2, 3,
         [r"The point $P(-4,6)$ lies on the curve $y=f(x)$. Find the point that $P$ maps to when the curve is transformed to:",
          r"(i) $y=f(x+3)$",
          r"(ii) $y=f\left(\tfrac12x\right)$",
          r"(iii) $y=-2f(-x)+1$"],
         [r"Spot: changes inside the bracket act on $x$, the opposite way to how they look. Changes outside act on $y$, as written.",
          r"Use: $f(x+3)$ moves left 3. $f\left(\tfrac12x\right)$ stretches $x$ by a factor of 2. $f(-x)$ reflects in the $y$-axis. $-2f$ multiplies $y$ by $-2$, then $+1$ moves up 1.",
          r"(i) $(-7,6)$",
          r"(ii) $(-8,6)$",
          r"(iii) $(4,-11)$"],
         [r"Reflect $x$ to 4, then multiply $y$ by $-2$ and add 1",
          r"Add 1 to $y$, then multiply by $-2$",
          r"Multiply $x$ by $-2$",
          r"Keep $x=-4$ and change $y$ only"],
         ask="How do you find the point in (iii)?"),
    card(2, 4,
         [r"A sequence is defined by $u_1=9$ and $u_{n+1}=ku_n-6$, where $k$ is a positive constant. Given that $u_3=2$,",
          r"(a) show that $9k^2-6k-8=0$.",
          r"(b)(i) Find the value of $k$. (ii) Find $\displaystyle\sum_{r=1}^{4}u_r$."],
         [r"Spot: a recurrence relation with an unknown $k$. Generate $u_2$ and $u_3$ in terms of $k$, then use the given value.",
          r"Use: $u_2=9k-6$ and $u_3=k(9k-6)-6$.",
          r"(a) $9k^2-6k-6=2\Rightarrow9k^2-6k-8=0$",
          r"(b)(i) $(3k-4)(3k+2)=0$ and $k>0$, so $k=\tfrac43$",
          r"(ii) $u_2=6$, $u_3=2$ and $u_4=\tfrac43(2)-6=-\tfrac{10}{3}$, so the sum is $9+6+2-\tfrac{10}{3}=\tfrac{41}{3}$"],
         [r"Write $u_2=9k-6$, then $u_3=k(9k-6)-6$, and set $u_3=2$",
          r"Use $u_3=u_1+2k$",
          r"Use $u_3=9k^2$",
          r"Use $u_3=9k-12$"],
         ask="How do you start part (a)?"),
    card(2, 5,
         [r"Given that $\theta$ is small and in radians, use the small angle approximations to find an approximate value of $\dfrac{3\theta\sin2\theta}{1-\cos4\theta}$."],
         [r"Spot: “small and in radians” means replace each trig function with its small angle approximation, and then the powers of $\theta$ cancel.",
          r"Use: $\sin k\theta\approx k\theta$ and $\cos k\theta\approx1-\dfrac{(k\theta)^2}{2}$.",
          r"Method: $1-\cos4\theta\approx\dfrac{16\theta^2}{2}=8\theta^2$, so the expression is about $\dfrac{3\theta\times2\theta}{8\theta^2}$.",
          r"Answer: $\dfrac34$"],
         [r"Use $\sin2\theta\approx2\theta$ and $\cos4\theta\approx1-8\theta^2$",
          r"Use $\cos4\theta\approx1-4\theta^2$",
          r"Use $\cos4\theta\approx1$",
          r"Use $\sin2\theta\approx1-2\theta^2$"]),
    card(2, 6,
         [r"$f(x)=e^{2x^2-3}$ and $g(x)=4\ln x$, for $x>0$.",
          r"(a) Find (i) $f'(x)$ (ii) $g'(x)$.",
          r"Given that $f'(x)=g'(x)$ at $x=\alpha$, (b) show that $\alpha$ satisfies $x^2+\ln x-1.5=0$.",
          r"The iterative formula $x_{n+1}=\sqrt{1.5-\ln x_n}$ is used with $x_1=1$.",
          r"(c) Find, to 4 d.p., (i) $x_2$ (ii) $\alpha$."],
         [r"Spot: $e^{\text{function}}$ needs the chain rule. When you set the derivatives equal, take logs to bring the power down.",
          r"Use: $\dfrac{d}{dx}e^{u}=u'e^{u}$ and $\ln\dfrac{1}{x^2}=-2\ln x$.",
          r"(a)(i) $4xe^{2x^2-3}$ (ii) $\dfrac4x$",
          r"(b) $4xe^{2x^2-3}=\dfrac4x\Rightarrow e^{2x^2-3}=\dfrac{1}{x^2}\Rightarrow2x^2-3=-2\ln x$, then divide by 2.",
          r"(c)(i) $x_2=\sqrt{1.5}=1.2247$ (ii) $\alpha=1.1619$"],
         [r"Set $4xe^{2x^2-3}=\frac4x$, then take logs",
          r"Set $e^{2x^2-3}=4\ln x$",
          r"Differentiate $e^{2x^2-3}$ as $e^{2x^2-3}$",
          r"Differentiate $e^{2x^2-3}$ as $(2x^2-3)e^{2x^2-4}$"],
         ask="How do you start part (b)?"),
    card(2, 7,
         [r"Relative to a fixed origin $O$, $A$ has position vector $\mathbf{i}+4\mathbf{j}-2\mathbf{k}$ and $B$ has position vector $3\mathbf{i}-2\mathbf{j}+2\mathbf{k}$. The line $l$ passes through $A$ and $B$.",
          r"(a) Find $\overrightarrow{AB}$.",
          r"The point $P$ lies on $l$, and $|\overrightarrow{AP}|=3|\overrightarrow{BP}|$.",
          r"(b) Find the possible position vectors of $P$."],
         [r"Spot: $P$ is on the line, so $\overrightarrow{AP}=\lambda\overrightarrow{AB}$. The distance condition has two cases: $P$ between $A$ and $B$, or beyond $B$.",
          r"Use: $\overrightarrow{BP}=(\lambda-1)\overrightarrow{AB}$, so $|\lambda|=3|\lambda-1|$.",
          r"(a) $2\mathbf{i}-6\mathbf{j}+4\mathbf{k}$",
          r"(b) $\lambda=\tfrac32$ or $\lambda=\tfrac34$",
          r"Answer: $4\mathbf{i}-5\mathbf{j}+4\mathbf{k}$ or $\tfrac52\mathbf{i}-\tfrac12\mathbf{j}+\mathbf{k}$"],
         [r"Write $\overrightarrow{AP}=\lambda\overrightarrow{AB}$, so $|\lambda|=3|\lambda-1|$",
          r"Use $\overrightarrow{OP}=3\overrightarrow{OB}$",
          r"Use the midpoint of $AB$",
          r"Use $\lambda=3$ only"],
         ask="How do you start part (b)?"),
    card(2, 8,
         [r"(a) Prove that $\dfrac{1}{\sec\theta-1}+\dfrac{1}{\sec\theta+1}\equiv2\cot\theta\cosec\theta$, for $\theta\ne90n^\circ$.",
          r"(b) Hence solve, for $0<x<90^\circ$, the equation $\dfrac{1}{\sec2x-1}+\dfrac{1}{\sec2x+1}=3\tan2x\cosec2x$. Give your answers to 1 d.p."],
         [r"Spot: (a) add the fractions. The denominator is a difference of two squares, $\sec^2\theta-1=\tan^2\theta$. (b) Use (a) with $\theta=2x$, and then $\cosec2x$ cancels.",
          r"Use: $\sec^2\theta-1=\tan^2\theta$, $\sec\theta=\dfrac{1}{\cos\theta}$ and $\cot\theta=\dfrac{1}{\tan\theta}$.",
          r"(a) $\dfrac{2\sec\theta}{\sec^2\theta-1}=\dfrac{2\sec\theta}{\tan^2\theta}=\dfrac{2}{\cos\theta}\times\dfrac{\cos^2\theta}{\sin^2\theta}=\dfrac{2\cos\theta}{\sin^2\theta}=2\cot\theta\cosec\theta$",
          r"(b) $2\cot2x\cosec2x=3\tan2x\cosec2x\Rightarrow\tan^22x=\tfrac23$",
          r"$2x=39.2^\circ$ or $140.8^\circ$, so $x=19.6^\circ$ or $70.4^\circ$"],
         [r"Use (a) with $\theta=2x$, cancel $\cosec2x$, then solve $\tan^22x=\frac23$",
          r"Use (a) with $\theta=x$",
          r"Square both sides first",
          r"Take only the positive root of $\tan^22x=\frac23$"],
         ask="How do you start part (b)?"),
    card(2, 9,
         [r"A small ball is thrown from $A(0,1.8)$ and caught at $B(24,1.2)$, where $x$ m is the horizontal distance and $H$ m is the height above horizontal ground. The ball is highest when $x=11$.",
          r"A quadratic model links $H$ and $x$. (a) Find $H$ in terms of $x$. (b) Give one limitation of the model.",
          r"Robin stands directly under the path, 20 m horizontally from $O$, and can catch the ball if it's less than 2.5 m above the ground.",
          r"(c) Use the model to decide whether Robin can catch the ball."],
         [r"Spot: the maximum at $x=11$ means use vertex form, $H=q-a(x-11)^2$. The two points give two equations.",
          r"Use: $1.8=q-121a$ and $1.2=q-169a$.",
          r"(a) $48a=0.6\Rightarrow a=0.0125$ and $q=3.3125$, so $H=3.3125-0.0125(x-11)^2=-0.0125x^2+0.275x+1.8$",
          r"(b) It ignores air resistance and wind, and treats the ball as a particle.",
          r"(c) $H(20)=3.3125-0.0125(81)=2.3$ m, which is less than 2.5 m, so Robin can catch it."],
         [r"Use $H=q-a(x-11)^2$ with the points $A$ and $B$",
          r"Use $H=ax^2+bx$",
          r"Use $H=a(x-11)^2$ with no constant",
          r"Use $H=1.8-(x-11)^2$"],
         ask="How do you start part (a)?"),
    card(2, 10,
         [r"A curve $C$ has parametric equations $x=(t+2)^2$, $y=2-t^3$, $-1.5\le t\le1$. The point $P(1,3)$ lies on $C$.",
          r"(a) Using parametric differentiation, show that the tangent to $C$ at $P$ has equation $3x+2y=9$.",
          r"$C$ models the profile of a water slide, in metres, where $y$ is the height above the water.",
          r"(b) Find the greatest height of the slide above the water."],
         [r"Spot: the parametric gradient is $\dfrac{dy/dt}{dx/dt}$. First find the value of $t$ at $P$.",
          r"Use: $\dfrac{dy}{dx}=\dfrac{-3t^2}{2(t+2)}$.",
          r"(a) $P$ is at $t=-1$, where $\dfrac{dy}{dx}=-\dfrac32$. So $y-3=-\tfrac32(x-1)\Rightarrow3x+2y=9$.",
          r"(b) $y=2-t^3$ decreases as $t$ increases, so the greatest height is at $t=-1.5$: $2+3.375=5.375$ m"],
         [r"Find $t$ at $P$, then use $\frac{dy}{dx}=\frac{dy/dt}{dx/dt}$",
          r"Use $\frac{dy}{dx}=\frac{dx/dt}{dy/dt}$",
          r"Substitute $t=1$",
          r"Differentiate $y$ with respect to $t$ and stop"],
         ask="How do you start part (a)?"),
    card(2, 11,
         [r"The curve $C$ has equation $y=9x^2e^{-2x}$, $x\ge0$. The region $R$ is bounded by $C$, the line $x=1$ and the $x$-axis.",
          r"Find the exact area of $R$, in the form $A+Be^{-2}$, where $A$ and $B$ are rational."],
         [r"Spot: a power of $x$ times an exponential means integration by parts. $x^2$ needs it twice, with $u$ as the power of $x$ each time.",
          r"Use: $\displaystyle\int u\frac{dv}{dx}\,dx=uv-\int v\frac{du}{dx}\,dx$, with $u=x^2$ and $\dfrac{dv}{dx}=e^{-2x}$.",
          r"Method: $\displaystyle\int x^2e^{-2x}\,dx=-\tfrac12x^2e^{-2x}-\tfrac12xe^{-2x}-\tfrac14e^{-2x}+c$",
          r"Answer: $9\left[\tfrac14-\tfrac54e^{-2}\right]=\dfrac94-\dfrac{45}{4}e^{-2}$"],
         [r"Use integration by parts twice, with $u=x^2$ first",
          r"Use integration by parts with $u=e^{-2x}$",
          r"Integrate $x^2$ and $e^{-2x}$ separately and multiply",
          r"Use the substitution $u=x^2$"]),
    card(2, 12,
         [r"(a) Express $\dfrac{1}{V(30-V)}$ in partial fractions.",
          r"The volume $V$ microlitres of a plant cell $t$ hours after watering is modelled by $\dfrac{dV}{dt}=\dfrac{1}{15}V(30-V)$. The initial volume is 10 microlitres.",
          r"(b) Find the time taken, in minutes, for the volume to reach 20 microlitres.",
          r"(c) Show that $V=\dfrac{A}{B+e^{-kt}}$, where $A$, $B$ and $k$ are constants to be found.",
          r"(d) The model predicts an upper limit $L$ on the volume. Find $L$, with a reason."],
         [r"Spot: separate the variables. The $V$ side needs the partial fractions from (a).",
          r"Use: $\dfrac{1}{V(30-V)}=\dfrac{1}{30V}+\dfrac{1}{30(30-V)}$, and $\displaystyle\int\frac{dV}{30-V}=-\ln|30-V|$.",
          r"(b) $\dfrac{1}{30}\ln\dfrac{V}{30-V}=\dfrac{t}{15}+c$, with $c=\tfrac{1}{30}\ln\tfrac12$. $V=20$ gives $t=\ln2$ hours, about 41.6 minutes.",
          r"(c) $\dfrac{V}{30-V}=\tfrac12e^{2t}\Rightarrow V=\dfrac{30}{1+2e^{-2t}}=\dfrac{15}{\frac12+e^{-2t}}$, so $A=15$, $B=\tfrac12$ and $k=2$",
          r"(d) As $t\to\infty$, $e^{-2t}\to0$, so $V\to30$. $L=30$."],
         [r"Separate the variables, using the partial fractions to integrate $\frac{1}{V(30-V)}$",
          r"Integrate $V(30-V)$ with respect to $t$",
          r"Integrate $\frac{1}{V(30-V)}$ as $\ln V(30-V)$",
          r"Assume $\frac{dV}{dt}$ is constant"],
         ask="How do you start part (b)?"),
    card(2, 13,
         [r"The number of subscribers to a streaming service, $P$ millions, is modelled by $P=ab^t$, where $t$ is the number of years after 2015.",
          r"A graph of $\log_{10}P$ against $t$ is close to a straight line with gradient 0.12 and intercept 1.3.",
          r"(a) Estimate $a$ and $b$ to 3 d.p. (b) Interpret (i) $a$ (ii) $b$ in context.",
          r"(c) Estimate the number of subscribers in 2030. (d) Comment on the reliability of your answer to (c)."],
         [r"Spot: $P=ab^t$ becomes a straight line when you take logs: $\log P=\log a+t\log b$. The intercept is $\log a$ and the gradient is $\log b$.",
          r"Use: $a=10^{\text{intercept}}$ and $b=10^{\text{gradient}}$.",
          r"(a) $a=10^{1.3}\approx19.953$ and $b=10^{0.12}\approx1.318$",
          r"(b)(i) There were about 20 million subscribers in 2015. (ii) The number grows by about 31.8% each year.",
          r"(c) $t=15$: $\log_{10}P=1.3+15(0.12)=3.1$, so $P\approx1260$ million",
          r"(d) It's unreliable: it extrapolates 15 years ahead, and growth of 32% a year can't continue."],
         [r"Take logs: $\log P=\log a+t\log b$, so $a=10^{1.3}$ and $b=10^{0.12}$",
          r"Use $a=1.3$ and $b=0.12$",
          r"Use $a=e^{1.3}$ and $b=e^{0.12}$",
          r"Use $a=0.12$ and $b=1.3$"],
         ask="How do you start part (a)?"),
    card(2, 14,
         [r"The circle $C_1$ has equation $x^2+y^2+4x-10y+20=0$.",
          r"(a) Find (i) the coordinates of the centre (ii) the radius of $C_1$.",
          r"The circle $C_2$ has centre $(4,1)$ and radius $k$. $C_1$ and $C_2$ meet at two distinct points.",
          r"(b) Find the range of values of $k$, in set notation."],
         [r"Spot: two circles meet at two points when the distance between the centres is less than the sum of the radii and more than their difference.",
          r"Use: $|r_1-r_2|<d<r_1+r_2$.",
          r"(a) $(x+2)^2+(y-5)^2=9$, so the centre is $(-2,5)$ and the radius is 3.",
          r"(b) $d=\sqrt{6^2+4^2}=2\sqrt{13}$, so $k+3>2\sqrt{13}$ and $|k-3|<2\sqrt{13}$.",
          r"Answer: $\{k:2\sqrt{13}-3<k<2\sqrt{13}+3\}$"],
         [r"Compare the distance between the centres with $k+3$ and $|k-3|$",
          r"Set the distance between the centres equal to $k+3$",
          r"Use $k>3$ only",
          r"Use $k<2\sqrt{13}$ only"],
         ask="How do you start part (b)?"),
    card(2, 15,
         [r"The curve $C$ has equation $(x+y)^3=2x^2-y-1$.",
          r"(a) Find $\dfrac{dy}{dx}$ in terms of $x$ and $y$.",
          r"The point $P(1,0)$ lies on $C$. (b) Show that the normal to $C$ at $P$ has equation $y=4-4x$.",
          r"(c) Prove, using algebra, that the normal at $P$ doesn't meet $C$ again."],
         [r"Spot: implicit differentiation, with the chain rule on $(x+y)^3$. In (c), substitute the normal into $C$. You already know $x=1$ is a root, so factorise and show the other factor has no real roots.",
          r"Use: $\dfrac{d}{dx}(x+y)^3=3(x+y)^2\left(1+\dfrac{dy}{dx}\right)$.",
          r"(a) $3(x+y)^2\left(1+\dfrac{dy}{dx}\right)=4x-\dfrac{dy}{dx}\Rightarrow\dfrac{dy}{dx}=\dfrac{4x-3(x+y)^2}{3(x+y)^2+1}$",
          r"(b) At $P$ the gradient is $\dfrac14$, so the normal has gradient $-4$: $y=-4(x-1)$",
          r"(c) $(4-3x)^3=2x^2+4x-5\Rightarrow27x^3-106x^2+148x-69=0\Rightarrow(x-1)(27x^2-79x+69)=0$",
          r"$79^2-4(27)(69)=-1211<0$, so $x=1$ is the only intersection."],
         [r"Substitute $y=4-4x$ into $C$, factor out $(x-1)$, then use the discriminant",
          r"Solve $\frac{dy}{dx}=-4$",
          r"Show the normal and the tangent are perpendicular",
          r"Substitute $x=1$ into $C$"],
         ask="How do you start part (c)?"),
]


def check():
    a, n, u, h = sp.symbols("a n u h")
    xp = sp.symbols("xp", positive=True)
    # P1 Q1
    g1 = 2 * x**3 - 9 * x**2 + (k - 5) * x + 2 * k
    assert sp.solve(g1.subs(x, 4), k) == [6]
    # P1 Q2
    ser = sp.series(sp.sqrt(1 + 8 * x), x, 0, 4).removeO()
    assert same(ser, 1 + 4 * x - 8 * x**2 + 32 * x**3) and 1 + 8 * sp.Rational(1, 4) == 3
    # P1 Q3
    f3 = lambda v: 2 * v + math.tan(v / 2)
    fp3 = lambda v: 2 + 0.5 / math.cos(v / 2)**2
    assert round(f3(3.4), 3) == -0.897 and round(f3(3.5), 3) == 1.480 and round(fp3(3.5), 3) == 17.737
    assert round(3.5 - f3(3.5) / fp3(3.5), 3) == 3.417 and math.pi < 3.4 and 3.5 < 1.5 * math.pi
    assert same(sp.diff(2 * x + sp.tan(x / 2), x), 2 + sp.sec(x / 2)**2 / 2)
    # P1 Q4
    assert sp.limit(((x + h)**3 - x**3) / h, h, 0) == 3 * x**2
    # P1 Q5
    d5 = sp.together(sp.diff((3 * x + 2) / (x**2 + 5), x))
    assert same(d5, (-3 * x**2 - 4 * x + 15) / (x**2 + 5)**2)
    dec = sp.solve_univariate_inequality(-3 * x**2 - 4 * x + 15 < 0, x, relational=False)
    assert dec == sp.Union(sp.Interval.open(-sp.oo, -3), sp.Interval.open(sp.Rational(5, 3), sp.oo))
    # P1 Q6
    V = lambda v: 2 * abs(v - 3) + 4
    sols6 = [v for v in (sp.Rational(21, 5), 9) if 19 - 3 * v == V(v)]
    assert sols6 == [sp.Rational(21, 5)]

    def meets(kv):
        pts = set()
        if kv != 2:
            xr = sp.Rational(-3, 1) / (kv - 2)  # kx+1 = 2x-2
            if xr >= 3:
                pts.add(xr)
        xl = sp.Rational(9, 1) / (kv + 2)  # kx+1 = 10-2x
        if xl < 3:
            pts.add(xl)
        return len(pts)
    assert all(meets(sp.Rational(v, 10)) == 2 for v in range(11, 20))
    assert all(meets(sp.Rational(v, 10)) < 2 for v in (0, 5, 10, 20, 25, 40))
    # P1 Q7
    H7 = sp.Rational(3, 5) * sp.exp(-t / 4) + sp.Rational(7, 5)
    assert same(sp.diff(H7, t), sp.Rational(-15, 100) * sp.exp(-t / 4)) and H7.subs(t, 0) == 2
    t7 = 4 * math.log(2)
    assert close(float(H7.subs(t, t7)), 1.7) and (int(t7), round((t7 - int(t7)) * 60)) == (2, 46)
    assert sp.limit(H7, t, sp.oo) == sp.Rational(7, 5)
    # P1 Q8
    f8 = lambda v: 3 - 2 * v**2
    g8 = lambda v: 3 / (2 * v - 7)
    assert f8(g8(sp.Integer(4))) == -15
    ginv = (3 + 7 * x) / (2 * x)
    assert same(g8(ginv), x) and same(g8(f8(x)), -3 / (1 + 4 * x**2))
    q8 = sp.expand(f8(x) - (x**2 - 4 * x + k))
    assert same(-q8, 3 * x**2 - 4 * x + k - 3)
    assert sp.solve(sp.discriminant(-q8, x), k) == [sp.Rational(13, 3)]
    # P1 Q9
    assert sp.solve(sp.Eq(2 * 2 * (8 - 2 * k), (4 * k - 5) + (k - 2)), k) == [3]
    terms = [2**(4 * 3 - 5), 4**(8 - 2 * 3), 2**(3 - 2)]
    assert terms == [128, 16, 2] and sp.Rational(terms[0]) / (1 - sp.Rational(1, 8)) == sp.Rational(1024, 7)
    # P1 Q10
    C10 = 2 * xp - xp**sp.Rational(3, 2)
    assert C10.subs(xp, 4) == 0 and sp.diff(C10, xp).subs(xp, 4) == -1 and sp.diff(C10, xp).subs(xp, 0) == 2
    under = sp.integrate(C10, (xp, 0, 4))
    assert under == sp.Rational(16, 5) and sp.Rational(1, 2) * 4 * sp.Rational(8, 3) - under == sp.Rational(32, 15)
    # P1 Q11
    yp = sp.symbols("yp", positive=True)
    area11 = sp.integrate(6, (yp, 0, 3 * sp.sqrt(3))) + sp.integrate(2 * sp.sqrt(36 - yp**2), (yp, 3 * sp.sqrt(3), 6))
    assert same(area11, 9 * sp.sqrt(3) + 6 * sp.pi)
    # P1 Q12
    al = math.degrees(math.atan2(350, 120))
    assert math.hypot(120, 350) == 370 and round(al, 2) == 71.08
    for d in range(0, 360, 7):
        assert close(120 * math.cos(math.radians(d)) - 350 * math.sin(math.radians(d)), 370 * math.cos(math.radians(d + al)), 1e-9) or abs(370 * math.cos(math.radians(d + al))) < 1e-9
    assert 3 < (180 - al) / 30 < 4 and round(830 + 370 * math.cos(math.radians(220 + al))) == 963
    # P1 Q13
    av = 2.0
    lhs13 = float(sp.Integral(sp.sqrt(x / (av - x)), (x, 0, 0.75 * av)).evalf())
    rhs13 = float(sp.Integral(2 * av * sp.sin(theta)**2, (theta, 0, sp.pi / 3)).evalf())
    assert close(lhs13, rhs13, 1e-8) and close(lhs13, av * (math.pi / 3 - math.sqrt(3) / 4), 1e-8)
    assert same(sp.integrate(2 * a * sp.sin(theta)**2, (theta, 0, sp.pi / 3)), a * (sp.pi / 3 - sp.sqrt(3) / 4))
    # P1 Q14
    r14 = sp.sqrt(16 * t + 20)
    assert same(sp.diff(r14, t) - 8 / r14, 0) and r14.subs(t, 5) == 10 and (8 / r14).subs(t, 5) == sp.Rational(4, 5)
    assert round(float(r14.subs(t, 12)), 1) == 14.6
    # P1 Q15
    assert same(k**2 + 6 * k + 11, (k + 3)**2 + 2)
    assert not [(i, j) for i in range(1, 80) for j in range(1, 80) if (3 * i + 2 * j) * (i - 3 * j) == 20]
    for p_, q_, yv in ((10, 2, sp.Rational(4, 11)), (20, 1, sp.Rational(17, 11)), (5, 4, sp.Rational(-7, 11))):
        sol = sp.solve([3 * x + 2 * y - p_, x - 3 * y - q_], [x, y])
        assert sol[y] == yv
    assert sp.solve([3 * x + 2 * y - 10, x - 3 * y - 2], [x, y]) == {x: sp.Rational(34, 11), y: sp.Rational(4, 11)}

    # P2 Q1
    y1 = 2 * x**3 + 9 * x**2 - 4 * x + 3
    assert same(sp.diff(y1, x), 6 * x**2 + 18 * x - 4) and sp.solve(sp.diff(y1, x, 2), x) == [sp.Rational(-3, 2)]
    # P2 Q2
    S = n / 2 * (600 - 10 * (n - 1))
    assert same(sp.expand((S - 4500) * -sp.Rational(1, 5)), n**2 - 61 * n + 900)
    assert sorted(sp.solve(n**2 - 61 * n + 900, n)) == [25, 36] and 300 - 10 * 11 == 190 and 300 - 10 * 35 < 0
    # P2 Q3
    f3b = lambda v: v**2 - 10
    assert f3b(-4) == 6 and f3b(-7 + 3) == 6 and f3b(-8 / 2) == 6 and -2 * f3b(-4) + 1 == -11
    # P2 Q4
    assert same(sp.expand(k * (9 * k - 6) - 6 - 2), 9 * k**2 - 6 * k - 8)
    kk = sp.Rational(4, 3)
    us = [sp.Integer(9)]
    for _ in range(3):
        us.append(kk * us[-1] - 6)
    assert us == [9, 6, 2, sp.Rational(-10, 3)] and sum(us) == sp.Rational(41, 3)
    # P2 Q5
    assert sp.limit(3 * theta * sp.sin(2 * theta) / (1 - sp.cos(4 * theta)), theta, 0) == sp.Rational(3, 4)
    # P2 Q6
    assert same(sp.diff(sp.exp(2 * x**2 - 3), x), 4 * x * sp.exp(2 * x**2 - 3))
    xs = [1.0]
    for _ in range(80):
        xs.append(math.sqrt(1.5 - math.log(xs[-1])))
    assert round(xs[1], 4) == 1.2247 and round(xs[-1], 4) == 1.1619
    al6 = xs[-1]
    assert close(4 * al6 * math.exp(2 * al6**2 - 3), 4 / al6, 1e-9)
    # P2 Q7
    A7, B7 = sp.Matrix([1, 4, -2]), sp.Matrix([3, -2, 2])
    assert B7 - A7 == sp.Matrix([2, -6, 4])
    for lam, pos in ((sp.Rational(3, 2), [4, -5, 4]), (sp.Rational(3, 4), [sp.Rational(5, 2), sp.Rational(-1, 2), 1])):
        P = A7 + lam * (B7 - A7)
        assert list(P) == pos and same((P - A7).norm(), 3 * (P - B7).norm())
    # P2 Q8
    lhs8 = 1 / (sp.sec(theta) - 1) + 1 / (sp.sec(theta) + 1)
    assert identity(lhs8 - 2 * sp.cot(theta) * sp.csc(theta), theta, 0.1, 1.4)
    sols8 = [math.degrees(math.atan(math.sqrt(2 / 3))) / 2, (180 - math.degrees(math.atan(math.sqrt(2 / 3)))) / 2]
    assert [round(s_, 1) for s_ in sols8] == [19.6, 70.4]
    for s_ in sols8:
        r_ = math.radians(2 * s_)
        lhs = 1 / (1 / math.cos(r_) - 1) + 1 / (1 / math.cos(r_) + 1)
        assert close(lhs, 3 * math.tan(r_) / math.sin(r_), 1e-9)
    # P2 Q9
    H9 = lambda v: 3.3125 - 0.0125 * (v - 11)**2
    assert close(H9(0), 1.8) and close(H9(24), 1.2) and close(H9(20), 2.3)
    assert same(sp.expand(sp.Rational(53, 16) - sp.Rational(1, 80) * (x - 11)**2), -sp.Rational(1, 80) * x**2 + sp.Rational(11, 40) * x + sp.Rational(9, 5))
    # P2 Q10
    X10, Y10 = (t + 2)**2, 2 - t**3
    assert X10.subs(t, -1) == 1 and Y10.subs(t, -1) == 3
    grad = (sp.diff(Y10, t) / sp.diff(X10, t)).subs(t, -1)
    assert grad == sp.Rational(-3, 2) and same(sp.expand(2 * (y - 3 - grad * (x - 1))), 3 * x + 2 * y - 9)
    assert max(float(Y10.subs(t, -1.5 + i / 100)) for i in range(0, 251)) == 5.375
    # P2 Q11
    assert same(sp.integrate(9 * x**2 * sp.exp(-2 * x), (x, 0, 1)), sp.Rational(9, 4) - sp.Rational(45, 4) * sp.exp(-2))
    # P2 Q12
    Vv = sp.symbols("Vv")
    assert same(1 / (Vv * (30 - Vv)), 1 / (30 * Vv) + 1 / (30 * (30 - Vv)))
    V12 = 15 / (sp.Rational(1, 2) + sp.exp(-2 * t))
    assert V12.subs(t, 0) == 10 and same(sp.diff(V12, t) - V12 * (30 - V12) / 15, 0)
    assert same(V12.subs(t, sp.log(2)), 20) and round(math.log(2) * 60, 1) == 41.6 and sp.limit(V12, t, sp.oo) == 30
    # P2 Q13
    assert round(10**1.3, 3) == 19.953 and round(10**0.12, 3) == 1.318 and round(10**3.1, -1) == 1260
    # P2 Q14
    assert same(x**2 + y**2 + 4 * x - 10 * y + 20, (x + 2)**2 + (y - 5)**2 - 9)
    d14 = math.hypot(6, 4)
    assert close(d14, 2 * math.sqrt(13))
    for kv in (d14 - 2.9, 5, d14 + 2.9):
        assert abs(kv - 3) < d14 < kv + 3
    for kv in (d14 - 3.1, d14 + 3.1, 1):
        assert not (abs(kv - 3) < d14 < kv + 3)
    # P2 Q15
    F15 = (x + y)**3 - 2 * x**2 + y + 1
    assert F15.subs({x: 1, y: 0}) == 0
    dydx = -sp.diff(F15, x) / sp.diff(F15, y)
    assert same(dydx, (4 * x - 3 * (x + y)**2) / (3 * (x + y)**2 + 1)) and dydx.subs({x: 1, y: 0}) == sp.Rational(1, 4)
    cub = sp.expand(-F15.subs(y, 4 - 4 * x))
    assert same(cub, 27 * x**3 - 106 * x**2 + 148 * x - 69) and same(cub, (x - 1) * (27 * x**2 - 79 * x + 69))
    assert 79**2 - 4 * 27 * 69 == -1211 and [r_ for r_ in sp.solve(cub, x) if r_.is_real] == [1]
