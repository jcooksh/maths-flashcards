"""June 2022 (9MA0/01 and 9MA0/02), with the numbers changed."""
import math
import sympy as sp
from common import card, close, same, identity, x, y, t, k, theta, u

SERIES = {"id": "paper-2022-06", "title": "June 2022", "hue": 160}

CARDS = [
    # ---------------- Paper 1 ----------------
    card(1, 1,
         [r"The point $P(3,-4)$ lies on the curve $y=f(x)$. Find the point that $P$ maps to when the curve is transformed to:",
          r"(a) $y=f(x)-3$",
          r"(b) $y=|f(x)|$",
          r"(c) $y=2f(x+1)-5$"],
         [r"Spot: changes inside the bracket affect $x$, and they work the opposite way to how they look. Changes outside affect $y$, and they work as written.",
          r"Use: $f(x+1)$ shifts left by 1. $2f$ stretches $y$ by 2. $-5$ shifts down by 5. $|f|$ makes negative $y$ values positive.",
          r"(a) $(3,-7)$",
          r"(b) $(3,4)$",
          r"(c) $x\to3-1=2$ and $y\to2(-4)-5=-13$, giving $(2,-13)$"],
         [r"Apply the change inside the bracket to $x$ (opposite way), and the outside changes to $y$",
          r"Add 1 to the $x$-coordinate for $f(x+1)$",
          r"Apply the $-5$ before multiplying by 2",
          r"Change only the $y$-coordinate"]),
    card(1, 2,
         [r"$f(x)=(x-3)(x^2+2x+k)+36$, where $k$ is a constant.",
          r"Given that $(x+1)$ is a factor of $f(x)$, find $k$."],
         [r"Spot: “$(x+1)$ is a factor” means $f(-1)=0$. There's no need to expand.",
          r"Use: substitute $x=-1$ straight into the given form.",
          r"Method: $(-4)(1-2+k)+36=0\Rightarrow-4k+4+36=0$",
          r"Answer: $k=10$"],
         [r"Substitute $x=-1$ and set $f(-1)=0$",
          r"Expand the brackets fully, then divide by $(x+1)$",
          r"Set $x^2+2x+k=0$",
          r"Substitute $x=1$"]),
    card(1, 3,
         [r"A circle has equation $x^2+y^2+6x-8y=24$.",
          r"(a) Find the centre and radius.",
          r"(b) $P$ is the point on the circle furthest from the origin $O$. Find the exact length $OP$."],
         [r"Spot: furthest from the origin means go from $O$ through the centre and out to the circle, so $OP=|OC|+r$.",
          r"Use: complete the square: $(x+3)^2+(y-4)^2=49$.",
          r"(a) The centre is $(-3,4)$ and $r=7$.",
          r"(b) $|OC|=\sqrt{9+16}=5$, so $OP=5+7=12$."],
         [r"Complete the square, then use $OP=|OC|+r$",
          r"Use $OP=r$",
          r"Use $OP=|OC|-r$",
          r"Use $OP=\sqrt{24}$"]),
    card(1, 4,
         [r"(a) Express $\displaystyle\lim_{\delta x\to0}\sum_{x=1.5}^{7.5}\frac3x\,\delta x$ as an integral.",
          r"(b) Hence show that this limit equals $\ln k$, where $k$ is a constant to be found."],
         [r"Spot: the limit of a sum of $f(x)\,\delta x$ is a definite integral. $\dfrac{3}{x}$ integrates to a log.",
          r"Use: $\displaystyle\int\frac{3}{x}\,dx=3\ln x$ and $3\ln5=\ln5^3$.",
          r"(a) $\displaystyle\int_{1.5}^{7.5}\frac3x\,dx$",
          r"(b) $3\ln7.5-3\ln1.5=3\ln5=\ln125$",
          r"Answer: $k=125$"],
         [r"Recognise it as $\displaystyle\int_{1.5}^{7.5}\frac3x\,dx$",
          r"Add up $\frac3x$ for $x=1.5,\dots,7.5$",
          r"Differentiate $\frac3x$",
          r"Integrate $\frac3x$ to $-\frac{3}{x^2}$"]),
    card(1, 5,
         [r"The height $h$ m of a tree $t$ years after planting is modelled by $h^2=at+b$, $0\le t<25$.",
          r"The tree was 2.80 m tall after 3 years and 5.50 m tall after 12 years.",
          r"(a) Find $a$ and $b$ to 3 s.f.",
          r"(b) The tree was 6.50 m tall after 20 years. Evaluate the model."],
         [r"Spot: two data points and two unknowns. Square the heights first, because the model is in $h^2$.",
          r"Use: $7.84=3a+b$ and $30.25=12a+b$.",
          r"(a) $9a=22.41\Rightarrow a\approx2.49$, and $b=7.84-3a\approx0.370$",
          r"(b) The model gives $h=\sqrt{20a+b}\approx7.08$ m, compared with 6.50 m, so it overestimates. It may not hold for older trees."],
         [r"Square the heights, then solve $7.84=3a+b$ and $30.25=12a+b$",
          r"Solve $2.8=3a+b$ and $5.5=12a+b$",
          r"Take logs of both sides",
          r"Assume $b=0$"]),
    card(1, 6,
         [r"A cubic curve $y=f(x)$ passes through the origin, has a maximum at $(1,4)$ and a minimum at $(3,0)$.",
          r"(a) Write down the set of values of $x$ for which $f'(x)<0$.",
          r"(b) The line $y=k$ meets the curve at only one point. Find the possible values of $k$.",
          r"(c) Find the equation of the curve."],
         [r"Spot: a minimum touching the $x$-axis at $(3,0)$ means a repeated root, so there's a factor of $(x-3)^2$.",
          r"Use: $f(x)=ax(x-3)^2$, then the maximum point to find $a$.",
          r"(a) It's decreasing between the turning points: $\{x:1<x<3\}$",
          r"(b) $\{k:k<0\}\cup\{k:k>4\}$",
          r"(c) $f(1)=4a=4\Rightarrow a=1$, so $y=x(x-3)^2$"],
         [r"Use the repeated root: $f(x)=ax(x-3)^2$",
          r"Use $f(x)=ax(x-1)(x-3)$",
          r"Use $f(x)=a(x-1)^2(x-3)$",
          r"Integrate $f'(x)=(x-1)(x-3)$ and stop"],
         ask="How do you start part (c)?"),
    card(1, 7,
         [r"(i) $p$ and $q$ are integers with $p^2q$ even. Prove by contradiction that at least one of $p$ and $q$ is even.",
          r"(ii) $x$ and $y$ are integers with $x<0$ and $(x-y)^2<5x^2+y^2$. Show that $y<-2x$."],
         [r"Spot: (i) contradiction: assume both are odd. (ii) Expand, cancel, then divide by a negative quantity, which flips the inequality.",
          r"Use: odd $\times$ odd $=$ odd. Since $x<0$, $-2x>0$.",
          r"(i) Suppose $p$ and $q$ are both odd. Then $p^2$ is odd, so $p^2q$ is odd. That's a contradiction.",
          r"(ii) $x^2-2xy+y^2<5x^2+y^2\Rightarrow-2xy<4x^2$",
          r"Divide by $-2x>0$: $y<-2x$"],
         [r"Assume $p$ and $q$ are both odd and show $p^2q$ is then odd",
          r"Assume $p$ and $q$ are both even",
          r"Try $p=1$ and $q=2$",
          r"Use proof by exhaustion over all integers"],
         ask="How do you start part (i)?"),
    card(1, 8,
         [r"A car's speed between two sets of traffic lights is modelled by $v=(12-0.5t)\ln(t+1)$, $0\le t\le T$.",
          r"(a) Find $T$.",
          r"(b) Show that the maximum speed occurs when $t=\dfrac{25}{1+\ln(t+1)}-1$.",
          r"(c) Using $t_{n+1}=\dfrac{25}{1+\ln(t_n+1)}-1$ with $t_1=6$, find $t_3$ to 3 d.p., and the time of maximum speed."],
         [r"Spot: the car stops when $v=0$. The maximum speed is where $\dfrac{dv}{dt}=0$, which needs the product rule.",
          r"Use: $\dfrac{dv}{dt}=-0.5\ln(t+1)+\dfrac{12-0.5t}{t+1}$.",
          r"(a) $12-0.5t=0\Rightarrow T=24$",
          r"(b) $12-0.5t=0.5(t+1)\ln(t+1)\Rightarrow25=(t+1)\left(1+\ln(t+1)\right)$, which rearranges to the given form.",
          r"(c) $t_2=7.486$ and $t_3=6.966$, converging to $t\approx7.09$ s"],
         [r"Use the product rule and set $\dfrac{dv}{dt}=0$",
          r"Set $v=0$",
          r"Differentiate $\ln(t+1)$ only",
          r"Integrate $v$"],
         ask="How do you start part (b)?"),
    card(1, 9,
         [r"$PQRS$ is a parallelogram with $\overrightarrow{PQ}=2\mathbf{i}+6\mathbf{j}+3\mathbf{k}$ and $\overrightarrow{QR}=6\mathbf{i}-2\mathbf{j}+3\mathbf{k}$.",
          r"(a) Show that $PQRS$ is a rhombus.",
          r"(b) Find the exact area of $PQRS$."],
         [r"Spot: a rhombus is a parallelogram with equal sides, so compare $|\overrightarrow{PQ}|$ and $|\overrightarrow{QR}|$. Area $=ab\sin\theta$.",
          r"Use: $\cos\theta=\dfrac{\mathbf{a}\cdot\mathbf{b}}{|\mathbf{a}||\mathbf{b}|}$, then $\sin\theta=\sqrt{1-\cos^2\theta}$.",
          r"(a) $|\overrightarrow{PQ}|=\sqrt{4+36+9}=7$ and $|\overrightarrow{QR}|=\sqrt{36+4+9}=7$",
          r"(b) $\overrightarrow{PQ}\cdot\overrightarrow{QR}=12-12+9=9$, so $\cos\theta=\pm\dfrac{9}{49}$ and $\sin\theta=\dfrac{\sqrt{2320}}{49}$.",
          r"Area $=7\times7\times\dfrac{\sqrt{2320}}{49}=4\sqrt{145}$"],
         [r"Show $|\overrightarrow{PQ}|=|\overrightarrow{QR}|$, then use area $=ab\sin\theta$",
          r"Show $\overrightarrow{PQ}\cdot\overrightarrow{QR}=0$",
          r"Use area $=|\overrightarrow{PQ}|\times|\overrightarrow{QR}|$",
          r"Use area $=\tfrac12ab\sin\theta$"]),
    card(1, 10,
         [r"The number of bees (in thousands) is modelled by $N_b=30+150e^{0.04t}$, where $t$ is the number of years from the start of the study.",
          r"(a) Find the number of bees at the start.",
          r"(b) Show that after exactly 15 years the number is increasing at about 11 thousand per year.",
          r"(c) The number of wasps is $N_w=20+600e^{-0.04t}$. Find $T$, to 2 d.p., when the numbers of bees and wasps are equal."],
         [r"Spot: “rate” means differentiate. Equal populations with $e^{kt}$ and $e^{-kt}$ means let $u=e^{0.04T}$ to get a quadratic.",
          r"Use: $\dfrac{dN_b}{dt}=6e^{0.04t}$, and $e^{-0.04T}=\dfrac1u$.",
          r"(a) $30+150=180$ thousand",
          r"(b) $6e^{0.6}\approx10.9\approx11$ thousand per year",
          r"(c) $30+150u=20+\dfrac{600}{u}\Rightarrow15u^2+u-60=0\Rightarrow u\approx1.967$",
          r"Answer: $T=25\ln u\approx16.91$"],
         [r"Let $u=e^{0.04T}$ and multiply through by $u$ to get a quadratic",
          r"Take logs of each term",
          r"Set $150e^{0.04T}=600e^{-0.04T}$ and ignore the constants",
          r"Differentiate both models and equate them"],
         ask="How do you start part (c)?"),
    card(1, 11,
         [r"$C_1$: $y=2x^3+5$, $x>0$, and $C_2$: $y=23x-9x^2-4$, $x>0$.",
          r"(a) Verify that the curves intersect at $x=\dfrac12$.",
          r"(b) They intersect again at $P$. Using algebra, find the exact $x$-coordinate of $P$."],
         [r"Spot: you already know one intersection, so $(2x-1)$ is a factor of the cubic you get when you equate the curves.",
          r"Use: $2x^3+9x^2-23x+9=0$, then divide by $(2x-1)$.",
          r"(a) Both give $y=5.25$ at $x=\tfrac12$.",
          r"(b) $(2x-1)(x^2+5x-9)=0\Rightarrow x=\dfrac{-5\pm\sqrt{61}}{2}$",
          r"Answer: $x>0$, so $x=\dfrac{-5+\sqrt{61}}{2}$"],
         [r"Equate the curves, then divide the cubic by $(2x-1)$",
          r"Differentiate both curves",
          r"Use the quadratic formula on $2x^3+9x^2-23x+9$",
          r"Substitute $x=1$"],
         ask="How do you start part (b)?"),
    card(1, 12,
         [r"Show that $\displaystyle\int_1^{e^2}\sqrt x\,\ln x\,dx=ae^3+b$, where $a$ and $b$ are rational constants to be found."],
         [r"Spot: a power of $x$ times $\ln x$ means integration by parts with $u=\ln x$, because it differentiates to something simpler.",
          r"Use: $u=\ln x$ and $\dfrac{dv}{dx}=x^{\frac12}$, so $v=\tfrac23x^{\frac32}$.",
          r"Method: $\left[\tfrac23x^{\frac32}\ln x\right]_1^{e^2}-\displaystyle\int_1^{e^2}\tfrac23x^{\frac12}\,dx=\tfrac43e^3-\left[\tfrac49x^{\frac32}\right]_1^{e^2}$",
          r"Answer: $\dfrac89e^3+\dfrac49$"],
         [r"Use integration by parts with $u=\ln x$ and $\dfrac{dv}{dx}=\sqrt x$",
          r"Use integration by parts with $u=\sqrt x$ and $\dfrac{dv}{dx}=\ln x$",
          r"Substitute $u=\sqrt x$",
          r"Integrate $\ln x$ to $\dfrac1x$"]),
    card(1, 13,
         [r"(i) Prove that the sum of the first $n$ terms of an arithmetic series is $S_n=\dfrac n2\left[2a+(n-1)d\right]$.",
          r"(ii) Ama saves £12 in week 1, £11.50 in week 2, £11 in week 3, and so on. She needs £122.50 for a printer and takes $n$ weeks to save exactly that much.",
          r"(a) Show that $n^2-49n+490=0$. (b) Solve it. (c) State how many weeks she takes, with a reason."],
         [r"Spot: (i) write the sum forwards and backwards, then add. (ii) Saving less each week means an arithmetic series with $d=-0.5$.",
          r"Use: $S_n=\dfrac n2\left[2(12)+(n-1)(-0.5)\right]=122.5$.",
          r"(a) $\dfrac n2(24.5-0.5n)=122.5\Rightarrow49n-n^2=490$",
          r"(b) $(n-14)(n-35)=0$, so $n=14$ or $35$",
          r"(c) 14 weeks. From week 26 the weekly amount would be negative, so $n=35$ makes no sense."],
         [r"Use $S_n$ with $a=12$ and $d=-0.5$, and set it equal to 122.5",
          r"Use $d=0.5$",
          r"Use $u_n=122.5$",
          r"Use the geometric series formula"],
         ask="How do you start part (ii)(a)?"),
    card(1, 14,
         [r"(a) Given that $2\cos(x+60^\circ)=\sin(x+30^\circ)$, show that $\tan x=\dfrac{\sqrt3}{9}$.",
          r"(b) Hence, or otherwise, solve $2\cos2\theta=\sin(2\theta-30^\circ)$ for $0\le\theta<180^\circ$, to 1 d.p."],
         [r"Spot: compound angles with exact angles means expand both sides, then collect the $\sin x$ and $\cos x$ terms to get $\tan x$.",
          r"Use: the $\cos(A+B)$ and $\sin(A+B)$ expansions, and $\cos60^\circ=\sin30^\circ=\tfrac12$.",
          r"(a) $\cos x-\sqrt3\sin x=\tfrac{\sqrt3}{2}\sin x+\tfrac12\cos x\Rightarrow\tfrac12\cos x=\tfrac{3\sqrt3}{2}\sin x\Rightarrow\tan x=\dfrac{1}{3\sqrt3}=\dfrac{\sqrt3}{9}$",
          r"(b) Let $x=2\theta-60^\circ$. Then $\tan(2\theta-60^\circ)=\dfrac{\sqrt3}{9}$, so $2\theta-60^\circ=10.9^\circ+180n$.",
          r"Answer: $\theta=35.4^\circ,\ 125.4^\circ$"],
         [r"Expand both sides with the compound angle formulae, then divide by $\cos x$",
          r"Use the R-form straight away",
          r"Square both sides",
          r"Use $\cos(x+60^\circ)=\cos x+\cos60^\circ$"],
         ask="How do you start part (a)?"),
    card(1, 15,
         [r"A toy is a prism whose cross-section is a sector of a circle with radius $r$ cm and angle 1.2 radians. Its length is $h$ cm, and its volume is $300\text{ cm}^3$.",
          r"(a) Show that its surface area is $S=1.2r^2+\dfrac{1600}{r}$.",
          r"(b) Find the value of $r$ for which $S$ is stationary.",
          r"(c) Prove that this gives the minimum surface area."],
         [r"Spot: “minimise surface area” with a fixed volume means use the volume to remove $h$, then differentiate.",
          r"Use: volume $=\tfrac12r^2(1.2)h=0.6r^2h$, and the area is two sectors plus two rectangles plus the curved face.",
          r"(a) $h=\dfrac{500}{r^2}$, and $S=2(0.6r^2)+(2r+1.2r)h=1.2r^2+\dfrac{1600}{r}$",
          r"(b) $\dfrac{dS}{dr}=2.4r-\dfrac{1600}{r^2}=0\Rightarrow r^3=\dfrac{2000}{3}\Rightarrow r\approx8.74$",
          r"(c) $\dfrac{d^2S}{dr^2}=2.4+\dfrac{3200}{r^3}>0$, so it's a minimum."],
         [r"Use the volume to write $h$ in terms of $r$, then substitute into $S$",
          r"Differentiate $S$ with respect to $h$",
          r"Use the sector area $\pi r^2$",
          r"Set $r=h$"]),
    card(1, 16,
         [r"A curve $C$ has parametric equations $x=4\sin^2t$, $y=3\sin2t+2\sin t$, $0\le t\le\dfrac{\pi}{2}$.",
          r"The region $R$ is bounded by $C$, the $x$-axis and the line $x=2$.",
          r"(a) Show that the area of $R$ is $\displaystyle\int_0^{a}\left(6-6\cos4t+16\sin^2t\cos t\right)dt$, where $a$ is a constant.",
          r"(b) Hence find the exact area of $R$."],
         [r"Spot: parametric area means $\displaystyle\int y\frac{dx}{dt}\,dt$. Convert the $x$ limits to $t$ limits.",
          r"Use: $\dfrac{dx}{dt}=8\sin t\cos t=4\sin2t$ and $\sin^22t=\dfrac{1-\cos4t}{2}$. $x=2$ gives $\sin^2t=\tfrac12$, so $t=\dfrac{\pi}{4}$.",
          r"(a) $(3\sin2t+2\sin t)(4\sin2t)=12\sin^22t+8\sin t\sin2t=6-6\cos4t+16\sin^2t\cos t$, with $a=\dfrac{\pi}{4}$",
          r"(b) $\left[6t-\tfrac32\sin4t+\tfrac{16}{3}\sin^3t\right]_0^{\frac{\pi}{4}}$",
          r"Answer: $\dfrac{3\pi}{2}+\dfrac{4\sqrt2}{3}$"],
         [r"Use area $=\displaystyle\int y\frac{dx}{dt}\,dt$ and change the $x$ limits to $t$",
          r"Use area $=\displaystyle\int y\,dt$ from 0 to 2",
          r"Eliminate $t$ first",
          r"Use area $=\displaystyle\int x\frac{dy}{dt}\,dt$"]),

    # ---------------- Paper 2 ----------------
    card(2, 1,
         [r"Solve $|5-3x|=9+x$."],
         [r"Spot: modulus equal to a linear expression means two cases: inside $=\pm$ the right-hand side. Check every answer.",
          r"Use: $5-3x=9+x$ or $5-3x=-(9+x)$.",
          r"Method: $5-3x=9+x\Rightarrow x=-1$, and $3x-5=9+x\Rightarrow x=7$",
          r"Answer: $x=-1$ or $x=7$ (both check: $8=8$ and $16=16$)"],
         [r"Solve $5-3x=9+x$ and $5-3x=-(9+x)$, then check both",
          r"Solve $5-3x=9+x$ only",
          r"Square both sides and ignore the check",
          r"Drop the modulus signs"]),
    card(2, 2,
         [r"(a) Sketch $y=5^x$, stating where it meets the axes.",
          r"(b) Solve $5^x=80$, giving your answer to 2 d.p."],
         [r"Spot: an exponential graph has a $y$-intercept of 1 and an asymptote $y=0$. To solve for a power, take logs.",
          r"Use: $x=\log_580=\dfrac{\ln80}{\ln5}$.",
          r"(a) An increasing curve through $(0,1)$, approaching $y=0$ as $x\to-\infty$",
          r"(b) $x=\dfrac{\ln80}{\ln5}\approx2.72$"],
         [r"Take logs: $x=\dfrac{\ln80}{\ln5}$",
          r"Divide 80 by 5",
          r"Use $x=\ln\dfrac{80}{5}$",
          r"Square root 80"],
         ask="How do you solve part (b)?"),
    card(2, 3,
         [r"A sequence is defined by $a_1=4$ and $a_{n+1}=\dfrac{1}{1-a_n}$.",
          r"(a) Show that the sequence is periodic and state its order.",
          r"(b) Find $\displaystyle\sum_{n=1}^{40}a_n$."],
         [r"Spot: “periodic” means generate terms until $a_1$ comes back.",
          r"Use: count the full cycles in 40 terms, plus the leftovers.",
          r"(a) $4,\ -\tfrac13,\ \tfrac34,\ 4,\dots$, so it's periodic of order 3.",
          r"(b) Each cycle adds to $4-\tfrac13+\tfrac34=\tfrac{53}{12}$. 13 cycles cover 39 terms, then add $a_{40}=4$.",
          r"Answer: $13\times\dfrac{53}{12}+4=\dfrac{737}{12}$"],
         [r"Work out terms until 4 appears again",
          r"Use the arithmetic series formula",
          r"Use the geometric series formula",
          r"Assume $a_n$ tends to a limit"]),
    card(2, 4,
         [r"Given that $y=3x^2-5x$, use differentiation from first principles to show that $\dfrac{dy}{dx}=6x-5$."],
         [r"Spot: “first principles” means start from $\displaystyle\lim_{h\to0}\frac{f(x+h)-f(x)}{h}$.",
          r"Use: expand $3(x+h)^2-5(x+h)$, cancel, then divide by $h$.",
          r"Method: $\dfrac{3x^2+6xh+3h^2-5x-5h-3x^2+5x}{h}=6x+3h-5$",
          r"As $h\to0$, this tends to $6x-5$."],
         [r"Write $\dfrac{f(x+h)-f(x)}{h}$, expand, simplify, then let $h\to0$",
          r"Use the power rule",
          r"Substitute $h=0$ first",
          r"Integrate $6x-5$"]),
    card(2, 5,
         [r"The table shows values of $y=\log_2(3x)$, to 2 d.p.",
          r"$x$: 2, 3, 4, 5, 6. $y$: 2.58, 3.17, 3.58, 3.91, 4.17",
          r"(a) Use the trapezium rule with all the values to estimate $\displaystyle\int_2^6\log_2(3x)\,dx$.",
          r"(b) Hence estimate (i) $\displaystyle\int_2^6\log_2(27x^3)\,dx$ and (ii) $\displaystyle\int_2^6\log_2(12x)\,dx$."],
         [r"Spot: (b) means rewrite each new integrand in terms of $\log_2(3x)$ using the laws of logs, then reuse (a).",
          r"Use: $\log_2(27x^3)=\log_2(3x)^3=3\log_2(3x)$ and $\log_2(12x)=\log_24+\log_2(3x)=2+\log_2(3x)$.",
          r"(a) $\tfrac12\left[(2.58+4.17)+2(3.17+3.58+3.91)\right]=14.035$",
          r"(b)(i) $3\times14.035\approx42.1$",
          r"(ii) $\displaystyle\int_2^62\,dx+14.035=8+14.035\approx22.0$"],
         [r"Rewrite the new logs in terms of $\log_2(3x)$ using the laws of logs",
          r"Use the trapezium rule again with new values",
          r"Multiply the answer to (a) by 4 for (ii)",
          r"Differentiate the answer to (a)"],
         ask="How do you start part (b)?"),
    card(2, 6,
         [r"$f(x)=10\sin\left(\dfrac x2\right)-4x+6$, $x>0$, with $x$ in radians. $P$ is a local maximum.",
          r"(a) Find the $x$-coordinate of $P$ to 3 s.f.",
          r"(b) The curve crosses the $x$-axis at $\alpha$. Given $f(3)=3.975$ and $f(4)=-0.907$, explain why $3<\alpha<4$.",
          r"(c) With $x_0=4$, apply Newton–Raphson once to find a second approximation to $\alpha$, to 3 s.f."],
         [r"Spot: a local maximum means $f'(x)=0$. “Explain why it's in the interval” means a sign change on a continuous function. Newton–Raphson is in the booklet.",
          r"Use: $f'(x)=5\cos\left(\dfrac x2\right)-4$ and $x_1=x_0-\dfrac{f(x_0)}{f'(x_0)}$.",
          r"(a) $\cos\dfrac x2=0.8\Rightarrow x=2\arccos0.8\approx1.29$",
          r"(b) $f$ is continuous and changes sign between 3 and 4.",
          r"(c) $x_1=4-\dfrac{-0.907}{5\cos2-4}\approx3.85$"],
         [r"Differentiate and solve $5\cos\left(\frac x2\right)-4=0$",
          r"Set $f(x)=0$",
          r"Differentiate $\sin\frac x2$ as $\cos\frac x2$ with no factor of $\frac12$",
          r"Use degrees"],
         ask="How do you start part (a)?"),
    card(2, 7,
         [r"(a) Find the first four terms, in ascending powers of $x$, of the binomial expansion of $\sqrt{9-8x}$.",
          r"(b) A student uses this expansion with $x=\dfrac34$ to approximate $\sqrt3$. Without calculating, state whether it will overestimate or underestimate, with a reason."],
         [r"Spot: take the 9 out first: $\sqrt{9-8x}=3\left(1-\dfrac{8x}{9}\right)^{\frac12}$.",
          r"Use: $(1+x)^n$ with $n=\tfrac12$ and $x$ replaced by $-\dfrac{8x}{9}$.",
          r"(a) $3-\dfrac43x-\dfrac{8}{27}x^2-\dfrac{32}{243}x^3$",
          r"(b) Overestimate: every term after the first is negative, so the terms you leave out would make it smaller."],
         [r"Write $\sqrt{9-8x}=3\left(1-\frac{8x}{9}\right)^{\frac12}$, then expand",
          r"Use $(1+x)^n$ with $x$ replaced by $-8x$, without taking out the 9",
          r"Use $\sqrt9-\sqrt{8x}$",
          r"Square the expansion"]),
    card(2, 8,
         [r"The region $R$ is bounded by the curve $y=\dfrac{(x-1)(x-2)}{3\sqrt x}$, $x>0$, and the $x$-axis.",
          r"Find the exact area of $R$ in the form $a\sqrt2+b$."],
         [r"Spot: a fraction over $\sqrt x$ means divide each term by $x^{\frac12}$ to get powers of $x$. The region is between the roots 1 and 2, below the axis.",
          r"Use: $y=\tfrac13\left(x^{\frac32}-3x^{\frac12}+2x^{-\frac12}\right)$. Below the axis, area $=-\displaystyle\int y\,dx$.",
          r"Method: $\displaystyle\int_1^2y\,dx=\tfrac13\left[\tfrac25x^{\frac52}-2x^{\frac32}+4x^{\frac12}\right]_1^2=\tfrac13\left(\tfrac{8\sqrt2}{5}-\tfrac{12}{5}\right)<0$",
          r"Answer: area $=\dfrac45-\dfrac{8}{15}\sqrt2$"],
         [r"Expand and divide by $\sqrt x$, then integrate between the roots",
          r"Use the quotient rule",
          r"Integrate from 0 to 2",
          r"Use the trapezium rule"]),
    card(2, 9,
         [r"A passenger's height $H$ m on a Ferris wheel is modelled by $H=|A\sin(bt+\alpha)^\circ|$, where $t$ is in seconds.",
          r"The maximum height is 64 m. The passenger is 2 m above the ground at the start, and one revolution takes 900 s.",
          r"(a) Find $A$ and $b$ exactly, and $\alpha$ to 3 s.f.",
          r"(b) Explain why $H=|A\sin(bt+\alpha)^\circ|+d$, with $d>0$, would be a better model."],
         [r"Spot: $|\sin|$ repeats every $180^\circ$, so one revolution is one hump: $\dfrac{180}{b}=900$.",
          r"Use: the maximum gives $A$, and $t=0$ gives $\alpha$.",
          r"(a) $A=64$, $b=\dfrac{180}{900}=0.2$, and $64\sin\alpha=2\Rightarrow\alpha\approx1.79$",
          r"(b) In this model the height reaches 0, so the passenger would touch the ground. The $+d$ lifts the lowest point above the ground."],
         [r"Use $\dfrac{180}{b}=900$, because $|\sin|$ has period $180^\circ$",
          r"Use $\dfrac{360}{b}=900$",
          r"Use $b=900$",
          r"Use $A=32$"]),
    card(2, 10,
         [r"$f(x)=\dfrac{6x+1}{3x+2}$, $x>-\dfrac23$, and $g(x)=\sqrt{9-x^2}$, $0\le x\le3$.",
          r"(a) Find $f^{-1}(1)$.",
          r"(b) Show that $f(x)=A+\dfrac{B}{3x+2}$.",
          r"(c) State the range of $g^{-1}$.",
          r"(d) Find the range of $fg^{-1}$."],
         [r"Spot: $f^{-1}(1)$ means solve $f(x)=1$. The range of $g^{-1}$ is the domain of $g$.",
          r"Use: $f(x)=2-\dfrac{3}{3x+2}$, which is increasing.",
          r"(a) $6x+1=3x+2\Rightarrow x=\tfrac13$",
          r"(b) $A=2$ and $B=-3$",
          r"(c) $0\le g^{-1}(x)\le3$",
          r"(d) Apply $f$ to $[0,3]$: $\dfrac12\le fg^{-1}(x)\le\dfrac{19}{11}$"],
         [r"Solve $f(x)=1$",
          r"Find $\dfrac{1}{f(1)}$",
          r"Substitute $x=1$ into $f$",
          r"Differentiate $f$"],
         ask="How do you start part (a)?"),
    card(2, 11,
         [r"Prove, using algebra, that $n^2+3n+5$ is odd for all $n\in\mathbb{N}$."],
         [r"Spot: odd or even for all $n$ means split into $n$ even ($2k$) and $n$ odd ($2k+1$).",
          r"Use: even $+$ even $=$ even, and odd $+$ odd $=$ even.",
          r"$n=2k$: $4k^2+6k+5=2(2k^2+3k+2)+1$, which is odd.",
          r"$n=2k+1$: $4k^2+4k+1+6k+3+5=2(2k^2+5k+4)+1$, which is odd."],
         [r"Consider $n=2k$ and $n=2k+1$ separately",
          r"Check $n=1,2,3$",
          r"Factorise $n^2+3n+5$",
          r"Use the quadratic formula"]),
    card(2, 12,
         [r"$f(x)=\dfrac{e^{2x}}{x^2+k}$, where $k$ is a positive constant.",
          r"(a) Show that $f'(x)=(x^2-x+k)g(x)$, where $g(x)$ is a function to be found.",
          r"(b) Given that $y=f(x)$ has at least one stationary point, find the possible values of $k$."],
         [r"Spot: quotient rule. Then “at least one stationary point” means the quadratic factor has real roots: $b^2-4ac\ge0$.",
          r"Use: $e^{2x}$ and the denominator are never 0, so only the quadratic can be 0.",
          r"(a) $f'(x)=\dfrac{2e^{2x}(x^2+k)-2xe^{2x}}{(x^2+k)^2}$, so $g(x)=\dfrac{2e^{2x}}{(x^2+k)^2}$",
          r"(b) $1-4k\ge0$ and $k>0$, so $0<k\le\dfrac14$"],
         [r"Use the quotient rule, then factorise out $2e^{2x}$",
          r"Differentiate the top and bottom separately",
          r"Use the product rule without the chain rule",
          r"Take logs and integrate"]),
    card(2, 13,
         [r"$A$, $B$ and $C$ have position vectors $2\mathbf{i}+\mathbf{j}-3\mathbf{k}$, $3\mathbf{j}+\mathbf{k}$ and $-4\mathbf{i}+p\mathbf{j}+9\mathbf{k}$, and lie on a straight line.",
          r"(a) Find $p$.",
          r"(b) $OB$ is extended to a point $D$ so that $\overrightarrow{CD}$ is parallel to $\overrightarrow{OA}$. Find $|\overrightarrow{OD}|$ as a simplified surd."],
         [r"Spot: collinear means $\overrightarrow{AC}$ is a multiple of $\overrightarrow{AB}$. “Extended” means $\overrightarrow{OD}=\mu\overrightarrow{OB}$.",
          r"Use: compare the components of $\overrightarrow{CD}=\lambda\overrightarrow{OA}$.",
          r"(a) $\overrightarrow{AB}=(-2,2,4)$ and $\overrightarrow{AC}=(-6,p-1,12)=3\overrightarrow{AB}$, so $p=7$.",
          r"(b) $D=(0,3\mu,\mu)$ and $\overrightarrow{CD}=(4,3\mu-7,\mu-9)=\lambda(2,1,-3)$, giving $\lambda=2$ and $\mu=3$.",
          r"Answer: $|\overrightarrow{OD}|=\sqrt{0+81+9}=3\sqrt{10}$"],
         [r"Set $\overrightarrow{AC}=k\overrightarrow{AB}$ and compare components",
          r"Set $\overrightarrow{OC}=k\overrightarrow{OA}$",
          r"Use the dot product",
          r"Find the midpoint of $AB$"],
         ask="How do you start part (a)?"),
    card(2, 14,
         [r"(a) Express $\dfrac{5}{(3x-2)(x+1)}$ in partial fractions.",
          r"The volume $V\text{ m}^3$ of gas produced $t$ hours after mixing satisfies $\dfrac{dV}{dt}=\dfrac{5V}{(3t-2)(t+1)}$. After 3 hours, $V=7$.",
          r"(b) Show that $V=\dfrac{4(3t-2)}{t+1}$.",
          r"(c) Deduce the time delay before gas is produced, in minutes, and the limit of the volume produced."],
         [r"Spot: separate the variables. The right-hand side then needs the partial fractions from (a).",
          r"Use: $\dfrac{5}{(3x-2)(x+1)}=\dfrac{3}{3x-2}-\dfrac{1}{x+1}$.",
          r"(b) $\ln V=\ln(3t-2)-\ln(t+1)+c\Rightarrow V=\dfrac{A(3t-2)}{t+1}$. $V(3)=\dfrac{7A}{4}=7\Rightarrow A=4$.",
          r"(c) $V=0$ at $t=\tfrac23$ h, so the delay is 40 minutes. As $t\to\infty$, $V\to12\text{ m}^3$."],
         [r"Separate the variables and use the partial fractions from (a)",
          r"Integrate $5V$ with respect to $t$",
          r"Differentiate the partial fractions",
          r"Assume $V$ is constant"],
         ask="How do you start part (b)?"),
    card(2, 15,
         [r"The first three terms of a geometric series are $8\cos\theta$, $3+2\sin\theta$ and $4\tan\theta$.",
          r"(a) Show that $4\sin^2\theta-20\sin\theta+9=0$.",
          r"(b) Given that $\theta$ is obtuse and in radians, find its exact value.",
          r"(c) Show that the sum to infinity is $k(1-\sqrt3)$, where $k$ is a constant to be found."],
         [r"Spot: three terms in a GP means the middle term squared equals the product of the outer two.",
          r"Use: $(3+2\sin\theta)^2=8\cos\theta\cdot4\tan\theta=32\sin\theta$.",
          r"(a) $9+12\sin\theta+4\sin^2\theta=32\sin\theta$, which rearranges to the quadratic.",
          r"(b) $(2\sin\theta-1)(2\sin\theta-9)=0$, so $\sin\theta=\tfrac12$ and, since it's obtuse, $\theta=\dfrac{5\pi}{6}$.",
          r"(c) $a=8\cos\dfrac{5\pi}{6}=-4\sqrt3$ and $r=\dfrac{4}{-4\sqrt3}=-\dfrac{1}{\sqrt3}$",
          r"$S_\infty=\dfrac{-4\sqrt3}{1+\frac{1}{\sqrt3}}=-\dfrac{12}{\sqrt3+1}=6(1-\sqrt3)$, so $k=6$."],
         [r"Use $(\text{middle})^2=\text{first}\times\text{third}$",
          r"Use $\text{middle}=\dfrac{\text{first}+\text{third}}{2}$",
          r"Set the first term equal to the third",
          r"Use $S_\infty$ straight away"]),
    card(2, 16,
         [r"$C$ has parametric equations $x=2\tan t-1$, $y=3\sec^2t-1$, $-\dfrac{\pi}{4}\le t\le\dfrac{\pi}{3}$. The line $l$ is the normal to $C$ at $t=\dfrac{\pi}{4}$.",
          r"(a) Show that $l$ has equation $y=-\dfrac13x+\dfrac{16}{3}$.",
          r"(b) Show that all points on $C$ satisfy $y=\dfrac34(x+1)^2+2$.",
          r"(c) The line $y=-\dfrac13x+k$ meets $C$ at two distinct points. Find the possible values of $k$."],
         [r"Spot: parametric gradient $\dfrac{dy/dt}{dx/dt}$. For the Cartesian equation, use $\sec^2t\equiv1+\tan^2t$. Two intersections on a limited curve means check the discriminant and the endpoints.",
          r"Use: $\dfrac{dy}{dx}=\dfrac{6\sec^2t\tan t}{2\sec^2t}=3\tan t$. The values of $x$ run from $-3$ to $2\sqrt3-1$.",
          r"(a) At $t=\dfrac{\pi}{4}$: the point is $(1,5)$ and the gradient is 3, so the normal has gradient $-\tfrac13$.",
          r"(b) $\tan t=\dfrac{x+1}{2}$, so $y=3\left(1+\dfrac{(x+1)^2}{4}\right)-1$.",
          r"(c) $9x^2+22x+33-12k=0$. Two roots need $432k-704>0$, so $k>\tfrac{44}{27}$. The endpoint $(-3,5)$ gives $k=4$.",
          r"Answer: $\dfrac{44}{27}<k\le4$"],
         [r"Use $\dfrac{dy}{dx}=\dfrac{dy/dt}{dx/dt}$ at $t=\frac{\pi}{4}$, then the perpendicular gradient",
          r"Differentiate $y$ with respect to $t$ only",
          r"Use the gradient of the tangent for the normal",
          r"Eliminate $t$ using $\sin^2t+\cos^2t=1$"],
         ask="How do you start part (a)?"),
]


