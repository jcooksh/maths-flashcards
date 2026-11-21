"""June 2025 (9MA0/01 and 9MA0/02), with the numbers changed."""
import math
import sympy as sp
from common import card, close, same, identity, x, y, t, k, theta, u

SERIES = {"id": "paper-2025-06", "title": "June 2025", "hue": 280}

CARDS = [
    # ---------------- Paper 1 ----------------
    card(1, 1,
         [r"The point $P(-3,-5)$ lies on the curve $y=f(x)$. Find the point that $P$ maps to when the curve is transformed to:",
          r"(a) $y=f(x-4)$",
          r"(b) $y=f^{-1}(x)$",
          r"(c) $y=3|f(x)|-7$"],
         [r"Spot: $f^{-1}$ is a reflection in $y=x$, so swap the coordinates. $|f(x)|$ makes a negative $y$ positive before anything else happens to it.",
          r"Use: $f(x-4)$ moves right 4. For $3|f(x)|-7$, take the modulus of $y$, multiply by 3, then subtract 7.",
          r"(a) $(1,-5)$",
          r"(b) $(-5,-3)$",
          r"(c) $3\times5-7=8$, so $(-3,8)$"],
         [r"Make $y$ positive, multiply by 3, then subtract 7",
          r"Multiply $-5$ by 3, then subtract 7",
          r"Subtract 7, then take the modulus",
          r"Change $x$ to 3 as well"],
         ask="How do you find the point in (c)?"),
    card(1, 2,
         [r"The circle $C$ has equation $(x-5)^2+(y+2)^2=28$.",
          r"(a)(i) State the coordinates of the centre of $C$. (ii) Find the radius of $C$ as a fully simplified surd.",
          r"(b) Determine, giving a reason, whether the origin lies inside $C$."],
         [r"Spot: compare the distance from the centre to the origin with the radius. Comparing the squares, 29 and 28, avoids surds.",
          r"Use: $(x-a)^2+(y-b)^2=r^2$ has centre $(a,b)$ and radius $r$.",
          r"(a)(i) $(5,-2)$ (ii) $\sqrt{28}=2\sqrt7$",
          r"(b) The centre is $\sqrt{5^2+2^2}=\sqrt{29}$ from $O$. $\sqrt{29}>\sqrt{28}$, so the origin is outside $C$."],
         [r"Compare the distance from the centre to $O$ with the radius",
          r"Substitute $(0,0)$ and check whether you get 0",
          r"Check whether the centre is in the first quadrant",
          r"Compare $5+2$ with 28"],
         ask="How do you start part (b)?"),
    card(1, 3,
         [r"The first three terms of an arithmetic sequence are $5k$, 14 and $k+4$, where $k$ is a constant.",
          r"(a) Find the value of $k$.",
          r"(b) Hence find the sum of the first 50 terms."],
         [r"Spot: in an arithmetic sequence the differences are equal: $u_2-u_1=u_3-u_2$.",
          r"Use: $S_n=\dfrac n2\left[2a+(n-1)d\right]$.",
          r"(a) $14-5k=(k+4)-14\Rightarrow24=6k\Rightarrow k=4$",
          r"(b) The terms are $20,14,8$, so $a=20$ and $d=-6$. $S_{50}=25\left[40+49(-6)\right]=-6350$"],
         [r"Use $14-5k=(k+4)-14$",
          r"Use $14^2=5k(k+4)$",
          r"Use $5k+14+(k+4)=0$",
          r"Use $\frac{14}{5k}=\frac{k+4}{14}$"],
         ask="How do you start part (a)?"),
    card(1, 4,
         [r"$f(x)=3x^3+7x^2-2x+12$ and $f(-3)=0$.",
          r"(a) Write $f(x)$ in the form $(x+a)Q(x)$, where $a$ is a constant and $Q(x)$ is a quadratic.",
          r"(b) Hence prove that $-3$ is the only real root of $f(x)=0$."],
         [r"Spot: $f(-3)=0$ means $(x+3)$ is a factor. Divide it out, and then the quadratic factor decides whether there are any more roots.",
          r"Use: algebraic division or comparing coefficients, then $b^2-4ac$.",
          r"(a) $f(x)=(x+3)(3x^2-2x+4)$",
          r"(b) For $3x^2-2x+4$, $b^2-4ac=4-48=-44<0$, so it has no real roots. The only real root is $x=-3$."],
         [r"Divide by $(x+3)$, then show the quadratic has $b^2-4ac<0$",
          r"Divide by $(x-3)$",
          r"Show that $f(3)\ne0$",
          r"Use $b^2-4ac$ on the cubic"]),
    card(1, 5,
         [r"(a) Express $\displaystyle\lim_{\delta x\to0}\sum_{x=2.25}^{6.25}\frac{3}{\sqrt x}\,\delta x$ as an integral.",
          r"(b) Hence show that this limit equals $k$, where $k$ is an integer to be found."],
         [r"Spot: the limit of a sum of $f(x)\,\delta x$ is the definite integral of $f(x)$ between the same limits.",
          r"Use: $\dfrac{3}{\sqrt x}=3x^{-\frac12}$, which integrates to $6x^{\frac12}$.",
          r"(a) $\displaystyle\int_{2.25}^{6.25}\frac{3}{\sqrt x}\,dx$",
          r"(b) $\left[6\sqrt x\right]_{2.25}^{6.25}=6(2.5)-6(1.5)=6$, so $k=6$"],
         [r"Recognise it as $\displaystyle\int_{2.25}^{6.25}\frac{3}{\sqrt x}\,dx$",
          r"Add up $\frac{3}{\sqrt x}$ for $x=2.25,\dots,6.25$",
          r"Differentiate $\frac{3}{\sqrt x}$",
          r"Use the trapezium rule"]),
    card(1, 6,
         [r"A sea bird dives from its nest on a cliff. Its height above the sea, $h$ m, $t$ seconds after leaving the nest is modelled by $h=A-Bt^{1.5}$, $h\ge0$, $0\le t\le T$, where $A$, $B$ and $T$ are positive constants.",
          r"The bird is 26.8 m above the sea after 4 seconds, and 19.2 m above the sea after 9 seconds.",
          r"(a) Find a complete equation for the model.",
          r"Find, according to the model, (b) the height of the nest above the sea (c) the limitation on the value of $T$."],
         [r"Spot: two data points and two unknowns: substitute both and solve them simultaneously. $4^{1.5}=8$ and $9^{1.5}=27$.",
          r"Use: $26.8=A-8B$ and $19.2=A-27B$.",
          r"(a) $19B=7.6\Rightarrow B=0.4$ and $A=30$, so $h=30-0.4t^{1.5}$",
          r"(b) At $t=0$, $h=30$ m.",
          r"(c) $h\ge0\Rightarrow t^{1.5}\le75\Rightarrow t\le75^{\frac23}\approx17.8$, so $T\le17.8$"],
         [r"Substitute both points to get $26.8=A-8B$ and $19.2=A-27B$",
          r"Use $26.8=A-4B$",
          r"Assume $A=0$",
          r"Use $4^{1.5}=6$"],
         ask="How do you start part (a)?"),
    card(1, 7,
         [r"A curve $C$ has equation $y=f(x)$, where $f(x)$ is a quartic. $C$ has maximum points at $(-2,0)$ and $(4,0)$, crosses the $y$-axis at $(0,-32)$, and has a minimum point where $x=1$.",
          r"(a) Find the set of values of $x$ for which $f'(x)\ge0$, in set notation.",
          r"(b) Find the equation of $C$. You may leave it in factorised form.",
          r"The curve $C_1$ has equation $y=f(x)+k$, where $k$ is a constant, and meets the $x$-axis at exactly four points. (c) Find the range of values of $k$."],
         [r"Spot: a maximum on the $x$-axis is a repeated root, so $(x+2)$ and $(x-4)$ are both squared. Two maxima mean the quartic is negative.",
          r"Use: $f(x)=a(x+2)^2(x-4)^2$, then the $y$-intercept gives $a$.",
          r"(a) It's increasing up to each maximum: $\{x:x\le-2\}\cup\{x:1\le x\le4\}$",
          r"(b) $f(0)=64a=-32\Rightarrow a=-\tfrac12$, so $y=-\tfrac12(x+2)^2(x-4)^2$",
          r"(c) The minimum is $f(1)=-\tfrac12(9)(9)=-40.5$. Shifting up by $k$ gives four roots when $0<k<40.5$."],
         [r"Use $f(x)=a(x+2)^2(x-4)^2$, then the $y$-intercept",
          r"Use $f(x)=a(x+2)(x-4)$",
          r"Use $f(x)=a(x+2)(x-1)(x-4)$",
          r"Use $f(x)=(x+2)^2(x-4)^2$"],
         ask="How do you start part (b)?"),
    card(1, 8,
         [r"A student was asked to prove that the cube of any integer can be written as $9n$ or $9n\pm1$, where $n$ is an integer. Their proof starts:",
          r"Let $m=3k$: $m^3=27k^3=9(3k^3)=9n$.",
          r"Let $m=3k+1$: $m^3=27k^3+9k^2+9k+1=9(3k^3+k^2+k)+1=9n+1$.",
          r"(a) Identify and correct the algebraic error. (b) Complete the proof."],
         [r"Spot: proof by exhaustion. Every integer is $3k$, $3k+1$ or $3k+2$, so check each case.",
          r"Use: $(a+b)^3=a^3+3a^2b+3ab^2+b^3$.",
          r"(a) $(3k+1)^3=27k^3+27k^2+9k+1$, so it should be $9(3k^3+3k^2+k)+1$.",
          r"(b) Let $m=3k+2$: $m^3=27k^3+54k^2+36k+8=9(3k^3+6k^2+4k+1)-1=9n-1$.",
          r"Every integer is $3k$, $3k+1$ or $3k+2$, so every cube is $9n$ or $9n\pm1$."],
         [r"Check the remaining case $m=3k+2$, writing $m^3$ as $9n-1$",
          r"Check $m=1$, 2 and 3",
          r"Check $m=9k$",
          r"Assume $m^3=9n+2$"],
         ask="How do you complete part (b)?"),
    card(1, 9,
         [r"A car's speed is modelled by $v=12t-te^{0.25t}$, $0\le t\le T$, where $t$ seconds is the time after it starts from rest, and it stops at time $T$.",
          r"(a) Find $T$ to 1 d.p.",
          r"(b) Show that the maximum speed occurs when $t=4\ln\left(\dfrac{48}{t+4}\right)$.",
          r"(c) Using $t_{n+1}=4\ln\left(\dfrac{48}{t_n+4}\right)$ with $t_1=5$, find (i) $t_3$ to 3 d.p. (ii) the time to reach maximum speed, by repeated iteration."],
         [r"Spot: the car stops when $v=0$ with $t>0$. The maximum speed is where $\dfrac{dv}{dt}=0$, and $te^{0.25t}$ needs the product rule.",
          r"Use: $\dfrac{dv}{dt}=12-e^{0.25t}-0.25te^{0.25t}$.",
          r"(a) $t(12-e^{0.25t})=0\Rightarrow e^{0.25T}=12\Rightarrow T=4\ln12\approx9.9$",
          r"(b) $e^{0.25t}(1+0.25t)=12\Rightarrow e^{0.25t}=\dfrac{48}{t+4}$, then take logs.",
          r"(c)(i) $t_2=6.696$ and $t_3=6.005$ (ii) The iterates converge to $t\approx6.197$ s."],
         [r"Use the product rule on $te^{0.25t}$ and set $\frac{dv}{dt}=0$",
          r"Set $v=0$",
          r"Differentiate $te^{0.25t}$ as $0.25e^{0.25t}$",
          r"Integrate $v$"],
         ask="How do you start part (b)?"),
    card(1, 10,
         [r"$\overrightarrow{PQ}=2\mathbf{i}+3\mathbf{j}+6\mathbf{k}$ and $\overrightarrow{QR}=6\mathbf{i}+2\mathbf{j}-3\mathbf{k}$.",
          r"(a) Find $\overrightarrow{PR}$.",
          r"(b) Hence show that triangle $PQR$ is both right-angled and isosceles."],
         [r"Spot: $\overrightarrow{PR}=\overrightarrow{PQ}+\overrightarrow{QR}$. Then compare the three side lengths: two equal sides make it isosceles, and Pythagoras shows the right angle.",
          r"Use: $|a\mathbf{i}+b\mathbf{j}+c\mathbf{k}|=\sqrt{a^2+b^2+c^2}$.",
          r"(a) $8\mathbf{i}+5\mathbf{j}+3\mathbf{k}$",
          r"(b) $PQ=\sqrt{49}=7$, $QR=\sqrt{49}=7$ and $PR=\sqrt{98}$. $7^2+7^2=98$, so there's a right angle at $Q$, and $PQ=QR$ makes it isosceles."],
         [r"Add $\overrightarrow{PQ}+\overrightarrow{QR}$, then compare the three lengths",
          r"Use $\overrightarrow{PR}=\overrightarrow{QR}-\overrightarrow{PQ}$",
          r"Show $\overrightarrow{PQ}$ and $\overrightarrow{QR}$ are parallel",
          r"Show $\overrightarrow{PQ}\cdot\overrightarrow{PR}=0$"]),
    card(1, 11,
         [r"The value of a car, £$V$, is modelled by $V=2000+Ae^{-kt}$, where $A$ and $k$ are positive constants and $t$ is the car's age in years.",
          r"The car was worth £26 000 when new and £14 000 when it was 3 years old.",
          r"(a) Find a complete equation for the model, giving $A$ exactly and $k$ to 3 s.f.",
          r"(b) Show that the rate of change of the value can be written as $-k(V-2000)$.",
          r"(c) State a limitation of this model."],
         [r"Spot: “when new” means $t=0$, and $e^0=1$ gives $A$. The second value gives $k$ once you take logs.",
          r"Use: $\dfrac{d}{dt}Ae^{-kt}=-kAe^{-kt}$, and $Ae^{-kt}=V-2000$.",
          r"(a) $26000=2000+A\Rightarrow A=24000$. $14000=2000+24000e^{-3k}\Rightarrow e^{-3k}=\tfrac12\Rightarrow k=\tfrac13\ln2\approx0.231$",
          r"(b) $\dfrac{dV}{dt}=-24000ke^{-kt}=-k(V-2000)$",
          r"(c) It says the car is always worth more than £2000, however old it is."],
         [r"Use $t=0$ to find $A$, then $t=3$ and logs to find $k$",
          r"Use $26000=Ae^{-k}$",
          r"Use $A=26000$",
          r"Take logs of $2000+Ae^{-kt}$ term by term"],
         ask="How do you start part (a)?"),
    card(1, 12,
         [r"The curve $C$ has equation $y=\dfrac{10x}{(x+2)(2x-3)}$, $x\ne-2$, $x\ne\tfrac32$, and the line $l$ has equation $y=2x-4$.",
          r"(a) Verify that $C$ and $l$ intersect where $x=3$.",
          r"$C$ and $l$ also intersect at the point $Q$, where $0<x<\tfrac32$.",
          r"(b) Show that the $x$-coordinate of $Q$ is a solution of $2x^3-3x^2-13x+12=0$.",
          r"(c) Using algebra, find the exact $x$-coordinate of $Q$."],
         [r"Spot: you already know one intersection, $x=3$, so $(x-3)$ is a factor of the cubic. Divide it out and solve the quadratic.",
          r"Use: set the curve equal to the line, then multiply out the denominators.",
          r"(a) $C$ gives $\dfrac{30}{5\times3}=2$, and $l$ gives $6-4=2$.",
          r"(b) $10x=(2x-4)(x+2)(2x-3)\Rightarrow4x^3-6x^2-26x+24=0$, then divide by 2.",
          r"(c) $(x-3)(2x^2+3x-4)=0\Rightarrow x=\dfrac{-3\pm\sqrt{41}}{4}$. $Q$ has $0<x<\tfrac32$, so $x=\dfrac{-3+\sqrt{41}}{4}$."],
         [r"Divide the cubic by $(x-3)$, then solve the quadratic",
          r"Divide the cubic by $(x+3)$",
          r"Use the quadratic formula on the cubic",
          r"Use Newton–Raphson"],
         ask="How do you start part (c)?"),
    card(1, 13,
         [r"Show that $\displaystyle\int_0^1\frac{x}{(3x+1)^3}\,dx=\frac{1}{32}$."],
         [r"Spot: $x$ over a power of a linear bracket: substitute $u=3x+1$. That splits it into simple powers of $u$.",
          r"Use: $x=\dfrac{u-1}{3}$ and $dx=\dfrac{du}{3}$. The limits become $u=1$ and $u=4$.",
          r"Method: $\displaystyle\frac19\int_1^4\left(u^{-2}-u^{-3}\right)du=\frac19\left[-\frac1u+\frac{1}{2u^2}\right]_1^4$",
          r"$=\dfrac19\left(-\dfrac{7}{32}+\dfrac12\right)=\dfrac19\times\dfrac{9}{32}=\dfrac{1}{32}$"],
         [r"Substitute $u=3x+1$ and change the limits",
          r"Integrate the top and bottom separately",
          r"Integrate it to $\ln(3x+1)$",
          r"Substitute $u=x^2$"]),
    card(1, 14,
         [r"(a) Show that $\sqrt3\sin(x+60^\circ)+\cos(x+60^\circ)\equiv2\cos x$.",
          r"(b) Hence solve, for $0\le\theta<360^\circ$, $\sqrt3\sin(\theta+60^\circ)+\cos(\theta+60^\circ)=5\sin2\theta$, giving answers to 1 d.p. where appropriate."],
         [r"Spot: expand both compound angles with exact values. In (b), replace the left side with $2\cos\theta$, use $\sin2\theta=2\sin\theta\cos\theta$, and factorise. Don't divide by $\cos\theta$.",
          r"Use: $\sin(A+B)$ and $\cos(A+B)$, with $\sin60^\circ=\tfrac{\sqrt3}{2}$ and $\cos60^\circ=\tfrac12$.",
          r"(a) $\tfrac{\sqrt3}{2}\sin x+\tfrac32\cos x+\tfrac12\cos x-\tfrac{\sqrt3}{2}\sin x=2\cos x$",
          r"(b) $2\cos\theta=10\sin\theta\cos\theta\Rightarrow2\cos\theta(1-5\sin\theta)=0$",
          r"Answer: $\theta=11.5^\circ,\ 90^\circ,\ 168.5^\circ,\ 270^\circ$"],
         [r"Replace the left side with $2\cos\theta$, then factorise out $\cos\theta$",
          r"Divide both sides by $\cos\theta$",
          r"Use $\sin2\theta=2\sin\theta$",
          r"Square both sides"],
         ask="How do you start part (b)?"),
    card(1, 15,
         [r"The plan of a stage is a sector $AOB$ of a circle, with radius $r$ m and angle $\theta$ radians, joined along $OB$ to a rectangle $OBCD$ measuring $r$ m by $\tfrac14r$ m. The total area is $200\text{ m}^2$.",
          r"(a) Show that the perimeter of the stage is $P=2r+\dfrac{400}{r}$.",
          r"(b) Using algebraic differentiation, find the value of $r$ for which $P$ is stationary.",
          r"(c) Prove, by further differentiation, that this gives the minimum perimeter."],
         [r"Spot: there are two unknowns, $r$ and $\theta$. Use the area to write $r\theta$ in terms of $r$, then substitute into the perimeter.",
          r"Use: sector area $=\tfrac12r^2\theta$ and arc $=r\theta$. The perimeter is the arc, $OA$, $DC$ and the two short sides.",
          r"(a) $\tfrac12r^2\theta+\tfrac14r^2=200\Rightarrow r\theta=\dfrac{400}{r}-\dfrac r2$, so $P=r\theta+2r+\tfrac12r=2r+\dfrac{400}{r}$",
          r"(b) $\dfrac{dP}{dr}=2-\dfrac{400}{r^2}=0\Rightarrow r=\sqrt{200}=10\sqrt2\approx14.1$",
          r"(c) $\dfrac{d^2P}{dr^2}=\dfrac{800}{r^3}>0$, so it's a minimum."],
         [r"Use the area to write $r\theta$ in terms of $r$, then substitute into the perimeter",
          r"Set $\theta=\frac{\pi}{2}$",
          r"Include $OB$ in the perimeter",
          r"Use the sector area $\pi r^2\theta$"],
         ask="How do you start part (a)?"),
    card(1, 16,
         [r"The curve $C$ has equation $y=\dfrac{1}{x^2\sqrt{9-x^2}}$, $0<x<3$. The region $R$ is bounded by $C$, the $x$-axis and the lines $x=\tfrac32$ and $x=\tfrac{3\sqrt3}{2}$.",
          r"(a) Use the substitution $x=3\sin u$ to show that the area of $R$ is $\displaystyle\int_a^bk\cosec^2u\,du$, where $a$, $b$ and $k$ are constants.",
          r"(b) Hence find the exact area of $R$ in its simplest form."],
         [r"Spot: with $x=3\sin u$, $\sqrt{9-x^2}$ becomes $3\cos u$, because $1-\sin^2u=\cos^2u$. Change $dx$ and the limits too.",
          r"Use: $dx=3\cos u\,du$ and $\displaystyle\int\cosec^2u\,du=-\cot u+c$.",
          r"(a) $\dfrac{3\cos u}{9\sin^2u\times3\cos u}=\dfrac19\cosec^2u$, with $u$ from $\dfrac{\pi}{6}$ to $\dfrac{\pi}{3}$",
          r"(b) $\dfrac19\left[-\cot u\right]_{\frac{\pi}{6}}^{\frac{\pi}{3}}=\dfrac19\left(\sqrt3-\dfrac{1}{\sqrt3}\right)=\dfrac{2\sqrt3}{27}$"],
         [r"Use $\sqrt{9-9\sin^2u}=3\cos u$ and $dx=3\cos u\,du$",
          r"Use $dx=3\,du$",
          r"Keep the $x$ limits",
          r"Use $\sqrt{9-9\sin^2u}=3\sin u$"],
         ask="How do you start part (a)?"),

    # ---------------- Paper 2 ----------------
    card(2, 1,
         [r"Factorise completely $3x^3-21x^2+30x$."],
         [r"Spot: every term has a common factor of $3x$. Take that out first, then factorise the quadratic that's left.",
          r"Use: two numbers that multiply to 10 and add to $-7$.",
          r"Method: $3x(x^2-7x+10)$",
          r"Answer: $3x(x-2)(x-5)$"],
         [r"Take out $3x$, then factorise the quadratic",
          r"Use the quadratic formula on the cubic",
          r"Take out $x$ and stop",
          r"Divide by $x$ and solve"]),
    card(2, 2,
         [r"Find $\displaystyle\int\left(x^3-\frac{8x}{\sqrt x}+2\right)dx$, giving the answer in its simplest form."],
         [r"Spot: simplify each term to a single power of $x$ first: $\dfrac{8x}{\sqrt x}=8x^{\frac12}$.",
          r"Use: $\displaystyle\int x^n\,dx=\frac{x^{n+1}}{n+1}+c$.",
          r"Method: $\displaystyle\int\left(x^3-8x^{\frac12}+2\right)dx$",
          r"Answer: $\dfrac14x^4-\dfrac{16}{3}x^{\frac32}+2x+c$"],
         [r"Write $\frac{8x}{\sqrt x}$ as $8x^{\frac12}$, then integrate term by term",
          r"Integrate $8x$ and $\sqrt x$ separately, then divide",
          r"Write $\frac{8x}{\sqrt x}$ as $8x^{-\frac12}$",
          r"Differentiate each term"]),
    card(2, 3,
         [r"Given that $5^x=2^{3y}$, find the exact value of $\dfrac xy$."],
         [r"Spot: the unknowns are in the powers, so take logs of both sides to bring them down.",
          r"Use: $\ln a^n=n\ln a$.",
          r"Method: $x\ln5=3y\ln2$",
          r"Answer: $\dfrac xy=\dfrac{3\ln2}{\ln5}=\dfrac{\ln8}{\ln5}$"],
         [r"Take $\ln$ of both sides, so $x\ln5=3y\ln2$",
          r"Divide both sides by 5",
          r"Use $\frac xy=\frac{2\times3}{5}$",
          r"Set $x=3y$"]),
    card(2, 4,
         [r"Triangle $ABD$ has $AD=5$ cm, $BD=11$ cm and $BA=9$ cm. It contains a sector $ABC$ of a circle with centre $B$ and radius 9 cm, where $C$ lies on $BD$.",
          r"(a) Show that angle $ABC=0.465$ radians to 3 s.f.",
          r"The region $R$ is bounded by the line $CD$, the line $DA$ and the arc $AC$.",
          r"(b) Find the area of $R$ to 3 s.f."],
         [r"Spot: three sides of a triangle and you want an angle: cosine rule. $R$ is the whole triangle minus the sector.",
          r"Use: $\cos B=\dfrac{a^2+d^2-b^2}{2ad}$, triangle $=\tfrac12ab\sin C$, sector $=\tfrac12r^2\theta$.",
          r"(a) $\cos B=\dfrac{81+121-25}{2(9)(11)}=\dfrac{177}{198}\Rightarrow B\approx0.465$",
          r"(b) $\tfrac12(9)(11)\sin B-\tfrac12(81)B\approx22.19-18.82\approx3.36\text{ cm}^2$"],
         [r"Use triangle $ABD$ minus sector $ABC$",
          r"Use the sector minus the triangle",
          r"Use the sector with radius 11",
          r"Treat the triangle as right-angled"],
         ask="How do you start part (b)?"),
    card(2, 5,
         [r"The curve $C$ has parametric equations $x=\dfrac{t+3}{3}$, $y=2(t-1)^3$, $t\in\mathbb{R}$. The point $P$ on $C$ has $x$-coordinate $-1$.",
          r"(a) Find the $y$-coordinate of $P$.",
          r"(b) Find a Cartesian equation for $C$ in the form $y=f(x)$.",
          r"(c) Hence, or otherwise, find the gradient of $C$ at $P$."],
         [r"Spot: $x$ is linear in $t$, so make $t$ the subject and substitute it into $y$.",
          r"Use: $t=3x-3$, then the chain rule on $(3x-4)^3$.",
          r"(a) $t=-6$, so $y=2(-7)^3=-686$",
          r"(b) $y=2(3x-4)^3$",
          r"(c) $\dfrac{dy}{dx}=18(3x-4)^2$, which is $18(49)=882$ at $x=-1$"],
         [r"Make $t$ the subject of the $x$ equation and substitute it into $y$",
          r"Set $t=-1$",
          r"Make $t$ the subject of the $y$ equation and stop",
          r"Differentiate $y$ with respect to $t$ only"],
         ask="How do you start part (b)?"),
    card(2, 6,
         [r"(a) Given that $x$ is small and in radians, use the small angle approximation for $\cos\theta$ to show that $1-\cos^2(3x)\approx9x^2-\dfrac{81}{4}x^4$.",
          r"(b) Using (a) and the small angle approximations for $\sin\theta$ and $\tan\theta$, show that $\dfrac{1-\cos^2(3x)}{\sin\left(\frac x2\right)\tan3x}\approx a+bx^2$, where $a$ and $b$ are constants.",
          r"(c) Hence, for very small $x$, deduce an approximate value of this expression, giving a reason."],
         [r"Spot: replace each trig function with its small angle approximation, square carefully, and keep the terms up to $x^4$.",
          r"Use: $\cos\theta\approx1-\dfrac{\theta^2}{2}$, $\sin\theta\approx\theta$ and $\tan\theta\approx\theta$.",
          r"(a) $\cos3x\approx1-\dfrac{9x^2}{2}$, so $\cos^23x\approx1-9x^2+\dfrac{81}{4}x^4$",
          r"(b) $\dfrac{9x^2-\frac{81}{4}x^4}{\frac x2\times3x}=\dfrac{9x^2-\frac{81}{4}x^4}{\frac32x^2}=6-\dfrac{27}{2}x^2$",
          r"(c) About 6, because the $x^2$ term is negligible when $x$ is very small."],
         [r"Divide the answer to (a) by $\frac x2\times3x=\frac32x^2$",
          r"Use $\tan3x\approx1-\frac{9x^2}{2}$",
          r"Use $\sin\frac x2\approx\frac{x^2}{2}$",
          r"Divide the answer to (a) by $x$"],
         ask="How do you start part (b)?"),
    card(2, 7,
         [r"Given that $\dfrac{2x^3+x^2-6x-11}{(x-2)(x+1)}\equiv Ax+B+\dfrac{C}{x-2}+\dfrac{D}{x+1}$, for $x\ne2$ and $x\ne-1$, find the values of $A$, $B$, $C$ and $D$."],
         [r"Spot: the top has a higher degree than the bottom, so there's a polynomial part $Ax+B$ as well as the partial fractions.",
          r"Use: $2x^3+x^2-6x-11\equiv(Ax+B)(x-2)(x+1)+C(x+1)+D(x-2)$. Substitute $x=2$ and $x=-1$, then compare coefficients.",
          r"$x=2$: $-3=3C\Rightarrow C=-1$. $x=-1$: $-6=-3D\Rightarrow D=2$.",
          r"Comparing $x^3$: $A=2$. Comparing constants: $-11=-2B+C-2D\Rightarrow B=3$.",
          r"Answer: $A=2$, $B=3$, $C=-1$, $D=2$"],
         [r"Multiply through by $(x-2)(x+1)$, then substitute $x=2$ and $x=-1$ and compare coefficients",
          r"Use $\frac{C}{x-2}+\frac{D}{x+1}$ only, with no $Ax+B$",
          r"Substitute $x=0$ only",
          r"Divide the denominator by the numerator"]),
    card(2, 8,
         [r"$f(x)=x^4-\tfrac23x^3-8x^2+ax+\tfrac{16}{3}$, where $a$ is a constant. The curve $y=f(x)$ has a local maximum at $x=\tfrac12$.",
          r"(a) Show that $a=8$. (b) Find the exact $y$-coordinate of the local maximum.",
          r"The equation $f(x)=k$, where $k$ is a constant, has 4 distinct solutions.",
          r"(c) Using algebra, find the range of values of $k$, in set notation."],
         [r"Spot: a local maximum means $f'\left(\tfrac12\right)=0$. Four solutions of $f(x)=k$ means the line $y=k$ cuts both dips of the W shape: above the higher minimum and below the maximum.",
          r"Use: $f'(x)=4x^3-2x^2-16x+a$. With $a=8$, it factorises as $(4x-2)(x^2-4)$.",
          r"(a) $f'\left(\tfrac12\right)=\tfrac12-\tfrac12-8+a=0\Rightarrow a=8$",
          r"(b) $f\left(\tfrac12\right)=\dfrac{117}{16}$",
          r"(c) The minima are at $x=\pm2$: $f(2)=0$ and $f(-2)=-\tfrac{64}{3}$. So $\left\{k:0<k<\tfrac{117}{16}\right\}$"],
         [r"Find both minima, then take $k$ between the higher minimum and the maximum",
          r"Take $k$ between the lower minimum and the maximum",
          r"Use $b^2-4ac>0$",
          r"Take $k>\frac{117}{16}$"],
         ask="How do you start part (c)?"),
    card(2, 9,
         [r"The total number of a new phone model sold in a region, $N$, $t$ months after its release is modelled by $N=8000-8000e^{-0.06t}$, $t\ge0$.",
          r"(a) Find the number sold in the first 4 months.",
          r"(b) Given that $N=5000$ when $t=T$, find $T$ to 2 d.p.",
          r"(c) Find the rate at which sales are increasing when $t=4$, to 3 s.f.",
          r"After an advertising campaign, total sales are expected to have an upper limit of 10 000. (d) Suggest one refinement to the model."],
         [r"Spot: “rate of increase” means $\dfrac{dN}{dt}$. To find $T$, isolate the exponential and take logs.",
          r"Use: $\dfrac{dN}{dt}=480e^{-0.06t}$. As $t\to\infty$, $N\to8000$, which is the model's upper limit.",
          r"(a) $8000-8000e^{-0.24}\approx1707$",
          r"(b) $e^{-0.06T}=\tfrac38\Rightarrow T=\dfrac{\ln\frac83}{0.06}\approx16.35$",
          r"(c) $480e^{-0.24}\approx378$ phones per month",
          r"(d) Replace both 8000s with 10 000: $N=10000-10000e^{-0.06t}$"],
         [r"Isolate $e^{-0.06T}$, then take logs",
          r"Divide 5000 by 8000 and stop",
          r"Take logs of each term",
          r"Differentiate first"],
         ask="How do you start part (b)?"),
    card(2, 10,
         [r"Water flows into a large container at a constant 0.6 m³ per hour. A tap at the bottom lets water out at $0.25V$ m³ per hour, where $V$ m³ is the volume $t$ hours after the tap is opened.",
          r"(a) Show that $20\dfrac{dV}{dt}=12-5V$.",
          r"When the tap was opened, the container held 0.4 m³.",
          r"(b) Solve the differential equation to show that $V=P-Qe^{-kt}$, where $P$, $Q$ and $k$ are positive constants to be found.",
          r"The container holds 2 m³, the tap stays open and the inflow stays the same. (c) Determine whether the container will ever become full, giving a reason."],
         [r"Spot: rate of change = rate in − rate out. Then separate the variables: the $V$ side integrates to a log.",
          r"Use: $\displaystyle\int\frac{20}{12-5V}\,dV=-4\ln|12-5V|$.",
          r"(a) $\dfrac{dV}{dt}=0.6-0.25V$, then multiply by 20.",
          r"(b) $-4\ln|12-5V|=t+c$. $V=0.4$ at $t=0$ gives $c=-4\ln10$, so $12-5V=10e^{-0.25t}$ and $V=2.4-2e^{-0.25t}$.",
          r"(c) $V\to2.4>2$, so yes: $2.4-2e^{-0.25t}=2$ when $t=4\ln5\approx6.4$ hours."],
         [r"Use rate in minus rate out, then separate the variables",
          r"Use rate in plus rate out",
          r"Integrate $0.6-0.25V$ with respect to $t$, treating $V$ as a constant",
          r"Use $V=0.6t-0.25t$"],
         ask="How do you start part (a)?"),
    card(2, 11,
         [r"A company is pricing a new game. At £30 each it expects to sell 1800 games a year, and at £50 each it expects to sell 600.",
          r"(a) Using a linear model, find $y$, the expected number sold in a year, in terms of the price £$x$.",
          r"Each game costs £15 to make, and the company has other costs of £12 000 a year.",
          r"(b) Show that the yearly profit, $P$ thousand pounds, is $P=-0.06x^2+4.5x-66$.",
          r"(c) Find the range of prices that give a profit. (d) Deduce the price that maximises the profit.",
          r"(e) One year the game sold at £40 and the profit was £16 200. Evaluate the model."],
         [r"Spot: a linear model through two points gives $y$. Profit is (price − cost) × number sold, minus the other costs.",
          r"Use: $P=\dfrac{(x-15)y-12000}{1000}$.",
          r"(a) The gradient is $\dfrac{600-1800}{50-30}=-60$, so $y=3600-60x$.",
          r"(b) $\dfrac{(x-15)(3600-60x)-12000}{1000}=\dfrac{-60x^2+4500x-66000}{1000}$",
          r"(c) $x^2-75x+1100<0\Rightarrow(x-20)(x-55)<0$, so $20<x<55$",
          r"(d) Halfway between the roots: £37.50",
          r"(e) The model gives $P(40)=18$, which is £18 000. That's £1800 more than the actual profit, so the model is a little optimistic."],
         [r"Use profit $=(x-15)y-12000$, then divide by 1000",
          r"Use profit $=xy-15-12000$",
          r"Use profit $=(x-15)y$",
          r"Use profit $=xy+12000$"],
         ask="How do you start part (b)?"),
    card(2, 12,
         [r"$f(x)=3|x+2|-4$, $x\in\mathbb{R}$.",
          r"(a) Given that $|a|=2$, find the possible values of $f(a)$.",
          r"$g(x)=5-2x$, $x\in\mathbb{R}$. (b) Find the range of $gf(x)$.",
          r"$h(x)=kx$, where $k$ is a constant, and the equation $f(x)=h(x)$ has no solutions.",
          r"(c) Find the range of values of $k$."],
         [r"Spot: the graph of $f$ is a V with vertex $(-2,-4)$ and arms of gradient $\pm3$. For (c), sketch it: the line through $O$ must pass below the vertex and be no steeper than the right arm.",
          r"Use: the range of $f$ is $f(x)\ge-4$. $g$ is decreasing, so it reverses the inequality.",
          r"(a) $f(2)=8$ and $f(-2)=-4$",
          r"(b) $gf(x)=5-2f(x)\le5-2(-4)=13$, so $gf(x)\le13$",
          r"(c) Below the vertex: $-2k<-4\Rightarrow k>2$. Not crossing the right arm: $k\le3$. So $2<k\le3$."],
         [r"Sketch the V and compare the line through $O$ with the vertex and the right arm",
          r"Solve $3(x+2)-4=kx$ only",
          r"Use $b^2-4ac<0$",
          r"Use $k<-3$"],
         ask="How do you start part (c)?"),
    card(2, 13,
         [r"For all values of $k$ with $0<|k|<1$, the equation $\sin(nx)=k$, $n\in\mathbb{N}$, has exactly 8 solutions in $0\le x<2\pi$.",
          r"(i) Deduce the value of $n$.",
          r"(ii) Deduce, with a reason, the number of solutions of $\sin^2(nx)=k^2$ in $0\le x<3\pi$."],
         [r"Spot: $\sin\theta=k$ has 2 solutions in every period. $\sin(nx)$ has period $\dfrac{2\pi}{n}$, so $[0,2\pi)$ holds $n$ periods.",
          r"Use: $\sin^2(nx)=k^2$ means $\sin(nx)=k$ or $\sin(nx)=-k$, which gives 4 solutions per period.",
          r"(i) $2n=8\Rightarrow n=4$",
          r"(ii) The period is $\dfrac{\pi}{2}$, so $[0,3\pi)$ holds 6 periods: $6\times4=24$ solutions."],
         [r"Count 2 solutions per period, with $n$ periods in $[0,2\pi)$",
          r"Count 1 solution per period",
          r"Use $n=8$",
          r"Use $n=2$"],
         ask="How do you start part (i)?"),
    card(2, 14,
         [r"$ABCD$ is a trapezium with $AD$ parallel to $BC$. $\overrightarrow{AB}=3\mathbf{a}+\mathbf{b}$, $\overrightarrow{BC}=12\mathbf{a}-8\mathbf{b}$ and $\overrightarrow{DB}=-6\mathbf{a}+k\mathbf{b}$, where $k$ is an integer.",
          r"(a) Show that $k=7$.",
          r"$N$ lies on $BC$ with $BN:NC=1:3$, and $AN$ meets $BD$ at $X$.",
          r"(b) Find $BX:XD$."],
         [r"Spot: parallel means $\overrightarrow{AD}$ is a multiple of $\overrightarrow{BC}$. For the intersection, write $\overrightarrow{AX}$ two ways and compare the coefficients of $\mathbf{a}$ and $\mathbf{b}$.",
          r"Use: $\overrightarrow{AD}=\overrightarrow{AB}+\overrightarrow{BD}$, $\overrightarrow{AX}=\lambda\overrightarrow{AN}$ and $\overrightarrow{AX}=\overrightarrow{AB}+\mu\overrightarrow{BD}$.",
          r"(a) $\overrightarrow{AD}=9\mathbf{a}+(1-k)\mathbf{b}$. Parallel to $12\mathbf{a}-8\mathbf{b}$ means $\dfrac{1-k}{9}=-\dfrac{8}{12}$, so $k=7$.",
          r"(b) $\overrightarrow{AN}=\overrightarrow{AB}+\tfrac14\overrightarrow{BC}=6\mathbf{a}-\mathbf{b}$. $\lambda(6\mathbf{a}-\mathbf{b})=3\mathbf{a}+\mathbf{b}+\mu(6\mathbf{a}-7\mathbf{b})$ gives $\mu=\tfrac14$.",
          r"Answer: $BX:XD=1:3$"],
         [r"Write $\overrightarrow{AX}$ two ways and compare the coefficients of $\mathbf{a}$ and $\mathbf{b}$",
          r"Assume $X$ is the midpoint of $BD$",
          r"Use $BX:XD=BN:NC$",
          r"Use the dot product"],
         ask="How do you start part (b)?"),
    card(2, 15,
         [r"$f(x)=\dfrac{4-x^2}{(4+x^2)^2}$. The curve $y=f(x)$ crosses the $x$-axis at $-2$ and 2, and has minimum points $P$ and $Q$, where $P$ has $x<0$.",
          r"(a) Use calculus to find the exact coordinates of $P$.",
          r"(b) Using the substitution $x=2\tan\theta$, show that $\displaystyle\int_{-2}^{2}f(x)\,dx=\int_\alpha^\beta\tfrac12\cos2\theta\,d\theta$, where $\alpha$ and $\beta$ are constants.",
          r"The region $R$ is bounded by the curve and the $x$-axis. (c) Use algebraic integration to find the area of $R$."],
         [r"Spot: (a) quotient rule, then take out the factor $-2x(4+x^2)$. (b) with $x=2\tan\theta$, $4+x^2$ becomes $4\sec^2\theta$.",
          r"Use: $1+\tan^2\theta=\sec^2\theta$, $dx=2\sec^2\theta\,d\theta$ and $\cos^2\theta-\sin^2\theta=\cos2\theta$.",
          r"(a) $f'(x)=\dfrac{-2x(12-x^2)}{(4+x^2)^3}=0\Rightarrow x=0$ or $x=\pm2\sqrt3$. So $P$ is $\left(-2\sqrt3,-\tfrac{1}{32}\right)$.",
          r"(b) $\dfrac{4(1-\tan^2\theta)\times2\sec^2\theta}{16\sec^4\theta}=\tfrac12(1-\tan^2\theta)\cos^2\theta=\tfrac12\cos2\theta$, with $\theta$ from $-\dfrac{\pi}{4}$ to $\dfrac{\pi}{4}$",
          r"(c) $\tfrac12\left[\tfrac12\sin2\theta\right]_{-\frac{\pi}{4}}^{\frac{\pi}{4}}=\tfrac12$"],
         [r"Substitute $x=2\tan\theta$, with $4+4\tan^2\theta=4\sec^2\theta$ and $dx=2\sec^2\theta\,d\theta$",
          r"Use $dx=2\,d\theta$",
          r"Keep the limits as $-2$ and 2",
          r"Use $4+4\tan^2\theta=4\cos^2\theta$"],
         ask="How do you start part (b)?"),
]


