# Implementation of the Apriori algorithm, in a game where the data is represented by a set of products that customers buy .
 
The idea behind the game is simple; use Apriori to predict (guess) the possible purchases based on the customer's habits and compare these results with the user's choices which will result in a success score.

We have set up a basic identification system, each customer is identified by a username, we will keep the transaction history of each customer in separate files to have results according to each of them. 

When the user "Rima" chooses products to buy from the list A and while clicking on "Play Game", the algorithm will try to guess the rest of the transaction based on the itemset A and the history of its transactions. At this stage, the algorithm will generate association rules of type A->B.

insert image

Here the user was going to buy (water, white bread, spaghetti, tuna), after selecting that (water, white bread) he asks the algorithm to guess the rest.
If the algorithm finds association rules containing (water, white bread) it displays a second list and waits for the user to identify the rest of the products.
If the products correspond to the itemsets found by the algorithm, they are displayed in green otherwise in red.

insert image here
