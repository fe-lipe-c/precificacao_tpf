
### Precificação dos títulos de renda fixa

O preço de qualquer título pode ser calculado a partir da seguinte fórmula:
$$
P_{t,T}^{\tiny\text{LTN}} = \frac{1000}{(1 + i_{t})^\frac{(T-t)}{252}}
$$

onde $P_{t}$ é o preço do título em $t$, $i_{t}$ é a taxa de juros em $t$ e $n$ é o número de dias até o vencimento. Note que o $t \in \mathbb{Z}$, ou seja, podemos três casos: t=0, t<0 e t>0.

-   ( t = 0 ): Neste caso, estamos calculando o preço spot da LTN, ou seja, o preço atual do título no mercado. A taxa de juros ( i_0 ) é a taxa de desconto que prevalece no mercado no momento da transação. Essa taxa pode ser determinada por condições de mercado, expectativas de inflação, política monetária e outros fatores econômicos. O preço spot reflete o consenso do mercado sobre o valor justo do título naquele momento específico.

- ( t < 0 ): Aqui, estamos olhando para o passado e calculando o preço que a LTN teve em um momento anterior à data atual. O valor de ( t ) representa o número de dias úteis no passado a partir do momento presente. A taxa de juros ( i_t ) para este caso já é conhecida, pois refere-se a uma taxa que foi efetivamente praticada no mercado naquele ponto do passado. Esse cálculo pode ser útil para análises históricas de preços, avaliação do desempenho de investimentos passados ou para fins de auditoria e comparação.

- ( t > 0 ): Neste caso, estamos lidando com uma negociação a termo, onde o preço é estabelecido hoje para uma transação que ocorrerá em uma data futura especificada. O valor de ( t ) indica quantos dias úteis no futuro a transação será realizada. A taxa de juros ( i_t ) reflete as expectativas do mercado para a taxa de desconto naquela data futura. Este preço a termo pode ser usado em contratos de forward, operações compromissadas ou outros instrumentos financeiros que envolvem o compromisso de compra ou venda de um título em uma data futura


### Títulos públicos federais

Existem 4 tipos de títulos públicos federais que são ofertados em leilões regulares pelo Tesouro Nacional:

- Letra do Tesouro Nacional (LTN): são títulos *zero-coupon* que pagam R$ 1.000,00 no vecimento, sendo emitidos com deságio. 

- Nota do Tesouro Nacional série F (NTN-F): 

- Nota do Tesouro Nacional série B (NTN-B):

- Letra Financeira do Tesouro (LFT):


#### LTN

O preço de uma LTN é feita a partir da fórmula:
$$ 
P_{t,T}^{\tiny\text{LTN}} = \frac{1000}{(1 + i_{t})^\frac{(T-t)}{252}}
$$

onde $P_{t}$ é o preço do título em $t$, $i_{t}$ é a taxa de juros em $t$ e $n$ é o número de dias até o vencimento. 
