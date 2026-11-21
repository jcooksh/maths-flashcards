"""June 2019 (9MA0/01 and 9MA0/02), with the numbers changed."""
import math
import sympy as sp
from common import card, close, same, identity, x, y, t, k, theta, u

SERIES = {"id": "paper-2019-06", "title": "June 2019", "hue": 45}

CARDS = [
    # ---------------- Paper 1 ----------------
    card(1, 1,
         [r"$f(x)=4x^3+3ax^2-2x+2a$",
          r"Given that $(x+2)$ is a factor of $f(x)$, find the value of the constant $a$."],
         [r"Spot: “$(x+2)$ is a factor” means $f(-2)=0$ (factor theorem).",
          r"Use: substitute $x=-2$, then solve the linear equation for $a$.",
          r"Method: $f(-2)=-32+12a+4+2a=14a-28=0$",
          r"Answer: $a=2$"],
         [r"Set $f(-2)=0$ and solve for $a$",
          r"Set $f(2)=0$ and solve for $a$",
          r"Divide $f(x)$ by $(x+2)$ and set the quotient to zero",
          r"Differentiate $f(x)$ and set $f'(-2)=0$"]),
    card(1, 2,
         [r"The curve $y=\cos x$ is drawn, with $x$ in radians.",
          r"(a) Explain why the equation $\cos x-3x-\dfrac14=0$ has only one real root.",
          r"(b) Given that the root $\alpha$ is small, use the small angle approximation for $\cos x$ to estimate $\alpha$ to 3 decimal places."],
         [r"Spot: “only one root” means compare two graphs: $y=\cos x$ and the line $y=3x+\dfrac14$. “$\alpha$ is small” means use $\cos x\approx1-\dfrac{x^2}{2}$.",
          r"Use: the line has gradient 3, but $\cos x$ never has a gradient steeper than 1.",
          r"(a) The line $y=3x+\tfrac14$ crosses $y=\cos x$ exactly once, because $\cos x-3x-\tfrac14$ has derivative $-\sin x-3<0$, so it's always decreasing.",
          r"(b) $1-\dfrac{x^2}{2}-3x-\dfrac14=0\Rightarrow2x^2+12x-3=0$",
          r"Take the small root: $x=\dfrac{-12+\sqrt{168}}{4}$",
          r"Answer: $\alpha\approx0.240$"],
         [r"Rearrange to $\cos x=3x+\tfrac14$ and draw the line on the cosine graph",
          r"Differentiate $\cos x$ and set it to zero",
          r"Use $\cos x\approx1$ straight away",
          r"Solve $\cos x=3x$ using the quadratic formula"]),
    card(1, 3,
         [r"$y=\dfrac{3x^2+12x}{(x+2)^2}$, $x\ne-2$",
          r"(a) Show that $\dfrac{dy}{dx}=\dfrac{A}{(x+2)^n}$, where $A$ and $n$ are constants to be found.",
          r"(b) Hence deduce the range of values of $x$ for which $\dfrac{dy}{dx}<0$."],
         [r"Spot: a fraction to differentiate means the quotient rule. You can also first write $y=3-\dfrac{12}{(x+2)^2}$.",
          r"Use: the quotient rule (booklet), then take out the factor $(x+2)$ to cancel.",
          r"(a) $\dfrac{(6x+12)(x+2)^2-(3x^2+12x)\cdot2(x+2)}{(x+2)^4}=\dfrac{24}{(x+2)^3}$",
          r"Answer: $A=24$ and $n=3$",
          r"(b) $\dfrac{24}{(x+2)^3}<0$ when $(x+2)^3<0$, so $x<-2$."],
         [r"Use the quotient rule, then cancel a factor of $(x+2)$",
          r"Differentiate the top and the bottom separately",
          r"Expand the denominator and use the product rule on the numerator only",
          r"Use partial fractions and integrate"]),
    card(1, 4,
         [r"(a) Find the first three terms, in ascending powers of $x$, of the binomial expansion of $\dfrac{1}{\sqrt{9-x}}$.",
          r"The expansion can be used to approximate $\sqrt3$. Possible values of $x$ are $-18$, $6$ and $-3$, since $\dfrac{1}{\sqrt{27}}=\dfrac{\sqrt3}{9}$, $\dfrac{1}{\sqrt3}=\dfrac{\sqrt3}{3}$ and $\dfrac{1}{\sqrt{12}}=\dfrac{\sqrt3}{6}$.",
          r"(b) Without evaluating, state which value should not be used, and which gives the most accurate approximation. Give reasons."],
         [r"Spot: $(9-x)^{-\frac12}$ isn't in the form $(1+x)^n$, so take out the factor $9^{-\frac12}$ first.",
          r"Use: $(1+x)^n=1+nx+\dfrac{n(n-1)}{2}x^2+\dots$ (booklet), valid for $\left|\dfrac{x}{9}\right|<1$.",
          r"(a) $\dfrac13\left(1-\dfrac{x}{9}\right)^{-\frac12}=\dfrac13+\dfrac{x}{54}+\dfrac{x^2}{648}+\dots$",
          r"(b) Don't use $x=-18$: the expansion needs $|x|<9$.",
          r"$x=-3$ is most accurate: it has the smallest $|x|$, so the ignored terms are smallest."],
         [r"Write $(9-x)^{-\frac12}=\tfrac13\left(1-\tfrac{x}{9}\right)^{-\frac12}$, then use the binomial series",
          r"Expand $(9-x)^{\frac12}$ with $n=\tfrac12$",
          r"Write it as $9^{-\frac12}-x^{-\frac12}$",
          r"Use $(1+x)^n$ with $n=-\tfrac12$ and $x$ replaced by $9-x$"]),
    card(1, 5,
         [r"$f(x)=3x^2-12x+17$, $x\in\mathbb{R}$",
          r"(a) Write $f(x)$ in the form $a(x+b)^2+c$.",
          r"(b) Sketch $y=f(x)$, showing any intercepts and the turning point.",
          r"(c)(i) Describe fully the transformation that maps $y=f(x)$ onto $y=g(x)$, where $g(x)=3(x+3)^2-12x-23$.",
          r"(ii) Find the range of $h(x)=\dfrac{20}{3x^2-12x+17}$."],
         [r"Spot: “the form $a(x+b)^2+c$” means complete the square. It gives the turning point and the minimum value.",
          r"Use: take out the factor 3 to complete the square. Expand $g$ before comparing it with $f$.",
          r"(a) $f(x)=3(x-2)^2+5$",
          r"(b) A U-shape with minimum $(2,5)$ and $y$-intercept $(0,17)$. It doesn't cross the $x$-axis.",
          r"(c)(i) $g(x)=3x^2+6x+4=3(x+1)^2+1$: a translation by $\begin{pmatrix}-3\\-4\end{pmatrix}$",
          r"(ii) The denominator is at least 5, so $0<h(x)\le4$."],
         [r"Take out the factor 3, then complete the square",
          r"Use the quadratic formula to find the roots",
          r"Differentiate and set $f'(x)=0$ to find the form",
          r"Factorise $3x^2-12x+17$"]),
    card(1, 6,
         [r"(a) Solve, for $-180^\circ\le\theta\le180^\circ$, the equation $3\sin2\theta=4\tan\theta$, giving answers to 1 decimal place where necessary.",
          r"(b) Deduce the smallest positive solution of $3\sin(2x+40^\circ)=4\tan(x+20^\circ)$."],
         [r"Spot: $\sin2\theta$ together with $\tan\theta$ means write everything in $\sin\theta$ and $\cos\theta$, then factorise. Don't divide by $\sin\theta$.",
          r"Use: $\sin2\theta\equiv2\sin\theta\cos\theta$ and $\tan\theta\equiv\dfrac{\sin\theta}{\cos\theta}$.",
          r"(a) $6\sin\theta\cos^2\theta=4\sin\theta\Rightarrow\sin\theta(6\cos^2\theta-4)=0$",
          r"$\sin\theta=0$ gives $\theta=-180^\circ,0^\circ,180^\circ$. $\cos\theta=\pm\sqrt{\tfrac23}$ gives $\theta=\pm35.3^\circ,\pm144.7^\circ$.",
          r"(b) Put $\theta=x+20^\circ$, so $x=\theta-20^\circ$. The smallest positive $x$ comes from $\theta=35.3^\circ$.",
          r"Answer: $x=15.3^\circ$"],
         [r"Write $\sin2\theta=2\sin\theta\cos\theta$, multiply by $\cos\theta$, then factorise out $\sin\theta$",
          r"Divide both sides by $\sin\theta$",
          r"Square both sides",
          r"Use $\tan\theta=\dfrac{\cos\theta}{\sin\theta}$"]),
    card(1, 7,
         [r"A car is worth £24 000 when new and £18 000 after one year.",
          r"(a) Use an exponential model to form an equation linking its value £$V$ with its age $t$ years.",
          r"(b) After 8 years the car is worth £2000. Evaluate the reliability of your model.",
          r"(c) Car B is worth the same when new but loses value more quickly. How would you adapt the model?"],
         [r"Spot: “exponential model” means $V=Ab^t$ or $V=Ae^{-kt}$, fitted to the two values given.",
          r"Use: $A$ is the value at $t=0$, and $b=\dfrac{18000}{24000}$.",
          r"(a) $V=24000\times0.75^t$ (or $V=24000e^{-0.288t}$)",
          r"(b) The model gives $24000\times0.75^8\approx£2400$, compared with the real £2000. That's fairly close, but the model overestimates the value.",
          r"(c) Use a smaller base than $0.75$ (or a larger $k$ in $e^{-kt}$)."],
         [r"Use $V=Ab^t$ with $A=24000$ and $b=\dfrac{18000}{24000}$",
          r"Use $V=24000-6000t$",
          r"Use $V=24000t^{0.75}$",
          r"Use $V=18000\times0.75^t$"]),
    card(1, 8,
         [r"A curve has equation $y=x(x+1)(x-3)$.",
          r"(a) $R_1$ is bounded by the curve and the negative $x$-axis. Show that its area is $\dfrac{7}{12}$.",
          r"(b) $R_2$ is bounded by the curve, the positive $x$-axis and the line $x=b$, where $0<b<3$. Given that $R_1$ and $R_2$ have equal areas, verify that $(b+1)^2(3b^2-14b+7)=0$.",
          r"(c) The roots of $3b^2-14b+7=0$ are $0.569$ and $4.097$. Explain the significance of $4.097$."],
         [r"Spot: an area below the $x$-axis gives a negative integral, so expand the cubic and keep track of the signs.",
          r"Use: $y=x^3-2x^2-3x$, so $\displaystyle\int y\,dx=\frac{x^4}{4}-\frac{2x^3}{3}-\frac{3x^2}{2}$.",
          r"(a) $\displaystyle\int_{-1}^{0}y\,dx=0-\left(\tfrac14+\tfrac23-\tfrac32\right)=\tfrac{7}{12}$",
          r"(b) $R_2$ is below the axis, so $-\displaystyle\int_0^b y\,dx=\tfrac{7}{12}$. This gives $3b^4-8b^3-18b^2+7=0$, which factorises as $(b+1)^2(3b^2-14b+7)=0$.",
          r"(c) For $b=4.097$, the area above the axis between $3$ and $4.097$ cancels part of the area below it. So $\displaystyle\int_0^{4.097}y\,dx=-\tfrac{7}{12}$ too, but it isn't the region described."],
         [r"Expand to $x^3-2x^2-3x$ and integrate between the roots $-1$ and $0$",
          r"Integrate $x(x+1)(x-3)$ from $-1$ to $3$",
          r"Use the trapezium rule between $-1$ and $0$",
          r"Differentiate and find the turning points"]),
    card(1, 9,
         [r"Given that $a>0$, $b>0$ and $\log a-\log b=\log(a+b)$,",
          r"(a) show that $a=\dfrac{b^2}{1-b}$,",
          r"(b) write down the full restriction on the value of $b$, explaining why."],
         [r"Spot: an equation of logs means combine them into a single log on each side, then remove the logs.",
          r"Use: $\log a-\log b=\log\dfrac{a}{b}$, and if $\log P=\log Q$ then $P=Q$.",
          r"(a) $\dfrac{a}{b}=a+b\Rightarrow a=ab+b^2\Rightarrow a(1-b)=b^2\Rightarrow a=\dfrac{b^2}{1-b}$",
          r"(b) $0<b<1$, because $a$ must be positive, so $1-b>0$."],
         [r"Use $\log a-\log b=\log\dfrac{a}{b}$ to get $\dfrac{a}{b}=a+b$",
          r"Use $\log(a+b)=\log a+\log b$",
          r"Cancel the logs to get $a-b=a+b$",
          r"Raise $e$ to each term: $a-b=e^{a+b}$"]),
    card(1, 10,
         [r"(i) Prove that for all $n\in\mathbb{N}$, $n^2+1$ is not divisible by 4.",
          r"(ii) “Given $x\in\mathbb{R}$, the value of $|2x-13|$ is greater than or equal to the value of $x-6$.” State whether this is always, sometimes or never true, giving a reason."],
         [r"Spot: (i) “for all $n$” with divisibility means proof by exhaustion: $n$ even or $n$ odd. (ii) Test where $x-6>0$ but $2x-13$ is small.",
          r"Use: $n=2k$ and $n=2k+1$.",
          r"(i) $n=2k$: $4k^2+1$ leaves remainder 1. $n=2k+1$: $4k^2+4k+2$ leaves remainder 2. Neither is a multiple of 4.",
          r"(ii) Sometimes true. For example, when $x=6.8$: $|13.6-13|=0.6$ but $x-6=0.8$.",
          r"It's false for $\tfrac{19}{3}<x<7$ and true everywhere else."],
         [r"Consider $n$ even ($n=2k$) and $n$ odd ($n=2k+1$) separately",
          r"Check $n=1,2,3$ and conclude",
          r"Assume $n^2+1=4k$ and differentiate",
          r"Prove it by contradiction using a single example"]),
    card(1, 11,
         [r"A runner runs each of the first 3 km of a 15 km race at 5 minutes per km.",
          r"After that, each kilometre is modelled to take 4% longer than the one before.",
          r"(a) Show that her estimated time for the first 5 km is 25 minutes 36 seconds.",
          r"(b) Show that her time for the $r$th kilometre, $4\le r\le15$, is $5\times1.04^{r-3}$ minutes.",
          r"(c) Estimate her total time for the race, in minutes and seconds."],
         [r"Spot: “4% longer than the one before” means each time is the previous one multiplied by $1.04$, so it's a geometric series.",
          r"Use: $S_n=\dfrac{a(r^n-1)}{r-1}$ (booklet), with $a=5\times1.04$ and 12 terms.",
          r"(a) $15+5(1.04)+5(1.04)^2=15+5.2+5.408=25.608$ min $=25$ min $36$ s",
          r"(c) $15+\dfrac{5.2(1.04^{12}-1)}{0.04}=15+78.13=93.13$ min",
          r"Answer: about 93 minutes 8 seconds"],
         [r"Treat km 4 to 15 as a geometric series with $a=5.2$ and $r=1.04$",
          r"Use an arithmetic series with $d=0.04$",
          r"Work out $5\times15\times1.04$",
          r"Use $5\times1.04^{15}$ for the total time"]),
    card(1, 12,
         [r"$f(x)=8e^{-\frac{x}{3}}\sin x$, $x\ge0$",
          r"(a) Show that the $x$-coordinates of the turning points of $y=f(x)$ satisfy $\tan x=3$.",
          r"$H(t)=\left|8e^{-\frac{t}{3}}\sin t\right|$ models the height, in metres, of a bouncing ball $t$ seconds after it's kicked.",
          r"(b) Sketch $H$ against $t$, showing its long-term behaviour.",
          r"(c) Find the maximum height of the ball between the first and second bounces.",
          r"(d) Explain why the model shouldn't be used to predict the time of each bounce."],
         [r"Spot: an exponential times a trig function means the product rule. Turning points are where $f'(x)=0$.",
          r"Use: $\dfrac{d}{dx}e^{-\frac{x}{3}}=-\tfrac13e^{-\frac{x}{3}}$, and $e^{-\frac{x}{3}}$ is never 0.",
          r"(a) $f'(x)=8e^{-\frac{x}{3}}\left(\cos x-\tfrac13\sin x\right)=0\Rightarrow\tan x=3$",
          r"(b) Humps above the axis that touch it at $t=k\pi$ and get smaller towards zero.",
          r"(c) Between the bounces at $\pi$ and $2\pi$: $t=\pi+\arctan3\approx4.391$, so $H\approx1.76$ m.",
          r"(d) In the model, bounces happen every $\pi$ seconds. A real ball's bounces get closer together."],
         [r"Differentiate with the product rule and set $f'(x)=0$",
          r"Differentiate $\sin x$ only and set it to zero",
          r"Take logs of $f(x)$ and integrate",
          r"Set $f(x)=0$ and solve"]),
    card(1, 13,
         [r"The curve $C$ has equation $y=\dfrac{p-3x}{(2x-q)(x+1)}$, $x\ne-1$, $x\ne1$, where $p$ and $q$ are constants.",
          r"$C$ passes through $\left(2,\dfrac12\right)$ and has vertical asymptotes $x=1$ and $x=-1$.",
          r"(a)(i) Explain why $q=2$. (ii) Show that $p=9$.",
          r"(b) The region $R$ is bounded by $C$, the $x$-axis and the line $x=2$. Show that its area is $a\ln2+b\ln3$, where $a$ and $b$ are rational constants to be found."],
         [r"Spot: vertical asymptotes are where the denominator is zero. An area under a rational function means partial fractions, then log integrals.",
          r"Use: $\dfrac{9-3x}{(2x-2)(x+1)}\equiv\dfrac{A}{2x-2}+\dfrac{B}{x+1}$. $C$ crosses the axis where $9-3x=0$, which is $x=3$.",
          r"(a) $2x-q=0$ at $x=1$, so $q=2$. Then $\dfrac{p-6}{2\times3}=\dfrac12$, so $p=9$.",
          r"(b) $A=3$ and $B=-3$: $\displaystyle\int_2^3\left(\frac{3}{2x-2}-\frac{3}{x+1}\right)dx=\left[\tfrac32\ln(2x-2)-3\ln(x+1)\right]_2^3$",
          r"Answer: $-\dfrac92\ln2+3\ln3$, so $a=-\dfrac92$ and $b=3$"],
         [r"Split it into partial fractions and integrate from $x=2$ to $x=3$",
          r"Integrate the top and bottom separately",
          r"Integrate from $x=-1$ to $x=1$",
          r"Use the substitution $u=(2x-2)(x+1)$"]),
    card(1, 14,
         [r"The curve $C$ has equation $x=5\sin3y$, $-\dfrac{\pi}{6}<y<\dfrac{\pi}{6}$, and passes through the origin.",
          r"(a) Find $\dfrac{dy}{dx}$ at the origin.",
          r"(b)(i) Use the small angle approximation for $\sin3y$ to find an equation linking $x$ and $y$ near the origin. (ii) Explain how this relates to (a).",
          r"(c) Show that, for all points on $C$, $\dfrac{dy}{dx}=\dfrac{1}{a\sqrt{b-x^2}}$, where $a$ and $b$ are constants to be found."],
         [r"Spot: $x$ is given in terms of $y$, so find $\dfrac{dx}{dy}$ and take the reciprocal.",
          r"Use: $\dfrac{dy}{dx}=1\Big/\dfrac{dx}{dy}$, and $\cos^2\equiv1-\sin^2$ to remove $y$.",
          r"(a) $\dfrac{dx}{dy}=15\cos3y=15$ at $y=0$, so $\dfrac{dy}{dx}=\dfrac{1}{15}$.",
          r"(b) $x\approx15y$, so $y=\dfrac{x}{15}$. This is the tangent at the origin, with the same gradient as (a).",
          r"(c) $\cos3y=\sqrt{1-\dfrac{x^2}{25}}=\dfrac{\sqrt{25-x^2}}{5}$, so $\dfrac{dy}{dx}=\dfrac{1}{3\sqrt{25-x^2}}$, with $a=3$ and $b=25$."],
         [r"Find $\dfrac{dx}{dy}$, then use $\dfrac{dy}{dx}=\dfrac{1}{dx/dy}$",
          r"Rearrange to $y=\tfrac13\arcsin(5x)$ and differentiate",
          r"Differentiate $5\sin3y$ with respect to $x$, treating $y$ as a constant",
          r"Use the product rule"]),

    # ---------------- Paper 2 ----------------
    card(2, 1,
         [r"Given that $3^x\times27^y=9\sqrt3$, express $y$ as a function of $x$."],
         [r"Spot: bases that are all powers of 3 means write everything as a power of 3, then compare the indices.",
          r"Use: $27^y=3^{3y}$ and $9\sqrt3=3^2\times3^{\frac12}=3^{\frac52}$.",
          r"Method: $3^{x+3y}=3^{\frac52}\Rightarrow x+3y=\dfrac52$",
          r"Answer: $y=\dfrac56-\dfrac{x}{3}$"],
         [r"Write every term as a power of 3 and equate the indices",
          r"Take logs base 10 of each term separately and add them",
          r"Divide $9\sqrt3$ by $27$",
          r"Set $x=0$ and solve for $y$"]),
    card(2, 2,
         [r"A jet's speed was measured every 6 seconds from when it turned onto a runway until it left the ground.",
          r"Time (s): 0, 6, 12, 18, 24, 30. Speed ($\text{m s}^{-1}$): 1, 4, 9, 17, 27, 40.",
          r"(a) Estimate the length of runway used.",
          r"(b) The jet's acceleration increased smoothly. Explain whether your answer is an underestimate or an overestimate."],
         [r"Spot: distance is the area under a speed–time graph. Equally spaced readings mean the trapezium rule.",
          r"Use: $\dfrac{h}{2}\left[y_0+y_n+2(y_1+\dots+y_{n-1})\right]$ with $h=6$ (booklet).",
          r"(a) $3\left[(1+40)+2(4+9+17+27)\right]=3(41+114)=465$ m",
          r"(b) The graph curves upwards (it's convex), so each trapezium lies above the curve. It's an overestimate."],
         [r"Use the trapezium rule with $h=6$ on the speed values",
          r"Add the speeds and multiply by 30",
          r"Find the gradient between each pair of readings",
          r"Use the trapezium rule with $h=1$"]),
    card(2, 3,
         [r"A sector $AOB$ has radius 6 cm and angle $AOB=50^\circ$.",
          r"A student writes: area $=\dfrac12r^2\theta=\dfrac12\times6^2\times50=900\text{ cm}^2$.",
          r"(a) Explain the error.",
          r"(b) Write out a correct solution."],
         [r"Spot: formulas with $\theta$ in them ($r\theta$ and $\tfrac12r^2\theta$) need $\theta$ in radians.",
          r"Use: $50^\circ=50\times\dfrac{\pi}{180}=\dfrac{5\pi}{18}$.",
          r"(a) The student used $\theta$ in degrees, but $\dfrac12r^2\theta$ only works in radians.",
          r"(b) $\dfrac12\times36\times\dfrac{5\pi}{18}=5\pi\approx15.7\text{ cm}^2$"],
         [r"Convert $50^\circ$ to radians before using $\tfrac12r^2\theta$",
          r"Use $\pi r^2$ instead",
          r"Halve the angle first",
          r"Use $\tfrac12r\theta$"]),
    card(2, 4,
         [r"The curve $C_1$ has parametric equations $x=6\cos t$, $y=2\sqrt3\sin t$, $0\le t<2\pi$.",
          r"It meets the circle $C_2$ with equation $x^2+y^2=30$ at four distinct points.",
          r"One of these points, $S$, lies in the fourth quadrant. Find the coordinates of $S$."],
         [r"Spot: a parametric curve meeting a Cartesian curve means substitute the parametric $x$ and $y$ into the Cartesian equation.",
          r"Use: $\cos^2t\equiv1-\sin^2t$ to get an equation in $\sin t$ only.",
          r"Method: $36\cos^2t+12\sin^2t=30\Rightarrow36-24\sin^2t=30\Rightarrow\sin^2t=\tfrac14$",
          r"In the fourth quadrant $x>0$ and $y<0$, so $\sin t=-\tfrac12$ and $\cos t=\tfrac{\sqrt3}{2}$.",
          r"Answer: $S=\left(3\sqrt3,\ -\sqrt3\right)$"],
         [r"Substitute $x=6\cos t$ and $y=2\sqrt3\sin t$ into $x^2+y^2=30$",
          r"Set $6\cos t=2\sqrt3\sin t$",
          r"Differentiate both curves and equate the gradients",
          r"Substitute $t=\dfrac{7\pi}{4}$ straight away"]),
    card(2, 5,
         [r"The curve $y=\sqrt[3]{x}$ is drawn. A thin rectangle of height $y$ and width $\delta x$ sits under the curve at the point $(x,y)$.",
          r"Calculate $\displaystyle\lim_{\delta x\to0}\sum_{x=1}^{8}\sqrt[3]{x}\,\delta x$."],
         [r"Spot: the limit of a sum of thin rectangles is a definite integral, which is the area under the curve.",
          r"Use: $\displaystyle\lim_{\delta x\to0}\sum f(x)\,\delta x=\int_a^bf(x)\,dx$, with $\sqrt[3]{x}=x^{\frac13}$.",
          r"Method: $\displaystyle\int_1^8x^{\frac13}\,dx=\left[\tfrac34x^{\frac43}\right]_1^8=\tfrac34(16-1)$",
          r"Answer: $\dfrac{45}{4}$"],
         [r"Recognise it as $\displaystyle\int_1^8x^{\frac13}\,dx$",
          r"Add $\sqrt[3]{x}$ for $x=1,2,\dots,8$",
          r"Differentiate $x^{\frac13}$",
          r"Use the trapezium rule with one strip"]),
    card(2, 6,
         [r"$g(x)=\begin{cases}(x-1)^2+3 & x\le1\\ 3x-2 & x>1\end{cases}$",
          r"(a) Find $gg(0)$.",
          r"(b) Find all values of $x$ for which $g(x)=19$.",
          r"$h(x)=(x-1)^2+3$, $x\le1$",
          r"(c) Explain why $h$ has an inverse but $g$ does not.",
          r"(d) Solve $h^{-1}(x)=-2$."],
         [r"Spot: for a piecewise function, check which branch each input uses. An inverse needs a one-to-one function.",
          r"Use: $h^{-1}(x)=-2$ means $x=h(-2)$, so you don't need to find $h^{-1}$.",
          r"(a) $g(0)=4$, then $g(4)=10$",
          r"(b) $(x-1)^2+3=19$ with $x\le1$ gives $x=-3$. $3x-2=19$ gives $x=7$.",
          r"(c) $h$ is one-to-one. $g$ is many-to-one: for example, $g(0)=g(2)=4$.",
          r"(d) $x=h(-2)=(-3)^2+3=12$"],
         [r"Use the $x\le1$ branch to find $g(0)$, then the other branch to find $g(4)$",
          r"Square $g(0)$",
          r"Use $3x-2$ for every input",
          r"Find $g^{-1}$ first"]),
    card(2, 7,
         [r"A factory's daily cost £$y$ of making $x$ bars of soap is a fixed cost plus a cost proportional to $x$.",
          r"(a) Write down a general equation linking $y$ and $x$.",
          r"Each bar sells for £1.50. When 1000 bars are made and sold, the profit is £400. When 400 are made and sold, there's a loss of £50.",
          r"(b) Show that $y=0.75x+350$.",
          r"(c) Interpret the value 0.75 in this model.",
          r"(d) Find the least number of bars that must be made in a day for a profit."],
         [r"Spot: fixed cost plus proportional cost means a linear model $y=a+bx$. Profit is revenue minus cost.",
          r"Use: revenue $=1.5x$, so cost $=$ revenue $-$ profit.",
          r"(b) $1500-400=1100=a+1000b$ and $600+50=650=a+400b$. Subtract to get $b=0.75$, then $a=350$.",
          r"(c) Each extra bar costs £0.75 to make.",
          r"(d) $1.5x>0.75x+350\Rightarrow x>466.7$",
          r"Answer: 467 bars"],
         [r"Use cost $=$ revenue $-$ profit to get two linear equations in $a$ and $b$",
          r"Set $y=1.5x$",
          r"Use $y=a+bx$ with $a=400$",
          r"Divide 400 by 1000"]),
    card(2, 8,
         [r"(i) Find the value of $\displaystyle\sum_{r=3}^{\infty}54\left(\frac13\right)^r$.",
          r"(ii) Show that $\displaystyle\sum_{n=1}^{78}\log_3\left(\frac{n+3}{n+2}\right)=3$."],
         [r"Spot: (i) an infinite geometric series that starts at $r=3$. (ii) A sum of logs of fractions means combine them, because most factors cancel (it telescopes).",
          r"Use: $S_\infty=\dfrac{a}{1-r}$ (booklet) and $\log x+\log y=\log xy$.",
          r"(i) $a=54\left(\tfrac13\right)^3=2$ and $r=\tfrac13$, so $S_\infty=\dfrac{2}{2/3}=3$.",
          r"(ii) $\log_3\left(\dfrac43\times\dfrac54\times\dots\times\dfrac{81}{80}\right)=\log_3\dfrac{81}{3}=\log_327=3$"],
         [r"Find the first term $54\left(\tfrac13\right)^3$, then use $S_\infty=\dfrac{a}{1-r}$",
          r"Use $S_\infty=\dfrac{54}{1-\frac13}$",
          r"Add the first three terms",
          r"Use $S_n$ with $n=3$"]),
    card(2, 9,
         [r"A car's braking distance $d$ m from a speed of $V\text{ km h}^{-1}$ is investigated. A graph of $\log_{10}d$ against $\log_{10}V$ is a straight line with intercept $-1.6$.",
          r"(a) Explain why this suggests $d=kV^n$, and show that $k\approx0.025$.",
          r"(b) One data point is $(V,d)=(40,30)$. Using $k=0.025$, find $n$ to 3 s.f.",
          r"(c) A driver doing $50\text{ km h}^{-1}$ sees a puddle 70 m ahead and takes 1 second to react. Will the car stop before the puddle?"],
         [r"Spot: a straight line on a log–log graph means a power law $d=kV^n$.",
          r"Use: $\log d=\log k+n\log V$. The intercept is $\log k$ and the gradient is $n$.",
          r"(a) $\log k=-1.6\Rightarrow k=10^{-1.6}\approx0.025$",
          r"(b) $30=0.025\times40^n\Rightarrow n=\dfrac{\log1200}{\log40}\approx1.92$",
          r"(c) Braking: $0.025\times50^{1.92}\approx46$ m. Reacting: $\dfrac{50}{3.6}\times1\approx14$ m. Total: about 60 m.",
          r"Answer: yes, it stops about 10 m before the puddle."],
         [r"Take logs: $\log d=\log k+n\log V$, so the intercept gives $k$",
          r"Use $d=kV+n$, because the graph is a straight line",
          r"Use the gradient of the $d$–$V$ graph as $k$",
          r"Use $d=ke^{nV}$"]),
    card(2, 10,
         [r"In triangle $OAB$, $\overrightarrow{OA}=\mathbf{a}$ and $\overrightarrow{OB}=\mathbf{b}$. The point $C$ is such that $\overrightarrow{OC}=3\overrightarrow{OA}$, and $M$ is the midpoint of $AB$.",
          r"The straight line through $C$ and $M$ meets $OB$ at $N$.",
          r"(a) Find $\overrightarrow{CM}$ in terms of $\mathbf{a}$ and $\mathbf{b}$.",
          r"(b) Show that $\overrightarrow{ON}=\left(3-\dfrac52\lambda\right)\mathbf{a}+\dfrac12\lambda\mathbf{b}$ for some scalar $\lambda$.",
          r"(c) Hence find the ratio $ON:NB$."],
         [r"Spot: a point that lies on two lines means write it two ways (along $CM$ and along $OB$), then compare coefficients of $\mathbf{a}$ and $\mathbf{b}$.",
          r"Use: $\overrightarrow{OM}=\tfrac12(\mathbf{a}+\mathbf{b})$ and $\overrightarrow{ON}=\overrightarrow{OC}+\lambda\overrightarrow{CM}$.",
          r"(a) $\overrightarrow{CM}=\tfrac12(\mathbf{a}+\mathbf{b})-3\mathbf{a}=-\tfrac52\mathbf{a}+\tfrac12\mathbf{b}$",
          r"(c) $N$ is on $OB$, so the coefficient of $\mathbf{a}$ is $0$: $\lambda=\tfrac65$ and $\overrightarrow{ON}=\tfrac35\mathbf{b}$.",
          r"Answer: $ON:NB=3:2$"],
         [r"Write $\overrightarrow{ON}=\overrightarrow{OC}+\lambda\overrightarrow{CM}$ and set the coefficient of $\mathbf{a}$ to zero",
          r"Find the lengths using Pythagoras",
          r"Assume $N$ is the midpoint of $OB$",
          r"Use $\overrightarrow{ON}=\overrightarrow{OA}+\overrightarrow{OB}$"]),
    card(2, 11,
         [r"The curve $C$ has equation $y=(2x)^x$, $x>0$.",
          r"(a) By first taking logarithms, find the $x$-coordinate of the turning point of $C$.",
          r"(b) The point $P(\alpha,4)$ lies on $C$. Show that $1.3<\alpha<1.4$.",
          r"(c) Using $x_{n+1}=\dfrac12\times4^{\frac{1}{x_n}}$ with $x_1=1.4$, find $x_4$ to 3 decimal places.",
          r"(d) Describe the long-term behaviour of $x_n$."],
         [r"Spot: the variable is in both the base and the power, so take logs first, then differentiate implicitly.",
          r"Use: $\ln y=x\ln(2x)$, so $\dfrac1y\dfrac{dy}{dx}=\ln(2x)+1$.",
          r"(a) $\ln(2x)+1=0\Rightarrow x=\dfrac{1}{2e}$",
          r"(b) $(2.6)^{1.3}\approx3.46<4$ and $(2.8)^{1.4}\approx4.23>4$, so $(2x)^x-4$ changes sign.",
          r"(c) $x_2=1.346$, $x_3=1.401$, $x_4=1.345$",
          r"(d) The values jump from one side of $\alpha$ to the other and very slowly drift away from it. The iteration does not converge."],
         [r"Take logs, $\ln y=x\ln(2x)$, then differentiate implicitly",
          r"Use the power rule: $\dfrac{dy}{dx}=x(2x)^{x-1}$",
          r"Treat it as an exponential: $\dfrac{dy}{dx}=(2x)^x\ln2$",
          r"Set $y=0$"]),
    card(2, 12,
         [r"(a) Prove that $\dfrac{\cos3\theta}{\cos\theta}+\dfrac{\sin3\theta}{\sin\theta}\equiv4\cos2\theta$, $\theta\ne(90n)^\circ$.",
          r"(b) Hence solve, for $0^\circ<\theta<90^\circ$, $\dfrac{\cos3\theta}{\cos\theta}+\dfrac{\sin3\theta}{\sin\theta}=3$, giving answers to 1 decimal place."],
         [r"Spot: two fractions mean use a common denominator. The numerator then matches the $\sin(A+B)$ expansion.",
          r"Use: $\sin A\cos B+\cos A\sin B\equiv\sin(A+B)$ and $\sin2\theta\equiv2\sin\theta\cos\theta$.",
          r"(a) $\dfrac{\cos3\theta\sin\theta+\sin3\theta\cos\theta}{\sin\theta\cos\theta}=\dfrac{\sin4\theta}{\frac12\sin2\theta}=\dfrac{4\sin2\theta\cos2\theta}{\sin2\theta}=4\cos2\theta$",
          r"(b) $\cos2\theta=\tfrac34$ with $0^\circ<2\theta<180^\circ$, so $2\theta=41.4^\circ$.",
          r"Answer: $\theta=20.7^\circ$"],
         [r"Combine the fractions over the common denominator $\sin\theta\cos\theta$",
          r"Cancel the $\theta$s to get $\cos3+\sin3$",
          r"Multiply only the first fraction by $\cos\theta$",
          r"Use the R-form"]),
    card(2, 13,
         [r"A storage tank is modelled as a hollow cylinder of radius $r$ m and height $h$ m, closed at one end, with a hemispherical shell of radius $r$ m at the other end.",
          r"The volume of the tank is $10\text{ m}^3$. (Sphere: $V=\tfrac43\pi r^3$, $A=4\pi r^2$.)",
          r"(a) Show that its surface area is $S=\dfrac{20}{r}+\dfrac53\pi r^2$.",
          r"(b) Use calculus to find the radius that minimises $S$.",
          r"(c) Find the minimum surface area, to the nearest integer."],
         [r"Spot: “minimise” with two variables means use the volume to eliminate $h$, then differentiate.",
          r"Use: $\pi r^2h+\tfrac23\pi r^3=10$ and $S=\pi r^2+2\pi rh+2\pi r^2$.",
          r"(a) $2\pi rh=\dfrac{2\left(10-\frac23\pi r^3\right)}{r}=\dfrac{20}{r}-\dfrac43\pi r^2$, so $S=\dfrac{20}{r}+\dfrac53\pi r^2$.",
          r"(b) $\dfrac{dS}{dr}=-\dfrac{20}{r^2}+\dfrac{10}{3}\pi r=0\Rightarrow r^3=\dfrac{6}{\pi}\Rightarrow r\approx1.24$ m",
          r"(c) $S\approx24\text{ m}^2$"],
         [r"Use the volume to write $h$ in terms of $r$, then substitute into $S$",
          r"Differentiate $S$ with respect to $h$",
          r"Set $r=h$",
          r"Use $S=4\pi r^2$ for the whole tank"]),
    card(2, 14,
         [r"(a) Use the substitution $u=3-\sqrt h$ to show that $\displaystyle\int\frac{dh}{3-\sqrt h}=-6\ln\left|3-\sqrt h\right|-2\sqrt h+k$.",
          r"The height $h$ m of a tree $t$ years after planting is modelled by $\dfrac{dh}{dt}=\dfrac{\sqrt t\,(3-\sqrt h)}{15}$.",
          r"(b) Find the range of heights that the model allows.",
          r"(c) A tree is 1 m tall when planted. Find how long it takes to reach 6 m, to 3 significant figures."],
         [r"Spot: (a) a given substitution means rewrite $h$ and $dh$ in terms of $u$. (c) $\dfrac{dh}{dt}=f(t)\,g(h)$ means separate the variables and use (a).",
          r"Use: $h=(3-u)^2$, so $dh=-2(3-u)\,du$.",
          r"(a) $\displaystyle\int\frac{-2(3-u)}{u}\,du=\int\left(2-\frac6u\right)du=2u-6\ln u$, and $2u=6-2\sqrt h$ (the 6 goes into $k$).",
          r"(b) $0<h<9$: the height increases towards 9 m but never reaches it.",
          r"(c) $-6\ln\left|3-\sqrt h\right|-2\sqrt h=\dfrac{2}{45}t^{\frac32}+c$. At $t=0$, $h=1$, so $c=-6\ln2-2$.",
          r"At $h=6$: $\dfrac{2}{45}t^{\frac32}\approx4.84\Rightarrow t\approx22.8$ years"],
         [r"Write $h=(3-u)^2$ and $dh=-2(3-u)\,du$, then integrate in $u$",
          r"Integrate $\dfrac{1}{3-\sqrt h}$ as $\ln\left|3-\sqrt h\right|$",
          r"Use integration by parts with $u=\sqrt h$",
          r"Multiply by $3+\sqrt h$ and integrate term by term"]),
]


