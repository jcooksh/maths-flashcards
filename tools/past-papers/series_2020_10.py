"""October 2020 (9MA0/01 and 9MA0/02), with the numbers changed."""
import math
import sympy as sp
from common import card, close, same, identity, x, y, t, k, theta

SERIES = {"id": "paper-2020-10", "title": "October 2020", "hue": 80}

CARDS = [
    # ---------------- Paper 1 ----------------
    card(1, 1,
         [r"(a) Find the first four terms, in ascending powers of $x$, of the binomial expansion of $(1-6x)^{\frac12}$.",
          r"(b) Explain how you could use $x=\dfrac{1}{24}$ in the expansion to find an approximation for $\sqrt3$. (You don't need to carry out the calculation.)"],
         [r"Spot: a fractional power of $(1+\text{something})$ means the binomial series from the formula booklet.",
          r"Use: $(1+x)^n=1+nx+\dfrac{n(n-1)}{2!}x^2+\dfrac{n(n-1)(n-2)}{3!}x^3$, with $n=\tfrac12$ and $x$ replaced by $-6x$.",
          r"(a) $1-3x-\dfrac92x^2-\dfrac{27}{2}x^3$",
          r"(b) $x=\dfrac{1}{24}$ gives $\sqrt{1-\tfrac14}=\dfrac{\sqrt3}{2}$. Substitute it into the expansion and double the result. It's valid because $|6x|<1$."],
         [r"Use the binomial series with $n=\tfrac12$, replacing $x$ by $-6x$",
          r"Use the binomial series with $n=2$",
          r"Expand $(1-6x)^{\frac12}$ as $1-(6x)^{\frac12}$",
          r"Use Pascal's triangle"]),
    card(1, 2,
         [r"By taking logarithms of both sides, solve $3^{2p+1}=7^{150}$, giving $p$ to one decimal place."],
         [r"Spot: the unknown is in a power, so take logs of both sides.",
          r"Use: $\log a^n=n\log a$.",
          r"Method: $(2p+1)\ln3=150\ln7\Rightarrow2p+1=\dfrac{150\ln7}{\ln3}\approx265.69$",
          r"Answer: $p\approx132.3$"],
         [r"Take logs: $(2p+1)\ln3=150\ln7$",
          r"Divide both sides by 3",
          r"Write $7^{150}$ as $(3+4)^{150}$",
          r"Take logs to get $\ln(2p+1)=\ln150$"]),
    card(1, 3,
         [r"Relative to a fixed origin $O$, $A$ has position vector $3\mathbf{i}+2\mathbf{j}-5\mathbf{k}$, $B$ has $5\mathbf{i}-\mathbf{j}-\mathbf{k}$ and $C$ has $4\mathbf{i}-6\mathbf{j}+8\mathbf{k}$.",
          r"(a) Find $\overrightarrow{AB}$.",
          r"(b) Show that the quadrilateral $OABC$ is a trapezium, giving reasons."],
         [r"Spot: a trapezium has exactly one pair of parallel sides. Parallel vectors are scalar multiples of each other.",
          r"Use: $\overrightarrow{AB}=\mathbf{b}-\mathbf{a}$, and compare $\overrightarrow{OC}$ with $\overrightarrow{AB}$.",
          r"(a) $\overrightarrow{AB}=2\mathbf{i}-3\mathbf{j}+4\mathbf{k}$",
          r"(b) $\overrightarrow{OC}=2\overrightarrow{AB}$, so $OC$ is parallel to $AB$. $\overrightarrow{OA}$ and $\overrightarrow{BC}=-\mathbf{i}-5\mathbf{j}+9\mathbf{k}$ aren't parallel, so $OABC$ is a trapezium."],
         [r"Find $\overrightarrow{AB}$ and check whether $\overrightarrow{OC}$ is a multiple of it",
          r"Show that all four sides have equal length",
          r"Show that $\overrightarrow{OA}\cdot\overrightarrow{OB}=0$",
          r"Find the midpoint of $AC$"]),
    card(1, 4,
         [r"$f(x)=\dfrac{2x+5}{x-3}$, $x\in\mathbb{R}$, $x\ne3$",
          r"(a) Find $f^{-1}(4)$.",
          r"(b) Show that $ff(x)=\dfrac{ax+b}{14-x}$, where $a$ and $b$ are integers to be found."],
         [r"Spot: $f^{-1}(4)$ is the input that $f$ sends to 4, so solve $f(x)=4$. For $ff(x)$, substitute $f(x)$ into $f$.",
          r"Use: multiply the top and bottom by $(x-3)$ to clear the fraction inside the fraction.",
          r"(a) $2x+5=4x-12\Rightarrow x=\dfrac{17}{2}$",
          r"(b) $ff(x)=\dfrac{2\left(\frac{2x+5}{x-3}\right)+5}{\frac{2x+5}{x-3}-3}=\dfrac{2(2x+5)+5(x-3)}{(2x+5)-3(x-3)}=\dfrac{9x-5}{14-x}$",
          r"Answer: $a=9$ and $b=-5$"],
         [r"Solve $f(x)=4$ for $x$",
          r"Work out $\dfrac{1}{f(4)}$",
          r"Substitute $x=4$ into $f(x)$",
          r"Find $f'(4)$"],
         ask="How do you find $f^{-1}(4)$ quickly?"),
    card(1, 5,
         [r"A bicycle has 7 gears. Its fastest speed is 12 km h$^{-1}$ in 1st gear and 42 km h$^{-1}$ in 7th gear.",
          r"(a) If the fastest speeds in successive gears form an arithmetic sequence, find the fastest speed in 3rd gear.",
          r"(b) If they form a geometric sequence instead, find the fastest speed in 5th gear."],
         [r"Spot: “arithmetic” means add a common difference $d$. “Geometric” means multiply by a common ratio $r$.",
          r"Use: $u_n=a+(n-1)d$ and $u_n=ar^{n-1}$, with $u_1=12$ and $u_7=42$.",
          r"(a) $12+6d=42\Rightarrow d=5$, so $u_3=12+2(5)=22\text{ km h}^{-1}$",
          r"(b) $12r^6=42\Rightarrow r=3.5^{\frac16}\approx1.232$, so $u_5=12r^4\approx27.7\text{ km h}^{-1}$"],
         [r"Use $u_7=u_1+6d$ to find $d$",
          r"Use $u_7=u_1+7d$ to find $d$",
          r"Divide 42 by 7",
          r"Use $S_n$ with $n=7$"]),
    card(1, 6,
         [r"(a) Express $2\sin x+3\cos x$ in the form $R\sin(x+\alpha)$, where $R>0$ and $0<\alpha<\dfrac{\pi}{2}$. Give $R$ exactly and $\alpha$ to 3 decimal places.",
          r"The temperature $\theta\,^\circ$C in a room is modelled by $\theta=12+2\sin\left(\dfrac{\pi t}{12}-2\right)+3\cos\left(\dfrac{\pi t}{12}-2\right)$, $0\le t<24$, where $t$ is hours after midnight.",
          r"(b) Deduce the maximum temperature.",
          r"(c) Find the time of day when it occurs, to the nearest minute."],
         [r"Spot: $a\sin x+b\cos x$ means use the R-form, and the maximum is when the sine equals 1.",
          r"Use: $R\cos\alpha=2$, $R\sin\alpha=3$, so $R=\sqrt{13}$ and $\tan\alpha=\tfrac32$.",
          r"(a) $\sqrt{13}\sin(x+0.983)$",
          r"(b) $12+\sqrt{13}\approx15.6\,^\circ$C",
          r"(c) $\dfrac{\pi t}{12}-2+0.983=\dfrac{\pi}{2}\Rightarrow t\approx9.885$ hours",
          r"Answer: 9:53 am"],
         [r"Use $R\cos\alpha=2$ and $R\sin\alpha=3$ to find $R$ and $\alpha$",
          r"Use $R=2+3$ and $\tan\alpha=\tfrac23$",
          r"Square both terms and add",
          r"Differentiate and set the result to zero"]),
    card(1, 7,
         [r"A curve $C$ with equation $y=f(x)$, where $f$ is quadratic, has its minimum turning point at $(1,4)$.",
          r"A straight line $l$ meets $C$ at $(1,4)$ and $(3,12)$. The region $R$ lies between $C$ and $l$.",
          r"Use inequalities to define $R$."],
         [r"Spot: you know the vertex of a quadratic, so use vertex form $y=a(x-p)^2+q$. A region between two graphs means $\text{lower}\le y\le\text{upper}$.",
          r"Use: $f(x)=a(x-1)^2+4$, and substitute $(3,12)$ to find $a$.",
          r"Method: $4a+4=12\Rightarrow a=2$, so $f(x)=2x^2-4x+6$. The line through $(1,4)$ and $(3,12)$ is $y=4x$.",
          r"Answer: $2x^2-4x+6\le y\le4x$ (which only holds for $1\le x\le3$)"],
         [r"Write $f(x)=a(x-1)^2+4$ and use $(3,12)$ to find $a$",
          r"Use $f(x)=x^2+4$",
          r"Integrate between $x=1$ and $x=3$",
          r"Write $f(x)=a(x-3)(x-1)$"]),
    card(1, 8,
         [r"The number of followers $N$ of an account, $t$ days after it was set up, increases at a rate proportional to $\sqrt N$.",
          r"Use this information to find a suitable equation for $N$ in terms of $t$."],
         [r"Spot: “rate of increase … proportional to $\sqrt N$” translates to $\dfrac{dN}{dt}=k\sqrt N$. Then separate the variables.",
          r"Use: $\displaystyle\int N^{-\frac12}\,dN=2N^{\frac12}$.",
          r"Method: $2\sqrt N=kt+c\Rightarrow\sqrt N=\dfrac{kt+c}{2}$",
          r"Answer: $N=(at+b)^2$ for constants $a$ and $b$"],
         [r"Write $\dfrac{dN}{dt}=k\sqrt N$ and separate the variables",
          r"Write $N=k\sqrt t$",
          r"Write $N=Ae^{kt}$",
          r"Write $\dfrac{dN}{dt}=\dfrac{k}{\sqrt N}$"]),
    card(1, 9,
         [r"$f(x)=2(x^2-3)e^{-x}$, $x\in\mathbb{R}$",
          r"(a) Show that $f'(x)=2(3+2x-x^2)e^{-x}$.",
          r"(b) Hence find the exact coordinates of the stationary points.",
          r"$g(x)=3f(x)$ for $x\in\mathbb{R}$, and $h(x)=3f(x)-5$ for $x\ge0$.",
          r"(c) Find the range of $g$ and the range of $h$."],
         [r"Spot: a polynomial times an exponential means the product rule, then factorise out $e^{-x}$.",
          r"Use: $\dfrac{d}{dx}e^{-x}=-e^{-x}$, and $e^{-x}>0$, so set the quadratic to zero.",
          r"(a) $4xe^{-x}-2(x^2-3)e^{-x}=2(3+2x-x^2)e^{-x}$",
          r"(b) $x^2-2x-3=0\Rightarrow x=3$ or $-1$: $(3,\,12e^{-3})$ and $(-1,\,-4e)$",
          r"(c) $f\ge-4e$, so $g(x)\ge-12e$. For $x\ge0$: $f(0)=-6$ and the maximum is $12e^{-3}$, so $-23\le h(x)\le36e^{-3}-5$."],
         [r"Use the product rule with $u=2(x^2-3)$ and $v=e^{-x}$",
          r"Differentiate $x^2-3$ and $e^{-x}$ separately and multiply",
          r"Use the quotient rule with denominator $e^{x}$, then set the denominator to zero",
          r"Take logs first"]),
    card(1, 10,
         [r"(a) Use the substitution $x=u^2+1$ to show that $\displaystyle\int_5^{17}\frac{2\,dx}{(x-1)\left(1+\sqrt{x-1}\right)}=\int_p^q\frac{4\,du}{u(1+u)}$, where $p$ and $q$ are positive constants to be found.",
          r"(b) Hence, using algebraic integration, show that the integral equals $\ln a$, where $a$ is a rational constant to be found."],
         [r"Spot: a given substitution means change the $x$s, the $dx$ and the limits. A fraction like $\dfrac{4}{u(1+u)}$ means partial fractions.",
          r"Use: $dx=2u\,du$, $\sqrt{x-1}=u$, and $x=5\to u=2$, $x=17\to u=4$.",
          r"(a) $\dfrac{2\cdot2u\,du}{u^2(1+u)}=\dfrac{4\,du}{u(1+u)}$ with $p=2$ and $q=4$",
          r"(b) $\dfrac{4}{u(1+u)}=\dfrac4u-\dfrac{4}{1+u}$, so the integral is $\left[4\ln u-4\ln(1+u)\right]_2^4=4\ln\dfrac45-4\ln\dfrac23=4\ln\dfrac65$",
          r"Answer: $a=\left(\dfrac65\right)^4=\dfrac{1296}{625}$"],
         [r"Replace $x$, $dx=2u\,du$ and the limits using $x=u^2+1$",
          r"Replace $x$ with $u^2+1$ but keep $dx$ and the limits",
          r"Integrate with respect to $x$ first, then substitute",
          r"Use integration by parts"]),
    card(1, 11,
         [r"Circle $C_1$ has equation $x^2+y^2=25$ and circle $C_2$ has equation $(x-8)^2+y^2=18$. They meet at $A$ and $B$.",
          r"(a) Show that angle $AOB=0.958$ radians to 3 s.f., where $O$ is the origin.",
          r"(b) The region inside both circles is shaded. Find its perimeter to 1 decimal place."],
         [r"Spot: two circles meeting means subtract their equations to get $x$ at the intersections. A perimeter made of arcs means $s=r\theta$ for each arc.",
          r"Use: angles found from right-angled triangles. Each arc uses its own circle's radius and centre angle.",
          r"(a) $x^2-(x-8)^2=7\Rightarrow16x=71\Rightarrow x=4.4375$, $y=\pm2.304$, so $\angle AOB=2\arctan\dfrac{2.304}{4.4375}\approx0.958$",
          r"(b) The angle at $C_2$'s centre is $2\arctan\dfrac{2.304}{3.5625}\approx1.148$.",
          r"Perimeter $=5(0.958)+\sqrt{18}(1.148)\approx9.7$"],
         [r"Subtract the circle equations to find the $x$-coordinate of $A$ and $B$",
          r"Add the two radii",
          r"Use the cosine rule with sides 25 and 18",
          r"Set the two $y$ values equal and solve a cubic"]),
    card(1, 12,
         [r"(a) Show that $\sec\theta-\cos\theta\equiv\sin\theta\tan\theta$, $\theta\ne(90+180n)^\circ$.",
          r"(b) Hence, or otherwise, solve for $0<x<180^\circ$: $\sec x-\cos x=\sin x\tan(3x-40^\circ)$."],
         [r"Spot: “hence” means rewrite the left-hand side using (a). Then the same factor appears on both sides, so factorise instead of cancelling.",
          r"Use: $\sec\theta-\cos\theta=\dfrac{1-\cos^2\theta}{\cos\theta}=\dfrac{\sin^2\theta}{\cos\theta}$, and $\tan A=\tan B\Rightarrow A=B+180n$.",
          r"(b) $\sin x\tan x=\sin x\tan(3x-40^\circ)$. $\sin x=0$ has no solutions in the interval, so $\tan x=\tan(3x-40^\circ)$.",
          r"$3x-40=x+180n\Rightarrow x=20+90n$",
          r"Answer: $x=20^\circ,\ 110^\circ$"],
         [r"Use (a) to replace the left side with $\sin x\tan x$, then compare",
          r"Divide both sides by $\sin x$ and $\cos x$ and stop there",
          r"Expand $\tan(3x-40^\circ)$ using the compound angle formula",
          r"Square both sides"],
         ask="How do you start part (b)?"),
    card(1, 13,
         [r"A sequence is defined by $a_{n+1}=\dfrac{k(a_n+3)}{a_n}$, $n\in\mathbb{N}$, where $k$ is a constant. The sequence is periodic of order 3, and $a_1=3$.",
          r"(a) Show that $2k^2+3k-9=0$.",
          r"(b) Explain why $k\ne\dfrac32$.",
          r"(c) Find $\displaystyle\sum_{r=1}^{50}a_r$."],
         [r"Spot: “periodic of order 3” means $a_4=a_1$. Generate the terms in terms of $k$.",
          r"Use: $a_2=2k$, $a_3=\dfrac{2k+3}{2}$, $a_4=\dfrac{k(2k+9)}{2k+3}$.",
          r"(a) $\dfrac{k(2k+9)}{2k+3}=3\Rightarrow2k^2+9k=6k+9\Rightarrow2k^2+3k-9=0$",
          r"(b) If $k=\tfrac32$ then $a_2=3=a_1$, so the order would be 1, not 3.",
          r"(c) $k=-3$: $3,-6,-\tfrac32,3,\dots$. Sixteen full cycles give $16\times(-4.5)=-72$, plus $a_{49}+a_{50}=3-6$.",
          r"Answer: $-75$"],
         [r"Generate $a_2$, $a_3$, $a_4$ in terms of $k$ and set $a_4=a_1$",
          r"Set $a_2=a_1$",
          r"Use the arithmetic series formula",
          r"Set $a_3=0$"]),
    card(1, 14,
         [r"A spherical balloon is deflating. At time $t$ s, its radius is $r$ cm and its volume is $V\text{ cm}^3$. The volume decreases at a constant rate.",
          r"(a) Show that $\dfrac{dr}{dt}=-\dfrac{k}{r^2}$, where $k$ is a positive constant.",
          r"The initial radius is 30 cm. After 4 seconds, the radius is 15 cm.",
          r"(b) Solve the differential equation to find an equation linking $r$ and $t$.",
          r"(c) Find the values of $t$ for which this equation is valid."],
         [r"Spot: a rate for $V$ and a question about $r$ means connect them with the chain rule, $\dfrac{dV}{dt}=\dfrac{dV}{dr}\cdot\dfrac{dr}{dt}$.",
          r"Use: $V=\tfrac43\pi r^3$, so $\dfrac{dV}{dr}=4\pi r^2$. Then separate the variables.",
          r"(a) $4\pi r^2\dfrac{dr}{dt}=-c\Rightarrow\dfrac{dr}{dt}=-\dfrac{k}{r^2}$",
          r"(b) $\dfrac{r^3}{3}=-kt+C$. Using $r=30$ at $t=0$ and $r=15$ at $t=4$: $r^3=27000-\dfrac{23625}{4}t$",
          r"(c) It's valid until the balloon is empty, at $r=0$: $0\le t\le\dfrac{32}{7}$"],
         [r"Use $\dfrac{dV}{dt}=4\pi r^2\dfrac{dr}{dt}$ with $\dfrac{dV}{dt}$ a negative constant",
          r"Write $r=30-kt$",
          r"Use $\dfrac{dr}{dt}=-k$",
          r"Differentiate $V=4\pi r^2$"]),
    card(1, 15,
         [r"The curve $C$ has equation $x^2\tan y=4$, $0<y<\dfrac{\pi}{2}$.",
          r"(a) Show that $\dfrac{dy}{dx}=\dfrac{-8x}{x^4+16}$.",
          r"(b) Prove that $C$ has a point of inflection at $x=\sqrt[4]{\tfrac{16}{3}}$."],
         [r"Spot: $x$ and $y$ mixed together means implicit differentiation. A point of inflection means $\dfrac{d^2y}{dx^2}=0$ and changes sign.",
          r"Use: $\dfrac{d}{dx}(\tan y)=\sec^2y\dfrac{dy}{dx}$, then $\tan y=\dfrac{4}{x^2}$ and $\sec^2y=1+\tan^2y$.",
          r"(a) $2x\tan y+x^2\sec^2y\dfrac{dy}{dx}=0\Rightarrow\dfrac{dy}{dx}=\dfrac{-2x\cdot\frac{4}{x^2}}{x^2\left(1+\frac{16}{x^4}\right)}=\dfrac{-8x}{x^4+16}$",
          r"(b) $\dfrac{d^2y}{dx^2}=\dfrac{-8(16-3x^4)}{(x^4+16)^2}$, which is $0$ at $x^4=\dfrac{16}{3}$ and changes sign there."],
         [r"Differentiate implicitly, using the product rule on $x^2\tan y$",
          r"Rearrange to $y=\arctan\dfrac{4}{x^2}$ and stop",
          r"Differentiate $\tan y$ as $\sec^2y$ without $\dfrac{dy}{dx}$",
          r"Take logs of both sides"]),
    card(1, 16,
         [r"Prove by contradiction that there are no positive integers $p$ and $q$ such that $9p^2-q^2=16$."],
         [r"Spot: “prove by contradiction” means assume solutions exist, then factorise the difference of two squares.",
          r"Use: $9p^2-q^2=(3p-q)(3p+q)$, and the factor pairs of 16.",
          r"Method: $3p+q>3p-q>0$ and both are integers with product 16, so the pairs are $(1,16)$, $(2,8)$ or $(4,4)$.",
          r"$(1,16)$ gives $6p=17$ and $(2,8)$ gives $6p=10$, so $p$ isn't an integer. $(4,4)$ gives $q=0$, which isn't positive.",
          r"Every case gives a contradiction, so there are no such $p$ and $q$."],
         [r"Assume there are solutions and factorise $(3p-q)(3p+q)=16$",
          r"Try $p=1,2,3$ and conclude",
          r"Assume $p$ and $q$ are both even",
          r"Use the quadratic formula on $9p^2=16+q^2$"]),

    # ---------------- Paper 2 ----------------
    card(2, 1,
         [r"The table shows values of $y=\sqrt{\dfrac{x}{x+3}}$ to 4 s.f.",
          r"$x$: 1, 1.5, 2, 2.5, 3. $y$: 0.5, 0.5774, 0.6325, 0.6742, 0.7071",
          r"(a) Use the trapezium rule with all of these values to estimate $\displaystyle\int_1^3\sqrt{\frac{x}{x+3}}\,dx$ to 3 s.f.",
          r"(b) Deduce an estimate for $\displaystyle\int_1^3\sqrt{\frac{4x}{x+3}}\,dx$.",
          r"(c) Given that the true value of the integral in (b) is 2.493 to 4 s.f., comment on the accuracy of your answer."],
         [r"Spot: “trapezium rule” with a table means the booklet formula with the strip width $h=0.5$.",
          r"Use: $\dfrac{h}{2}\left[y_0+y_n+2(y_1+\dots+y_{n-1})\right]$, and $\sqrt{4}=2$ comes out as a factor.",
          r"(a) $0.25\left[(0.5+0.7071)+2(0.5774+0.6325+0.6742)\right]\approx1.24$",
          r"(b) $\sqrt{\dfrac{4x}{x+3}}=2\sqrt{\dfrac{x}{x+3}}$, so the estimate is $2\times1.2438\approx2.49$",
          r"(c) It's a slight underestimate, but very close (an error of less than 0.5%)."],
         [r"Use the trapezium rule with $h=0.5$",
          r"Add the $y$ values and multiply by $0.5$",
          r"Use the trapezium rule with $h=1$",
          r"Integrate $\sqrt{\dfrac{x}{x+3}}$ by substitution"]),
    card(2, 2,
         [r"Points $P$, $Q$ and $R$ have position vectors $\mathbf{p}$, $\mathbf{q}$ and $\mathbf{r}$, and lie on a straight line.",
          r"$Q$ lies two fifths of the way from $P$ to $R$. Show that $\mathbf{q}=\dfrac15(3\mathbf{p}+2\mathbf{r})$."],
         [r"Spot: “a fraction of the way from $P$ to $R$” means start at $P$ and add that fraction of $\overrightarrow{PR}$.",
          r"Use: $\overrightarrow{PR}=\mathbf{r}-\mathbf{p}$.",
          r"Method: $\mathbf{q}=\mathbf{p}+\tfrac25(\mathbf{r}-\mathbf{p})=\tfrac35\mathbf{p}+\tfrac25\mathbf{r}=\tfrac15(3\mathbf{p}+2\mathbf{r})$"],
         [r"Write $\mathbf{q}=\mathbf{p}+\tfrac25(\mathbf{r}-\mathbf{p})$",
          r"Write $\mathbf{q}=\tfrac25(\mathbf{p}+\mathbf{r})$",
          r"Write $\mathbf{q}=\mathbf{r}+\tfrac25\mathbf{p}$",
          r"Write $\mathbf{q}=\tfrac25\mathbf{r}-\mathbf{p}$"]),
    card(2, 3,
         [r"(a) Given that $2\log(6-x)=\log(x+14)$, show that $x^2-13x+22=0$.",
          r"(b)(i) Write down the roots of $x^2-13x+22=0$.",
          r"(ii) State which root is not a solution of the log equation, giving a reason."],
         [r"Spot: a log equation means use the laws of logs to get $\log A=\log B$, then $A=B$. Always check the answers in the original logs.",
          r"Use: $2\log(6-x)=\log(6-x)^2$.",
          r"(a) $(6-x)^2=x+14\Rightarrow36-12x+x^2=x+14\Rightarrow x^2-13x+22=0$",
          r"(b)(i) $x=2$ or $x=11$",
          r"(ii) $x=11$ is not a solution: $6-x=-5$, and you can't take the log of a negative number."],
         [r"Use $2\log(6-x)=\log(6-x)^2$, then remove the logs",
          r"Use $2\log(6-x)=\log(12-2x)$",
          r"Divide both sides by $\log$",
          r"Take $e$ to the power of each term separately"]),
    card(2, 4,
         [r"In the binomial expansion of $(a+3x)^6$, where $a$ is a constant, the coefficient of $x^3$ is $-4320$.",
          r"Find the value of $a$."],
         [r"Spot: a single coefficient means use one general term, $\binom{n}{r}a^{n-r}(bx)^r$.",
          r"Use: $\binom63a^3(3x)^3$.",
          r"Method: $20\times27\times a^3=540a^3=-4320\Rightarrow a^3=-8$",
          r"Answer: $a=-2$"],
         [r"Use the $x^3$ term $\binom63a^3(3x)^3$ and set its coefficient to $-4320$",
          r"Use the $x^3$ term $\binom63a^3(3x)^3$ but forget to cube the 3",
          r"Expand $(1+3x)^6$ and multiply by $a$",
          r"Use $\binom64a^4(3x)^2$"]),
    card(2, 5,
         [r"The curve $y=2\times5^x$ meets the curve $y=24-5^{x+1}$ at the point $P$.",
          r"Find, using algebra, the exact $x$-coordinate of $P$."],
         [r"Spot: powers of the same base on both sides means write $5^{x+1}$ as $5\times5^x$ and treat $5^x$ like a single unknown.",
          r"Use: $5^{x+1}=5\cdot5^x$, then logs.",
          r"Method: $2\cdot5^x=24-5\cdot5^x\Rightarrow7\cdot5^x=24\Rightarrow5^x=\dfrac{24}{7}$",
          r"Answer: $x=\dfrac{\ln\frac{24}{7}}{\ln5}$"],
         [r"Write $5^{x+1}=5\times5^x$ and collect the $5^x$ terms",
          r"Take logs of each term separately",
          r"Write $5^{x+1}=5^x+5$",
          r"Square both sides"]),
    card(2, 6,
         [r"(a) Given that $\dfrac{2x^2+7x-1}{x+3}\equiv Ax+B+\dfrac{C}{x+3}$, find $A$, $B$ and $C$.",
          r"(b) Hence find the exact value of $\displaystyle\int_0^3\frac{2x^2+7x-1}{x+3}\,dx$, in the form $a+b\ln2$, where $a$ and $b$ are integers."],
         [r"Spot: the top has a higher degree than the bottom, so divide first (algebraic division) to get a polynomial plus a proper fraction.",
          r"Use: $\displaystyle\int\frac{C}{x+3}\,dx=C\ln|x+3|$.",
          r"(a) $2x^2+7x-1=(x+3)(2x+1)-4$, so $A=2$, $B=1$, $C=-4$.",
          r"(b) $\left[x^2+x-4\ln(x+3)\right]_0^3=12-4\ln6+4\ln3$",
          r"Answer: $12-4\ln2$"],
         [r"Divide $2x^2+7x-1$ by $x+3$, then integrate term by term",
          r"Integrate the top and bottom separately",
          r"Use integration by parts",
          r"Write it as $\ln(2x^2+7x-1)$ divided by $\ln(x+3)$"]),
    card(2, 7,
         [r"The curve $C$ has equation $y=\dfrac{9x^2+2x}{3\sqrt x}-6\ln x$, $x>0$.",
          r"(a) Show that $\dfrac{dy}{dx}=\dfrac{27x^2+2x-36\sqrt x}{6x\sqrt x}$.",
          r"(b) Show that the $x$-coordinate of the minimum point $P$ satisfies $x=\left(\dfrac43-\dfrac{2\sqrt x}{27}\right)^{\frac23}$.",
          r"(c) Use $x_{n+1}=\left(\dfrac43-\dfrac{2\sqrt{x_n}}{27}\right)^{\frac23}$ with $x_1=1$ to find $x_2$ to 5 d.p. and the $x$-coordinate of $P$ to 5 d.p."],
         [r"Spot: a fraction with $\sqrt x$ underneath means split it into separate powers of $x$ before differentiating.",
          r"Use: $y=3x^{\frac32}+\tfrac23x^{\frac12}-6\ln x$.",
          r"(a) $\dfrac{dy}{dx}=\tfrac92x^{\frac12}+\tfrac13x^{-\frac12}-\dfrac6x$. Put this over the common denominator $6x\sqrt x$.",
          r"(b) Set $27x^2+2x=36\sqrt x$ and divide by $27\sqrt x$: $x^{\frac32}=\dfrac43-\dfrac{2\sqrt x}{27}$",
          r"(c) $x_2=1.16612$, and the iterates converge to $x=1.16254$"],
         [r"Split the fraction into powers of $x$, then differentiate term by term",
          r"Use the quotient rule on the whole of $y$",
          r"Differentiate the top and bottom separately",
          r"Use the chain rule on $\ln x$ only"]),
    card(2, 8,
         [r"A curve $C$ has equation $y=f(x)$, where $f'(x)=3x^2+ax-14$ for a constant $a$.",
          r"The $y$-intercept of $C$ is $8$, and $(x-2)$ is a factor of $f(x)$.",
          r"Find $f(x)$ in its simplest form."],
         [r"Spot: you're given $f'(x)$, so integrate. The $y$-intercept gives the constant, and the factor theorem gives $a$.",
          r"Use: $f(x)=x^3+\dfrac a2x^2-14x+c$ with $c=8$, then $f(2)=0$.",
          r"Method: $f(2)=8+2a-28+8=2a-12=0\Rightarrow a=6$",
          r"Answer: $f(x)=x^3+3x^2-14x+8$"],
         [r"Integrate $f'(x)$, use the intercept for the constant, then $f(2)=0$",
          r"Differentiate $f'(x)$ again",
          r"Set $f'(2)=0$",
          r"Set $f'(0)=8$"]),
    card(2, 9,
         [r"The temperature $\theta\,^\circ$C of some ethanol $t$ seconds after heating began is modelled by $\theta=A-Be^{-0.05t}$.",
          r"The initial temperature was $20\,^\circ$C, and after 15 seconds it was $50\,^\circ$C.",
          r"(a) Find $A$ and $B$ to 3 s.f.",
          r"(b) Ethanol boils at about $78\,^\circ$C. Use this to evaluate the model."],
         [r"Spot: two pieces of data and two unknowns means two equations. Use $t=0$ first, because $e^0=1$.",
          r"Use: $A-B=20$ and $A-Be^{-0.75}=50$.",
          r"(a) $B(1-e^{-0.75})=30\Rightarrow B\approx56.9$ and $A\approx76.9$",
          r"(b) As $t\to\infty$, $\theta\to A\approx76.9\,^\circ$C, which is below $78\,^\circ$C. The model says the ethanol never boils, so it's unsuitable near boiling point."],
         [r"Substitute $t=0$ to get $A-B=20$, then use $t=15$",
          r"Substitute $t=15$ only",
          r"Take logs of both sides straight away",
          r"Assume $A=78$"]),
    card(2, 10,
         [r"(a) Show that $\sin3A\equiv3\sin A-4\sin^3A$.",
          r"(b) Hence solve, for $0\le x<360^\circ$, $\sin3x+\cos^2x=1$."],
         [r"Spot: “hence” with $\sin3x$ means replace it with the cubic in $\sin x$. Use $1-\cos^2x=\sin^2x$ to get everything in $\sin x$.",
          r"Use: $\sin(2A+A)$, $\sin2A\equiv2\sin A\cos A$, $\cos2A\equiv1-2\sin^2A$.",
          r"(b) $3\sin x-4\sin^3x=\sin^2x\Rightarrow\sin x(4\sin x-3)(\sin x+1)=0$",
          r"$\sin x=0,\ \tfrac34,\ -1$",
          r"Answer: $x=0^\circ,\ 48.6^\circ,\ 131.4^\circ,\ 180^\circ,\ 270^\circ$"],
         [r"Write $\sin3x=3\sin x-4\sin^3x$ and $1-\cos^2x=\sin^2x$, then factorise",
          r"Divide everything by $\sin x$",
          r"Use $\sin3x=3\sin x$",
          r"Use the R-form"],
         ask="How do you start part (b)?"),
    card(2, 11,
         [r"The graph of $y=3|x-2|-4$ has its vertex at $P$.",
          r"(a) Find the coordinates of $P$.",
          r"(b) Solve $x+10=3|x-2|-4$.",
          r"(c) The line $y=ax$ meets the graph at least once. Find the possible values of $a$, in set notation."],
         [r"Spot: a modulus graph is a V. Split it into the two arms $x\ge2$ and $x<2$, and check every answer against its condition.",
          r"Use: the arms $y=3x-10$ for $x\ge2$ and $y=-3x+2$ for $x<2$.",
          r"(a) $P=(2,-4)$",
          r"(b) $x+10=3x-10\Rightarrow x=10$, and $x+10=-3x+2\Rightarrow x=-2$. Both are valid.",
          r"(c) The line through the origin and $P$ has gradient $-2$. A line steeper than the left arm (gradient below $-3$) also meets it.",
          r"Answer: $\{a:a<-3\}\cup\{a:a\ge-2\}$"],
         [r"Split into $x\ge2$ and $x<2$ and solve each linear equation",
          r"Square both sides immediately",
          r"Remove the modulus signs and solve once",
          r"Set $x-2=0$"],
         ask="How do you solve part (b)?"),
    card(2, 12,
         [r"A curve has parametric equations $x=4\sin t$, $y=3\sin2t$, $0\le t\le\dfrac{\pi}{2}$. The region $R$ is bounded by the curve and the $x$-axis.",
          r"(a) Show that the area of $R$ is $\displaystyle\int_0^{\frac{\pi}{2}}24\sin t\cos^2t\,dt$, and hence that it is exactly 8.",
          r"(b) Part of the curve models a dam whose vertical wall is 2.4 m high, with a horizontal walkway $MN$ along the top. Find the width of the walkway."],
         [r"Spot: area under a parametric curve means $\displaystyle\int y\dfrac{dx}{dt}\,dt$, with the limits in $t$.",
          r"Use: $\dfrac{dx}{dt}=4\cos t$ and $\sin2t=2\sin t\cos t$. Then $\displaystyle\int\sin t\cos^2t\,dt=-\tfrac13\cos^3t$.",
          r"(a) $\displaystyle\int3\sin2t\cdot4\cos t\,dt=\int24\sin t\cos^2t\,dt=\left[-8\cos^3t\right]_0^{\frac{\pi}{2}}=8$",
          r"(b) $3\sin2t=2.4\Rightarrow\sin2t=0.8$, so $\sin t=\dfrac{1}{\sqrt5}$ or $\dfrac{2}{\sqrt5}$",
          r"$x_N-x_M=4\left(\dfrac{2}{\sqrt5}-\dfrac{1}{\sqrt5}\right)$",
          r"Answer: $\dfrac{4}{\sqrt5}\approx1.79$ m"],
         [r"Use area $=\displaystyle\int y\frac{dx}{dt}\,dt$",
          r"Use area $=\displaystyle\int y\,dt$",
          r"Use area $=\displaystyle\int x\frac{dy}{dt}\,dt$",
          r"Eliminate $t$ first, then integrate"]),
    card(2, 13,
         [r"$g(x)=\dfrac{2\ln x+5}{\ln x+3}$, $x>0$, $x\ne k$",
          r"(a) Deduce the value of $k$.",
          r"(b) Prove that $g'(x)>0$ for all $x$ in the domain.",
          r"(c) Find the values of $a$ for which $g(a)>0$."],
         [r"Spot: the excluded value is where the denominator is zero. To show $g'(x)>0$, use the quotient rule; the numerator simplifies to a constant.",
          r"Use: $\dfrac{d}{dx}\ln x=\dfrac1x$.",
          r"(a) $\ln k+3=0\Rightarrow k=e^{-3}$",
          r"(b) $g'(x)=\dfrac{\frac2x(\ln x+3)-\frac1x(2\ln x+5)}{(\ln x+3)^2}=\dfrac{1}{x(\ln x+3)^2}>0$",
          r"(c) The top and bottom must have the same sign: $0<a<e^{-3}$ or $a>e^{-\frac52}$"],
         [r"Use the quotient rule and simplify the numerator",
          r"Use the product rule on $(2\ln x+5)(\ln x+3)$",
          r"Differentiate the top and bottom separately",
          r"Let $u=\ln x$ and integrate"],
         ask="How do you prove part (b)?"),
    card(2, 14,
         [r"A circle $C$ of radius $r$ lies only in the first quadrant and touches both axes. The line $l$ has equation $x+3y=12$.",
          r"(a) Show that the $y$-coordinates of the intersections of $l$ and $C$ satisfy $10y^2+(4r-72)y+(r^2-24r+144)=0$.",
          r"(b) Given that $l$ is a tangent to $C$, find the two possible values of $r$ as simplified surds."],
         [r"Spot: a circle touching both axes in the first quadrant has centre $(r,r)$. “Tangent” means a repeated root, so the discriminant is $0$.",
          r"Use: $(x-r)^2+(y-r)^2=r^2$ with $x=12-3y$, then $b^2-4ac=0$.",
          r"(a) $(12-3y-r)^2+(y-r)^2=r^2$ expands to the quadratic shown.",
          r"(b) $(4r-72)^2-40(r^2-24r+144)=0\Rightarrow r^2-16r+24=0$",
          r"Answer: $r=8\pm2\sqrt{10}$"],
         [r"Write the circle as $(x-r)^2+(y-r)^2=r^2$ and substitute $x=12-3y$",
          r"Write the circle as $x^2+y^2=r^2$",
          r"Set the gradient of $l$ equal to the radius",
          r"Use the distance from the origin to $l$"]),
    card(2, 15,
         [r"A geometric series has first term $a$ and common ratio $r$, with $r\ne1$ and $a\ne0$.",
          r"(a) Prove that $S_n=\dfrac{a(1-r^n)}{1-r}$.",
          r"(b) Given that $S_8$ is 17 times $S_4$, find the exact possible values of $r$."],
         [r"Spot: (a) write out $S_n$ and $rS_n$, then subtract. (b) Use $1-r^8=(1-r^4)(1+r^4)$.",
          r"Use: $S_n=a+ar+\dots+ar^{n-1}$ and $rS_n=ar+\dots+ar^n$.",
          r"(a) $S_n-rS_n=a-ar^n\Rightarrow S_n=\dfrac{a(1-r^n)}{1-r}$",
          r"(b) $1-r^8=17(1-r^4)\Rightarrow1+r^4=17\Rightarrow r^4=16$",
          r"Answer: $r=2$ or $r=-2$"],
         [r"Write out $S_n$ and $rS_n$ and subtract",
          r"Use the arithmetic series formula",
          r"Prove it for $n=1$ and $n=2$ only",
          r"Differentiate $S_n$ with respect to $r$"]),
    card(2, 16,
         [r"Use algebra to prove that the cube of any integer is either a multiple of 9, or one more or one less than a multiple of 9."],
         [r"Spot: “any integer” with a multiple of 3 involved means split the integers into $3k$, $3k+1$ and $3k-1$ (proof by exhaustion).",
          r"Use: $(3k\pm1)^3=27k^3\pm27k^2+9k\pm1$.",
          r"Method: $(3k)^3=27k^3=9(3k^3)$",
          r"$(3k+1)^3=9(3k^3+3k^2+k)+1$ and $(3k-1)^3=9(3k^3-3k^2+k)-1$",
          r"Every integer is one of these forms, so the result holds."],
         [r"Write any integer as $3k$, $3k+1$ or $3k-1$ and cube each case",
          r"Check $n=1,2,3$",
          r"Write any integer as $9k$",
          r"Use proof by contradiction with $n$ even"]),
]


