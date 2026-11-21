"""June 2023 (9MA0/01 and 9MA0/02), with the numbers changed."""
import math
import sympy as sp
from common import card, close, same, identity, x, y, t, k, theta

SERIES = {"id": "paper-2023-06", "title": "June 2023", "hue": 200}

CARDS = [
    # ---------------- Paper 1 ----------------
    card(1, 1,
         [r"Find $\displaystyle\int\frac{\sqrt x(4x-3)}{2}\,dx$, writing each term in its simplest form."],
         [r"Spot: you can't integrate a root multiplied by a bracket as it stands. Expand it into separate powers of $x$ first.",
          r"Use: $\sqrt x=x^{\frac12}$ and $\displaystyle\int x^n\,dx=\frac{x^{n+1}}{n+1}+c$.",
          r"Method: $\dfrac{\sqrt x(4x-3)}{2}=2x^{\frac32}-\dfrac32x^{\frac12}$",
          r"Answer: $\dfrac45x^{\frac52}-x^{\frac32}+c$"],
         [r"Expand to $2x^{\frac32}-\frac32x^{\frac12}$, then integrate each term",
          r"Integrate $\sqrt x$ and $4x-3$ separately, then multiply",
          r"Integrate the top and the bottom separately",
          r"Use $\displaystyle\int\sqrt x\,dx=\frac{1}{2\sqrt x}$"]),
    card(1, 2,
         [r"$f(x)=2x^3+3x^2-11x+2a$, where $a$ is a positive constant. $(x-a)$ is a factor of $f(x)$.",
          r"(a) Show that $a(2a^2+3a-9)=0$.",
          r"(b)(i) Find the value of $a$. (ii) Use algebra to find the exact solutions of $f(x)=3$."],
         [r"Spot: “$(x-a)$ is a factor” means $f(a)=0$, which gives an equation in $a$ alone.",
          r"Use: the factor theorem. In (b)(ii) the constant term cancels, so take out a factor of $x$.",
          r"(a) $2a^3+3a^2-11a+2a=0\Rightarrow a(2a^2+3a-9)=0$",
          r"(b)(i) $a(2a-3)(a+3)=0$ and $a>0$, so $a=\tfrac32$.",
          r"(ii) $2x^3+3x^2-11x=0\Rightarrow x(2x^2+3x-11)=0$",
          r"Answer: $x=0$ or $x=\dfrac{-3\pm\sqrt{97}}{4}$"],
         [r"Substitute $x=a$ and set $f(a)=0$",
          r"Substitute $x=-a$ and set it equal to 0",
          r"Set $f(0)=0$",
          r"Divide $f(x)$ by $x$"],
         ask="How do you start part (a)?"),
    card(1, 3,
         [r"Relative to a fixed origin $O$, $A$ has position vector $4\mathbf{i}-5\mathbf{j}+3\mathbf{k}$ and $B$ has position vector $3\mathbf{i}+2\mathbf{j}+a\mathbf{k}$, where $a$ is a positive integer.",
          r"(a) Show that $|\overrightarrow{OA}|=5\sqrt2$.",
          r"(b) Find the smallest value of $a$ for which $|\overrightarrow{OB}|>|\overrightarrow{OA}|$."],
         [r"Spot: compare the magnitudes by comparing their squares. That way there are no square roots.",
          r"Use: $|x\mathbf{i}+y\mathbf{j}+z\mathbf{k}|=\sqrt{x^2+y^2+z^2}$.",
          r"(a) $\sqrt{16+25+9}=\sqrt{50}=5\sqrt2$",
          r"(b) $9+4+a^2>50\Rightarrow a^2>37$. $6^2=36$ is too small, so $a=7$."],
         [r"Compare $|\overrightarrow{OB}|^2=13+a^2$ with 50",
          r"Set $\overrightarrow{OB}=\overrightarrow{OA}$",
          r"Use the dot product $\overrightarrow{OA}\cdot\overrightarrow{OB}$",
          r"Compare $3+2+a$ with $4-5+3$"],
         ask="How do you start part (b)?"),
    card(1, 4,
         [r"The curve $C$ has equation $y=f(x)$, where $f'(x)=5x+2\cos x$. $C$ has a stationary point with $x$-coordinate $\alpha$, where $\alpha$ is small.",
          r"(a) Use the small angle approximation for $\cos x$ to estimate $\alpha$ to 3 decimal places.",
          r"The point $P(0,3)$ lies on $C$.",
          r"(b) Find the equation of the tangent to $C$ at $P$, in the form $y=mx+c$."],
         [r"Spot: “$\alpha$ is small” means replace $\cos\alpha$ with $1-\dfrac{\alpha^2}{2}$. A stationary point means $f'(\alpha)=0$.",
          r"Use: $\cos x\approx1-\dfrac{x^2}{2}$, then solve the quadratic and take the small root.",
          r"(a) $5\alpha+2-\alpha^2=0\Rightarrow\alpha^2-5\alpha-2=0\Rightarrow\alpha=\dfrac{5-\sqrt{33}}{2}\approx-0.372$",
          r"(b) The gradient is $f'(0)=2$, so $y=2x+3$."],
         [r"Replace $\cos\alpha$ with $1-\frac{\alpha^2}{2}$ and set $f'(\alpha)=0$",
          r"Replace $\cos\alpha$ with 1",
          r"Replace $\cos\alpha$ with $\alpha$",
          r"Integrate $f'(x)$ and set it equal to 0"],
         ask="How do you start part (a)?"),
    card(1, 5,
         [r"A continuous curve has equation $y=f(x)$. The table shows values of $x$ and $y$, where $a$ and $b$ are constants.",
          r"$x$: 2, 2.2, 2.4, 2.6, 2.8, 3. $y$: $a$, 12.4, $b$, 15.1, 14.6, 11.9",
          r"The trapezium rule with all the $y$ values gives 13.45 as an estimate of the area under the curve from $x=2$ to $x=3$.",
          r"(a) Show that $a+2b=38.4$.",
          r"(b) The $y$ values in the table add up to 78.1. Find $a$ and $b$."],
         [r"Spot: the trapezium rule gives one equation in $a$ and $b$. The total of the $y$ values gives a second, so solve them simultaneously.",
          r"Use: area $\approx\dfrac h2\left[y_0+y_n+2(y_1+\dots+y_{n-1})\right]$ with $h=0.2$.",
          r"(a) $0.1\left[a+11.9+2(12.4+b+15.1+14.6)\right]=13.45\Rightarrow a+2b+96.1=134.5$",
          r"(b) $a+b+54=78.1\Rightarrow a+b=24.1$",
          r"Answer: $b=14.3$ and $a=9.8$"],
         [r"Use the trapezium rule with $h=0.2$ to make an equation in $a$ and $b$",
          r"Use the trapezium rule with $h=1$",
          r"Use the trapezium rule with $h=\frac16$",
          r"Add up the $y$ values and multiply by 0.2"],
         ask="How do you start part (a)?"),
    card(1, 6,
         [r"$a=\log_3x$ and $b=\log_3(x+9)$. Write each expression in terms of $a$ and/or $b$:",
          r"(a) $\log_3\sqrt[3]{x}$",
          r"(b) $\log_3(x^2+9x)$",
          r"(c) $\log_3\left(27+\dfrac{243}{x}\right)$"],
         [r"Spot: rewrite each expression so its only factors are $x$, $(x+9)$ and powers of 3. Then split it up with the log laws.",
          r"Use: $\log pq=\log p+\log q$, $\log\dfrac pq=\log p-\log q$, $\log p^n=n\log p$ and $\log_327=3$.",
          r"(a) $\tfrac13a$",
          r"(b) $\log_3x(x+9)=a+b$",
          r"(c) $27+\dfrac{243}{x}=\dfrac{27(x+9)}{x}$, so it equals $3+b-a$."],
         [r"Write $27+\frac{243}{x}=\frac{27(x+9)}{x}$, then use the log laws",
          r"Split it into $\log_327+\log_3\frac{243}{x}$",
          r"Use $\log_3(x+9)=\log_3x+\log_39$",
          r"Divide $b$ by $a$"],
         ask="How do you start part (c)?"),
    card(1, 7,
         [r"$f(x)=2+\sqrt{x-5}$, $x>5$.",
          r"(a) State the range of $f$. (b) Find $f^{-1}$.",
          r"$g(x)=\dfrac{14}{x-2}$, $x\ne2$.",
          r"(c) Find $gf(9)$.",
          r"(d) Find the exact value of the constant $a$ for which $f(a^2+5)=g(a)$."],
         [r"Spot: to find $f^{-1}$, swap $x$ and $y$ and rearrange. The domain of $f^{-1}$ is the range of $f$. In (d), $\sqrt{a^2}=|a|$.",
          r"Use: $f(a^2+5)=2+\sqrt{a^2}$.",
          r"(a) $f(x)>2$",
          r"(b) $f^{-1}(x)=(x-2)^2+5$, $x>2$",
          r"(c) $f(9)=4$, so $gf(9)=\dfrac{14}{2}=7$",
          r"(d) $(2+a)(a-2)=14\Rightarrow a^2=18$. $g(a)$ has to be more than 2, so $a>2$ and $a=3\sqrt2$."],
         [r"Substitute to get $2+a=\frac{14}{a-2}$, then solve",
          r"Find $f^{-1}(a)$ and set it equal to $g(a)$",
          r"Set $a^2+5=\frac{14}{a-2}$",
          r"Find $gf(a)$ and set it equal to $a$"],
         ask="How do you start part (d)?"),
    card(1, 8,
         [r"The plan of a stage is a sector $OCDE$ of a circle with centre $O$, between two congruent triangles $ABO$ and $GFO$.",
          r"$AOG$ is a straight line of length 16 m along the back of the stage. $B$ lies on $OC$ extended and $F$ lies on $OE$ extended. Angle $COE=2.1$ radians and arc $CDE=21$ m.",
          r"(a) Show that $OC=10$ m. (b) Show that angle $AOB=0.521$ radians to 3 d.p.",
          r"(c) The front of the stage, $BC$ plus arc $CDE$ plus $EF$, is 26 m long. Find the total area of the stage to the nearest $\text{m}^2$."],
         [r"Spot: the angles on the straight line $AOG$ add to $\pi$. $B$ is on $OC$ extended, so $OB=OC+CB$. Each triangle has two known sides and the angle between them.",
          r"Use: arc $=r\theta$, sector $=\tfrac12r^2\theta$, triangle $=\tfrac12ab\sin C$.",
          r"(a) $2.1r=21\Rightarrow r=10$",
          r"(b) $2\theta+2.1=\pi\Rightarrow\theta=\dfrac{\pi-2.1}{2}\approx0.521$",
          r"(c) $BC=EF=\tfrac12(26-21)=2.5$, so $OB=12.5$ and $OA=8$.",
          r"Area $=\tfrac12(10^2)(2.1)+2\times\tfrac12(8)(12.5)\sin0.521\approx105+49.8\approx155\text{ m}^2$"],
         [r"Find $OB=OC+BC$, then add the sector and two triangles using $\frac12ab\sin C$",
          r"Use the sector area $\pi r^2\theta$",
          r"Treat each triangle as right-angled",
          r"Use the arc length 21 m as the radius"],
         ask="How do you start part (c)?"),
    card(1, 9,
         [r"The first three terms of a geometric sequence are $2k+2$, $18-2k$ and $k+6$, where $k$ is a constant.",
          r"(a) Show that $k^2-43k+156=0$.",
          r"Given that the sequence converges,",
          r"(b)(i) find $k$, giving a reason. (ii) Find $S_\infty$."],
         [r"Spot: three terms of a geometric sequence means $\dfrac{u_2}{u_1}=\dfrac{u_3}{u_2}$, so $(u_2)^2=u_1u_3$. “Converges” means $|r|<1$.",
          r"Use: $S_\infty=\dfrac{a}{1-r}$.",
          r"(a) $(18-2k)^2=(2k+2)(k+6)\Rightarrow324-72k+4k^2=2k^2+14k+12$, which simplifies to the quadratic.",
          r"(b)(i) $(k-4)(k-39)=0$. $k=4$ gives $10,10,10$ with $r=1$, which doesn't converge, so $k=39$.",
          r"(ii) The terms are $80,-60,45$, so $r=-\tfrac34$ and $S_\infty=\dfrac{80}{1+\frac34}=\dfrac{320}{7}$."],
         [r"Use $(18-2k)^2=(2k+2)(k+6)$",
          r"Use $18-2k=\frac{(2k+2)+(k+6)}{2}$",
          r"Use $(2k+2)^2=(18-2k)(k+6)$",
          r"Use $r=\frac{k+6}{2k+2}$"],
         ask="How do you start part (a)?"),
    card(1, 10,
         [r"A circle $C$ has equation $x^2+y^2-4kx+2ky+5=0$, where $k$ is a constant.",
          r"(a) Find, in terms of $k$, (i) the coordinates of the centre (ii) the radius.",
          r"The line $y=x+1$ meets $C$ at two distinct points.",
          r"(b) Find the range of possible values of $k$."],
         [r"Spot: “two distinct points” means substitute the line into the circle and use $b^2-4ac>0$.",
          r"Use: complete the square for the centre and radius.",
          r"(a) $(x-2k)^2+(y+k)^2=5k^2-5$, so the centre is $(2k,-k)$ and the radius is $\sqrt{5k^2-5}$.",
          r"(b) $2x^2+(2-2k)x+2k+6=0$, so $(2-2k)^2-8(2k+6)>0\Rightarrow k^2-6k-11>0$",
          r"Answer: $k<3-2\sqrt5$ or $k>3+2\sqrt5$. Both ranges also make the radius real."],
         [r"Substitute $y=x+1$ into the circle and use $b^2-4ac>0$",
          r"Substitute $y=x+1$ and use $b^2-4ac=0$",
          r"Substitute $x=0$ into the circle",
          r"Solve $5k^2-5>0$ and stop"],
         ask="How do you start part (b)?"),
    card(1, 11,
         [r"The value, $V$ pounds, of a laptop $t$ months after it was bought is modelled by $V=ab^t$, where $a$ and $b$ are constants.",
          r"The graph of $\log_{10}V$ against $t$ is a straight line through $(0,2.8)$ and $(12,2.56)$.",
          r"(a) Find the initial value of the laptop.",
          r"(b) Find a complete equation for $V$ in terms of $t$, giving $a$ exactly and $b$ to 3 s.f.",
          r"(c) Exactly 3 years after it was bought, the laptop was worth £118. Evaluate the reliability of the model."],
         [r"Spot: $V=ab^t$ with a graph of $\log V$ means take logs: $\log V=\log a+t\log b$. The intercept is $\log a$ and the gradient is $\log b$.",
          r"Use: gradient $=\dfrac{2.56-2.8}{12}=-0.02$.",
          r"(a) $\log_{10}a=2.8\Rightarrow a=10^{2.8}\approx631$, so £631",
          r"(b) $b=10^{-0.02}\approx0.955$, so $V=10^{2.8}(0.955)^t$",
          r"(c) $t=36$ gives $V\approx£120$. That's close to £118, so the model is reliable here."],
         [r"Take logs: $\log V=\log a+t\log b$, so the intercept is $\log a$",
          r"Use $a=2.8$",
          r"Use $b=-0.02$",
          r"Use $V=2.8-0.02t$"]),
    card(1, 12,
         [r"$y=\cos x$, where $x$ is in radians. Use differentiation from first principles to show that $\dfrac{dy}{dx}=-\sin x$.",
          r"You may use the formula for $\cos(A\pm B)$, and assume that as $h\to0$, $\dfrac{\sin h}{h}\to1$ and $\dfrac{\cos h-1}{h}\to0$."],
         [r"Spot: “first principles” means start from $\dfrac{f(x+h)-f(x)}{h}$. Expand $\cos(x+h)$, then group the terms so the given limits appear.",
          r"Use: $\cos(x+h)=\cos x\cos h-\sin x\sin h$.",
          r"Method: $\dfrac{\cos x\cos h-\sin x\sin h-\cos x}{h}=\cos x\left(\dfrac{\cos h-1}{h}\right)-\sin x\left(\dfrac{\sin h}{h}\right)$",
          r"As $h\to0$, this tends to $\cos x\times0-\sin x\times1=-\sin x$."],
         [r"Write $\frac{\cos(x+h)-\cos x}{h}$, expand $\cos(x+h)$ and group into the given limits",
          r"Use $\cos(x+h)=\cos x+\cos h$",
          r"Substitute $h=0$ straight away",
          r"Use the chain rule"]),
    card(1, 13,
         [r"Carriages on a roller coaster go round the same circuit again and again. A carriage's maximum height is 48 m, and it starts each circuit 3 m above the ground.",
          r"Its height $H$ m, $t$ seconds after it starts the first circuit, is modelled by $H=a-b(t-15)^2$, where $a$ and $b$ are positive constants.",
          r"(a) Find a complete equation for the model. (b) Find the height when $t=30$.",
          r"An alternative model is $H=22.5\cos(12t+\alpha)^\circ+\beta$, $0\le\alpha<360$.",
          r"(c) Find $\alpha$ and $\beta$. (d) The carriage moves continuously for 2 minutes. Give a reason why the alternative model is more appropriate."],
         [r"Spot: in $a-b(t-15)^2$ the maximum is $a$, and $t=0$ gives $b$. In the cosine model, $\beta$ is the midline and $\cos=-1$ at the lowest point.",
          r"Use: $\beta=\dfrac{\max+\min}{2}$, and the amplitude $\dfrac{\max-\min}{2}=22.5$ checks out.",
          r"(a) $a=48$, and $3=48-225b\Rightarrow b=0.2$, so $H=48-0.2(t-15)^2$",
          r"(b) $H=48-0.2(225)=3$ m",
          r"(c) $\beta=25.5$, and $22.5\cos\alpha+25.5=3\Rightarrow\cos\alpha=-1\Rightarrow\alpha=180$",
          r"(d) The cosine model repeats every 30 s, like the circuits. The quadratic gives negative heights after $t=30$."],
         [r"Use the maximum for $a$, then $t=0$ and $H=3$ to find $b$",
          r"Use $t=15$ and $H=3$",
          r"Set $a=3$",
          r"Set $b=48$"],
         ask="How do you start part (a)?"),
    card(1, 14,
         [r"Prove, using algebra, that $n^3+(n+1)^3$ is odd for all $n\in\mathbb{N}$."],
         [r"Spot: odd or even for all $n$ means consider $n$ even and $n$ odd separately.",
          r"Use: $n=2k$ and $n=2k+1$, then write each result as $2(\dots)+1$.",
          r"$n=2k$: $8k^3+(2k+1)^3=16k^3+12k^2+6k+1=2(8k^3+6k^2+3k)+1$, which is odd.",
          r"$n=2k+1$: $(2k+1)^3+(2k+2)^3=16k^3+36k^2+30k+9=2(8k^3+18k^2+15k+4)+1$, which is odd."],
         [r"Consider $n=2k$ and $n=2k+1$ separately",
          r"Check $n=1$, 2 and 3",
          r"Write it as $(2n+1)^3$",
          r"Expand and set it equal to 0"]),
    card(1, 15,
         [r"$f(x)=\dfrac{5xe^x}{\sqrt{e^{3x}-3}}$, $x>\tfrac13\ln3$.",
          r"(a) Show that $f'(x)=\dfrac{5e^x\left(e^{3x}(2-x)+Ax+B\right)}{2(e^{3x}-3)^{\frac32}}$, where $A$ and $B$ are constants to be found.",
          r"(b) Hence show that the $x$-coordinates of the turning points satisfy $x=\dfrac{2e^{3x}-6}{e^{3x}+6}$. This equation has roots $\alpha$ and $\beta$, where $\beta>\alpha>0$.",
          r"(c) Using $x_{n+1}=\dfrac{2e^{3x_n}-6}{e^{3x_n}+6}$ with $x_1=1$, find $x_2$ and $\beta$ to 3 d.p.",
          r"(d) Using a suitable interval and function, show that $\alpha=0.676$ to 3 d.p."],
         [r"Spot: write it as $5xe^x(e^{3x}-3)^{-\frac12}$ and use the product rule with the chain rule. Turning points mean the bracket on top is 0.",
          r"Use: $\dfrac{d}{dx}(e^{3x}-3)^{-\frac12}=-\tfrac32e^{3x}(e^{3x}-3)^{-\frac32}$.",
          r"(a) Take out $\dfrac{5e^x}{2(e^{3x}-3)^{\frac32}}$ to leave $2(1+x)(e^{3x}-3)-3xe^{3x}=e^{3x}(2-x)-6x-6$, so $A=B=-6$.",
          r"(b) $e^{3x}(2-x)=6x+6\Rightarrow2e^{3x}-6=x(e^{3x}+6)$",
          r"(c) $x_2=1.310$, and the iterates converge to $\beta=1.949$.",
          r"(d) Let $h(x)=x-\dfrac{2e^{3x}-6}{e^{3x}+6}$. $h(0.6755)>0$ and $h(0.6765)<0$, and $h$ is continuous, so $\alpha=0.676$."],
         [r"Write it as $5xe^x(e^{3x}-3)^{-\frac12}$ and use the product and chain rules",
          r"Differentiate the top and the bottom separately",
          r"Use the chain rule on $e^{3x}$ only",
          r"Take logs of the top only"],
         ask="How do you start part (a)?"),

    # ---------------- Paper 2 ----------------
    card(2, 1,
         [r"$f(x)=2x^3-9x^2+4x-7$.",
          r"(a) Find $f''(x)$.",
          r"(b)(i) Solve $f''(x)=0$. (ii) Hence find the values of $x$ for which $f(x)$ is concave."],
         [r"Spot: concave means $f''(x)\le0$. Convex means $f''(x)\ge0$.",
          r"Use: differentiate twice.",
          r"(a) $f'(x)=6x^2-18x+4$, so $f''(x)=12x-18$",
          r"(b)(i) $x=\tfrac32$ (ii) $12x-18\le0\Rightarrow x\le\tfrac32$"],
         [r"Solve $f''(x)\le0$",
          r"Solve $f''(x)\ge0$",
          r"Solve $f'(x)\le0$",
          r"Solve $f(x)\le0$"],
         ask="How do you find where $f$ is concave?"),
    card(2, 2,
         [r"A sequence is defined by $u_1=20$ and $u_{n+1}=u_n+6\cos\left(\dfrac{n\pi}{2}\right)+4(-1)^n$.",
          r"(a)(i) Show that $u_2=16$. (ii) Find $u_3$ and $u_4$.",
          r"The sequence is periodic with order 4.",
          r"(b)(i) Write down $u_5$. (ii) Find $\displaystyle\sum_{r=1}^{30}u_r$."],
         [r"Spot: periodic with order 4 means the terms repeat every 4. For the sum, count the full cycles, then add the leftover terms.",
          r"Use: $\cos\dfrac{\pi}{2}=0$, $\cos\pi=-1$, $\cos\dfrac{3\pi}{2}=0$ and $\cos2\pi=1$.",
          r"(a)(i) $u_2=20+0-4=16$ (ii) $u_3=16-6+4=14$ and $u_4=14+0-4=10$",
          r"(b)(i) $u_5=20$",
          r"(ii) Each cycle adds to 60. 30 terms are 7 cycles plus $u_1+u_2$, so the sum is $7(60)+36=456$."],
         [r"Use 7 full cycles of 4 terms, then add $u_{29}+u_{30}=u_1+u_2$",
          r"Use $\frac{30}{2}(u_1+u_{30})$",
          r"Multiply $u_1$ by 30",
          r"Use 8 full cycles of 4 terms"],
         ask="How do you start part (b)(ii)?"),
    card(2, 3,
         [r"Given that $\log_3(x+3)+\log_3(x+6)=1+2\log_3x$,",
          r"(a) show that $2x^2-9x-18=0$.",
          r"(b)(i) Write down the roots of $2x^2-9x-18=0$. (ii) Hence state which root is not a solution of the log equation, giving a reason."],
         [r"Spot: combine each side into a single log, then drop the logs. Write the 1 as $\log_33$.",
          r"Use: $\log a+\log b=\log ab$ and $2\log x=\log x^2$.",
          r"(a) $\log_3(x+3)(x+6)=\log_3(3x^2)\Rightarrow x^2+9x+18=3x^2$",
          r"(b)(i) $(2x+3)(x-6)=0$, so $x=6$ or $x=-\tfrac32$",
          r"(ii) $x=-\tfrac32$, because $\log_3x$ isn't defined for negative $x$."],
         [r"Write 1 as $\log_33$, then combine each side into a single log",
          r"Write 1 as $\log_31$",
          r"Use $\log_3(x+3)+\log_3(x+6)=\log_3(2x+9)$",
          r"Divide both sides by $\log_3x$"],
         ask="How do you start part (a)?"),
    card(2, 4,
         [r"The temperature of a cup of tea, $H$ °C, $t$ minutes after it is made is modelled by $H=Ae^{-Bt}+22$, where $A$ and $B$ are constants.",
          r"Initially the tea is at 90 °C.",
          r"(a) State the value of $A$.",
          r"Initially the tea is cooling at 6.2 °C per minute.",
          r"(b) Find a complete equation linking $H$ and $t$, giving $B$ to 3 d.p."],
         [r"Spot: “initially” means $t=0$. A rate of cooling is $\dfrac{dH}{dt}$, which is negative.",
          r"Use: $\dfrac{dH}{dt}=-ABe^{-Bt}$, which is $-AB$ at $t=0$.",
          r"(a) $90=A+22\Rightarrow A=68$",
          r"(b) $-68B=-6.2\Rightarrow B\approx0.091$, so $H=68e^{-0.091t}+22$"],
         [r"Differentiate and set $\frac{dH}{dt}=-6.2$ at $t=0$",
          r"Set $H=6.2$ at $t=1$",
          r"Use $B=6.2$",
          r"Set $H=90-6.2t$"],
         ask="How do you start part (b)?"),
    card(2, 5,
         [r"The curve $C$ has equation $y=f(x)$. It passes through $P(2,5)$ and has a turning point at $P$.",
          r"Given that $\dfrac{dy}{dx}=3x^3-8x^2+2x+k$, where $k$ is a constant,",
          r"(a) show that $k=4$.",
          r"(b) Hence find the coordinates of the point where $C$ crosses the $y$-axis."],
         [r"Spot: a turning point at $P$ means $\dfrac{dy}{dx}=0$ when $x=2$. To get back to $y$, integrate, then use $P$ to find $c$.",
          r"Use: $y=\displaystyle\int\frac{dy}{dx}\,dx$, with $(2,5)$ on the curve.",
          r"(a) $24-32+4+k=0\Rightarrow k=4$",
          r"(b) $y=\tfrac34x^4-\tfrac83x^3+x^2+4x+c$, and $5=\tfrac83+c\Rightarrow c=\tfrac73$",
          r"Answer: $\left(0,\tfrac73\right)$"],
         [r"Integrate, then substitute $(2,5)$ to find $c$",
          r"Substitute $x=0$ into $\frac{dy}{dx}$",
          r"Differentiate $\frac{dy}{dx}$ again",
          r"Set $\frac{dy}{dx}=5$"],
         ask="How do you start part (b)?"),
    card(2, 6,
         [r"Relative to a fixed origin $O$, the points $A$, $B$, $C$ and $D$ have position vectors $9\mathbf{i}$, $12\mathbf{j}$, $32\mathbf{i}+72\mathbf{j}$ and $17\mathbf{i}+15\mathbf{j}$.",
          r"(a) Show that $AD$ is parallel to $BC$.",
          r"The points model the corners of a running track, with lengths in metres. A runner runs along all four sides for each lap, and completes 3 laps in exactly 2 minutes.",
          r"(b) Find the runner's average speed in km/h."],
         [r"Spot: parallel means one vector is a multiple of the other. For the speed you need the perimeter, so find all four side lengths.",
          r"Use: $\overrightarrow{AD}=\mathbf{d}-\mathbf{a}$, and speed $=\dfrac{\text{distance}}{\text{time}}$, then change the units.",
          r"(a) $\overrightarrow{AD}=8\mathbf{i}+15\mathbf{j}$ and $\overrightarrow{BC}=32\mathbf{i}+60\mathbf{j}=4\overrightarrow{AD}$",
          r"(b) $AB=15$, $BC=68$, $CD=\sqrt{15^2+57^2}\approx58.94$ and $DA=17$, so a lap is about 158.94 m.",
          r"$3\times158.94\approx476.8$ m in 2 minutes, which is about 14.3 km/h"],
         [r"Find all four side lengths, add them for one lap, then multiply by 3",
          r"Use $|\overrightarrow{OC}|$ as the length of a lap",
          r"Use $|\overrightarrow{AD}|+|\overrightarrow{BC}|$ as the length of a lap",
          r"Divide 2 minutes by 3 laps"],
         ask="How do you start part (b)?"),
    card(2, 7,
         [r"A curve has equation $x^3-3xy+2y^2=26$.",
          r"(a) Find $\dfrac{dy}{dx}$ in terms of $x$ and $y$.",
          r"The point $P(-1,3)$ lies on the curve.",
          r"(b) Find the equation of the normal at $P$, in the form $ax+by+c=0$, where $a$, $b$ and $c$ are integers."],
         [r"Spot: $x$ and $y$ mixed together means implicit differentiation. The $xy$ term needs the product rule.",
          r"Use: $\dfrac{d}{dx}(y^2)=2y\dfrac{dy}{dx}$ and $\dfrac{d}{dx}(xy)=y+x\dfrac{dy}{dx}$.",
          r"(a) $3x^2-3y-3x\dfrac{dy}{dx}+4y\dfrac{dy}{dx}=0\Rightarrow\dfrac{dy}{dx}=\dfrac{3y-3x^2}{4y-3x}$",
          r"(b) At $P$ the gradient is $\dfrac{6}{15}=\dfrac25$, so the normal has gradient $-\dfrac52$.",
          r"Answer: $5x+2y-1=0$"],
         [r"Differentiate implicitly, using the product rule on $3xy$",
          r"Make $y$ the subject first",
          r"Differentiate $3xy$ as $3y$",
          r"Treat $y$ as a constant"],
         ask="How do you start part (a)?"),
    card(2, 8,
         [r"(a) Express $4\sin\theta+6\cos\theta$ in the form $R\sin(\theta+\alpha)$, where $R>0$ and $0<\alpha<\dfrac{\pi}{2}$. Give $R$ exactly and $\alpha$ in radians to 3 d.p.",
          r"The first three terms of an arithmetic sequence are $2\sin x$, $2\sin x+\cos x$ and $2\sin x+2\cos x$. $S_7$ is the sum of the first 7 terms, as $x$ varies.",
          r"(b)(i) Find the exact maximum value of $S_7$. (ii) Deduce the smallest positive value of $x$ at which it occurs."],
         [r"Spot: the sum of an arithmetic sequence with $a=2\sin x$ and $d=\cos x$ is a mix of $\sin x$ and $\cos x$, so use the R-form from (a).",
          r"Use: $S_n=\dfrac n2\left[2a+(n-1)d\right]$. $R\sin(x+\alpha)$ has maximum $R$, when $x+\alpha=\dfrac{\pi}{2}$.",
          r"(a) $R=\sqrt{16+36}=2\sqrt{13}$ and $\tan\alpha=\dfrac64$, so $\alpha\approx0.983$",
          r"(b)(i) $S_7=\dfrac72(4\sin x+6\cos x)=7\sqrt{13}\sin(x+\alpha)$, so the maximum is $7\sqrt{13}$.",
          r"(ii) $x+0.983=\dfrac{\pi}{2}\Rightarrow x\approx0.588$"],
         [r"Use $S_7=\frac72[2a+6d]$ with $a=2\sin x$ and $d=\cos x$, then the R-form",
          r"Use $S_7=7a$",
          r"Use $d=2\sin x$",
          r"Use the geometric series formula"],
         ask="How do you start part (b)?"),
    card(2, 9,
         [r"The curve $C$ has parametric equations $x=t^2-4t-5$, $y=4\ln(t-2)$, $t>2$.",
          r"(a) Show that a Cartesian equation of $C$ is $y=A\ln(x+B)$, $x>-B$, where $A$ and $B$ are integers.",
          r"$C$ cuts the $y$-axis at $P$.",
          r"(b) Show that the tangent to $C$ at $P$ can be written as $ax+by=c\ln3$, where $a$, $b$ and $c$ are integers."],
         [r"Spot: complete the square on the quadratic in $t$ so that $t-2$, the expression inside the log, appears on its own.",
          r"Use: $x=(t-2)^2-9$ and $\ln\sqrt u=\tfrac12\ln u$.",
          r"(a) $t-2=\sqrt{x+9}$, so $y=4\ln\sqrt{x+9}=2\ln(x+9)$. $A=2$ and $B=9$.",
          r"(b) At $x=0$: $y=2\ln9=4\ln3$, and $\dfrac{dy}{dx}=\dfrac{2}{x+9}=\dfrac29$.",
          r"Answer: $y-4\ln3=\tfrac29x\Rightarrow2x-9y=-36\ln3$"],
         [r"Complete the square: $x=(t-2)^2-9$",
          r"Use $t=\frac{x+5}{-4}$",
          r"Differentiate both equations with respect to $t$",
          r"Set $t=0$"],
         ask="How do you start part (a)?"),
    card(2, 10,
         [r"$f(x)=\dfrac{4kx+12}{(x+3)(x-1)}$, where $k$ is a positive constant.",
          r"(a) Express $f(x)$ in partial fractions in terms of $k$.",
          r"(b) Hence find the exact value of $k$ for which $\displaystyle\int_{-2}^{0}f(x)\,dx=10$."],
         [r"Spot: the partial fractions turn the integral into logs. Between $-2$ and 0, $x-1$ is negative, so use $\ln|x-1|$.",
          r"Use: $\dfrac{4kx+12}{(x+3)(x-1)}\equiv\dfrac{A}{x+3}+\dfrac{B}{x-1}$, then substitute $x=1$ and $x=-3$.",
          r"(a) $\dfrac{3k-3}{x+3}+\dfrac{k+3}{x-1}$",
          r"(b) $\left[(3k-3)\ln|x+3|+(k+3)\ln|x-1|\right]_{-2}^{0}=(3k-3)\ln3-(k+3)\ln3=(2k-6)\ln3$",
          r"Answer: $(2k-6)\ln3=10\Rightarrow k=\dfrac{5}{\ln3}+3$"],
         [r"Integrate the partial fractions to logs, then set the result equal to 10",
          r"Integrate the numerator and denominator separately",
          r"Substitute $x=0$ and $x=-2$ into $f(x)$ and subtract",
          r"Differentiate the partial fractions"],
         ask="How do you start part (b)?"),
    card(2, 11,
         [r"A cuboid tank has a base 15 m by 8 m and a height of 4 m. Water flows in, and after $t$ minutes it's $h$ m deep with volume $V\text{ m}^3$.",
          r"In a model, the rate of change of $V$ is inversely proportional to $\sqrt h$.",
          r"(a) Show that $\dfrac{dh}{dt}=\dfrac{\lambda}{\sqrt h}$, where $\lambda$ is a constant.",
          r"Initially the water is 0.64 m deep. After 10 minutes it's 2.25 m deep.",
          r"(b) Find an equation linking $h$ and $t$ in the form $h^{\frac32}=At+B$.",
          r"(c) Find how long the tank takes to fill completely."],
         [r"Spot: link $\dfrac{dh}{dt}$ and $\dfrac{dV}{dt}$ with the chain rule. $V=120h$, so $\dfrac{dV}{dh}=120$. Then separate the variables.",
          r"Use: $\dfrac{dh}{dt}=\dfrac{dh}{dV}\times\dfrac{dV}{dt}=\dfrac{1}{120}\times\dfrac{k}{\sqrt h}$.",
          r"(b) $\displaystyle\int\sqrt h\,dh=\int\lambda\,dt\Rightarrow\tfrac23h^{\frac32}=\lambda t+c$, so $h^{\frac32}=At+B$.",
          r"$t=0$ gives $B=0.64^{1.5}=0.512$. $t=10$ gives $3.375=10A+0.512$, so $A=0.2863$.",
          r"(c) Full means $h=4$: $8=0.2863t+0.512\Rightarrow t\approx26.2$ minutes"],
         [r"Use $\frac{dh}{dt}=\frac{dh}{dV}\times\frac{dV}{dt}$ with $V=120h$",
          r"Integrate $V=120h$",
          r"Use $\frac{dV}{dt}=k\sqrt h$",
          r"Use $V=\frac13\pi r^2h$"],
         ask="How do you start part (a)?"),
    card(2, 12,
         [r"The numbers of subscribers, in thousands, to two streaming companies are modelled by $N_A=|t-4|+2$ and $N_B=11-|2t-8|$, $t\ge0$, where $t$ is the time in years.",
          r"(a) Find the initial difference between the numbers of subscribers.",
          r"When $t=T$, company A cut its prices and its number of subscribers rose. (b) Suggest a value for $T$, with a reason.",
          r"(c) Find the values of $t$ for which $N_A>N_B$, in set notation.",
          r"(d) State a limitation of the model for company B."],
         [r"Spot: both moduli contain $t-4$, because $|2t-8|=2|t-4|$. So the inequality becomes one in $|t-4|$.",
          r"Use: $|t-4|>3$ means $t<1$ or $t>7$.",
          r"(a) $N_A(0)=6$ and $N_B(0)=3$, so the difference is 3 thousand.",
          r"(b) $T=4$, where $N_A$ stops falling and starts rising.",
          r"(c) $|t-4|+2>11-2|t-4|\Rightarrow|t-4|>3$, so $\{t:0\le t<1\}\cup\{t:t>7\}$",
          r"(d) $N_B$ becomes negative for $t>9.5$, which is impossible."],
         [r"Write $|2t-8|=2|t-4|$, then solve for $|t-4|$",
          r"Square both sides",
          r"Solve $N_A=N_B$ and take the region between the roots",
          r"Remove the modulus signs and solve $t+2>11-(2t-8)$"],
         ask="How do you start part (c)?"),
    card(2, 13,
         [r"(a) Find the first three terms, in ascending powers of $x$, of the binomial expansion of $(2+x)^{-2}$.",
          r"(b) Using your answer to (a) and algebraic integration, estimate $\displaystyle\int_{0.1}^{0.3}\frac{8x}{(2+x)^2}\,dx$ to 4 s.f.",
          r"(c) Find the exact value of this integral, in the form $a\ln b+c$."],
         [r"Spot: (b) multiply the expansion by $8x$ and integrate the polynomial. (c) needs an exact method: substitute $u=2+x$.",
          r"Use: $(2+x)^{-2}=\tfrac14\left(1+\tfrac x2\right)^{-2}$. For (c), $x=u-2$ and $dx=du$.",
          r"(a) $\dfrac14-\dfrac14x+\dfrac{3}{16}x^2$",
          r"(b) $\displaystyle\int_{0.1}^{0.3}\left(2x-2x^2+\tfrac32x^3\right)dx\approx0.06567$",
          r"(c) $\displaystyle\int_{2.1}^{2.3}\left(\frac8u-\frac{16}{u^2}\right)du=\left[8\ln u+\frac{16}{u}\right]_{2.1}^{2.3}=8\ln\frac{23}{21}-\frac{320}{483}$"],
         [r"Substitute $u=2+x$ to split it into $\frac8u-\frac{16}{u^2}$",
          r"Integrate the expansion from (a)",
          r"Use $\displaystyle\int\frac{8x}{(2+x)^2}\,dx=4\ln(2+x)^2$",
          r"Use the trapezium rule"],
         ask="How do you start part (c)?"),
    card(2, 14,
         [r"(a) Show that $2\tan\theta(5\cos\theta+12\sin^2\theta)=5\sin2\theta(1+\tan^2\theta)$ can be written as $\sin2\theta(A\cos^2\theta+B\cos\theta+C)=0$, where $A$, $B$ and $C$ are constants.",
          r"(b) Hence solve $2\tan x(5\cos x+12\sin^2x)=5\sin2x(1+\tan^2x)$ for $180^\circ\le x\le360^\circ$, $x\ne270^\circ$, to 1 d.p."],
         [r"Spot: $1+\tan^2\theta=\sec^2\theta$, so multiply both sides by $\cos^2\theta$ to clear the fractions. Then $\sin2\theta$ appears on both sides.",
          r"Use: $\sin2\theta=2\sin\theta\cos\theta$ and $\sin^2\theta=1-\cos^2\theta$.",
          r"(a) $\sin2\theta(5\cos\theta+12\sin^2\theta)=5\sin2\theta\Rightarrow\sin2\theta(-12\cos^2\theta+5\cos\theta+7)=0$",
          r"(b) $\sin2x=0$ gives $x=180^\circ$ or $360^\circ$ ($270^\circ$ is excluded). $(12\cos x+7)(\cos x-1)=0$ gives $\cos x=1$ or $\cos x=-\tfrac{7}{12}$, so $x=234.3^\circ$.",
          r"Answer: $x=180^\circ,\ 234.3^\circ,\ 360^\circ$"],
         [r"Use $1+\tan^2\theta=\sec^2\theta$, then multiply through by $\cos^2\theta$",
          r"Divide both sides by $\sin2\theta$",
          r"Use $1+\tan^2\theta=\cos^2\theta$",
          r"Expand $\sin2\theta$ as $2\sin\theta$"],
         ask="How do you start part (a)?"),
    card(2, 15,
         [r"Given that $x$ is an acute angle, use algebra to prove by contradiction that $\sin x+\cos x>1$."],
         [r"Spot: contradiction means assume the opposite, $\sin x+\cos x\le1$. Both sides are positive, so you can square.",
          r"Use: $\sin^2x+\cos^2x=1$.",
          r"Assume $\sin x+\cos x\le1$. Then $(\sin x+\cos x)^2\le1\Rightarrow1+2\sin x\cos x\le1\Rightarrow\sin x\cos x\le0$.",
          r"But $\sin x>0$ and $\cos x>0$ for an acute angle, so $\sin x\cos x>0$. That's a contradiction, so $\sin x+\cos x>1$."],
         [r"Assume $\sin x+\cos x\le1$, square, then use $\sin^2x+\cos^2x=1$",
          r"Assume $\sin x+\cos x<1$",
          r"Assume $\sin x+\cos x>1$",
          r"Try $x=45^\circ$"]),
]


