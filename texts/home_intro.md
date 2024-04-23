
### Precificação de títulos de renda fixa

O preço de um título de renda fixa pode ser calculado a partir da seguinte fórmula:
$$
\begin{equation}
P_{t,T} = \left[\sum_{i=1}^{n} \frac{C_{t_{i}}}{(1+y_{t})^\frac{(t_{i}-t)}{252}}\right] + \frac{M_{T}}{(1+y_{t})^\frac{(T-t)}{252}}
\end{equation}
$$

onde $P_{t, T}$ é o preço do título em $t$ (dias úteis) que vence em $T$ (dias úteis), $C_{t_{i}}$ é o cupom em $t_{i}$, onde $t < t_{i} \leq t_{n} = T$, $M_{T}$ é o principal que vence em $T$ e $y_{t}$ é a *yield to maturity* em $t$. 

Podemos considerar que $t \in \mathbb{Z}$, ou seja, $t$ pode assumir três valores: $t=0$, $t<0$ e $t>0$.

- $\left(t = 0\right)$: Neste caso, estamos calculando o preço atual da LTN, ou seja, o preço no qual o título está sendo negociado no mercado (ou no qual está sendo emitido). A *yield to maturity*  $y_0$ é a taxa pela qual o título é negociado no mercado secundário ou a taxa pela qual a STN emite o papel, que determinará o preço que será pago pela instituição financeira. Essa taxa pode ser determinada por condições de mercado, expectativas de inflação, política monetária e outros fatores econômicos, refletindo o consenso do mercado sobre o valor justo do título naquele momento específico. 

- $\left(t < 0\right)$: Aqui, estamos olhando para o passado e calculando o preço que a LTN teve em um momento anterior à data atual, ou seja, $t$ representa o número de dias úteis no passado a partir do momento presente. A taxa de juros $y_t$ para este caso já é conhecida, pois refere-se a uma taxa que foi efetivamente praticada no mercado naquele ponto do passado. Esse cálculo pode ser útil para análises históricas de preços, avaliação do desempenho de investimentos passados ou para fins de comparação.

- $\left(t > 0\right)$: Neste caso, estamos lidando com uma negociação a termo (contrato futuro), onde o preço é estabelecido hoje para uma transação que ocorrerá em uma data futura especificada. O valor de $t$ indica quantos dias úteis no futuro a transação será realizada. A taxa de juros $y_t$ reflete as expectativas do mercado para a taxa naquela data futura, que pode ser, por exemplo, a taxa forward. Este preço a termo pode ser usado em contratos de forward, operações compromissadas ou outros instrumentos financeiros que envolvem o compromisso de compra ou venda de um título em uma data futura.

Note que no caso de uma análise histórica, podemos simplificar e considerar que $t = 0$ para todo ponto $t < \mathbb{Z}$ em que se deseje precificar um título, que é a abordagem que utilizaremos a seguir. Dessa maneira, também poderemos calcular taxas forward históricas de forma mais simples.

Outra forma de preficiar um título de renda fixa é a partir da seguinte fórmula:
$$
\begin{equation}
P_{t,T} = \left[\sum_{i=1}^{n} \frac{C_{t_{i}}}{(1+y_{t,t_{i}})^\frac{(t_{i}-t)}{252}}\right] + \frac{M_{T}}{(1+y_{t,t_{n}})^\frac{(T-t)}{252}}
\end{equation}
$$
em que $y_{t,t_{i}}$ é a taxa de juros entre $t$ e $t_{i}$ e $y_{t,t_{n}}$ é a taxa de juros entre $t$ e $t_{n} = T$. Essas taxas poderiam ser obtidas, por exemplo, através da curva DI, no caso de um título pré-fixado.

A ideia por trás das equações $(1)$ e $(2)$ é descontar cada fluxo de caixa do título por uma ou mais taxas, encontrando, assim, o valor presente de cada fluxo. O preço do título será a soma desses valores presentes. Note que o preço pode ser uma função tanto da taxa quanto dos cupons, no caso em que estes forem variáveis aleatórias, como é o caso dos títulos indexados à inflação.


### Títulos públicos federais

Existem 4 tipos de títulos públicos federais que são ofertados em leilões regulares pelo Tesouro Nacional:

- Nota do Tesouro Nacional série F (NTN-F): são títulos que pagam R$ 1.000,00 no vencimento (valor nominal), com pagamento de cupons semestrais de 10% ao ano (aproximadamente 4,88% ao semestre) do valor nominal do título, sendo emitidos com deságio. 

- Letra do Tesouro Nacional (LTN): são títulos *zero-coupon* que pagam R$ 1.000,00 no vecimento, sendo emitidos com deságio. 

- Nota do Tesouro Nacional série B (NTN-B):

- Letra Financeira do Tesouro (LFT):


#### NTN-F

O preço de uma NTN-F é determinado a partir da seguinte equação:
$$
\begin{equation}
P_{t,T} = \left[\sum_{i=1}^{n} \frac{1000 \times (1,10)^{\frac{1}{2}}}{(1+y_{t})^\frac{(t_{i}-t)}{252}}\right] + \frac{1000}{(1+y_{t})^\frac{(T-t)}{252}}
\end{equation}
$$