def check():
    a, b, n = sp.symbols("a b n")
    xp = sp.symbols("xp", positive=True)
    # P1 Q1
    f1 = lambda v: v**2 - 14  # any function through (-3, -5)
    assert f1(-3) == -5 and f1(1 - 4) == -5 and 3 * abs(f1(-3)) - 7 == 8
    # P1 Q2
    assert same(sp.sqrt(28), 2 * sp.sqrt(7)) and 5**2 + 2**2 == 29 > 28
    # P1 Q3
    assert sp.solve(sp.Eq(14 - 5 * k, (k + 4) - 14), k) == [4]
    assert sum(20 - 6 * i for i in range(50)) == -6350
    # P1 Q4
    f4 = 3 * x**3 + 7 * x**2 - 2 * x + 12
    assert f4.subs(x, -3) == 0 and same(f4, (x + 3) * (3 * x**2 - 2 * x + 4)) and (-2)**2 - 4 * 3 * 4 == -44
    # P1 Q5
    assert sp.integrate(3 / sp.sqrt(xp), (xp, sp.Rational(9, 4), sp.Rational(25, 4))) == 6
    # P1 Q6
    A6, B6 = sp.symbols("A6 B6")
    sol6 = sp.solve([A6 - 8 * B6 - sp.Rational(268, 10), A6 - 27 * B6 - sp.Rational(192, 10)], [A6, B6])
    assert sol6 == {A6: 30, B6: sp.Rational(2, 5)} and round(75**(2 / 3), 1) == 17.8
    # P1 Q7
    f7 = -sp.Rational(1, 2) * (x + 2)**2 * (x - 4)**2
    assert f7.subs(x, 0) == -32 and sorted(sp.solve(sp.diff(f7, x), x)) == [-2, 1, 4]
    assert f7.subs(x, 1) == sp.Rational(-81, 2) and sp.diff(f7, x, 2).subs(x, 1) > 0
    assert sp.solve_univariate_inequality(sp.diff(f7, x) >= 0, x, relational=False) == sp.Union(sp.Interval(-sp.oo, -2), sp.Interval(1, 4))
    # P1 Q8
    assert same((3 * k + 1)**3, 9 * (3 * k**3 + 3 * k**2 + k) + 1)
    assert same((3 * k + 2)**3, 9 * (3 * k**3 + 6 * k**2 + 4 * k + 1) - 1)
    assert all(m**3 % 9 in (0, 1, 8) for m in range(-300, 300))
    # P1 Q9
    v9 = 12 * t - t * sp.exp(t / 4)
    assert round(4 * math.log(12), 1) == 9.9 and close(float(v9.subs(t, 4 * math.log(12))), 0)
    dv = sp.diff(v9, t)
    assert identity(dv - (12 - sp.exp(t / 4) * (1 + t / 4)), t, 0.5, 9)
    ts = [5.0]
    for _ in range(100):
        ts.append(4 * math.log(48 / (ts[-1] + 4)))
    assert round(ts[1], 3) == 6.696 and round(ts[2], 3) == 6.005 and round(ts[-1], 3) == 6.197
    assert abs(float(dv.subs(t, ts[-1]))) < 1e-9
    # P1 Q10
    PQ, QR = sp.Matrix([2, 3, 6]), sp.Matrix([6, 2, -3])
    PR = PQ + QR
    assert list(PR) == [8, 5, 3] and PQ.norm() == 7 == QR.norm() and PR.norm()**2 == 98 and PQ.dot(QR) == 0
    # P1 Q11
    k11 = math.log(2) / 3
    V11 = lambda tv: 2000 + 24000 * math.exp(-k11 * tv)
    assert close(V11(0), 26000) and close(V11(3), 14000) and round(k11, 3) == 0.231
    Vs = 2000 + sp.Symbol("A", positive=True) * sp.exp(-k * t)
    assert same(sp.diff(Vs, t), -k * (Vs - 2000))
    # P1 Q12
    C12 = 10 * x / ((x + 2) * (2 * x - 3))
    assert C12.subs(x, 3) == 2 and 2 * 3 - 4 == 2
    cub = sp.expand((2 * x - 4) * (x + 2) * (2 * x - 3) - 10 * x)
    assert same(cub, 2 * (2 * x**3 - 3 * x**2 - 13 * x + 12)) and same(2 * x**3 - 3 * x**2 - 13 * x + 12, (x - 3) * (2 * x**2 + 3 * x - 4))
    xq = (-3 + sp.sqrt(41)) / 4
    assert 0 < float(xq) < 1.5 and same(C12.subs(x, xq), 2 * xq - 4)
    assert float((-3 - sp.sqrt(41)) / 4) < 0
    # P1 Q13
    assert sp.integrate(x / (3 * x + 1)**3, (x, 0, 1)) == sp.Rational(1, 32)
    # P1 Q14
    assert identity(sp.sqrt(3) * sp.sin(x + sp.pi / 3) + sp.cos(x + sp.pi / 3) - 2 * sp.cos(x), x, -3, 3)
    sols14 = [math.degrees(math.asin(0.2)), 90, 180 - math.degrees(math.asin(0.2)), 270]
    assert [round(s_, 1) for s_ in sols14] == [11.5, 90, 168.5, 270]
    for d in sols14:
        r_ = math.radians(d)
        assert abs(math.sqrt(3) * math.sin(r_ + math.pi / 3) + math.cos(r_ + math.pi / 3) - 5 * math.sin(2 * r_)) < 1e-9
    # P1 Q15
    rr = sp.symbols("rr", positive=True)
    rtheta = (200 - rr**2 / 4) / (rr / 2)
    assert same(rtheta + 2 * rr + rr / 2, 2 * rr + 400 / rr)
    P15 = 2 * rr + 400 / rr
    assert sp.solve(sp.diff(P15, rr), rr) == [10 * sp.sqrt(2)] and sp.diff(P15, rr, 2).subs(rr, 10 * sp.sqrt(2)) > 0
    # P1 Q16
    integrand = 1 / (x**2 * sp.sqrt(9 - x**2))
    sub = (integrand.subs(x, 3 * sp.sin(u)) * sp.diff(3 * sp.sin(u), u))
    assert identity(sub - sp.Rational(1, 9) / sp.sin(u)**2, u, 0.55, 1.0)
    area16 = sp.integrate(sp.Rational(1, 9) / sp.sin(u)**2, (u, sp.pi / 6, sp.pi / 3))
    assert same(area16, 2 * sp.sqrt(3) / 27)
    num16 = float(sp.Integral(integrand, (x, 1.5, 1.5 * math.sqrt(3))).evalf())
    assert close(num16, 2 * math.sqrt(3) / 27, 1e-8)

    # P2 Q1
    assert same(3 * x**3 - 21 * x**2 + 30 * x, 3 * x * (x - 2) * (x - 5))
    # P2 Q2
    assert same(sp.integrate(xp**3 - 8 * xp / sp.sqrt(xp) + 2, xp), xp**4 / 4 - sp.Rational(16, 3) * xp**sp.Rational(3, 2) + 2 * xp)
    # P2 Q3
    yv = 1.7
    xv = 3 * yv * math.log(2) / math.log(5)
    assert close(5**xv, 2**(3 * yv)) and close(xv / yv, math.log(8) / math.log(5))
    # P2 Q4
    B4 = math.acos(177 / 198)
    assert round(B4, 3) == 0.465 and round(0.5 * 9 * 11 * math.sin(B4) - 0.5 * 81 * B4, 2) == 3.36
    # P2 Q5
    X5, Y5 = (t + 3) / 3, 2 * (t - 1)**3
    assert sp.solve(X5 + 1, t) == [-6] and Y5.subs(t, -6) == -686
    assert same(Y5.subs(t, 3 * x - 3), 2 * (3 * x - 4)**3)
    assert sp.diff(2 * (3 * x - 4)**3, x).subs(x, -1) == 882 and (sp.diff(Y5, t) / sp.diff(X5, t)).subs(t, -6) == 882
    # P2 Q6
    assert same(sp.expand(1 - (1 - 9 * x**2 / 2)**2), 9 * x**2 - sp.Rational(81, 4) * x**4)
    assert same((9 * x**2 - sp.Rational(81, 4) * x**4) / ((x / 2) * (3 * x)), 6 - sp.Rational(27, 2) * x**2)
    assert sp.limit((1 - sp.cos(3 * x)**2) / (sp.sin(x / 2) * sp.tan(3 * x)), x, 0) == 6
    # P2 Q7
    lhs7 = (2 * x**3 + x**2 - 6 * x - 11) / ((x - 2) * (x + 1))
    assert same(lhs7, 2 * x + 3 - 1 / (x - 2) + 2 / (x + 1))
    # P2 Q8
    f8 = x**4 - sp.Rational(2, 3) * x**3 - 8 * x**2 + a * x + sp.Rational(16, 3)
    assert sp.solve(sp.diff(f8, x).subs(x, sp.Rational(1, 2)), a) == [8]
    g8 = f8.subs(a, 8)
    assert same(sp.diff(g8, x), (4 * x - 2) * (x**2 - 4))
    assert g8.subs(x, sp.Rational(1, 2)) == sp.Rational(117, 16) and g8.subs(x, 2) == 0 and g8.subs(x, -2) == sp.Rational(-64, 3)
    for kv in (sp.Rational(1, 10), 3, 7):
        assert len([r_ for r_ in sp.Poly(g8 - kv, x).nroots() if abs(sp.im(r_)) < 1e-12]) == 4
    for kv in (-1, 8):
        assert len([r_ for r_ in sp.Poly(g8 - kv, x).nroots() if abs(sp.im(r_)) < 1e-12]) < 4
    # P2 Q9
    N9 = lambda tv: 8000 - 8000 * math.exp(-0.06 * tv)
    assert round(N9(4)) == 1707 and round(math.log(8 / 3) / 0.06, 2) == 16.35 and close(N9(math.log(8 / 3) / 0.06), 5000)
    assert round(480 * math.exp(-0.24)) == 378
    # P2 Q10
    V10 = sp.Rational(12, 5) - 2 * sp.exp(-t / 4)
    assert V10.subs(t, 0) == sp.Rational(2, 5) and same(20 * sp.diff(V10, t), 12 - 5 * V10)
    assert same(V10.subs(t, 4 * sp.log(5)), 2) and round(4 * math.log(5), 1) == 6.4
    # P2 Q11
    y11 = lambda xv: 3600 - 60 * xv
    assert y11(30) == 1800 and y11(50) == 600
    P11 = ((x - 15) * (3600 - 60 * x) - 12000) / 1000
    assert same(sp.expand(P11), -sp.Rational(3, 50) * x**2 + sp.Rational(9, 2) * x - 66)
    assert sorted(sp.solve(P11, x)) == [20, 55] and sp.solve(sp.diff(P11, x), x) == [sp.Rational(75, 2)]
    assert P11.subs(x, 40) == 18
    # P2 Q12
    f12 = lambda v: 3 * abs(v + 2) - 4
    assert (f12(2), f12(-2)) == (8, -4)

    def meets12(kv):
        hits = []
        if kv != 3:
            xr = sp.Rational(2, 1) / (kv - 3)  # kx = 3x + 2 for x >= -2
            if xr >= -2:
                hits.append(xr)
        if kv != -3:
            xl = sp.Rational(-10, 1) / (kv + 3)  # kx = -3x - 10 for x < -2
            if xl < -2:
                hits.append(xl)
        return len(hits)
    assert all(meets12(sp.Rational(v, 10)) == 0 for v in range(21, 31))
    assert all(meets12(sp.Rational(v, 10)) > 0 for v in (-40, -30, 0, 10, 20, 31, 40))
    # P2 Q13
    for kv in (0.3, -0.7, 0.95):
        sols = 0
        for i in range(40000):
            x0, x1 = 2 * math.pi * i / 40000, 2 * math.pi * (i + 1) / 40000
            if (math.sin(4 * x0) - kv) * (math.sin(4 * x1) - kv) < 0:
                sols += 1
        assert sols == 8
        sols2 = 0
        for i in range(60000):
            x0, x1 = 3 * math.pi * i / 60000, 3 * math.pi * (i + 1) / 60000
            if (math.sin(4 * x0)**2 - kv**2) * (math.sin(4 * x1)**2 - kv**2) < 0:
                sols2 += 1
        assert sols2 == 24
    # P2 Q14
    av, bv = sp.symbols("av bv")
    AB, BC, DB = 3 * av + bv, 12 * av - 8 * bv, -6 * av + k * bv
    AD = sp.expand(AB - DB)
    assert sp.solve(sp.Eq(AD.coeff(bv) / AD.coeff(av), -sp.Rational(8, 12)), k) == [7]
    lam, mu = sp.symbols("lam mu")
    AN = AB + BC / 4
    eq = sp.expand(lam * AN - (AB + mu * (-DB.subs(k, 7))))
    sol = sp.solve([eq.coeff(av), eq.coeff(bv)], [lam, mu])
    assert sol[mu] == sp.Rational(1, 4)
    # P2 Q15
    f15 = (4 - x**2) / (4 + x**2)**2
    assert same(sp.diff(f15, x), -2 * x * (12 - x**2) / (4 + x**2)**3)
    assert f15.subs(x, -2 * sp.sqrt(3)) == sp.Rational(-1, 32) and sp.diff(f15, x, 2).subs(x, -2 * sp.sqrt(3)) > 0
    sub15 = f15.subs(x, 2 * sp.tan(theta)) * sp.diff(2 * sp.tan(theta), theta)
    assert identity(sub15 - sp.cos(2 * theta) / 2, theta, -0.7, 0.7)
    assert sp.integrate(f15, (x, -2, 2)) == sp.Rational(1, 2)