def check():
    a, b, n, u, h = sp.symbols("a b n u h")
    # P1 Q1
    assert same(sp.integrate(sp.sqrt(x) * (4 * x - 3) / 2, x), sp.Rational(4, 5) * x**sp.Rational(5, 2) - x**sp.Rational(3, 2))
    # P1 Q2
    f2 = 2 * x**3 + 3 * x**2 - 11 * x + 2 * a
    assert same(f2.subs(x, a), a * (2 * a**2 + 3 * a - 9)) and same(2 * a**2 + 3 * a - 9, (2 * a - 3) * (a + 3))
    g2 = f2.subs(a, sp.Rational(3, 2)) - 3
    assert same(g2, x * (2 * x**2 + 3 * x - 11))
    assert set(sp.solve(g2, x)) == {0, (-3 + sp.sqrt(97)) / 4, (-3 - sp.sqrt(97)) / 4}
    # P1 Q3
    assert same(sp.Matrix([4, -5, 3]).norm(), 5 * sp.sqrt(2))
    assert min(v for v in range(1, 20) if 13 + v * v > 50) == 7
    # P1 Q4
    al = (5 - math.sqrt(33)) / 2
    assert round(al, 3) == -0.372 and abs(al**2 - 5 * al - 2) < 1e-12
    root = float(sp.nsolve(5 * x + 2 * sp.cos(x), x, -0.37))
    assert abs(root - al) < 0.001
    # P1 Q5
    assert close(0.1 * (9.8 + 11.9 + 2 * (12.4 + 14.3 + 15.1 + 14.6)), 13.45)
    assert close(9.8 + 2 * 14.3, 38.4) and close(9.8 + 12.4 + 14.3 + 15.1 + 14.6 + 11.9, 78.1)
    # P1 Q6
    for xv in (0.5, 2.0, 7.3):
        A, B = math.log(xv, 3), math.log(xv + 9, 3)
        assert close(math.log(xv**(1 / 3), 3), A / 3)
        assert close(math.log(xv**2 + 9 * xv, 3), A + B)
        assert close(math.log(27 + 243 / xv, 3), 3 + B - A)
    # P1 Q7
    f7 = lambda v: 2 + sp.sqrt(v - 5)
    g7 = lambda v: 14 / (v - 2)
    assert g7(f7(9)) == 7 and same(f7((x - 2)**2 + 5).subs(x, 6), 6)
    av = 3 * sp.sqrt(2)
    assert same(f7(av**2 + 5), g7(av)) and not same(f7(av**2 + 5), g7(-av))
    # P1 Q8
    th = (math.pi - 2.1) / 2
    area = 0.5 * 100 * 2.1 + 2 * 0.5 * 8 * 12.5 * math.sin(th)
    assert 21 / 2.1 == 10 and round(th, 3) == 0.521 and round(area) == 155
    # P1 Q9
    eq9 = sp.expand((18 - 2 * k)**2 - (2 * k + 2) * (k + 6))
    assert same(eq9, 2 * (k**2 - 43 * k + 156)) and sorted(sp.solve(eq9, k)) == [4, 39]
    a9, r9 = 2 * 39 + 2, sp.Rational(18 - 78, 80)
    assert r9 == sp.Rational(-3, 4) and r9 * (18 - 78) == 39 + 6 and a9 / (1 - r9) == sp.Rational(320, 7)
    # P1 Q10
    assert same(x**2 + y**2 - 4 * k * x + 2 * k * y + 5, (x - 2 * k)**2 + (y + k)**2 - (5 * k**2 - 5))
    q10 = sp.expand(x**2 + (x + 1)**2 - 4 * k * x + 2 * k * (x + 1) + 5)
    assert same(q10, 2 * x**2 + (2 - 2 * k) * x + 2 * k + 6)
    assert same(sp.discriminant(q10, x), 4 * (k**2 - 6 * k - 11))
    assert set(sp.solve(k**2 - 6 * k - 11, k)) == {3 - 2 * sp.sqrt(5), 3 + 2 * sp.sqrt(5)}
    assert 5 * (3 - 2 * math.sqrt(5))**2 - 5 > 0
    # P1 Q11
    assert round(10**2.8) == 631 and round(10**-0.02, 3) == 0.955
    assert round(10**2.8 * 0.955**36) == 120 and round(10**(2.8 - 0.02 * 36)) == 120
    # P1 Q12
    hh = sp.symbols("hh")
    lhs = (sp.cos(x + hh) - sp.cos(x)) / hh
    rhs = sp.cos(x) * (sp.cos(hh) - 1) / hh - sp.sin(x) * sp.sin(hh) / hh
    assert sp.simplify(sp.expand_trig(lhs - rhs)) == 0
    assert sp.limit(lhs, hh, 0) == -sp.sin(x)
    # P1 Q13
    H = lambda tv: 48 - 0.2 * (tv - 15)**2
    assert close(H(0), 3) and close(H(15), 48) and close(H(30), 3) and H(31) < 3 and H(45) < 0
    Halt = lambda tv: 22.5 * math.cos(math.radians(12 * tv + 180)) + 25.5
    assert close(Halt(0), 3) and close(Halt(15), 48) and close(Halt(30), 3) and close(Halt(45), 48)
    # P1 Q14
    for m in range(0, 300):
        assert (m**3 + (m + 1)**3) % 2 == 1
    assert same((2 * k)**3 + (2 * k + 1)**3, 2 * (8 * k**3 + 6 * k**2 + 3 * k) + 1)
    assert same((2 * k + 1)**3 + (2 * k + 2)**3, 2 * (8 * k**3 + 18 * k**2 + 15 * k + 4) + 1)
    # P1 Q15
    f15 = 5 * x * sp.exp(x) / sp.sqrt(sp.exp(3 * x) - 3)
    target = 5 * sp.exp(x) * (sp.exp(3 * x) * (2 - x) - 6 * x - 6) / (2 * (sp.exp(3 * x) - 3)**sp.Rational(3, 2))
    assert identity(sp.diff(f15, x) - target, x, 0.5, 2.5)
    g15 = lambda v: (2 * math.exp(3 * v) - 6) / (math.exp(3 * v) + 6)
    xs = [1.0]
    for _ in range(60):
        xs.append(g15(xs[-1]))
    assert round(xs[1], 3) == 1.310 and round(xs[-1], 3) == 1.949
    h15 = lambda v: v - g15(v)
    assert h15(0.6755) > 0 > h15(0.6765) and math.log(3) / 3 < 0.6755

    # P2 Q1
    f1 = 2 * x**3 - 9 * x**2 + 4 * x - 7
    assert same(sp.diff(f1, x, 2), 12 * x - 18) and sp.solve(sp.diff(f1, x, 2), x) == [sp.Rational(3, 2)]
    # P2 Q2
    us = [20]
    for m in range(1, 40):
        us.append(us[-1] + round(6 * math.cos(m * math.pi / 2)) + 4 * (-1)**m)
    assert us[:5] == [20, 16, 14, 10, 20] and sum(us[:30]) == 456
    # P2 Q3
    lhs3 = sp.expand((x + 3) * (x + 6) - 3 * x**2)
    assert same(-lhs3, 2 * x**2 - 9 * x - 18) and set(sp.solve(lhs3, x)) == {6, sp.Rational(-3, 2)}
    assert close(math.log(9, 3) + math.log(12, 3), 1 + 2 * math.log(6, 3))
    # P2 Q4
    assert round(6.2 / 68, 3) == 0.091 and 68 + 22 == 90
    # P2 Q5
    d5 = 3 * x**3 - 8 * x**2 + 2 * x + k
    assert sp.solve(d5.subs(x, 2), k) == [4]
    y5 = sp.integrate(d5.subs(k, 4), x)
    c5 = 5 - y5.subs(x, 2)
    assert c5 == sp.Rational(7, 3)
    # P2 Q6
    A6, B6, C6, D6 = (sp.Matrix(v) for v in ([9, 0], [0, 12], [32, 72], [17, 15]))
    assert C6 - B6 == 4 * (D6 - A6)
    lap = (B6 - A6).norm() + (C6 - B6).norm() + (D6 - C6).norm() + (A6 - D6).norm()
    assert (B6 - A6).norm() == 15 and (C6 - B6).norm() == 68 and (A6 - D6).norm() == 17
    assert round(float(3 * lap) / 120 * 3.6, 1) == 14.3
    # P2 Q7
    F7 = x**3 - 3 * x * y + 2 * y**2 - 26
    assert F7.subs({x: -1, y: 3}) == 0
    dydx = -sp.diff(F7, x) / sp.diff(F7, y)
    assert same(dydx, (3 * y - 3 * x**2) / (4 * y - 3 * x)) and dydx.subs({x: -1, y: 3}) == sp.Rational(2, 5)
    assert same(sp.expand(2 * (y - 3 + sp.Rational(5, 2) * (x + 1))), 5 * x + 2 * y - 1)
    # P2 Q8
    al8 = math.atan2(6, 4)
    assert round(al8, 3) == 0.983 and same(sp.sqrt(52), 2 * sp.sqrt(13))
    S7 = lambda v: 3.5 * (2 * 2 * math.sin(v) + 6 * math.cos(v))
    xmax = math.pi / 2 - al8
    assert round(xmax, 3) == 0.588 and close(S7(xmax), 7 * math.sqrt(13))
    assert max(S7(i / 1000) for i in range(0, 6284)) <= 7 * math.sqrt(13) + 1e-9
    # P2 Q9
    X9, Y9 = t**2 - 4 * t - 5, 4 * sp.log(t - 2)
    assert identity(Y9 - 2 * sp.log(X9 + 9), t, 2.2, 6)
    assert sp.solve(X9, t) == [-1, 5] and same(Y9.subs(t, 5), 4 * sp.log(3))
    grad = (sp.diff(Y9, t) / sp.diff(X9, t)).subs(t, 5)
    assert grad == sp.Rational(2, 9)
    # P2 Q10
    f10 = (4 * k * x + 12) / ((x + 3) * (x - 1))
    assert same(f10, (3 * k - 3) / (x + 3) + (k + 3) / (x - 1))
    kv = 5 / math.log(3) + 3
    val = float(sp.Integral(f10.subs(k, kv), (x, -2, 0)).evalf())
    assert close(val, 10, 1e-7) and close((2 * kv - 6) * math.log(3), 10)
    # P2 Q11
    B11 = 0.64**1.5
    A11 = (2.25**1.5 - B11) / 10
    assert close(B11, 0.512) and close(A11, 0.2863) and round((4**1.5 - B11) / A11, 1) == 26.2
    # P2 Q12
    NA = lambda v: abs(v - 4) + 2
    NB = lambda v: 11 - abs(2 * v - 8)
    assert NA(0) - NB(0) == 3
    for i in range(0, 2000):
        tv = i / 100
        if abs(tv - 1) > 1e-9 and abs(tv - 7) > 1e-9:
            assert (NA(tv) > NB(tv)) == (tv < 1 or tv > 7), tv
    assert NB(9.5) == 0 and NB(9.6) < 0
    # P2 Q13
    ser = sp.series((2 + x)**-2, x, 0, 3).removeO()
    assert same(ser, sp.Rational(1, 4) - x / 4 + sp.Rational(3, 16) * x**2)
    est = sp.integrate(sp.expand(8 * x * ser), (x, sp.Rational(1, 10), sp.Rational(3, 10)))
    assert est == sp.Rational(197, 3000) and round(float(est), 7) == 0.0656667
    exact = sp.integrate(8 * x / (2 + x)**2, (x, sp.Rational(1, 10), sp.Rational(3, 10)))
    assert close(float(exact), float(8 * sp.log(sp.Rational(23, 21)) - sp.Rational(320, 483)))
    # P2 Q14
    lhs14 = 2 * sp.tan(theta) * (5 * sp.cos(theta) + 12 * sp.sin(theta)**2) - 5 * sp.sin(2 * theta) * (1 + sp.tan(theta)**2)
    form = sp.sin(2 * theta) * (-12 * sp.cos(theta)**2 + 5 * sp.cos(theta) + 7)
    assert identity(lhs14 * sp.cos(theta)**2 - form, theta, 0.1, 1.4)
    assert same(12 * u**2 - 5 * u - 7, (12 * u + 7) * (u - 1))
    sols = [180, 360 - math.degrees(math.acos(-7 / 12)), 360]
    assert round(sols[1], 1) == 234.3
    E = lambda d: 2 * math.tan(math.radians(d)) * (5 * math.cos(math.radians(d)) + 12 * math.sin(math.radians(d))**2) - 5 * math.sin(math.radians(2 * d)) * (1 + math.tan(math.radians(d))**2)
    for d in sols:
        assert abs(E(d)) < 1e-9
    G = lambda d: math.sin(math.radians(2 * d)) * (12 * math.cos(math.radians(d)) + 7) * (math.cos(math.radians(d)) - 1)
    for i in range(1800, 3601):
        d = i / 10
        if i != 2700 and min(abs(d - s) for s in sols) > 0.5:
            assert abs(G(d)) > 1e-7, d
    # P2 Q15
    for d in range(1, 90):
        r_ = math.radians(d)
        assert math.sin(r_) + math.cos(r_) > 1