def check():
    # P1 Q2
    assert sp.solve(((x - 3) * (x**2 + 2 * x + k) + 36).subs(x, -1), k) == [10]
    # P1 Q3
    assert same(x**2 + y**2 + 6 * x - 8 * y - 24, (x + 3)**2 + (y - 4)**2 - 49)
    # P1 Q4
    assert same(sp.integrate(3 / x, (x, sp.Rational(3, 2), sp.Rational(15, 2))), sp.log(125))
    # P1 Q5
    a5 = (5.5**2 - 2.8**2) / 9
    b5 = 2.8**2 - 3 * a5
    assert round(a5, 2) == 2.49 and round(b5, 3) == 0.370 and round(math.sqrt(20 * a5 + b5), 2) == 7.08
    # P1 Q6
    f6 = x * (x - 3)**2
    assert f6.subs(x, 1) == 4 and sorted(sp.solve(sp.diff(f6, x), x)) == [1, 3]
    # P1 Q7
    for xv in range(-20, 0):
        for yv in range(-60, 60):
            if (xv - yv)**2 < 5 * xv * xv + yv * yv:
                assert yv < -2 * xv
    # P1 Q8
    v = (12 - t / 2) * sp.log(t + 1)
    assert sp.solve(12 - t / 2, t) == [24]
    lhs = sp.diff(v, t)
    assert identity(lhs * (t + 1) * 2 - (25 - (t + 1) * (1 + sp.log(t + 1))), t, 0.5, 20)
    ts = [6.0]
    for _ in range(60):
        ts.append(25 / (1 + math.log(ts[-1] + 1)) - 1)
    assert round(ts[1], 3) == 7.486 and round(ts[2], 3) == 6.966 and round(ts[-1], 2) == 7.09
    # P1 Q9
    PQ, QR = sp.Matrix([2, 6, 3]), sp.Matrix([6, -2, 3])
    assert PQ.norm() == 7 == QR.norm() and PQ.dot(QR) == 9
    assert same(PQ.cross(QR).norm(), 4 * sp.sqrt(145)) and same(sp.sqrt(2320), 4 * sp.sqrt(145))
    # P1 Q10
    assert round(6 * math.exp(0.6), 1) == 10.9
    uu = (-1 + math.sqrt(1 + 3600)) / 30
    T = 25 * math.log(uu)
    assert round(uu, 3) == 1.967 and round(T, 2) == 16.91
    assert close(30 + 150 * math.exp(0.04 * T), 20 + 600 * math.exp(-0.04 * T))
    # P1 Q11
    cub = 2 * x**3 + 5 - (23 * x - 9 * x**2 - 4)
    assert cub.subs(x, sp.Rational(1, 2)) == 0 and (2 * sp.Rational(1, 8) + 5) == sp.Rational(21, 4)
    assert same(cub, (2 * x - 1) * (x**2 + 5 * x - 9))
    # P1 Q12
    F12 = sp.Rational(2, 3) * x**sp.Rational(3, 2) * sp.log(x) - sp.Rational(4, 9) * x**sp.Rational(3, 2)
    assert identity(sp.diff(F12, x) - sp.sqrt(x) * sp.log(x), x, 0.5, 8)
    assert same(F12.subs(x, sp.E**2) - F12.subs(x, 1), sp.Rational(8, 9) * sp.E**3 + sp.Rational(4, 9))
    # P1 Q13
    nn = sp.symbols("nn")
    S = nn / 2 * (2 * 12 + (nn - 1) * sp.Rational(-1, 2))
    assert same(sp.expand(4 * (S - sp.Rational(245, 2))), -(nn**2 - 49 * nn + 490))
    assert sorted(sp.solve(nn**2 - 49 * nn + 490, nn)) == [14, 35]
    assert 12 - 0.5 * 24 == 0 and 12 - 0.5 * 25 < 0
    # P1 Q14
    tx = math.sqrt(3) / 9
    xr = math.atan(tx)
    assert abs(2 * math.cos(xr + math.pi / 3) - math.sin(xr + math.pi / 6)) < 1e-12
    base = math.degrees(xr)
    th = [(base + 60) / 2, (base + 240) / 2]
    for d in th:
        r_ = math.radians(d)
        assert abs(2 * math.cos(2 * r_) - math.sin(2 * r_ - math.pi / 6)) < 1e-9
    assert [round(d, 1) for d in th] == [35.4, 125.4] and round(base, 1) == 10.9
    # P1 Q15
    rr = sp.symbols("rr", positive=True)
    hh = 300 / (sp.Rational(6, 10) * rr**2)
    Ssurf = 2 * sp.Rational(6, 10) * rr**2 + (2 * rr + sp.Rational(12, 10) * rr) * hh
    assert same(Ssurf, sp.Rational(6, 5) * rr**2 + 1600 / rr)
    ropt = (2000 / 3)**(1 / 3)
    assert round(ropt, 2) == 8.74
    # P1 Q16
    integrand = (3 * sp.sin(2 * t) + 2 * sp.sin(t)) * sp.diff(4 * sp.sin(t)**2, t)
    assert identity(integrand - (6 - 6 * sp.cos(4 * t) + 16 * sp.sin(t)**2 * sp.cos(t)), t)
    area = sp.integrate(6 - 6 * sp.cos(4 * t) + 16 * sp.sin(t)**2 * sp.cos(t), (t, 0, sp.pi / 4))
    assert same(area, 3 * sp.pi / 2 + 4 * sp.sqrt(2) / 3)
    assert same((4 * sp.sin(sp.pi / 4)**2), 2)

    # P2 Q1
    for xv in (-1, 7):
        assert abs(5 - 3 * xv) == 9 + xv
    # P2 Q2
    assert round(math.log(80) / math.log(5), 2) == 2.72
    # P2 Q3
    seq = [sp.Integer(4)]
    for _ in range(39):
        seq.append(1 / (1 - seq[-1]))
    assert seq[:4] == [4, -sp.Rational(1, 3), sp.Rational(3, 4), 4] and sum(seq) == sp.Rational(737, 12)
    # P2 Q4
    hs = sp.symbols("hs")
    fd = ((3 * (x + hs)**2 - 5 * (x + hs)) - (3 * x**2 - 5 * x)) / hs
    assert same(sp.simplify(fd), 6 * x + 3 * hs - 5)
    # P2 Q5
    ys = [round(math.log2(3 * v), 2) for v in (2, 3, 4, 5, 6)]
    assert ys == [2.58, 3.17, 3.58, 3.91, 4.17]
    est = 0.5 * ((2.58 + 4.17) + 2 * (3.17 + 3.58 + 3.91))
    assert close(est, 14.035) and round(3 * est, 1) == 42.1 and round(8 + est, 1) == 22.0
    # P2 Q6
    f = lambda v: 10 * math.sin(v / 2) - 4 * v + 6
    fp = lambda v: 5 * math.cos(v / 2) - 4
    assert round(2 * math.acos(0.8), 2) == 1.29 and round(f(3), 3) == 3.975 and round(f(4), 3) == -0.907
    assert round(4 - f(4) / fp(4), 2) == 3.85
    # P2 Q7
    ser = sp.series(sp.sqrt(9 - 8 * x), x, 0, 4).removeO()
    assert same(ser, 3 - sp.Rational(4, 3) * x - sp.Rational(8, 27) * x**2 - sp.Rational(32, 243) * x**3)
    assert same(sp.sqrt(9 - 8 * sp.Rational(3, 4)), sp.sqrt(3)) and ser.subs(x, sp.Rational(3, 4)) > sp.sqrt(3)
    # P2 Q8
    xp = sp.symbols("xp", positive=True)
    Y = (xp - 1) * (xp - 2) / (3 * sp.sqrt(xp))
    integral = sp.integrate(Y, (xp, 1, 2))
    assert float(integral) < 0 and same(-integral, sp.Rational(4, 5) - sp.Rational(8, 15) * sp.sqrt(2))
    # P2 Q9
    assert round(math.degrees(math.asin(2 / 64)), 2) == 1.79 and 180 / 900 == 0.2
    # P2 Q10
    f10 = (6 * x + 1) / (3 * x + 2)
    assert sp.solve(sp.Eq(f10, 1), x) == [sp.Rational(1, 3)] and same(f10, 2 - 3 / (3 * x + 2))
    assert f10.subs(x, 0) == sp.Rational(1, 2) and f10.subs(x, 3) == sp.Rational(19, 11)
    # P2 Q11
    assert all((m * m + 3 * m + 5) % 2 == 1 for m in range(0, 500))
    # P2 Q12
    kp = sp.symbols("kp", positive=True)
    F = sp.exp(2 * x) / (x**2 + kp)
    assert same(sp.diff(F, x), (x**2 - x + kp) * 2 * sp.exp(2 * x) / (x**2 + kp)**2)
    # P2 Q13
    A, B = sp.Matrix([2, 1, -3]), sp.Matrix([0, 3, 1])
    C = sp.Matrix([-4, 7, 9])
    assert C - A == 3 * (B - A)
    D = 3 * B
    assert (D - C) == 2 * A and same(D.norm(), 3 * sp.sqrt(10))
    # P2 Q14
    assert same(5 / ((3 * x - 2) * (x + 1)), 3 / (3 * x - 2) - 1 / (x + 1))
    V = 4 * (3 * t - 2) / (t + 1)
    assert V.subs(t, 3) == 7 and same(sp.diff(V, t) - 5 * V / ((3 * t - 2) * (t + 1)), 0)
    assert sp.solve(V, t) == [sp.Rational(2, 3)] and sp.limit(V, t, sp.oo) == 12
    # P2 Q15
    s = sp.symbols("s")
    assert same(sp.expand((3 + 2 * s)**2 - 32 * s), 4 * s**2 - 20 * s + 9)
    a1 = 8 * sp.cos(5 * sp.pi / 6)
    r = (3 + 2 * sp.sin(5 * sp.pi / 6)) / a1
    assert same(r * (3 + 2 * sp.sin(5 * sp.pi / 6)), 4 * sp.tan(5 * sp.pi / 6))
    assert same(a1 / (1 - r), 6 * (1 - sp.sqrt(3)))
    # P2 Q16
    X = 2 * sp.tan(t) - 1
    Yp = 3 / sp.cos(t)**2 - 1
    grad = sp.diff(Yp, t) / sp.diff(X, t)
    assert same(grad.subs(t, sp.pi / 4), 3) and same(X.subs(t, sp.pi / 4), 1) and same(Yp.subs(t, sp.pi / 4), 5)
    assert identity(Yp - (sp.Rational(3, 4) * (X + 1)**2 + 2), t, -0.7, 1.0)
    kk = sp.symbols("kk")
    quad = sp.expand(12 * (sp.Rational(3, 4) * (x + 1)**2 + 2 - (-x / 3 + kk)))
    assert same(quad, 9 * x**2 + 22 * x + 33 - 12 * kk)
    assert sp.solve(sp.discriminant(quad, x), kk) == [sp.Rational(44, 27)]
    xmin, xmax = -3, 2 * math.sqrt(3) - 1
    for kv in (1.7, 2.5, 3.9, 4.0):
        roots = [complex(v) for v in sp.solve(quad.subs(kk, kv), x)]
        assert sum(abs(r_.imag) < 1e-12 and xmin - 1e-9 <= r_.real <= xmax for r_ in roots) == 2, kv
    for kv in (4.1, 1.6):
        roots = [complex(v) for v in sp.solve(quad.subs(kk, kv), x)]
        assert sum(abs(r_.imag) < 1e-12 and xmin - 1e-9 <= r_.real <= xmax for r_ in roots) < 2, kv
