
### Precificação de títulos de renda fixa

O preço de um título de renda fixa pode ser calculado a partir da seguinte fórmula:
$$
\begin{equation}
P_{t,T} = \frac{C_{t_{1}}}{(1+y_{t})^\frac{(t_{1}-t)}{252}} + \dots + \frac{C_{t_{n}}}{(1+y_{t})^\frac{(t_{n}-t)}{252}} + \frac{M_{T}}{(1+y_{t})^\frac{(T-t)}{252}}
\end{equation}
$$
onde $P_{t, T}$ é o preço do título em $t$ (dias úteis) que vence em $T$ (dias úteis), $C_{t_{i}}$ é o cupom em $t_{i}$, onde $t < t_{i} \leq t_{n} = T$, $M_{T}$ é o principal que vence em $T$ e $y_{t}$ é a *yield to maturity* em $t$. 

Podemos considerar que $t \in \mathbb{Z}$, ou seja, $t$ pode assumir três valores: t=0, t<0 e t>0.

- $\left(t = 0\right)$: Neste caso, estamos calculando o preço atual da LTN, ou seja, o preço no qual o título está sendo negociado no mercado (ou no qual está sendo emitido). A *yield to maturity*  $y_0$ é a taxa pela qual o título é negociado no mercado secundário ou a taxa pela qual a STN emite o papel, que determinará o preço que será pago pela instituição financeira. Essa taxa pode ser determinada por condições de mercado, expectativas de inflação, política monetária e outros fatores econômicos, refletindo o consenso do mercado sobre o valor justo do título naquele momento específico.

- $\left(t < 0\right)$: Aqui, estamos olhando para o passado e calculando o preço que a LTN teve em um momento anterior à data atual, ou seja, $t$ representa o número de dias úteis no passado a partir do momento presente. A taxa de juros $y_t$ para este caso já é conhecida, pois refere-se a uma taxa que foi efetivamente praticada no mercado naquele ponto do passado. Esse cálculo pode ser útil para análises históricas de preços, avaliação do desempenho de investimentos passados ou para fins de comparação.

- $\left(t > 0\right)$: Neste caso, estamos lidando com uma negociação a termo (contrato futuro), onde o preço é estabelecido hoje para uma transação que ocorrerá em uma data futura especificada. O valor de $t$ indica quantos dias úteis no futuro a transação será realizada. A taxa de juros $y_t$ reflete as expectativas do mercado para a taxa naquela data futura. Este preço a termo pode ser usado em contratos de forward, operações compromissadas ou outros instrumentos financeiros que envolvem o compromisso de compra ou venda de um título em uma data futura.

### Títulos públicos federais

Existem 4 tipos de títulos públicos federais que são ofertados em leilões regulares pelo Tesouro Nacional:

- Letra do Tesouro Nacional (LTN): são títulos *zero-coupon* que pagam R$ 1.000,00 no vecimento, sendo emitidos com deságio. 

- Nota do Tesouro Nacional série F (NTN-F): 

- Nota do Tesouro Nacional série B (NTN-B):

- Letra Financeira do Tesouro (LFT):


#### LTN

Como uma LTN não paga cupons, apenas o principal $M_T = 1000$, o seu preço é determinado a partir da seguinte equação:
$$
\begin{equation}
P_{t,T}^{\tiny\text{LTN}} = \frac{1000}{(1 + i_{t})^\frac{(T-t)}{252}}
\end{equation}
$$