def check():
    a, b = sp.symbols("a b")
    # P1 Q1
    f = 4 * x**3 + 3 * a * x**2 - 2 * x + 2 * a
    assert sp.solve(f.subs(x, -2), a) == [2]
    # P1 Q2
    root = (-12 + math.sqrt(168)) / 4
    assert round(root, 3) == 0.240
    true_root = float(sp.nsolve(sp.cos(x) - 3 * x - sp.Rational(1, 4), x, 0.24))
    assert abs(true_root - root) < 2e-3
    assert same(sp.expand(-4 * (1 - x**2 / 2 - 3 * x - sp.Rational(1, 4))), 2 * x**2 + 12 * x - 3)
    # P1 Q3
    Y = (3 * x**2 + 12 * x) / (x + 2)**2
    assert same(sp.diff(Y, x), 24 / (x + 2)**3)
    # P1 Q4
    ser = sp.series(1 / sp.sqrt(9 - x), x, 0, 3).removeO()
    assert same(ser, sp.Rational(1, 3) + x / 54 + x**2 / 648)
    assert same(1 / sp.sqrt(27), sp.sqrt(3) / 9) and same(1 / sp.sqrt(12), sp.sqrt(3) / 6)
    # P1 Q5
    assert same(3 * x**2 - 12 * x + 17, 3 * (x - 2)**2 + 5)
    g = 3 * (x + 3)**2 - 12 * x - 23
    assert same(g, 3 * (x + 1)**2 + 1)
    # translation (-3, -4): f(x+3) - 4 == g
    assert same((3 * (x - 2)**2 + 5).subs(x, x + 3) - 4, g)
    assert sp.Rational(20, 5) == 4
    # P1 Q6
    sols = []
    for c in (math.sqrt(2 / 3), -math.sqrt(2 / 3)):
        base = math.degrees(math.acos(c))
        sols += [base, -base]
    assert sorted(round(s, 1) for s in sols) == [-144.7, -35.3, 35.3, 144.7]
    for s in sols + [0, 180, -180]:
        r_ = math.radians(s)
        assert abs(3 * math.sin(2 * r_) - 4 * math.tan(r_)) < 1e-9
    assert round(math.degrees(math.acos(math.sqrt(2 / 3))) - 20, 1) == 15.3
    # P1 Q7
    assert round(24000 * 0.75**8) == 2403 and round(math.log(0.75), 3) == -0.288
    # P1 Q8
    Yc = x * (x + 1) * (x - 3)
    assert sp.integrate(Yc, (x, -1, 0)) == sp.Rational(7, 12)
    bb = sp.symbols("bb")
    eq = -sp.integrate(Yc, (x, 0, bb)) - sp.Rational(7, 12)
    assert same(sp.expand(12 * eq), -(3 * bb**4 - 8 * bb**3 - 18 * bb**2 + 7))
    assert same(3 * bb**4 - 8 * bb**3 - 18 * bb**2 + 7, (bb + 1)**2 * (3 * bb**2 - 14 * bb + 7))
    rts = sorted(float(v) for v in sp.solve(3 * bb**2 - 14 * bb + 7, bb))
    assert [round(v, 3) for v in rts] == [0.569, 4.097]
    assert close(sp.integrate(Yc, (x, 0, rts[1])), -7 / 12, 1e-6)
    # P1 Q9
    A_ = sp.symbols("A_", positive=True)
    B_ = sp.symbols("B_", positive=True)
    assert same(sp.solve(sp.Eq(A_ / B_, A_ + B_), A_)[0], B_**2 / (1 - B_))
    # P1 Q10
    for nn in range(1, 200):
        assert (nn * nn + 1) % 4 != 0
    for v in [6.0, 6.3, 19 / 3, 7, 8, 0, -3]:
        assert abs(2 * v - 13) >= v - 6 - 1e-12
    for v in [6.34, 6.8, 6.99]:
        assert abs(2 * v - 13) < v - 6
    # P1 Q11
    first5 = 15 + 5 * 1.04 + 5 * 1.04**2
    assert close(first5, 25.608) and round((first5 - 25) * 60) == 36
    total = 15 + 5.2 * (1.04**12 - 1) / 0.04
    assert round(total, 2) == 93.13 and round((total - 93) * 60) == 8
    assert close(total, 15 + sum(5 * 1.04**(r_ - 3) for r_ in range(4, 16)))
    # P1 Q12
    F = 8 * sp.exp(-x / 3) * sp.sin(x)
    assert identity(sp.diff(F, x) - 8 * sp.exp(-x / 3) * (sp.cos(x) - sp.sin(x) / 3), x)
    tm = math.pi + math.atan(3)
    assert round(tm, 3) == 4.391 and round(abs(8 * math.exp(-tm / 3) * math.sin(tm)), 2) == 1.76
    # P1 Q13
    Yr = (9 - 3 * x) / ((2 * x - 2) * (x + 1))
    assert Yr.subs(x, 2) == sp.Rational(1, 2)
    assert same(Yr, 3 / (2 * x - 2) - 3 / (x + 1))
    area = sp.integrate(Yr, (x, 2, 3))
    assert same(area, -sp.Rational(9, 2) * sp.log(2) + 3 * sp.log(3)) and float(area) > 0
    # P1 Q14
    dxdy = sp.diff(5 * sp.sin(3 * y), y)
    assert dxdy.subs(y, 0) == 15
    assert identity((1 / dxdy).subs(y, sp.asin(x / 5) / 3) - 1 / (3 * sp.sqrt(25 - x**2)), x, -4.5, 4.5)

    # P2 Q1
    assert same(sp.log(9 * sp.sqrt(3), 3), sp.Rational(5, 2))
    # P2 Q2
    speeds = [1, 4, 9, 17, 27, 40]
    assert 3 * (speeds[0] + speeds[-1] + 2 * sum(speeds[1:-1])) == 465
    # P2 Q3
    assert same(sp.Rational(1, 2) * 36 * 50 * sp.pi / 180, 5 * sp.pi) and round(5 * math.pi, 1) == 15.7
    # P2 Q4
    s_ = sp.symbols("s_")
    assert sorted(sp.solve(36 * (1 - s_**2) + 12 * s_**2 - 30, s_)) == [-sp.Rational(1, 2), sp.Rational(1, 2)]
    S = (6 * sp.sqrt(3) / 2, 2 * sp.sqrt(3) * -sp.Rational(1, 2))
    assert same(S[0], 3 * sp.sqrt(3)) and same(S[1], -sp.sqrt(3)) and same(S[0]**2 + S[1]**2, 30)
    # P2 Q5
    assert sp.integrate(x**sp.Rational(1, 3), (x, 1, 8)) == sp.Rational(45, 4)
    # P2 Q6
    gp = lambda v: (v - 1)**2 + 3 if v <= 1 else 3 * v - 2
    assert gp(0) == 4 and gp(gp(0)) == 10 and gp(2) == 4 and gp(-3) == 19 and gp(7) == 19
    assert (-2 - 1)**2 + 3 == 12
    # P2 Q7
    aa, bc = sp.symbols("aa bc")
    sol = sp.solve([aa + 1000 * bc - 1100, aa + 400 * bc - 650], [aa, bc])
    assert sol == {aa: 350, bc: sp.Rational(3, 4)}
    assert math.ceil(350 / 0.75 + 1e-9) == 467
    # P2 Q8
    assert sp.summation(54 * sp.Rational(1, 3)**sp.Symbol("r", integer=True), (sp.Symbol("r", integer=True), 3, sp.oo)) == 3
    assert same(sum(sp.log(sp.Rational(n + 3, n + 2), 3) for n in range(1, 79)), 3)
    # P2 Q9
    nexp = math.log10(1200) / math.log10(40)
    assert round(nexp, 2) == 1.92 and round(10**-1.6, 3) == 0.025
    brake = 0.025 * 50**1.92
    react = 50 / 3.6
    assert round(brake) == 46 and round(react) == 14 and round(brake + react) == 60 and brake + react < 70
    # P2 Q10
    lam = sp.symbols("lam")
    assert sp.solve(3 - sp.Rational(5, 2) * lam, lam) == [sp.Rational(6, 5)]
    # ON = 3/5 b, so ON:NB = 3/5 : 2/5
    # P2 Q11
    yy = (2 * x)**x
    assert identity(sp.diff(yy, x) / yy - (sp.log(2 * x) + 1), x, 0.2, 3)
    assert same(sp.solve(sp.log(2 * x) + 1, x)[0], 1 / (2 * sp.E))
    assert round(2.6**1.3, 2) == 3.46 and round(2.8**1.4, 2) == 4.23
    xs = [1.4]
    for _ in range(60):
        xs.append(0.5 * 4**(1 / xs[-1]))
    assert [round(v, 3) for v in xs[1:4]] == [1.346, 1.401, 1.345]
    alpha = float(sp.nsolve((2 * x)**x - 4, x, 1.36))
    dist = [abs(v - alpha) for v in xs]
    assert dist[40] > dist[2] and (xs[10] - alpha) * (xs[11] - alpha) < 0   # oscillates and drifts away
    # P2 Q12
    expr = sp.cos(3 * theta) / sp.cos(theta) + sp.sin(3 * theta) / sp.sin(theta) - 4 * sp.cos(2 * theta)
    assert identity(expr, theta)
    th = math.degrees(math.acos(0.75)) / 2
    assert round(th, 1) == 20.7 and round(math.degrees(math.acos(0.75)), 1) == 41.4
    # P2 Q13
    rr = sp.symbols("rr", positive=True)
    hh = (10 - sp.Rational(2, 3) * sp.pi * rr**3) / (sp.pi * rr**2)
    Ssurf = sp.pi * rr**2 + 2 * sp.pi * rr * hh + 2 * sp.pi * rr**2
    assert same(Ssurf, 20 / rr + sp.Rational(5, 3) * sp.pi * rr**2)
    ropt = (6 / math.pi)**(1 / 3)
    assert round(ropt, 2) == 1.24 and round(20 / ropt + 5 / 3 * math.pi * ropt**2) == 24
    # P2 Q14
    hs = sp.symbols("hs", positive=True)
    anti = -6 * sp.log(3 - sp.sqrt(hs)) - 2 * sp.sqrt(hs)
    assert identity(sp.diff(anti, hs) - 1 / (3 - sp.sqrt(hs)), hs, 0.5, 8)
    c0 = -6 * math.log(2) - 2
    lhs6 = -6 * math.log(3 - math.sqrt(6)) - 2 * math.sqrt(6) - c0
    tt = (lhs6 * 45 / 2)**(2 / 3)
    assert round(lhs6, 2) == 4.84 and round(tt, 1) == 22.8