def check():
    a = sp.symbols("a")
    # P1 Q1
    ser = sp.series(sp.sqrt(1 - 6 * x), x, 0, 4).removeO()
    assert same(ser, 1 - 3 * x - sp.Rational(9, 2) * x**2 - sp.Rational(27, 2) * x**3)
    assert same(sp.sqrt(1 - 6 * sp.Rational(1, 24)), sp.sqrt(3) / 2)
    # P1 Q2
    p = (150 * math.log(7) / math.log(3) - 1) / 2
    assert round(p, 1) == 132.3 and round(150 * math.log(7) / math.log(3), 2) == 265.69
    # P1 Q3
    A, B, C = sp.Matrix([3, 2, -5]), sp.Matrix([5, -1, -1]), sp.Matrix([4, -6, 8])
    assert B - A == sp.Matrix([2, -3, 4]) and C == 2 * (B - A)
    assert C - B == sp.Matrix([-1, -5, 9]) and (A.cross(C - B)).norm() != 0
    # P1 Q4
    f = (2 * x + 5) / (x - 3)
    assert sp.solve(sp.Eq(f, 4), x) == [sp.Rational(17, 2)]
    assert same(f.subs(x, f), (9 * x - 5) / (14 - x))
    # P1 Q5
    assert 12 + 2 * 5 == 22
    r = 3.5**(1 / 6)
    assert round(r, 3) == 1.232 and round(12 * r**4, 1) == 27.7
    # P1 Q6
    al = math.atan2(3, 2)
    assert round(al, 3) == 0.983
    assert identity(2 * sp.sin(x) + 3 * sp.cos(x) - sp.sqrt(13) * sp.sin(x + sp.atan(sp.Rational(3, 2))), x)
    assert round(12 + math.sqrt(13), 1) == 15.6
    tmax = 12 * (math.pi / 2 + 2 - al) / math.pi
    assert round(tmax, 3) == 9.885 and (int(tmax), round((tmax % 1) * 60)) == (9, 53)
    # P1 Q7
    fq = 2 * (x - 1)**2 + 4
    assert fq.subs(x, 3) == 12 and same(fq, 2 * x**2 - 4 * x + 6)
    assert sp.solve(sp.Eq(fq, 4 * x), x) == [1, 3] and fq.subs(x, 2) < 8
    # P1 Q8
    N = sp.Function("N")
    sol = sp.dsolve(sp.Eq(N(t).diff(t), k * sp.sqrt(N(t))))
    assert "t" in str(sol)
    # P1 Q9
    F = 2 * (x**2 - 3) * sp.exp(-x)
    assert same(sp.diff(F, x), 2 * (3 + 2 * x - x**2) * sp.exp(-x))
    assert sorted(sp.solve(3 + 2 * x - x**2, x)) == [-1, 3]
    assert same(F.subs(x, 3), 12 * sp.exp(-3)) and same(F.subs(x, -1), -4 * sp.E)
    assert F.subs(x, 0) == -6 and 3 * (-6) - 5 == -23
    # global minimum of f is at x = -1 (f -> oo as x -> -oo, f -> 0 as x -> oo)
    xs = [i / 100 for i in range(-1000, 2000)]
    assert min(float(F.subs(x, v)) for v in xs[::50]) >= float(-4 * sp.E) - 1e-9
    # P1 Q10
    integrand = 2 / ((x - 1) * (1 + sp.sqrt(x - 1)))
    val = sp.integrate(4 / (u_ := sp.Symbol("u_", positive=True)) / (1 + u_), (u_, 2, 4))
    assert same(val, sp.log(sp.Rational(1296, 625)))
    assert close(sp.Integral(integrand, (x, 5, 17)).evalf(), math.log(1296 / 625), 1e-8)
    # P1 Q11
    xi = sp.Rational(71, 16)
    yi = math.sqrt(25 - float(xi)**2)
    aob = 2 * math.atan2(yi, float(xi))
    ang2 = 2 * math.atan2(yi, 8 - float(xi))
    assert round(aob, 3) == 0.958 and round(ang2, 3) == 1.148 and round(yi, 3) == 2.304
    assert round(5 * aob + math.sqrt(18) * ang2, 1) == 9.7
    assert 8 - math.sqrt(18) < float(xi)   # the arc of C2 inside C1 is the minor arc
    # P1 Q12
    assert identity(1 / sp.cos(theta) - sp.cos(theta) - sp.sin(theta) * sp.tan(theta), theta)
    for d in (20, 110):
        xr = math.radians(d)
        assert abs((1 / math.cos(xr) - math.cos(xr)) - math.sin(xr) * math.tan(math.radians(3 * d - 40))) < 1e-9
    # P1 Q13
    kk = sp.symbols("kk")
    a1 = sp.Integer(3)
    a2 = kk * (a1 + 3) / a1
    a3 = sp.simplify(kk * (a2 + 3) / a2)
    a4 = sp.simplify(kk * (a3 + 3) / a3)
    assert same(sp.numer(sp.together(a4 - 3)), sp.expand(2 * kk**2 + 3 * kk - 9)) or \
        same(sp.numer(sp.together(a4 - 3)), -sp.expand(2 * kk**2 + 3 * kk - 9))
    assert sorted(sp.solve(2 * kk**2 + 3 * kk - 9, kk)) == [-3, sp.Rational(3, 2)]
    seq = [sp.Integer(3)]
    for _ in range(49):
        seq.append(-3 * (seq[-1] + 3) / seq[-1])
    assert seq[:4] == [3, -6, -sp.Rational(3, 2), 3] and sum(seq) == -75
    # P1 Q14
    kc = sp.Rational(23625, 12)
    rr = (27000 - 3 * kc * t)**sp.Rational(1, 3)
    assert rr.subs(t, 0) == 30 and same(rr.subs(t, 4), 15) and 3 * kc == sp.Rational(23625, 4)
    assert sp.solve(27000 - 3 * kc * t, t) == [sp.Rational(32, 7)]
    # P1 Q15
    yy = sp.atan(4 / x**2)
    d1 = sp.diff(yy, x)
    assert same(d1, -8 * x / (x**4 + 16))
    d2 = sp.diff(d1, x)
    assert same(d2, -8 * (16 - 3 * x**4) / (x**4 + 16)**2)
    xi_ = (16 / 3)**0.25
    f2 = sp.lambdify(x, d2)
    assert f2(xi_ - 0.01) * f2(xi_ + 0.01) < 0
    # P1 Q16
    assert not any(9 * pp * pp - qq * qq == 16 for pp in range(1, 200) for qq in range(1, 600))

    # P2 Q1
    ys = [math.sqrt(v / (v + 3)) for v in (1, 1.5, 2, 2.5, 3)]
    assert [float(f"{v:.4g}") for v in ys] == [0.5, 0.5774, 0.6325, 0.6742, 0.7071]
    tr = 0.25 * ((0.5 + 0.7071) + 2 * (0.5774 + 0.6325 + 0.6742))
    assert round(tr, 2) == 1.24 and round(2 * tr, 2) == 2.49
    true_b = float(sp.Integral(sp.sqrt(4 * x / (x + 3)), (x, 1, 3)).evalf())
    assert float(f"{true_b:.4g}") == 2.493 and 2 * tr < true_b and (true_b - 2 * tr) / true_b < 0.005
    # P2 Q3
    assert sorted(sp.solve((6 - x)**2 - (x + 14), x)) == [2, 11]
    # P2 Q4
    assert sp.binomial(6, 3) * 27 == 540 and sp.solve(540 * a**3 + 4320, a)[0] == -2
    # P2 Q5
    xp = sp.solve(sp.Eq(2 * 5**x, 24 - 5**(x + 1)), x)
    assert any(close(v, math.log(24 / 7) / math.log(5)) for v in xp)
    # P2 Q6
    assert same((2 * x**2 + 7 * x - 1) / (x + 3), 2 * x + 1 - 4 / (x + 3))
    assert same(sp.integrate((2 * x**2 + 7 * x - 1) / (x + 3), (x, 0, 3)), 12 - 4 * sp.log(2))
    # P2 Q7
    Y = (9 * x**2 + 2 * x) / (3 * sp.sqrt(x)) - 6 * sp.log(x)
    assert same(sp.diff(Y, x), (27 * x**2 + 2 * x - 36 * sp.sqrt(x)) / (6 * x * sp.sqrt(x)))
    it = [1.0]
    for _ in range(80):
        it.append((4 / 3 - 2 * math.sqrt(it[-1]) / 27)**(2 / 3))
    root = float(sp.nsolve(27 * x**2 + 2 * x - 36 * sp.sqrt(x), x, 1.16))
    assert round(it[1], 5) == 1.16612 and round(it[-1], 5) == round(root, 5) == 1.16254
    assert sp.diff(Y, x, 2).subs(x, root) > 0
    # P2 Q8
    fx = x**3 + 3 * x**2 - 14 * x + 8
    assert same(sp.diff(fx, x), 3 * x**2 + 6 * x - 14) and fx.subs(x, 0) == 8 and fx.subs(x, 2) == 0
    # P2 Q9
    Bv = 30 / (1 - math.exp(-0.75))
    assert round(Bv, 1) == 56.9 and round(Bv + 20, 1) == 76.9
    # P2 Q10
    assert identity(sp.sin(3 * x) - (3 * sp.sin(x) - 4 * sp.sin(x)**3), x)
    sols = [0, 180, 270, math.degrees(math.asin(0.75)), 180 - math.degrees(math.asin(0.75))]
    for d in sols:
        xr = math.radians(d)
        assert abs(math.sin(3 * xr) + math.cos(xr)**2 - 1) < 1e-9
    assert sorted(round(d, 1) for d in sols) == [0, 48.6, 131.4, 180, 270]
    # P2 Q11
    g = lambda v: 3 * abs(v - 2) - 4
    assert g(10) == 20 and g(-2) == 8
    for av in [-5, -3.5, -2, -1, 0, 1, 2.9, 3, 5, 10]:
        assert any(abs(av * v - g(v)) < 1e-6 or (av * v - g(v)) * (av * (v + 0.001) - g(v + 0.001)) <= 0
                   for v in [i / 1000 for i in range(-200000, 200000)]), av
    for av in [-3, -2.9, -2.5, -2.01]:
        assert all((av * v - g(v)) < 0 for v in [i / 100 for i in range(-20000, 20000)]), av
    # P2 Q12
    area = sp.integrate(3 * sp.sin(2 * t) * 4 * sp.cos(t), (t, 0, sp.pi / 2))
    assert area == 8
    assert identity(3 * sp.sin(2 * t) * 4 * sp.cos(t) - 24 * sp.sin(t) * sp.cos(t)**2, t)
    t1, t2 = math.asin(0.8) / 2, (math.pi - math.asin(0.8)) / 2
    w = 4 * math.sin(t2) - 4 * math.sin(t1)
    assert close(w, 4 / math.sqrt(5)) and round(w, 2) == 1.79
    # P2 Q13
    G = (2 * sp.log(x) + 5) / (sp.log(x) + 3)
    assert same(sp.diff(G, x), 1 / (x * (sp.log(x) + 3)**2))
    for v in [0.01, 0.04, 0.09, 1, 5]:
        assert (float(G.subs(x, v)) > 0) == (v < math.exp(-3) or v > math.exp(-2.5))
    # P2 Q14
    rq = sp.symbols("rq", positive=True)
    quad = sp.expand((12 - 3 * y - rq)**2 + (y - rq)**2 - rq**2)
    assert same(quad, 10 * y**2 + (4 * rq - 72) * y + rq**2 - 24 * rq + 144)
    disc = sp.expand((4 * rq - 72)**2 - 40 * (rq**2 - 24 * rq + 144))
    assert sorted(sp.solve(disc, rq), key=float) == [8 - 2 * sp.sqrt(10), 8 + 2 * sp.sqrt(10)]
    # P2 Q15
    assert sorted(v for v in sp.solve(x**4 - 16, x) if v.is_real) == [-2, 2]
    for rv in (2, -2):
        S = lambda n: (1 - rv**n) / (1 - rv)
        assert S(8) == 17 * S(4)
    # P2 Q16
    for nn in range(-300, 300):
        assert (nn**3) % 9 in (0, 1, 8)
